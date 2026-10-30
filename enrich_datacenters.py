"""
Enrich FracTracker's US data center records with ownership / jurisdiction fields
via Perplexity (targeted web search) + Claude (extraction into the target schema).

Seed: data/Data_Centers_Database.xlsx, sheet DB_Output_V2 (the other sheet has
unresolved IMPORTRANGE formulas), plus data/trackdatacenters_seed.csv: facilities
from trackdatacenters.com not already in FracTracker, used only as a seed list
(name, city, county, state; lat/long are our own Nominatim geocodes, and no other
field of theirs is copied). Output is a local CSV only - nothing is
written to Supabase. The submarinecables table is only read (anon key) to
compute cable_landing_proximity.

Usage:
  python enrich_datacenters.py            # dry run: first 10 rows -> data/datacenter_enrichment_dryrun_opus.csv
  python enrich_datacenters.py --full     # every row -> data/datacenter_enrichment.csv (resumable)

Options: --model opus|sonnet (default opus), --limit N, --batch-size 25, --batch-rows 200, --batch-delay 10, --workers 4, --output PATH

Re-running skips any facility_id already in the output CSV, so a crash or rate
limit never loses completed rows. Rows that fail are logged to <output>.errors.jsonl
and retried on the next run. Raw Perplexity + Claude responses for every row
go to <output>.raw.jsonl for auditing. Perplexity results are cached in
data/datacenter_searches.jsonl as soon as they arrive (shared by every run and
model), so a retry or a model comparison never pays for the same search twice.
"""

import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd
import requests

from pipeline_common import DATASET_PATH, canonical_country, env_key, fetch_all, get_anon_client

SEED_PATH = 'data/Data_Centers_Database.xlsx'
SEED_SHEET = 'DB_Output_V2'
# Extra seed rows (name + place only) appended after FracTracker's, with TDC- facility_ids.
EXTRA_SEED_PATH = 'data/trackdatacenters_seed.csv'
GEOCODE_CACHE = 'data/landing_station_coords.csv'
DRY_RUN_OUTPUT = 'data/datacenter_enrichment_dryrun_{model}.csv'
# Perplexity results don't depend on the Claude model, so every run shares one cache.
SEARCH_CACHE = 'data/datacenter_searches.jsonl'
FULL_OUTPUT = 'data/datacenter_enrichment.csv'
DRY_RUN_ROWS = 10

PERPLEXITY_URL = 'https://api.perplexity.ai/chat/completions'
PERPLEXITY_MODEL = 'sonar-pro'
CLAUDE_MODELS = {'opus': 'claude-opus-5-5', 'sonnet': 'claude-sonnet-5-5'}

# USD. Perplexity responses usually report their own cost (usage.cost.total_cost);
# this table is only the fallback when they don't.
CLAUDE_PRICE = {
    'claude-opus-5-5': {'input': 4.00 / 1e6, 'output': 20.00 / 1e6, 'cache_read': 0.20 / 1e6},
    'claude-sonnet-5-5': {'input': 2.00 / 1e6, 'output': 10.00 / 1e6, 'cache_read': 0.20 / 1e6},
}
BATCH_DISCOUNT = 0.5  # Message Batches: half price on every token, cache reads/writes included
BATCH_SAFETY = 1.05  # margin on the worst-case per-row batch rate (output length varies)
PERPLEXITY_PRICE = {'input': 3.00 / 1e6, 'output': 15.00 / 1e6, 'request': 10.00 / 1000}

NOT_DISCLOSED = 'not disclosed'
# Station names that are only a state/province ('Maryland, United States') geocode to a
# region centroid hundreds of km from the real landing, so they're left out of the match.
REGION_NAMES = {
    'alabama', 'alaska', 'california', 'connecticut', 'delaware', 'florida', 'georgia', 'hawaii',
    'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'mississippi', 'new hampshire',
    'new jersey', 'new york', 'north carolina', 'oregon', 'rhode island', 'south carolina', 'texas',
    'virginia', 'washington', 'british columbia', 'new brunswick', 'newfoundland and labrador',
    'nova scotia', 'ontario', 'prince edward island', 'quebec',
}
LIVE_CABLE_STATUSES = {'in service', 'in service (partial)', 'ready for service', 'partially retired'}
DENSITY_RADIUS_KM = 50

OUTPUT_COLUMNS = [
    'facility_id', 'facility_name', 'operator', 'owner_parent', 'country', 'city', 'lat', 'lon',
    'capacity_mw_coded', 'capacity_basis', 'capacity_estimated_mw', 'capacity_raw',
    'operator_nationality', 'owner_origin', 'legal_domicile', 'ownership_structure',
    'ownership_structure_raw', 'operator_type', 'service_model', 'tier_rating',
    'siting_determinants', 'interconnection_density', 'cable_landing_proximity',
    'operator_siting_logic', 'bis_listed', 'ofac_listed', 'fdi_screening',
    'data_localization', 'status', 'source_urls', 'attribution_tier', 'notes',
    'foreign_linked_entities',
]
# Rows written before foreign_linked_entities existed; distinct from "not disclosed",
# which means the field was extracted and nothing was found.
NOT_EXTRACTED = 'not extracted (row predates this field)'

SEED_CONTEXT_COLUMNS = [
    'facility_name', 'address', 'city', 'state', 'zip', 'county', 'status', 'purpose',
    'operator_name', 'tenant', 'mw', 'sizerank', 'power_source', 'cooling_type',
    'facility_size_sqft', 'project_cost', 'expected_date_online', 'nda', 'other_info',
]
SEED_SOURCE_COLUMNS = [f'info_source_{i}' for i in range(1, 9)]

# Landing stations near enough to a US facility to ever be its nearest one.
# Only these get geocoded (Nominatim allows ~1 request/second).
NEAR_US_COUNTRIES = {
    'united states', 'canada', 'mexico', 'bahamas', 'bermuda', 'cuba', 'puerto rico',
    'cayman islands', 'jamaica', 'turks and caicos islands', 'dominican republic', 'haiti',
    'virgin islands (u.s.)', 'virgin islands (british)', 'us virgin islands', 'guam',
    'american samoa', 'northern mariana islands', 'russia',
}


# ============================================================================
# PROMPTS + OUTPUT SCHEMA
# ============================================================================

PERPLEXITY_SYSTEM = """You research the ownership of specific US data center facilities.
Answer only about the facility described, not other sites run by the same company - \
if you can only find company-level information, say so explicitly. Cite a source for \
every claim. If something cannot be found, say "not found" rather than speculating."""

PERPLEXITY_QUESTION = """Facility: {facility_name}
Location: {location}
{operator_line}

For this specific facility, find:
1. The current operator, and the entity that owns the facility (including any LLC or \
special-purpose entity named in permits, zoning or tax-abatement filings).
2. The ultimate parent company of the owner and the operator, the country where each is \
headquartered, and the jurisdiction where the owning entity is incorporated.
3. The ownership structure: wholly owned, joint venture (name the partners), private-equity \
or infrastructure-fund backed (name the funds), REIT, publicly listed, or state-owned.
4. Any state backing: government, sovereign wealth fund or state-owned enterprise investment, \
including government shareholdings in the owner's or operator's parent company.
5. Any CFIUS / foreign-investment review, BIS Entity List, OFAC sanctions or other \
export-control mentions involving the facility, its owner or its operator.
6. Power capacity in MW, and whether that figure was announced by the company or estimated \
by a third party.
7. The business model (self-built for own use, wholesale or retail colocation, \
build-to-suit lease, crypto mining / hosting), any Uptime Institute tier rating, and the \
reasons the company gave for choosing this site.
8. Any non-US companies, funds or governments involved with this facility in any role - \
tenants or anchor customers, investors, lenders or funders, joint-venture or project \
partners - with each one's country and whether it is government-owned or government-funded."""

ROW_FIELDS = [
    'operator', 'owner_parent', 'operator_nationality', 'owner_origin', 'legal_domicile',
    'ownership_structure', 'ownership_structure_raw', 'operator_type', 'service_model',
    'tier_rating', 'capacity_mw_coded', 'capacity_basis', 'capacity_estimated_mw',
    'siting_determinants', 'operator_siting_logic', 'bis_listed', 'ofac_listed',
    'fdi_screening', 'data_localization', 'attribution_tier', 'notes',
]

ENUMS = {
    'ownership_structure': ['wholly_owned', 'joint_venture', 'private_equity_or_fund',
                            'reit', 'public_company', 'state_owned_or_backed', 'other',
                            NOT_DISCLOSED],
    'operator_type': ['hyperscaler', 'colocation', 'ai_neocloud', 'crypto_mining',
                      'enterprise', 'developer', 'telecom', 'utility_or_energy',
                      'government', 'other', NOT_DISCLOSED],
    'service_model': ['owner_operated', 'wholesale_colocation', 'retail_colocation',
                      'build_to_suit_lease', 'powered_shell', 'hosting', 'other',
                      NOT_DISCLOSED],
    'capacity_basis': ['primary_disclosure', 'secondary_report', 'estimate', NOT_DISCLOSED],
    'bis_listed': ['yes', NOT_DISCLOSED],
    'ofac_listed': ['yes', NOT_DISCLOSED],
    'attribution_tier': ['1', '2', '3', NOT_DISCLOSED],
}

FOREIGN_RELATIONSHIPS = ['owner', 'tenant', 'investor', 'lender_or_funder', 'project_partner', 'other']

EXTRACTION_SCHEMA = {
    'type': 'object',
    'properties': {
        **{f: ({'type': 'string', 'enum': ENUMS[f]} if f in ENUMS else {'type': 'string'})
           for f in ROW_FIELDS},
        'owner_parent_from_public_knowledge': {'type': 'boolean'},
        'foreign_linked_entities': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'entity': {'type': 'string'},
                    'relationship': {'type': 'string', 'enum': FOREIGN_RELATIONSHIPS},
                    'country': {'type': 'string'},
                    'state_linked': {'type': 'boolean'},
                },
                'required': ['entity', 'relationship', 'country', 'state_linked'],
                'additionalProperties': False,
            },
        },
        'evidence_results': {'type': 'array', 'items': {'type': 'integer'}},
    },
    'required': ROW_FIELDS + ['owner_parent_from_public_knowledge', 'foreign_linked_entities', 'evidence_results'],
    'additionalProperties': False,
}

CLAUDE_SYSTEM = f"""You code ownership and jurisdiction fields for US data center facilities \
in a research dataset on infrastructure sovereignty. You receive a FracTracker Alliance \
seed record and a Perplexity web-search answer with its search results. Fill every field \
from that evidence only - never from background knowledge, with the single owner_parent \
exception below, and never by guessing. Any field the evidence does not support is exactly \
"{NOT_DISCLOSED}".

Fields:
- operator: company that runs the facility day to day.
- owner_parent: ultimate parent of the facility owner (the top of the ownership chain, \
e.g. Alphabet Inc., not a site LLC). Exception to evidence-only: when the evidence \
identifies the operator or owner as a well-known publicly listed company or its \
self-named subsidiary (Google -> Alphabet Inc., Meta -> Meta Platforms, Inc., \
AWS -> Amazon.com, Inc.), you may fill its widely known listed parent and set \
owner_parent_from_public_knowledge to true. Never use this exception for private \
companies, site LLCs or SPVs, joint ventures, funds, state backing, or foreign or \
offshore holding structures - those stay evidence-only. It covers owner_parent alone; \
every other field, including owner_origin, still needs evidence. If owner_parent comes \
from the evidence, owner_parent_from_public_knowledge is false.
- operator_nationality: country where the operator is headquartered.
- owner_origin: country where owner_parent is headquartered.
- legal_domicile: jurisdiction where the owning entity is incorporated, e.g. "Delaware, US".
- ownership_structure: one code; ownership_structure_raw: the specifics in words, naming \
JV partners, funds, site LLCs and state investors. Code the structure of the entity that \
owns this facility, as the evidence documents it. A listed operator or a listed parent - \
including one filled in under the owner_parent exception - is not evidence of how the \
facility itself is owned: use public_company only when a source says the listed company \
(or a subsidiary the source links to it) owns this facility, and wholly_owned only when a \
source says one entity owns it outright. If the owning entity or its relationship to the \
operator is undocumented, ownership_structure is "{NOT_DISCLOSED}" even when the operator \
is well known.
- operator_type, service_model: one code each.
- tier_rating: Uptime Institute tier as stated (e.g. "Tier III").
- capacity_mw_coded: the single best facility-level MW figure, as a plain number. \
capacity_basis: primary_disclosure if the operator/owner or a government record stated it; \
secondary_report if only a news outlet, FracTracker or another compiler reports it without \
attributing it to the company; estimate if a source explicitly calls it an estimate. \
capacity_estimated_mw: a third-party estimated figure when one is given - never compute \
one yourself.
- siting_determinants: the factors sources cite for the location (power, land, fiber, \
water, tax incentives, ...), ";"-separated.
- operator_siting_logic: the operator's own stated rationale for the site, briefly.
- bis_listed / ofac_listed: "yes" only if a source says the owner, operator or parent is on \
the BIS Entity List / an OFAC sanctions list.
- fdi_screening: any CFIUS or foreign-investment review, briefly, with outcome.
- data_localization: any data residency, sovereignty or government-hosting requirement \
tied to the facility.
- attribution_tier: the kind of source behind operator / owner_parent / ownership, using \
the strongest source available:
    1 = operator-confirmed: the operator's or owner's own website, press release or \
statement.
    2 = filing-confirmed: an SEC filing or a government record (permits, zoning or \
planning documents, tax-abatement agreements, utility commission or economic development \
agency records).
    3 = analyst-attributed: news coverage, trade press, FracTracker or another compiler, \
or third-party estimates.
  "{NOT_DISCLOSED}" when no source identifies the operator or owner. When unsure between \
two tiers, choose the higher number.
- notes: one or two sentences on ambiguities, conflicts between sources, or when the \
evidence is only about the company and not this facility.
- owner_parent_from_public_knowledge: see owner_parent.
- foreign_linked_entities: every non-US company, fund or government the evidence ties to \
this facility in any role, whether or not it owns the facility - e.g. a foreign tenant, a \
sovereign fund in the project, a foreign government funding associated infrastructure. \
For each: entity (name it as the source does, adding the parent in parentheses only if the \
source names it, e.g. "Core42 (G42)"), relationship, country of headquarters as the source \
states it, and state_linked = true only if a source says it is government-owned, \
government-controlled or government-funded. Evidence-only, like ownership chains: do not \
add entities or countries from background knowledge, and leave out US entities. If the \
evidence names none, return an empty list.
- evidence_results: the numbers of the search results (the [n] in <search_results>) that \
support the fields you filled.

The FracTracker fields are a secondary compilation (tier 3). Its source URLs are listed but \
were not fetched; use only what the Perplexity answer and search results actually say."""


# ============================================================================
# SEED + GEOGRAPHY
# ============================================================================

def facility_id(row):
    """Stable across re-exports: hash of the fields that uniquely identify a row."""
    key = '|'.join(str(row[c]) for c in ('facility_name', 'address', 'city', 'state', 'lat', 'long'))
    return 'FT-' + hashlib.sha1(key.encode()).hexdigest()[:10]


def extra_facility_id(row):
    """Name + place only: the lat/long are our own geocodes and may be redone."""
    key = '|'.join(str(row[c]) for c in ('facility_name', 'city', 'state'))
    return 'TDC-' + hashlib.sha1(key.encode()).hexdigest()[:10]


def load_seed():
    df = pd.read_excel(SEED_PATH, sheet_name=SEED_SHEET)
    df['facility_id'] = df.apply(facility_id, axis=1)
    if os.path.exists(EXTRA_SEED_PATH):
        extra = pd.read_csv(EXTRA_SEED_PATH)
        extra['facility_id'] = extra.apply(extra_facility_id, axis=1)
        df = pd.concat([df, extra[[c for c in extra.columns if c in df.columns]]], ignore_index=True)
    if df['facility_id'].duplicated().any():
        sys.exit('Seed rows produced duplicate facility_ids; refusing to run.')
    return df


def haversine_km(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(np.radians, (lat1, lon1, lat2, lon2))
    a = np.sin((lat2 - lat1) / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin((lon2 - lon1) / 2) ** 2
    return 6371.0 * 2 * np.arcsin(np.sqrt(a))


def load_landing_stations():
    """{station name: True if any in-service cable lands there} from submarinecables (anon key, read-only).

    Falls back to the local dataset that table is synced from if Supabase is unreachable.
    Lake cables (e.g. Lake Michigan) are included; planned / under-construction cables
    are kept but marked not live, so they never count as live infrastructure.
    """
    try:
        cables = fetch_all(get_anon_client(), 'submarinecables', 'id,landing_stations,status')
        print(f"Landing stations: read submarinecables from Supabase ({len(cables)} cables)")
    except Exception as e:
        cables = pd.read_excel(DATASET_PATH)[['landing_stations', 'status']].to_dict('records')
        print(f"⚠ Supabase unreachable ({type(e).__name__}); using {DATASET_PATH}, "
              f"the dataset submarinecables is synced from ({len(cables)} cables)")
    stations = {}
    for cable in cables:
        if not isinstance(cable['landing_stations'], str):
            continue
        live = str(cable['status']).strip().lower() in LIVE_CABLE_STATUSES
        for name in (n.strip() for n in cable['landing_stations'].split(';') if n.strip()):
            parts = [p.strip().lower() for p in name.split(',')]
            if parts[-1] in NEAR_US_COUNTRIES and not (len(parts) == 2 and parts[0] in REGION_NAMES):
                stations[name] = stations.get(name, False) or live
    return stations


def geocode_stations(stations):
    """(name, lat, lon, live) per station via Nominatim, cached in GEOCODE_CACHE so each name is looked up once."""
    cache = {}
    if os.path.exists(GEOCODE_CACHE):
        for r in csv.DictReader(open(GEOCODE_CACHE)):
            cache[r['station']] = r
    missing = [s for s in stations if s not in cache]
    if missing:
        print(f"Geocoding {len(missing)} landing stations (~{len(missing)}s, cached afterwards)...")
        new_file = not os.path.exists(GEOCODE_CACHE)
        with open(GEOCODE_CACHE, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['station', 'lat', 'lon'])
            if new_file:
                writer.writeheader()
            for s in missing:
                resp = requests.get('https://nominatim.openstreetmap.org/search',
                                    params={'q': s, 'format': 'json', 'limit': 1},
                                    headers={'User-Agent': 'researchPlatform-datacenter-enrichment/1.0'},
                                    timeout=30)
                resp.raise_for_status()
                hit = resp.json()
                row = {'station': s, 'lat': hit[0]['lat'] if hit else '', 'lon': hit[0]['lon'] if hit else ''}
                writer.writerow(row)
                f.flush()
                cache[s] = row
                time.sleep(1.1)
    located = [(s, float(cache[s]['lat']), float(cache[s]['lon']), live)
               for s, live in sorted(stations.items()) if cache[s]['lat']]
    print(f"Landing stations: {len(located)} of {len(stations)} near-US stations geocoded")
    return located


def add_geographic_fields(seed, stations):
    """cable_landing_proximity (km to the nearest landing station of an in-service cable),
    a note when a planned / under-construction landing is closer, and interconnection_density."""
    lat, lon = seed['lat'].to_numpy(), seed['long'].to_numpy()
    s_lat = np.array([s[1] for s in stations])
    s_lon = np.array([s[2] for s in stations])
    live = np.array([s[3] for s in stations])
    dist = haversine_km(lat[:, None], lon[:, None], s_lat[None, :], s_lon[None, :])
    rows = np.arange(len(seed))

    live_dist = np.where(live[None, :], dist, np.inf)
    nearest_live = live_dist.argmin(axis=1)
    seed['cable_landing_proximity'] = live_dist[rows, nearest_live].round(1)
    nearest_any = dist.argmin(axis=1)
    seed['landing_note'] = [
        f"nearest in-service landing: {stations[i][0]}"
        + ('' if live[j] else f"; closer planned/under-construction landing (not live): "
                               f"{stations[j][0]} at {dist[r, j]:.1f} km")
        for r, (i, j) in enumerate(zip(nearest_live, nearest_any))
    ]

    pairwise = haversine_km(lat[:, None], lon[:, None], lat[None, :], lon[None, :])
    seed['interconnection_density'] = (pairwise <= DENSITY_RADIUS_KM).sum(axis=1) - 1
    return seed


# ============================================================================
# API CALLS
# ============================================================================

def clean(value):
    return '' if pd.isna(value) else str(value).strip()


def operator_line(row):
    if row['facility_id'].startswith('TDC-'):
        return 'Operator: unknown (identify it from your search)'
    return f"Operator per FracTracker Alliance (may be stale or incomplete): {clean(row['operator_name']) or 'unknown'}"


def search_perplexity(row, api_key):
    location = ', '.join(p for p in (clean(row['address']), clean(row['city']), clean(row['state'])) if p)
    prompt = PERPLEXITY_QUESTION.format(facility_name=clean(row['facility_name']), location=location,
                                        operator_line=operator_line(row))
    body = {
        'model': PERPLEXITY_MODEL,
        'messages': [{'role': 'system', 'content': PERPLEXITY_SYSTEM},
                     {'role': 'user', 'content': prompt}],
        'web_search_options': {'search_context_size': 'medium'},
    }
    for attempt in range(5):
        resp = requests.post(PERPLEXITY_URL, json=body, timeout=120,
                             headers={'Authorization': f'Bearer {api_key}'})
        if resp.status_code == 429 or resp.status_code >= 500:
            time.sleep(min(2 ** attempt * 5, 120))
            continue
        resp.raise_for_status()
        data = resp.json()
        usage = data.get('usage', {})
        cost = (usage.get('cost') or {}).get('total_cost')
        if cost is None:
            cost = (usage.get('prompt_tokens', 0) * PERPLEXITY_PRICE['input']
                    + usage.get('completion_tokens', 0) * PERPLEXITY_PRICE['output']
                    + PERPLEXITY_PRICE['request'])
        results = data.get('search_results') or [{'url': u} for u in data.get('citations', [])]
        return {'answer': data['choices'][0]['message']['content'], 'results': results,
                'usage': usage, 'cost': cost}
    resp.raise_for_status()


def user_content(row, search):
    seed = {c: clean(row[c]) for c in SEED_CONTEXT_COLUMNS if clean(row[c])}
    seed_sources = [clean(row[c]) for c in SEED_SOURCE_COLUMNS if clean(row[c])]
    results = '\n'.join(f"[{i + 1}] {r.get('title', '')} - {r['url']}"
                        + (f" ({r['date']})" if r.get('date') else '')
                        for i, r in enumerate(search['results']))
    return (f"<fractracker_record>\n{json.dumps(seed, indent=1)}\n"
            f"FracTracker source URLs (not fetched): {'; '.join(seed_sources) or 'none'}\n"
            f"</fractracker_record>\n\n"
            f"<perplexity_answer>\n{search['answer']}\n</perplexity_answer>\n\n"
            f"<search_results>\n{results or 'none'}\n</search_results>")


def request_params(model, row, search, cache_ttl):
    """Messages API params shared by the synchronous and Batches paths.

    The system prompt (plus the output schema, which renders ahead of it) is identical for
    every row, so it is cached; only the per-row user content is billed at the full rate.
    """
    cache_control = {'type': 'ephemeral', **({'ttl': cache_ttl} if cache_ttl != '5m' else {})}
    return {
        'model': model,
        'max_tokens': 16000,
        'system': [{'type': 'text', 'text': CLAUDE_SYSTEM, 'cache_control': cache_control}],
        'output_config': {'effort': 'medium',
                          'format': {'type': 'json_schema', 'schema': EXTRACTION_SCHEMA}},
        'messages': [{'role': 'user', 'content': user_content(row, search)}],
    }


def usage_cost(model, usage, batch=False):
    """USD for one response from its usage block (a dict), including cache writes/reads."""
    price = CLAUDE_PRICE[model]
    writes = usage.get('cache_creation') or {}
    write_5m = writes.get('ephemeral_5m_input_tokens', 0)
    write_1h = writes.get('ephemeral_1h_input_tokens', 0)
    if not writes:
        write_5m = usage.get('cache_creation_input_tokens') or 0
    cost = (usage['input_tokens'] * price['input']
            + write_5m * price['input'] * 1.25
            + write_1h * price['input'] * 2
            + (usage.get('cache_read_input_tokens') or 0) * price['cache_read']
            + usage['output_tokens'] * price['output'])
    return cost * (BATCH_DISCOUNT if batch else 1)


def parse_response(message):
    if message.stop_reason == 'refusal':
        raise RuntimeError(f"Claude refused extraction: {message.stop_details}")
    if message.stop_reason == 'max_tokens':
        raise RuntimeError('Claude hit max_tokens before finishing the extraction')
    return json.loads(next(b.text for b in message.content if b.type == 'text'))


def extract_with_claude(client, model, row, search):
    response = client.beta.messages.create(
        **request_params(model, row, search, cache_ttl='5m'),
        betas=['server-side-fallback-2026-07-01'],
        fallbacks='default',
    )
    return parse_response(response), response, usage_cost(model, response.usage.to_dict())


def build_row(row, fields, search):
    """Merge deterministic seed/geography fields with Claude's coded fields."""
    from_public_knowledge = fields.pop('owner_parent_from_public_knowledge')
    linked = fields.pop('foreign_linked_entities')
    allowed = {r['url'] for r in search['results']}
    # Claude cites search results by number; resolve them to the full URLs saved with the search.
    # (Rows extracted before this change cite URLs directly.)
    if 'evidence_results' in fields:
        numbers = fields.pop('evidence_results')
        cited = [search['results'][n - 1]['url'] for n in numbers if 1 <= n <= len(search['results'])]
    else:
        cited = fields.pop('evidence_urls')
    evidence = [u for u in dict.fromkeys(cited) if u in allowed]
    seed_sources = [clean(row[c]) for c in SEED_SOURCE_COLUMNS if clean(row[c])]

    out = {k: (v.strip() if isinstance(v, str) else v) for k, v in fields.items()}
    out = {k: (v if v not in ('', None) else NOT_DISCLOSED) for k, v in out.items()}
    for k in ('operator_nationality', 'owner_origin'):
        if out[k] != NOT_DISCLOSED:
            out[k] = canonical_country(out[k])
    notes = [out['notes']] if out['notes'] != NOT_DISCLOSED else []
    if from_public_knowledge and out['owner_parent'] != NOT_DISCLOSED:
        out['attribution_tier'] = '3'
        notes.append('owner_parent from public corporate structure, not facility-specific '
                     'evidence (tier set to 3)')
    notes.append(row['landing_note'])
    out.update({
        'facility_id': row['facility_id'],
        'facility_name': clean(row['facility_name']),
        'country': 'United States',
        'city': ', '.join(p for p in (clean(row['city']), clean(row['state'])) if p),
        'lat': row['lat'],
        'lon': row['long'],
        'capacity_raw': clean(row['mw']) or NOT_DISCLOSED,
        'status': clean(row['status']) or NOT_DISCLOSED,
        'cable_landing_proximity': row['cable_landing_proximity'],
        'interconnection_density': row['interconnection_density'],
        'source_urls': '; '.join(dict.fromkeys(evidence + seed_sources)) or NOT_DISCLOSED,
        'notes': ' | '.join(notes),
    })
    out['foreign_linked_entities'] = '; '.join(
        f"{e['entity'].strip()} | {e['relationship']} | {canonical_country(e['country'])}"
        + (' | state-linked' if e['state_linked'] else '')
        for e in linked
    ) or NOT_DISCLOSED
    return {c: out[c] for c in OUTPUT_COLUMNS}


# ============================================================================
# SPEND TRACKING
# ============================================================================

# Per-row rates from the Opus dry run, used only until real rows exist to average.
CLAUDE_ROW_ESTIMATE = 0.047
# Fixed system prompt + output schema, in tokens (fit from logged usage: ~2,825 before the
# foreign_linked_entities instructions were added). Used only for the cache-write allowance.
CACHE_PREFIX_TOKENS = 3200
SEARCH_ESTIMATE = 0.0073


def past_costs(output):
    """Claude cost of every row already in `output` and Perplexity cost of every cached search."""
    claude = []
    if os.path.exists(output + '.raw.jsonl'):
        for line in open(output + '.raw.jsonl'):
            c = json.loads(line)['claude']
            claude.append(c['cost'] if 'cost' in c else usage_cost(c['model'], c['usage']))
    searches = []
    if os.path.exists(SEARCH_CACHE):
        searches = [json.loads(line)['search']['cost'] for line in open(SEARCH_CACHE)]
    return claude, searches


def average(costs, default):
    return sum(costs) / len(costs) if costs else default


# ============================================================================
# RUN
# ============================================================================

def migrate_columns(output):
    """Add new OUTPUT_COLUMNS to an existing CSV, marking old rows NOT_EXTRACTED. Keeps a backup."""
    old = pd.read_csv(output, dtype=str, keep_default_na=False)
    added = [c for c in OUTPUT_COLUMNS if c not in old.columns]
    if not added:
        print(f"{output} already has every column; nothing to do.")
        return
    backup = output + '.pre-migration.bak'
    shutil.copyfile(output, backup)
    for c in added:
        old[c] = NOT_EXTRACTED
    old[OUTPUT_COLUMNS].to_csv(output, index=False)
    print(f"Added {added} to {len(old)} rows of {output} (marked '{NOT_EXTRACTED}'); backup at {backup}")


def print_remaining(output, searches, claude_costs, search_costs, model, total_seed):
    completed = set(pd.read_csv(output, usecols=['facility_id'])['facility_id'])
    remaining = load_seed().loc[lambda d: ~d['facility_id'].isin(completed), 'facility_id']
    claude_rate = average(claude_costs, CLAUDE_ROW_ESTIMATE)
    search_rate = average(search_costs, SEARCH_ESTIMATE)
    need_search = sum(i not in searches for i in remaining)
    print(f"\n{output}: {len(completed)} of {total_seed} rows completed, {len(remaining)} remaining "
          f"({len(remaining) - need_search} with cached searches).")
    print(f"To finish with {model}: Perplexity ~${need_search * search_rate:,.2f} for {need_search} searches "
          f"(${search_rate:.4f}/search over {len(search_costs)}); Claude ~${len(remaining) * claude_rate:,.2f} "
          f"at the logged average of ${claude_rate:.4f}/row over {len(claude_costs)} rows "
          f"(mostly synchronous, uncached - Batches + caching cost less).")
    print("Nothing was written to Supabase.")


def run_search_only(todo, searches, searches_f, api_key, search_costs, args):
    """Perplexity step alone: search and cache every remaining row that has no cached search."""
    rows = [r for _, r in todo.iterrows() if r['facility_id'] not in searches][:args.max_rows]
    cached = sum(r['facility_id'] in searches for _, r in todo.iterrows())
    print(f"{cached} remaining rows already have a cached search; searching {len(rows)} now. "
          f"Est. ${len(rows) * average(search_costs, SEARCH_ESTIMATE):.2f} at "
          f"${average(search_costs, SEARCH_ESTIMATE):.4f}/search (Perplexity's own reported cost).")
    err_path = SEARCH_CACHE.replace('.jsonl', '.errors.jsonl')
    spent, done, failed, stop = 0.0, 0, 0, None
    with open(err_path, 'a') as err_f:
        for start in range(0, len(rows), args.batch_size):
            batch = rows[start:start + args.batch_size]
            est = len(batch) * average(search_costs, SEARCH_ESTIMATE)
            if args.perplexity_cap is not None and spent + est > args.perplexity_cap:
                stop = f"Perplexity cap ${args.perplexity_cap:.2f}: ${spent:.2f} spent + next batch est. ${est:.2f}"
                break
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                futures = {pool.submit(search_perplexity, r, api_key): r for r in batch}
                for future in as_completed(futures):
                    row = futures[future]
                    try:
                        search = future.result()
                    except Exception as e:
                        failed += 1
                        err_f.write(json.dumps({'facility_id': row['facility_id'],
                                                'error': f"{type(e).__name__}: {e}"}) + '\n')
                        err_f.flush()
                        print(f"  ✗ {clean(row['facility_name'])} ({row['facility_id']}): {type(e).__name__}: {e}")
                        continue
                    searches_f.write(json.dumps({'facility_id': row['facility_id'], 'search': search}) + '\n')
                    searches_f.flush()
                    searches[row['facility_id']] = search
                    search_costs.append(search['cost'])
                    spent += search['cost']
                    done += 1
                    print(f"  [{done} of {len(rows)} searched] {clean(row['facility_name'])[:40]:40} "
                          f"${search['cost']:.4f} | run ${spent:.2f}")
            if start + args.batch_size < len(rows):
                time.sleep(args.batch_delay)
    print(f"\nSearched {done} rows, {failed} failed (see {err_path}). Perplexity reported cost: ${spent:.2f}.")
    if stop:
        print(f"Stopped before the next batch - {stop}.")
    print(f"{SEARCH_CACHE} now holds {len(searches)} searches. No Claude calls were made.")


def worst_case_batch_rate(model, claude_costs):
    """Per-row batch cost to size a chunk with, assuming every row writes the prompt cache.

    A big batch runs in parallel, so many rows miss the cache: on 2026-10-29 a third of a
    1,137-row batch wrote it (2x input price) instead of reading it, and the batch cost 21%
    over the average of earlier, mostly-cached rows. So take each logged batched row's
    cost as if its cache read had been a 1h write, average that, and add a margin.
    """
    price = CLAUDE_PRICE[model]
    miss_premium = (price['input'] * 2 - price['cache_read']) * BATCH_DISCOUNT
    rates = []
    for line in open(FULL_OUTPUT + '.raw.jsonl') if os.path.exists(FULL_OUTPUT + '.raw.jsonl') else []:
        c = json.loads(line)['claude']
        if c.get('batch'):
            rates.append(c['cost'] + (c['usage'].get('cache_read_input_tokens') or 0) * miss_premium)
    if rates:
        return average(rates, 0) * BATCH_SAFETY, f'worst case (every row a cache write) over {len(rates)} batched rows'
    p90 = float(np.percentile(claude_costs, 90)) if claude_costs else CLAUDE_ROW_ESTIMATE
    return (p90 * BATCH_DISCOUNT + CACHE_PREFIX_TOKENS * miss_premium) * BATCH_SAFETY, 'conservative: no batched rows yet'


def collect_batch(client, entry, seed, searches, writer, out_f, raw_f, err_f, claude_costs, state_path):
    """Wait for one submitted batch, write its results like the synchronous path, and return its cost."""
    batch_id = entry['batch_id']
    while True:
        b = client.messages.batches.retrieve(batch_id)
        c = b.request_counts
        print(f"  {time.strftime('%H:%M:%S')} batch {batch_id}: {b.processing_status} - "
              f"{c.succeeded} succeeded, {c.errored} errored, {c.processing} processing")
        if b.processing_status == 'ended':
            break
        time.sleep(60)
    spent = done = failed = 0
    for result in client.messages.batches.results(batch_id):
        fid = result.custom_id
        row, search = seed.loc[fid], searches[fid]
        try:
            if result.result.type != 'succeeded':
                raise RuntimeError(f"batch result {result.result.type}: {getattr(result.result, 'error', '')}")
            message = result.result.message
            fields = parse_response(message)
            usage = message.usage.to_dict()
            cost = usage_cost(entry['model'], usage, batch=True)
        except Exception as e:
            # A refused or invalid result may still be billed; count it if usage is there.
            if result.result.type == 'succeeded':
                spent += usage_cost(entry['model'], result.result.message.usage.to_dict(), batch=True)
            failed += 1
            err_f.write(json.dumps({'facility_id': fid, 'facility_name': clean(row['facility_name']),
                                    'error': f"{type(e).__name__}: {e}", 'batch_id': batch_id}) + '\n')
            err_f.flush()
            print(f"  ✗ {clean(row['facility_name'])} ({fid}): {type(e).__name__}: {e}")
            continue
        writer.writerow(build_row(row, dict(fields), search))
        out_f.flush()
        raw_f.write(json.dumps({'facility_id': fid, 'perplexity': {**search, 'cost': 0.0},
                                'claude': {'model': message.model, 'fields': fields, 'usage': usage,
                                           'cost': cost, 'batch': True, 'batch_id': batch_id}},
                               default=str) + '\n')
        raw_f.flush()
        claude_costs.append(cost)
        spent += cost
        done += 1
    with open(state_path, 'a') as f:
        f.write(json.dumps({'batch_id': batch_id, 'collected': True}) + '\n')
    print(f"\nBatch {batch_id}: {done} rows written, {failed} failed. Claude cost ${spent:.2f} "
          f"(${spent / max(done, 1):.4f}/row at batch price, cache included).")
    return spent


def run_batch(client, model, todo, searches, writer, out_f, raw_f, err_f, claude_costs, args, output):
    """Extract via the Message Batches API: collect any batch already submitted, then submit chunks
    of at most --batch-rows one at a time, each sized to what is left of --claude-cap after the
    billed cost of the chunks before it, at a worst-case per-row rate. A chunk is billed in full
    even if it overruns the balance, so no chunk may be able to exceed what remains."""
    state_path = output + '.batches.jsonl'
    state = [json.loads(line) for line in open(state_path)] if os.path.exists(state_path) else []
    collected = {s['batch_id'] for s in state if s.get('collected')}
    pending = [s for s in state if 'facility_ids' in s and s['batch_id'] not in collected]
    seed = load_seed()
    seed = add_geographic_fields(seed, geocode_stations(load_landing_stations())).set_index('facility_id', drop=False)
    collect = lambda entry: collect_batch(client, entry, seed, searches, writer, out_f, raw_f, err_f,
                                          claude_costs, state_path)

    # A batch left from an earlier run was budgeted then; count it against this cap anyway.
    spent = sum(collect(entry) for entry in pending)
    submitted = {fid for entry in pending for fid in entry['facility_ids']}
    rows = [r for _, r in todo.iterrows() if r['facility_id'] in searches and r['facility_id'] not in submitted]
    if len(rows) + len(submitted) < len(todo):
        print(f"{len(todo) - len(rows) - len(submitted)} remaining rows have no cached search yet - run --search-only first.")
    rows = rows[:args.max_rows]
    cache_write = CACHE_PREFIX_TOKENS * CLAUDE_PRICE[model]['input'] * 2 * BATCH_DISCOUNT
    while rows:
        per_row, basis = worst_case_batch_rate(model, claude_costs)
        left = args.claude_cap - spent
        n = min(len(rows), args.batch_rows, max(0, int((left - cache_write) // per_row)))
        if n == 0:
            print(f"${left:.2f} left of --claude-cap ${args.claude_cap:.2f} doesn't cover one row at "
                  f"${per_row:.4f}/row ({basis}); stopping with {len(rows)} rows unsubmitted.")
            break
        chunk, rows = rows[:n], rows[n:]
        print(f"Submitting {n} rows: at most ${n * per_row + cache_write:.2f} (${per_row:.4f}/row, {basis}); "
              f"${spent:.2f} spent so far this run, cap ${args.claude_cap:.2f}.")
        batch = client.messages.batches.create(requests=[
            {'custom_id': r['facility_id'],
             'params': request_params(model, r, searches[r['facility_id']], cache_ttl='1h')}
            for r in chunk
        ])
        entry = {'batch_id': batch.id, 'model': model, 'facility_ids': [r['facility_id'] for r in chunk],
                 'submitted_at': time.strftime('%Y-%m-%dT%H:%M:%S')}
        with open(state_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        print(f"Batch {batch.id} submitted; recorded in {state_path} so it can be collected if this exits.")
        spent += collect(entry)
    print(f"\nClaude cost this run: ${spent:.2f} of cap ${args.claude_cap:.2f}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--full', action='store_true', help='process every row (default: dry run on the first 10)')
    parser.add_argument('--limit', type=int, help='process only the first N seed rows')
    parser.add_argument('--ids', help='comma-separated facility_ids to process (instead of seed order)')
    parser.add_argument('--perplexity-cap', type=float, help='USD; stop before a batch that could exceed it')
    parser.add_argument('--claude-cap', type=float, help='USD; stop before a batch that could exceed it')
    parser.add_argument('--batch-size', type=int, default=25)
    parser.add_argument('--batch-delay', type=float, default=10.0, help='seconds to wait between batches')
    parser.add_argument('--workers', type=int, default=4, help='concurrent rows within a batch')
    parser.add_argument('--model', choices=CLAUDE_MODELS, default='opus', help='Claude model for extraction')
    parser.add_argument('--output')
    parser.add_argument('--batch-rows', type=int, default=200,
                        help='--batch: rows per submitted batch; each waits for the last so its real cost counts')
    parser.add_argument('--max-rows', type=int, help='process at most N of the remaining rows this run')
    parser.add_argument('--search-only', action='store_true',
                        help='run and cache only the Perplexity searches (no Claude calls)')
    parser.add_argument('--batch', action='store_true',
                        help='extract via the Message Batches API (half price; results within 24h); needs cached searches')
    parser.add_argument('--migrate-columns', action='store_true',
                        help='add columns this version writes to an existing output CSV (no API calls), then exit')
    args = parser.parse_args()

    if args.migrate_columns:
        migrate_columns(args.output or FULL_OUTPUT)
        return

    needed = ['PERPLEXITY_API_KEY'] if args.search_only else (
        ['ANTHROPIC_API_KEY'] if args.batch else ['PERPLEXITY_API_KEY', 'ANTHROPIC_API_KEY'])
    if args.batch and args.claude_cap is None:
        sys.exit('--batch needs --claude-cap: a submitted batch is billed in full, so its size is set from the cap.')
    keys = {name: env_key(name) for name in needed}
    missing = [name for name, value in keys.items() if not value]
    if missing:
        sys.exit(f"Missing {', '.join(missing)}: add {'them' if len(missing) > 1 else 'it'} to .env "
                 f"(gitignored) as NAME=value, or export in the environment.")

    client = None
    if 'ANTHROPIC_API_KEY' in keys:
        import anthropic
        # Retries aren't logged, and a request that fails after Anthropic processes it is still
        # billed - keep them to one so unlogged spend stays small.
        # Keys not scoped to a workspace (e.g. an org-level research key) must name one per request.
        workspace = env_key('ANTHROPIC_WORKSPACE_ID')
        client = anthropic.Anthropic(api_key=keys['ANTHROPIC_API_KEY'], max_retries=1,
                                     default_headers={'anthropic-workspace-id': workspace} if workspace else None)

    model = CLAUDE_MODELS[args.model]
    output = args.output or (FULL_OUTPUT if args.full else DRY_RUN_OUTPUT.format(model=args.model))
    seed = load_seed()
    seed = add_geographic_fields(seed, geocode_stations(load_landing_stations()))
    total_seed = len(seed)
    if args.ids:
        ids = [i.strip() for i in args.ids.split(',')]
        unknown = set(ids) - set(seed['facility_id'])
        if unknown:
            sys.exit(f"Unknown facility_ids: {', '.join(sorted(unknown))}")
        seed = seed.set_index('facility_id', drop=False).loc[ids].reset_index(drop=True)
    limit = args.limit or (None if args.full or args.ids else DRY_RUN_ROWS)
    if limit:
        seed = seed.head(limit)

    done = set()
    if os.path.exists(output):
        header = next(csv.reader(open(output)))
        if header != OUTPUT_COLUMNS:
            sys.exit(f"{output} has different columns than this version writes; "
                     f"run with --migrate-columns to add {sorted(set(OUTPUT_COLUMNS) - set(header))}.")
        done = set(pd.read_csv(output, usecols=['facility_id'])['facility_id'])
    todo = seed[~seed['facility_id'].isin(done)]
    # Rows that failed on an earlier run go first, then the rest in seed order.
    failed = []
    if os.path.exists(output + '.errors.jsonl'):
        failed = list(dict.fromkeys(json.loads(line)['facility_id'] for line in open(output + '.errors.jsonl')))
    todo = todo.assign(_retry=~todo['facility_id'].isin(failed)).sort_values('_retry', kind='stable').drop(columns='_retry')
    total = len(seed)
    mode = 'SEARCH ONLY' if args.search_only else 'BATCH' if args.batch else 'FULL RUN' if args.full else 'DRY RUN'
    print(f"\n{mode} ({'perplexity' if args.search_only else model}): {total} rows, "
          f"{total - len(todo)} already in {output}, {len(todo)} remaining\n")

    new_file = not os.path.exists(output)
    out_f = open(output, 'a', newline='')
    writer = csv.DictWriter(out_f, fieldnames=OUTPUT_COLUMNS)
    if new_file:
        writer.writeheader()
        out_f.flush()
    raw_f = open(output + '.raw.jsonl', 'a')
    searches_path = SEARCH_CACHE
    searches = {}
    if os.path.exists(searches_path):
        for line in open(searches_path):
            entry = json.loads(line)
            searches[entry['facility_id']] = entry['search']
    searches_f = open(searches_path, 'a')
    searches_lock = threading.Lock()
    err_f = open(output + '.errors.jsonl', 'a')

    stats = {'done': total - len(todo), 'new': 0, 'failed': 0, 'perplexity': 0.0, 'claude': 0.0}
    claude_costs, search_costs = past_costs(output)

    if args.search_only:
        run_search_only(todo, searches, searches_f, keys['PERPLEXITY_API_KEY'], search_costs, args)
        out_f.close(), raw_f.close(), err_f.close(), searches_f.close()
        return
    if args.batch:
        run_batch(client, model, todo, searches, writer, out_f, raw_f, err_f, claude_costs, args, output)
        out_f.close(), raw_f.close(), err_f.close(), searches_f.close()
        print_remaining(output, searches, claude_costs, search_costs, model, total_seed)
        return

    def process(row):
        search = searches.get(row['facility_id'])
        if search is None:
            search = search_perplexity(row, keys['PERPLEXITY_API_KEY'])
            with searches_lock:
                searches_f.write(json.dumps({'facility_id': row['facility_id'], 'search': search}) + '\n')
                searches_f.flush()
        else:
            search = {**search, 'cost': 0.0}
        fields, response, claude_cost = extract_with_claude(client, model, row, search)
        raw = {'facility_id': row['facility_id'], 'perplexity': search,
               'claude': {'model': response.model, 'fields': fields, 'usage': response.usage.to_dict(),
                          'cost': claude_cost, 'batch': False}}
        return build_row(row, dict(fields), search), raw, search['cost'], claude_cost

    rows = [r for _, r in todo.iterrows()][:args.max_rows]
    stopped_for_cap = None
    for start in range(0, len(rows), args.batch_size):
        batch = rows[start:start + args.batch_size]
        claude_rate, search_rate = average(claude_costs, CLAUDE_ROW_ESTIMATE), average(search_costs, SEARCH_ESTIMATE)
        est_claude = len(batch) * claude_rate
        est_search = sum(r['facility_id'] not in searches for r in batch) * search_rate
        for name, cap, spent_so_far, est in (('Perplexity', args.perplexity_cap, stats['perplexity'], est_search),
                                             ('Claude', args.claude_cap, stats['claude'], est_claude)):
            if cap is not None and spent_so_far + est > cap:
                stopped_for_cap = (f"{name} cap ${cap:.2f}: ${spent_so_far:.2f} spent + next batch "
                                   f"est. ${est:.2f} would exceed it")
        if stopped_for_cap:
            break
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(process, r): r for r in batch}
            for future in as_completed(futures):
                row = futures[future]
                try:
                    out_row, raw, p_cost, c_cost = future.result()
                except Exception as e:
                    stats['failed'] += 1
                    err_f.write(json.dumps({'facility_id': row['facility_id'],
                                            'facility_name': clean(row['facility_name']),
                                            'error': f"{type(e).__name__}: {e}"}) + '\n')
                    err_f.flush()
                    print(f"  ✗ {clean(row['facility_name'])} ({row['facility_id']}): {type(e).__name__}: {e}")
                    continue
                writer.writerow(out_row)
                out_f.flush()
                raw_f.write(json.dumps(raw, default=str) + '\n')
                raw_f.flush()
                stats['done'] += 1
                stats['new'] += 1
                stats['perplexity'] += p_cost
                stats['claude'] += c_cost
                claude_costs.append(c_cost)
                if p_cost:
                    search_costs.append(p_cost)
                spent = stats['perplexity'] + stats['claude']
                print(f"  [{stats['done']} of {total} done] {out_row['facility_name'][:40]:40} "
                      f"tier {out_row['attribution_tier']:>13} | row ${p_cost + c_cost:.3f} "
                      f"| run ${spent:.2f} (avg ${spent / stats['new']:.3f}/row)")
        if start + args.batch_size < len(rows):
            time.sleep(args.batch_delay)

    out_f.close(), raw_f.close(), err_f.close(), searches_f.close()
    spent = stats['perplexity'] + stats['claude']
    print(f"\nProcessed {stats['new']} new rows, {stats['failed']} failed "
          f"(see {output}.errors.jsonl; re-run to retry them).")
    if stopped_for_cap:
        print(f"Stopped before the next batch - {stopped_for_cap}.")
    print(f"Cost this run: ${spent:.2f} (Perplexity ${stats['perplexity']:.2f}, Claude ${stats['claude']:.2f})")

    print_remaining(output, searches, claude_costs, search_costs, model, total_seed)


if __name__ == '__main__':
    main()
