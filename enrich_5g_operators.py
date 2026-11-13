"""
Build the 5G operator-vendor panel: one row per licensed 5G mobile operator per observation
year, coding the briefing's five layers (physical, network, vendor, ownership, regulatory)
with vendor recorded per network element. Codebook: 5G Networks briefing (variable framework,
coding rules, missingness, worked German row).

Phase 1 (this script): the current year only.
  1. Discovery: one Perplexity search per market ("licensed mobile network operators offering
     5G service in <market>"), coded by Claude into data/5g_operators.csv. No seed file.
  2. Per operator: vendor, physical/network, ownership, spectrum-inventory and coverage
     searches, plus one regulatory
     search per market, all cached in data/5g_searches.jsonl so nothing is paid for twice.
  3. Claude codes each operator from its searches into data/5g_operator_panel.csv
     (resumable by row_id). Derived fields (vendor origin, per-element HHI) and the cable join
     to the submarinecables table are computed here, not by Claude.
Phase 2 (2019-present annual panel) reuses the same row shape with one row per year.

Every coded field records a status (value / not_disclosed / not_applicable /
not_yet_collected), an attribution tier (1 operator-confirmed, 2 filing-confirmed, 3
analyst-attributed with the house named) and its source. Nothing is left blank. Output is
local CSV only - nothing is written to Supabase; submarinecables is only read (anon key).

Usage:
  python enrich_5g_operators.py --estimate                      # cost estimate, no API calls
  python enrich_5g_operators.py --markets Germany \\
      --perplexity-cap 0.30 --claude-cap 1.20                   # dry run -> data/5g_operator_panel_dryrun.csv
  python enrich_5g_operators.py --full --batch \\
      --perplexity-cap X --claude-cap Y                         # every market -> data/5g_operator_panel.csv

Caps are required for any run that calls an API; each step stops before it could exceed them.
"""

import argparse
import json
import os
import re
import sys
import threading
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date

import jsonschema
import numpy as np
import pandas as pd

from pipeline_common import (anthropic_client, average, canonical_country, env_key, fetch_all, get_anon_client,
                             open_resumable_csv, perplexity_search, run_capped_batches, usage_cost,
                             worst_case_batch_rate)

# Core panel (panel_tier "core"). The contrast tier (Africa, Southeast Asia, Latin America)
# is added later with its own panel_tier value.
MARKETS = {
    'Germany': 'DE', 'Sweden': 'SE', 'United Kingdom': 'GB', 'France': 'FR', 'Italy': 'IT',
    'Spain': 'ES', 'Netherlands': 'NL', 'Poland': 'PL', 'Belgium': 'BE', 'Austria': 'AT',
    'Switzerland': 'CH', 'Norway': 'NO', 'Denmark': 'DK', 'Finland': 'FI', 'Ireland': 'IE',
    'Portugal': 'PT', 'Greece': 'GR', 'Czechia': 'CZ', 'Romania': 'RO', 'Hungary': 'HU',
    'Croatia': 'HR', 'Slovakia': 'SK', 'Bulgaria': 'BG', 'Estonia': 'EE', 'Lithuania': 'LT',
    'United States': 'US', 'China': 'CN',
}
PANEL_TIER = 'core'
MODEL = 'claude-opus-5-5'

VALUE = 'value'
NOT_DISCLOSED = 'not_disclosed'        # the value exists and nobody published it
NOT_APPLICABLE = 'not_applicable'      # the question does not arise
NOT_YET_COLLECTED = 'not_yet_collected'  # the coder has not reached the cell
STATUSES = [VALUE, NOT_DISCLOSED, NOT_APPLICABLE, NOT_YET_COLLECTED]
TIERS = ['1', '2', '3', 'none']

SEARCH_CACHE = 'data/5g_searches.jsonl'
OPERATORS_PATH = 'data/5g_operators.csv'
FULL_OUTPUT = 'data/5g_operator_panel.csv'
DRY_RUN_OUTPUT = 'data/5g_operator_panel_dryrun.csv'
DISCOVERY_LOG = 'data/5g_discovery.raw.jsonl'

# Priors until real rows exist to average (see --estimate). Searches: the data-center
# sonar-pro average was $0.0073; these prompts ask for more, so assume a little higher.
SEARCH_ESTIMATE = 0.009
DISCOVERY_ESTIMATE = 0.045   # one Claude call per market, synchronous
OPERATOR_ESTIMATE = 0.125    # one synchronous Claude extraction over six searches
# State equity (percent) above which an operator is state-backed whether or not it is also
# listed; at STATE_OWNED_PCT or more it is state-owned. Applied in the prompt and enforced in
# build_row from the coded state_equity_pct.
STATE_BACKED_PCT = 10
STATE_OWNED_PCT = 50
# Every state ownership_type stays provisional until Prof. Shen signs off on the state-holder
# list and the two open rules; flagged per row in ownership_type_provisional and the notes.
STATE_TYPES = ('state_owned', 'state_backed_minority')
PROVISIONAL_NOTE = ("ownership_type PROVISIONAL: pending Prof. Shen's sign-off on data/state_holders.csv and on "
                    "two open rules (sum state stakes across states or count per state; whether passive "
                    "sovereign-fund stakes such as Norges or GIC count)")

# Shareholders that are states or state-controlled (data/state_holders.csv), given to Claude as a
# reference list: shareholder disclosures name the holder, rarely the state behind it (e& for
# the UAE). Compiled by Claude from general knowledge, not from sources; each row carries a
# review_status and the source to verify it against. A holder not listed counts only when the
# evidence itself shows the state link, and every list-based classification is flagged per row.
STATE_HOLDERS_PATH = 'data/state_holders.csv'
STATE_HOLDERS = pd.read_csv(STATE_HOLDERS_PATH, dtype=str, keep_default_na=False)
STATE_HOLDER_ENTRIES = set(STATE_HOLDERS['entry'])
STATE_HOLDER_REFERENCE = '\n'.join(f"  {r.entry} | {r.also_named} | {r.state}" for r in STATE_HOLDERS.itertuples())

# Fixed system prompt (which carries the output schema), in tokens (messages.count_tokens, 2026-11-02). Used only
# for the cache-write allowance when sizing batches.
PREFIX_TOKENS = 10105
LAYERS = ['vendor', 'physical', 'ownership', 'spectrum', 'coverage']  # per-operator; 'regulatory' is per market
# Result-label prefix of each search block in the extraction input (and in build_row's URL lookup).
BLOCKS = (('vendor', 'V'), ('physical', 'P'), ('ownership', 'O'), ('spectrum', 'S'), ('coverage', 'C'),
          ('regulatory', 'R'))

# ============================================================================
# PERPLEXITY PROMPTS
# ============================================================================

PERPLEXITY_SYSTEM = """You research 5G mobile networks for an academic dataset on vendor \
dependence. Use regulator records, operator reports and filings, government instruments and \
named industry analysts. State only what sources say, with dates. For every vendor share or \
cost figure, name the house that produced it (e.g. Strand Consult, Dell'Oro, Omdia, Barclays) \
and say what it is a share of. Keep figures for a specific operator separate from figures for \
the whole national market. Write "not found" for anything the sources don't cover; never \
estimate."""

# The first line of the discovery prompt is the search the panel is defined by.
DISCOVERY_QUESTION = """licensed mobile network operators offering 5G service in {market}

List every mobile network operator in {market} that holds its own spectrum licence and offers \
commercial 5G service as of {year}. For each give: the operator's common name and legal \
entity, its brands, its parent company, its 5G commercial launch date (and whether launched or \
only soft-launched), and the licensing regulator. Exclude MVNOs and resellers without their own \
radio network, but name notable ones you excluded and why."""

LAYER_QUESTIONS = {
    'vendor': """{operator} ({market}) - 5G network equipment vendors as of {year}.
For each network element give the supplier(s) and, only where a source reports one, their \
share and what it is a share of:
1. Radio access network (RAN): radio and baseband vendors.
2. 5G core network vendor, and the 4G core (EPC) vendor if 5G runs non-standalone.
3. Transport / backhaul equipment vendors.
4. Network management, OSS, and RAN configuration / update-management system vendor.
5. Open RAN: deploying O-RAN interfaces in production, using O-RAN principles for future \
evolution, or neither.
6. Whether the 5G RAN was built on the operator's 4G footprint from the same vendor.
7. Any removal or replacement of Huawei or ZTE equipment: which element, deadline, and cost \
estimates (name who estimated).
Say which figures are for the national market rather than for {operator}.""",

    'physical': """{operator} ({market}) - 5G spectrum, licences, network and international \
connectivity as of {year}.
1. Spectrum held, in MHz, per band, using the regulator's own band names (e.g. 700 MHz, \
3.6 GHz, 26 GHz), and the award each came from.
2. For each 5G licence: award date, expiry date, and renewal conditions.
3. 5G core architecture: non-standalone, standalone, or both in parallel.
4. 5G coverage figures, each with its definition (share of population, share of territory, \
or standalone availability), date and who reported it.
5. International gateway: held by the operator, a state entity, or a third party.
6. Submarine cables the operator owns capacity on or depends on for international traffic.
7. Internet exchange points the operator peers at (how many) and its upstream IP transit \
providers.""",

    # Spectrum and coverage get their own searches (2026-11-13): inside the physical search they
    # came back mostly "not found" for bands outside the 5G auctions.
    'spectrum': """{operator} ({market}) - complete mobile spectrum holdings as of {year}.
List every band in which {operator} holds a mobile spectrum licence, for all technologies and \
not only 5G (e.g. 700, 800, 900 MHz, 1.5 GHz, 1800 MHz, 2.1, 2.3, 2.6 GHz, 3.4-3.8 GHz, 26 GHz), \
with the amount in MHz for each (paired bands as 2x n MHz), the licence expiry date, and the \
award it came from. Use the national regulator's spectrum register or licence table where \
possible, naming it and its date. Say whether the list is the operator's complete holding or \
only part of it.""",

    'coverage': """{operator} ({market}) - 5G coverage as of {year}.
1. The latest 5G coverage percentage that {operator} reports, or that the regulator reports for \
{operator}, with its exact definition (share of population, households or territory; outdoor or \
indoor; any minimum speed), its date and its source.
2. Any 5G standalone coverage or availability figure, with the same detail.
Keep {operator}'s figures separate from national-market and group-level figures.""",

    'ownership': """{operator} ({market}) - ownership as of {year}.
1. Ownership type: private, publicly listed, state-owned, or state-backed through a minority \
stake.
2. Significant shareholders: every holder of 3% or more of the operator and of its ultimate \
parent, as listed in the latest major-shareholding disclosures (annual report, securities \
regulator register such as the CNMV, AMF, BaFin or SEC filings), with the percentage and the \
date of each figure. Then say which of these holders are governments, state-owned companies or \
sovereign wealth funds, and the state behind each.
3. The ultimate parent company and the country where it is legally incorporated.
4. The operating entity's jurisdiction of incorporation, if different from {market}.""",

    'regulatory': """{market} - 5G vendor restrictions and telecom regulation as of {year}.
1. Any restriction on high-risk 5G suppliers (e.g. Huawei, ZTE): the instrument (statute, \
contract, licence condition, or administrative designation), whether it is binding, \
voluntary, or proposed, and which operators it binds.
2. Which network elements it covers: core, radio access network, transport, network \
management systems.
3. Removal or rip-and-replace deadlines per element, and any public funding for replacement.
4. Where relevant, the status of the EU 5G Toolbox and the proposed revision of the EU \
Cybersecurity Act for {market}.
5. Data localization requirements for subscriber or traffic data.
6. Foreign investment screening that covers telecom operators or licences, and the authority.
7. How 5G spectrum was awarded: auction, comparative selection, administrative allocation, \
or direct award.""",
}

# ============================================================================
# CLAUDE: DISCOVERY
# ============================================================================

DISCOVERY_SCHEMA = {
    'type': 'object',
    'properties': {
        'operators': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'operator_name': {'type': 'string'},
                    'legal_entity': {'type': 'string'},
                    'brands': {'type': 'string'},
                    'parent_company': {'type': 'string'},
                    'holds_spectrum_licence': {'type': 'string', 'enum': ['yes', 'no', 'unclear']},
                    'five_g_status': {'type': 'string',
                                      'enum': ['launched', 'soft_launched', 'announced', 'none', 'unclear']},
                    'five_g_launch_date': {'type': 'string'},
                    'evidence_results': {'type': 'array', 'items': {'type': 'integer'}},
                },
                'required': ['operator_name', 'legal_entity', 'brands', 'parent_company',
                             'holds_spectrum_licence', 'five_g_status', 'five_g_launch_date',
                             'evidence_results'],
                'additionalProperties': False,
            },
        },
        'notes': {'type': 'string'},
    },
    'required': ['operators', 'notes'],
    'additionalProperties': False,
}

DISCOVERY_SYSTEM = f"""You list the licensed mobile network operators in one national market \
for a research panel on 5G vendor dependence. You receive a Perplexity answer and its \
numbered search results. Use that evidence only.

Include every operator the evidence names that runs its own radio network, whether or not it \
offers 5G, and code each:
- operator_name: the name the national regulator uses for the operator (e.g. "Telekom \
Deutschland"), not a brand or the group.
- legal_entity: the licensed company, e.g. "Telekom Deutschland GmbH"; "{NOT_DISCLOSED}" if not given.
- brands: its consumer brands, ";"-separated.
- parent_company: the group it belongs to; "{NOT_DISCLOSED}" if not given.
- holds_spectrum_licence: yes if the evidence shows it holds its own mobile spectrum licence; \
no only if the evidence shows it has none (e.g. it runs on another operator's network); \
unclear when the evidence does not say. Silence is unclear, never no.
- five_g_status: launched, soft_launched, announced (the evidence says 5G is not yet \
commercial), none (the evidence says it offers no 5G), or unclear when the evidence does not \
establish which. Silence is unclear, never announced or none.
- five_g_launch_date: YYYY-MM-DD, YYYY-MM or YYYY as stated; "{NOT_DISCLOSED}" if not given.
- evidence_results: the numbers of the search results that support the entry.
List MVNOs, resellers and wholesale-only networks only in notes, saying why each is excluded. \
Two names for one licensed operator (a rebrand, a merger) are one entry: say so in notes."""

# ============================================================================
# CLAUDE: OPERATOR EXTRACTION
# ============================================================================

NULLABLE_NUMBER = {'anyOf': [{'type': 'number'}, {'type': 'null'}]}
ELEMENTS = ['core', 'ran', 'transport', 'management_system']


def obj(**props):
    return {'type': 'object', 'properties': props, 'required': list(props), 'additionalProperties': False}


def enum(*values):
    return {'type': 'string', 'enum': list(values)}


def listof(item):
    return {'type': 'array', 'items': item}


VENDOR_ENTRY = obj(vendor={'type': 'string'}, share_pct=NULLABLE_NUMBER, share_basis={'type': 'string'})

# Each coded field: name -> (layer, value schema).
FIELDS = {
    # Physical
    'spectrum_low': ('physical', obj(mhz=NULLABLE_NUMBER, regulator_band_labels={'type': 'string'})),
    'spectrum_mid': ('physical', obj(mhz=NULLABLE_NUMBER, regulator_band_labels={'type': 'string'})),
    'spectrum_high': ('physical', obj(mhz=NULLABLE_NUMBER, regulator_band_labels={'type': 'string'})),
    'licenses': ('physical', listof(obj(band_label={'type': 'string'}, award_date={'type': 'string'},
                                        expiry_date={'type': 'string'},
                                        renewal_condition={'type': 'string'}))),
    'core_architecture': ('physical', enum('non_standalone_only', 'both_in_parallel', 'standalone_only')),
    'population_coverage': ('physical', obj(pct=NULLABLE_NUMBER,
                                            definition=enum('population', 'geographic', 'standalone', ''))),
    # Network
    'international_gateway_control': ('network', enum('operator_held', 'state_held', 'third_party')),
    'cable_landing_dependency': ('network', listof({'type': 'string'})),
    'ixp_count': ('network', NULLABLE_NUMBER),
    'upstream_transit_provider': ('network', listof({'type': 'string'})),
    # Vendor
    'ran_vendor': ('vendor', listof(VENDOR_ENTRY)),
    'core_vendor': ('vendor', listof(VENDOR_ENTRY)),
    'transport_vendor': ('vendor', listof(VENDOR_ENTRY)),
    'management_system_vendor': ('vendor', listof(VENDOR_ENTRY)),
    'core_vendor_4g_legacy': ('vendor', listof(VENDOR_ENTRY)),
    'open_ran_status': ('vendor', enum('actively_deploying', 'guiding_future_evolution',
                                       'somewhat_integrated', 'not_integrated')),
    'legacy_4g_carryover': ('vendor', obj(carryover={'type': ['boolean', 'null']}, vendor={'type': 'string'})),
    # Ownership
    'ownership_type': ('ownership', enum('private', 'listed', 'state_owned', 'state_backed_minority')),
    'state_equity': ('ownership', obj(pct=NULLABLE_NUMBER, holders=listof(obj(
        holder={'type': 'string'}, pct=NULLABLE_NUMBER, state={'type': 'string'},
        state_link=enum('source', 'reference_list'), reference_entry={'type': 'string'})))),
    'parent_company_origin': ('ownership', obj(parent_company={'type': 'string'}, country={'type': 'string'})),
    'legal_domicile': ('ownership', {'type': 'string'}),
    # Regulatory
    'vendor_restriction_exists': ('regulatory', enum('yes', 'no')),
    'restriction_instrument_type': ('regulatory', listof(enum('statute', 'contract', 'licence_condition',
                                                              'administrative_designation'))),
    'restriction_bindingness': ('regulatory', enum('binding', 'voluntary', 'proposed')),
    'restriction_scope': ('regulatory', listof(enum(*ELEMENTS))),
    'rip_and_replace_deadline': ('regulatory', listof(obj(element=enum(*ELEMENTS), deadline={'type': 'string'},
                                                          funding_mechanism={'type': 'string'}))),
    'data_localization': ('regulatory', {'type': 'string'}),
    'telecom_fdi_screening': ('regulatory', {'type': 'string'}),
    'spectrum_award_mechanism': ('regulatory', listof(enum('auction', 'comparative_selection',
                                                           'administrative_allocation', 'direct_award'))),
}
VENDOR_ELEMENTS = ['ran_vendor', 'core_vendor', 'transport_vendor', 'management_system_vendor']
SPECTRUM_BANDS = ['spectrum_low', 'spectrum_mid', 'spectrum_high']


def empty_value(schema):
    """The value a field holds when its status is not 'value', shaped like its schema."""
    if schema.get('type') == 'object':
        return {k: empty_value(v) for k, v in schema['properties'].items()}
    if schema.get('type') == 'array':
        return []
    if schema.get('type') == 'boolean':
        return None
    return '' if schema.get('type') == 'string' else None


def coded(value_schema):
    # A single-choice value must be able to sit empty when its status is not 'value'.
    if 'enum' in value_schema and '' not in value_schema['enum']:
        value_schema = {**value_schema, 'enum': value_schema['enum'] + ['']}
    return obj(status=enum(*STATUSES), value=value_schema, tier=enum(*TIERS), source={'type': 'string'},
               evidence_results=listof({'type': 'string'}))


EXTRACTION_SCHEMA = obj(
    **{name: coded(schema) for name, (_, schema) in FIELDS.items()},
    market_vendor_shares=listof(obj(element=enum(*ELEMENTS), vendor={'type': 'string'}, share_pct=NULLABLE_NUMBER,
                                    share_basis={'type': 'string'}, analyst_house={'type': 'string'},
                                    year={'type': 'string'})),
    notes={'type': 'string'},
)

CLAUDE_SYSTEM = f"""You code one 5G mobile operator for a research panel on vendor dependence: \
whose equipment sits in which element of the operator's network, who owns the operator, and \
what law binds the arrangement. You receive the operator's record and six Perplexity answers \
with their search results: vendor (results V1, V2, ...), physical and network (P1, ...), \
ownership (O1, ...), spectrum holdings (S1, ...), coverage (C1, ...), and the national \
regulatory regime (R1, ...). Inside each answer, [n] \
refers to that block's result n. Code from that evidence only - never from background \
knowledge, and never by guessing. The observation is the year in the record; later or earlier \
events count only as dated context. The record's discovery_flag and researcher_note name open \
questions (an unconfirmed licence or launch, a shared network, an uncertain status) for the \
evidence to settle: they are not evidence, and notes should say how the evidence resolved them \
or that it did not.

Every field is an object with:
- status: "{VALUE}" when the evidence supports a value. "{NOT_DISCLOSED}" when the value exists \
but no source in the evidence publishes it. "{NOT_APPLICABLE}" when the question does not arise \
(restriction fields where no restriction applies; legal_domicile when the operating entity is \
incorporated in the market; core_vendor_4g_legacy when the operator runs standalone only). \
"{NOT_YET_COLLECTED}" only for a field these searches were not designed to answer. Never use \
"{VALUE}" with an empty value.
- value: the coded value (empty string, empty list or null when status is not "{VALUE}").
- tier: 1 = operator-confirmed (the operator's annual report, investor presentation or \
release). 2 = filing-confirmed (a regulator record or submission, an SEC filing, a government \
instrument, inquiry testimony, EU toolbox implementation reporting). 3 = analyst-attributed (a \
named research house, news or trade press). "none" when status is not "{VALUE}". When unsure \
between two tiers, choose the higher number.
- source: the specific source the value rests on. For tier 3 always name the analyst house or \
outlet, with its date (e.g. "Strand Consult via Light Reading, Jan 2025"). "" when status is \
not "{VALUE}".
- evidence_results: the result labels the value rests on, e.g. ["V3", "R1"].

Vendor layer (the reason this dataset exists):
- ran_vendor, core_vendor, transport_vendor, management_system_vendor: one list per network \
element, naming every supplier the evidence gives for this operator - multi-vendor supply is \
normal, and an operator can be Ericsson-core and Huawei-RAN at once. share_pct only when a \
source reports a share for this operator, with share_basis saying what it is a share of (e.g. \
"operator's 5G RAN sites"); otherwise null and "". Never derive a share from the number of \
vendors. A share of the whole national market is not this operator's share: record it in \
market_vendor_shares, with the analyst house and year, and not in the element list.
- core_vendor is the 5G core supplier. core_vendor_4g_legacy is the 4G core (EPC) supplier \
where 5G runs non-standalone, because there the 4G core is the core vendor of record.
- management_system_vendor is the supplier of the RAN configuration, orchestration and \
update-management system, coded separately from the equipment it manages.
- Software the operator or its group builds itself is a supplier entry named exactly \
"in-house (<group name>)".
- open_ran_status: actively_deploying (O-RAN interfaces in production), \
guiding_future_evolution (O-RAN principles guide RAN evolution), somewhat_integrated, \
not_integrated.
- legacy_4g_carryover: whether the 5G RAN was built on a 4G footprint from the same vendor, \
with that vendor named.
- Chinese operators disclose almost nothing about vendors: code what the evidence names (e.g. \
tender awards) at tier 3 with the source named.

Physical and network layers:
- spectrum_low / spectrum_mid / spectrum_high: total MHz the operator holds below 1 GHz, from 1 \
to 6 GHz, and above 24 GHz. regulator_band_labels lists the regulator's own band names with \
MHz each, e.g. "700 MHz: 2x10; 3.6 GHz: 90". Give mhz only when the evidence gives the \
operator's complete holding in that class - every band it holds there; then mhz is their sum. \
When only some of the operator's bands in a class are known, mhz is null and \
regulator_band_labels lists the known bands followed by "(partial)": a sum of the known bands \
is never a total. Bands between 6 and 24 GHz belong to no class: mention them in notes.
- licenses: one entry per 5G licence, with dates as YYYY-MM-DD (or YYYY-MM / YYYY when only \
that is stated) and the renewal condition as stated.
- core_architecture: non_standalone_only, both_in_parallel, or standalone_only.
- population_coverage: pct with its definition - population, geographic, or standalone. If \
the source doesn't say which kind of coverage a figure measures, status is \
"{NOT_DISCLOSED}": a coverage figure never enters without its definition.
- international_gateway_control: operator_held, state_held, or third_party.
- cable_landing_dependency: submarine cable names exactly as the sources write them.
- ixp_count: the number of internet exchange points the operator is reported at. \
upstream_transit_provider: named providers.

Ownership layer:
- ownership_type: private, listed, state_owned, or state_backed_minority. Where state_equity \
is coded, it decides, whether or not the company is also listed: {STATE_OWNED_PCT}% or more is \
state_owned; above {STATE_BACKED_PCT}% is state_backed_minority. Otherwise - including when no \
state equity is reported - code listed (the operator's or its ultimate parent's shares are \
publicly traded) or private from the evidence.
- state_equity: pct is the percent held directly or indirectly by any state - domestic or \
foreign - through government, state-owned companies or sovereign funds: the sum of holders. \
Stakes in the ultimate parent count, multiplied through the ownership chain (15% of a parent \
that owns 100% of the operator is 15%). holders: one entry per state holder, as the source \
names it, with its pct of the operator after that multiplication and the state behind it. \
state_link says how you know the holder is state-controlled: "source" only when a cited result \
itself says so; "reference_list" when the evidence names the holder but not its state link and \
the holder is on the reference list below - then reference_entry is that list's entry copied \
exactly (otherwise ""). A holder on neither is not a state holder. The stake itself always \
needs a source. A source saying the major shareholders include no state holder is pct 0 with \
no holders.
  Reference list of state-controlled holders (entry | also named | state):
{STATE_HOLDER_REFERENCE}
- parent_company_origin: the ultimate parent and the country of its legal incorporation (not \
its headquarters). country is the country's common English short name only (e.g. "United \
Kingdom", not "England and Wales"; "Netherlands", not "Kingdom of the Netherlands").
- legal_domicile: the operating entity's jurisdiction of incorporation, only where it differs \
from the market; "{NOT_APPLICABLE}" where it is incorporated in the market.

Regulatory layer, coded as the regime applies to this operator:
- vendor_restriction_exists: yes if a restriction on designated high-risk suppliers applies to \
this operator. no when a source says none applies, or when the evidence describes the national \
regime and its instruments do not reach this operator (e.g. contracts signed with named \
operators, and this operator is not one of them): tier and source are those of the evidence \
showing who the instruments bind. Only when the evidence says nothing about the national regime \
is it "{NOT_DISCLOSED}", because that may mean nobody asked.
- When vendor_restriction_exists is no, every other restriction field (instrument type, \
bindingness, scope, rip_and_replace_deadline) is "{NOT_APPLICABLE}"; describe instruments that \
bind other operators in notes.
- restriction_instrument_type: statute, contract, licence_condition, administrative_designation.
- restriction_bindingness: binding, voluntary, or proposed. A proposed instrument alongside a \
binding one: code binding, and describe the proposal in notes.
- restriction_scope: the set of network elements the restriction covers (core, ran, \
transport, management_system).
- rip_and_replace_deadline: one entry per covered element, with its deadline as YYYY-MM-DD \
("end of 2026" is 2026-12-31; a deadline stated only to the month is its last day) and the \
funding mechanism ("none stated" when no public money is attached).
- data_localization, telecom_fdi_screening: a brief description naming the instrument and \
authority.
- spectrum_award_mechanism: how this operator's 5G spectrum was assigned.

notes: one to three sentences on conflicts between sources, market-level figures, and anything \
the fields could not hold.

Reply with only a JSON object (no prose, no code fence) that validates against this JSON Schema:
""" + json.dumps(EXTRACTION_SCHEMA, separators=(',', ':'))

# The extraction schema is too large for constrained decoding ("compiled grammar is too large"
# at as few as 8 coded fields), so it travels in the system prompt and every reply is validated
# here instead. A reply that fails is logged as an error and retried on the next run.
EXTRACTION_VALIDATOR = jsonschema.Draft202012Validator(EXTRACTION_SCHEMA)

# ============================================================================
# DERIVED FIELDS
# ============================================================================

# Legal domicile of each vendor's ultimate parent (GLEIF-style, not headquarters), matched on
# the start of the vendor name. Reviewed 2026-11-02. A vendor not listed derives to
# not_yet_collected and is named in notes for review, never guessed from the brand.
VENDOR_ORIGIN = [
    ('huawei', 'China'), ('zte', 'China'), ('ericsson', 'Sweden'), ('nokia', 'Finland'),
    ('infinera', 'Finland'), ('samsung', 'South Korea'), ('nec', 'Japan'), ('fujitsu', 'Japan'),
    ('rakuten', 'Japan'), ('altiostar', 'Japan'), ('cisco', 'United States'), ('mavenir', 'United States'),
    ('ciena', 'United States'), ('oracle', 'United States'), ('microsoft', 'United States'),
    ('affirmed', 'United States'), ('juniper', 'United States'), ('hewlett packard', 'United States'),
    ('hpe', 'United States'), ('parallel wireless', 'United States'), ('dell', 'United States'),
    ('red hat', 'United States'), ('nvidia', 'United States'), ('vmware', 'United States'),
    ('amdocs', 'Guernsey'), ('netcracker', 'Japan'), ('capgemini', 'France'), ('atos', 'France'),
    ('accenture', 'Ireland'), ('ibm', 'United States'), ('commscope', 'United States'),
    ('adtran', 'United States'), ('adva optical', 'United States'),
    ('ribbon', 'United States'), ('casa systems', 'United States'), ('airspan', 'United States'),
    ('amazon', 'United States'), ('aws', 'United States'), ('google', 'United States'),
    ('qualcomm', 'United States'), ('fiberhome', 'China'), ('datang', 'China'), ('ceragon', 'Israel'),
    ('tata consultancy', 'India'), ('tcs', 'India'), ('tech mahindra', 'India'), ('infosys', 'India'),
    ('wipro', 'India'),
]
# ADVA Optical belongs to Adtran, NetCracker to NEC.


def vendor_origin(vendor, parent_origin=None):
    """Origin of a vendor's ultimate parent; in-house software takes the operator's parent origin."""
    v = vendor.lower().strip()
    if v.startswith('in-house'):
        return parent_origin
    return next((country for prefix, country in VENDOR_ORIGIN if v.startswith(prefix)), None)


def hhi(entries):
    """Herfindahl index (0-10,000) within one element, or None unless every listed vendor has a
    sourced share and the shares cover the element (95-105%)."""
    shares = [e['share_pct'] for e in entries]
    if not shares or any(s is None for s in shares) or not 95 <= sum(shares) <= 105:
        return None
    return round(sum(s * s for s in shares))


def normalize_cable(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', re.sub(r'\(.*?\)', ' ', name)).strip()


def cable_keys(name):
    """Lookup keys for a cable name: the normalized name, the same without spaces or a trailing
    'cable'/'submarine system' ('SEA-ME-WE 5' = 'SeaMeWe-5', 'PEACE' = 'PEACE Cable'), with the
    SMW-n shorthand spelled out, and any abbreviation in brackets ('Southeast Asia-Japan Cable 2
    (SJC2)' is also found as 'SJC2')."""
    full = normalize_cable(name)
    compact = re.sub(r'( submarine)?( cable)?( system)?$', '', full).replace(' ', '')
    keys = [full, re.sub(r'^smw(?=\d)', 'seamewe', compact)]
    keys += [normalize_cable(a).replace(' ', '') for a in re.findall(r'\((.*?)\)', name)]
    return [k for k in dict.fromkeys(keys) if k]


def match_cable(name, cables):
    return next((cables[k] for k in cable_keys(name) if k in cables), None)


def load_cable_names():
    """lookup key (see cable_keys) -> cable_name in submarinecables. cable_name is the stable
    join key: the table's id changes whenever push_submarinecables.py replaces its rows."""
    names = {}
    for r in fetch_all(get_anon_client(), 'submarinecables', 'id,cable_name'):
        for k in cable_keys(r['cable_name']):
            names.setdefault(k, r['cable_name'])
    return names

# ============================================================================
# SEARCHES AND CACHE
# ============================================================================


def slug(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', text).strip('-')


def search_key(kind, subject):
    return f"{kind}|{subject}"


class SearchCache:
    """Perplexity results keyed by '<kind>|<market or operator_id>', appended as they arrive."""

    def __init__(self, path=SEARCH_CACHE):
        self.path, self.lock, self.entries = path, threading.Lock(), {}
        if os.path.exists(path):
            for line in open(path):
                e = json.loads(line)
                self.entries[e['key']] = e

    def costs(self):
        return [e['search']['cost'] for e in self.entries.values()]

    def get(self, key):
        return self.entries.get(key)

    def fresh(self, key, prompt):
        """Cached under this key and asked with this exact question (a reworded question re-searches)."""
        return key in self.entries and self.entries[key]['prompt'] == prompt

    def put(self, key, search, prompt):
        entry = {'key': key, 'searched_at': date.today().isoformat(), 'prompt': prompt, 'search': search}
        with self.lock:
            with open(self.path, 'a') as f:
                f.write(json.dumps(entry) + '\n')
            self.entries[key] = entry
        return entry


class Spend:
    """Per-run spend against the caps, from each response's own cost."""

    def __init__(self, perplexity_cap, claude_cap):
        self.cap = {'perplexity': perplexity_cap, 'claude': claude_cap}
        self.spent = {'perplexity': 0.0, 'claude': 0.0}

    def allows(self, api, estimate):
        return self.spent[api] + estimate <= self.cap[api]

    def add(self, api, cost):
        self.spent[api] += cost

    def summary(self):
        return (f"Perplexity ${self.spent['perplexity']:.2f} of ${self.cap['perplexity']:.2f}, "
                f"Claude ${self.spent['claude']:.2f} of ${self.cap['claude']:.2f}")


def run_searches(jobs, cache, api_key, spend, workers):
    """jobs: (key, prompt). Searches every uncached job, in groups of `workers`, stopping before a
    group that could exceed the Perplexity cap. Returns the keys still missing."""
    todo = [(k, p) for k, p in jobs if not cache.fresh(k, p)]
    rate = average(cache.costs(), SEARCH_ESTIMATE)
    for start in range(0, len(todo), workers):
        group = todo[start:start + workers]
        if not spend.allows('perplexity', len(group) * rate):
            print(f"  Perplexity cap reached: {len(todo) - start} searches not run.")
            break
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {pool.submit(perplexity_search, PERPLEXITY_SYSTEM, p, api_key): (k, p) for k, p in group}
            for future in as_completed(futures):
                k, p = futures[future]
                try:
                    search = future.result()
                except Exception as e:
                    print(f"  ✗ search {k}: {type(e).__name__}: {e}")
                    continue
                cache.put(k, search, p)
                spend.add('perplexity', search['cost'])
                print(f"  searched {k:55} ${search['cost']:.4f}")
        rate = average(cache.costs(), SEARCH_ESTIMATE)
    return [k for k, p in jobs if not cache.fresh(k, p)]

# ============================================================================
# CLAUDE CALLS
# ============================================================================


def parse_response(message, validator=None):
    """The reply's JSON. With a validator (unconstrained extraction), strip any code fence and
    raise unless the reply matches the schema."""
    if message.stop_reason == 'refusal':
        raise RuntimeError(f"Claude refused extraction: {message.stop_details}")
    if message.stop_reason == 'max_tokens':
        raise RuntimeError('Claude hit max_tokens before finishing the extraction')
    text = next(b.text for b in message.content if b.type == 'text').strip()
    if validator is None:
        return json.loads(text)
    fields = json.loads(re.sub(r'^```(?:json)?\s*|\s*```$', '', text))
    errors = sorted(validator.iter_errors(fields), key=lambda e: list(e.path))
    if errors:
        raise ValueError(f"{len(errors)} schema error(s), first at {'/'.join(map(str, errors[0].path)) or 'root'}: "
                         f"{errors[0].message[:200]}")
    return fields


def request_params(system, schema, content, effort, cache_ttl):
    """Messages API params shared by the synchronous and Batches paths. The system prompt (plus
    the output schema, which renders ahead of it) is identical for every row, so it is cached.
    schema=None leaves the output unconstrained (the schema is then in the system prompt)."""
    cache_control = {'type': 'ephemeral', **({'ttl': cache_ttl} if cache_ttl != '5m' else {})}
    return {
        'model': MODEL,
        'max_tokens': 16000,
        'system': [{'type': 'text', 'text': system, 'cache_control': cache_control}],
        'output_config': {'effort': effort, **({'format': {'type': 'json_schema', 'schema': schema}} if schema else {})},
        'messages': [{'role': 'user', 'content': content}],
    }


def call_claude(client, params, validator=None):
    """(fields, response, cost). A reply that fails to parse raises CostlyError carrying its cost."""
    response = client.beta.messages.create(**params, betas=['server-side-fallback-2026-07-01'], fallbacks='default')
    # Price at the requested model: a fallback model may not be in the price table.
    cost = usage_cost(MODEL, response.usage.to_dict())
    try:
        return parse_response(response, validator), response, cost
    except Exception as e:
        raise CostlyError(f"{type(e).__name__}: {e}", cost) from e


class CostlyError(RuntimeError):
    """A billed response that could not be used."""
    def __init__(self, message, cost):
        super().__init__(message)
        self.cost = cost


def results_block(prefix, search):
    return '\n'.join(f"{prefix}{i}. {r.get('title', '')} | {r['url']}"
                     + (f" ({r['date']})" if r.get('date') else '')
                     for i, r in enumerate(search['results'], 1)) or 'none'


def discovery_content(market, year, search):
    return (f"<market>{market}</market>\n<observation_year>{year}</observation_year>\n\n"
            f"<perplexity_answer>\n{search['answer']}\n</perplexity_answer>\n\n"
            f"<search_results>\n{results_block('', search)}\n</search_results>")


def operator_content(op, year, searches):
    record = {k: op[k] for k in ('operator_id', 'operator_name', 'legal_entity', 'brands', 'parent_company',
                                 'market', 'five_g_status', 'five_g_launch_date', 'discovery_flag',
                                 'researcher_note')}
    record['observation_year'] = year
    blocks = [f"<operator_record>\n{json.dumps(record, indent=1)}\n</operator_record>"]
    for layer, prefix in BLOCKS:
        s = searches[layer]
        blocks.append(f"<{layer}_search>\n<answer>\n{s['answer']}\n</answer>\n"
                      f"<results>\n{results_block(prefix, s)}\n</results>\n</{layer}_search>")
    return '\n\n'.join(blocks)

# ============================================================================
# DISCOVERY -> OPERATOR LIST
# ============================================================================

OPERATOR_COLUMNS = ['operator_id', 'market', 'market_iso', 'operator_name', 'legal_entity', 'brands',
                    'parent_company', 'holds_spectrum_licence', 'five_g_status', 'five_g_launch_date',
                    'included', 'exclusion_reason', 'discovery_flag', 'source_urls', 'discovered_at']

# Decisions the researcher made about specific operators, kept apart from the discovery
# output (which stays evidence-only) and overlaid when the list is loaded. Each is dated and
# shown in researcher_note; an override of `included` is never written into the CSV.
RESEARCHER_DECISIONS = {
    # operator_id: (included override or None, note)
    'DK-tt-network': (None, "researcher 2026-11-03: Telia and Telenor's shared network company. One row "
                            "for vendor and network coding, since those decisions are made jointly; "
                            "ownership records both owners (Telia Company and Telenor)"),
    'ES-digi-spain': (True, "researcher 2026-11-03: included although discovery coded no 5G. Digi holds "
                            "spectrum but its status as a full network operator is unclear; to be "
                            "resolved by the research searches, not at discovery"),
    'GR-nova': (None, "researcher 2026-11-13: Nova incorporates WIND Hellas's mobile operations - WIND Hellas merged "
                      "with Nova Greece in Jan 2023 and its mobile services were rebranded Nova (confirmed by the "
                      "researcher from Wikipedia and an industry telecom portal), so WIND Hellas evidence is coded as "
                      "Nova's"),
    'US-dish-wireless': (None, "researcher 2026-11-03: whether DISH/EchoStar still runs its own network in "
                               "2026 is uncertain (most spectrum sold, Boost moving to AT&T's network); "
                               "to be resolved by the research searches. researcher 2026-11-13: kept in the "
                               "2026 panel as a restructured operator - its 600 MHz and 3.45 GHz spectrum "
                               "was sold to AT&T and AWS-4 to SpaceX, DISH Wireless entered bankruptcy and "
                               "its own network was being dismantled; vendor fields describe the network "
                               "as built"),
    'US-uscellular': (None, "researcher 2026-11-13: kept in the 2026 panel as a restructured operator - "
                            "T-Mobile absorbed UScellular's wireless operations on 1 Aug 2025 and its "
                            "spectrum was sold to AT&T and Verizon; vendor and spectrum fields describe "
                            "UScellular's own network before the transfer"),
    'IT-telecom-italia': (None, "researcher 2026-11-13: 'BlueMed' in the coded cable 'BlueMed/BlueRaman' is "
                                "read as the Blue cable (the Mediterranean leg, per Sparkle's own branding), "
                                "kept separate from Raman (the eastern leg) as submarinecables records them"),
}

# Cable names the researcher has matched by hand for one operator, alongside its RESEARCHER_DECISIONS
# note: operator_id -> {coded cable name: submarinecables cable_name}. Never applied to other rows.
RESEARCHER_CABLE_MATCHES = {
    'IT-telecom-italia': {'BlueMed/BlueRaman': 'Blue'},  # researcher 2026-11-13
}


def load_operators(raw=False):
    """The discovered operators, with RESEARCHER_DECISIONS overlaid (included, researcher_note)
    unless raw - discovery reads and rewrites the raw list, so overrides never reach the CSV."""
    if not os.path.exists(OPERATORS_PATH):
        return pd.DataFrame(columns=OPERATOR_COLUMNS + ([] if raw else ['researcher_note']))
    ops = pd.read_csv(OPERATORS_PATH, dtype=str, keep_default_na=False)
    if 'discovery_flag' not in ops:  # lists built before the flag existed
        ops.insert(ops.columns.get_loc('exclusion_reason') + 1, 'discovery_flag', 'none')
    ops['exclusion_reason'] = ops['exclusion_reason'].replace('', 'none')
    if raw:
        return ops
    ops['researcher_note'] = 'none'
    for oid, (include, note) in RESEARCHER_DECISIONS.items():
        hit = ops['operator_id'] == oid
        if not hit.any():
            sys.exit(f"RESEARCHER_DECISIONS names {oid}, which is not in {OPERATORS_PATH}")
        ops.loc[hit, 'researcher_note'] = note
        if include is not None:
            ops.loc[hit, 'included'] = 'yes' if include else 'no'
    return ops


def discover(markets, year, cache, client, api_key, spend, args):
    """Search and code each market without operators yet; append them to OPERATORS_PATH.
    operator_ids are assigned once and never re-derived, so later years keep the same ids."""
    known = load_operators(raw=True)
    if args.rediscover:
        redo = [m.strip() for m in args.rediscover.split(',')]
        known = known[~known['market'].isin(redo)]
    todo = [m for m in markets if m not in set(known['market'])]
    if not todo:
        return
    print(f"\nDiscovery: {len(todo)} market(s) without an operator list: {', '.join(todo)}")
    jobs = [(search_key('discovery', MARKETS[m]), DISCOVERY_QUESTION.format(market=m, year=year)) for m in todo]
    run_searches(jobs, cache, api_key, spend, args.workers)
    discovery_costs = [json.loads(l)['cost'] for l in open(DISCOVERY_LOG)] if os.path.exists(DISCOVERY_LOG) else []
    taken = set(known['operator_id'])
    rows = []
    for market in todo:
        entry = cache.get(search_key('discovery', MARKETS[market]))
        if not entry:
            continue
        if not spend.allows('claude', average(discovery_costs, DISCOVERY_ESTIMATE) * 1.5):
            print('  Claude cap reached: discovery stopped.')
            break
        search = entry['search']
        params = request_params(DISCOVERY_SYSTEM, DISCOVERY_SCHEMA, discovery_content(market, year, search),
                                args.effort, '5m')
        try:
            fields, response, cost = call_claude(client, params)
        except Exception as e:
            print(f"  ✗ discovery {market}: {type(e).__name__}: {e}")
            continue
        spend.add('claude', cost)
        discovery_costs.append(cost)
        with open(DISCOVERY_LOG, 'a') as f:
            f.write(json.dumps({'market': market, 'fields': fields, 'usage': response.usage.to_dict(),
                                'model': response.model, 'cost': cost}, default=str) + '\n')
        urls = [r['url'] for r in search['results']]
        for op in fields['operators']:
            base = f"{MARKETS[market]}-{slug(op['operator_name'])}"
            oid, n = base, 2
            while oid in taken:
                oid, n = f"{base}-{n}", n + 1
            taken.add(oid)
            # Exclude only on evidence: a licence the evidence says is missing, or 5G the evidence
            # says is not yet commercial. Silence on either includes the operator with a flag.
            licence, status = op['holds_spectrum_licence'], op['five_g_status']
            included = licence != 'no' and status in ('launched', 'soft_launched', 'unclear')
            reason = '' if included else (
                'evidence shows no own spectrum licence' if licence == 'no' else f"evidence shows 5G status: {status}")
            flags = (['own spectrum licence not evidenced in the discovery search'] if licence == 'unclear' else []) + \
                    (['5G launch not evidenced in the discovery search'] if status == 'unclear' else [])
            cited = [urls[i - 1] for i in op['evidence_results'] if 1 <= i <= len(urls)]
            rows.append({'operator_id': oid, 'market': market, 'market_iso': MARKETS[market],
                         'operator_name': op['operator_name'], 'legal_entity': op['legal_entity'],
                         'brands': op['brands'], 'parent_company': op['parent_company'],
                         'holds_spectrum_licence': op['holds_spectrum_licence'],
                         'five_g_status': op['five_g_status'], 'five_g_launch_date': op['five_g_launch_date'],
                         'included': 'yes' if included else 'no', 'exclusion_reason': reason or 'none',
                         'discovery_flag': '; '.join(flags) or 'none',
                         'source_urls': '; '.join(dict.fromkeys(cited)) or NOT_DISCLOSED,
                         'discovered_at': entry['searched_at']})
        names = ', '.join(o['operator_name'] for o in fields['operators'])
        print(f"  {market}: {len(fields['operators'])} operators ({names}) | ${cost:.3f}")
        if fields['notes']:
            print(f"    notes: {fields['notes']}")
    if rows:
        out = pd.concat([known, pd.DataFrame(rows, columns=OPERATOR_COLUMNS)])
        order = {m: i for i, m in enumerate(MARKETS)}
        out.sort_values('market', key=lambda c: c.map(order), kind='stable').to_csv(OPERATORS_PATH, index=False)

# ============================================================================
# PANEL ROWS
# ============================================================================


def flat_columns():
    cols = ['row_id', 'operator_id', 'operator_name', 'market', 'panel_tier', 'observation_year', 'reference_date']
    for name, (layer, _) in FIELDS.items():
        if name in SPECTRUM_BANDS:
            cols += [f'{name}_mhz', f'{name}_label']
        elif name == 'licenses':
            cols += ['license_award_date', 'license_expiry_date', 'license_renewal_condition']
        elif name == 'population_coverage':
            cols += ['population_coverage_pct', 'coverage_definition']
        elif name == 'state_equity':
            cols += ['state_equity_pct', 'state_holders', 'state_equity_from_reference_list']
        elif name == 'parent_company_origin':
            cols += ['parent_company', 'parent_company_origin']
        elif name == 'legacy_4g_carryover':
            cols += ['legacy_4g_carryover', 'legacy_4g_vendor']
        elif name == 'cable_landing_dependency':
            cols += ['cable_landing_dependency', 'cable_landing_unmatched']
        else:
            cols.append(name)
        if name in VENDOR_ELEMENTS:
            cols += [f'{name}_origin', f'{name}_hhi']
        elif name == 'core_vendor_4g_legacy':
            cols.append(f'{name}_origin')
        cols += [f'{name}_tier', f'{name}_source']
        if name == 'ownership_type':
            cols.append('ownership_type_provisional')
    return cols + ['market_vendor_shares', 'notes', 'source_urls']


PANEL_COLUMNS = flat_columns()


def fmt_num(x):
    if x is None:
        return ''
    x = round(float(x), 4)  # sums of shares carry float noise (20.005399999999998)
    return str(int(x)) if x.is_integer() else str(x)


def fmt_vendors(entries):
    return '; '.join(e['vendor'].strip() + (f" ({fmt_num(e['share_pct'])}% of {e['share_basis']})"
                                            if e['share_pct'] is not None else '') for e in entries)


def build_row(op, year, fields, searches, cables):
    """Flatten Claude's coded fields into one panel row, adding derived fields and the cable join.
    A missing value is written as its status code in every column it occupies, never blank."""
    out = {'row_id': f"{op['operator_id']}-{year}", 'operator_id': op['operator_id'],
           'operator_name': op['operator_name'], 'market': op['market'], 'panel_tier': PANEL_TIER,
           'observation_year': str(year),
           'reference_date': max(s['searched_at'] for s in searches.values())}
    notes = [fields['notes']] if fields['notes'].strip() else []
    notes += [f"discovery_flag: {op['discovery_flag']}"] if op['discovery_flag'] != 'none' else []
    notes += [op['researcher_note']] if op['researcher_note'] != 'none' else []
    labels = {}
    for layer, prefix in BLOCKS:
        for i, r in enumerate(searches[layer]['search']['results'], 1):
            labels[f'{prefix}{i}'] = r['url']
    cited = []
    po = fields['parent_company_origin']
    parent_origin = canonical_country(po['value']['country']) if po['status'] == VALUE and po['value']['country'] else None

    for name in FIELDS:
        f = fields[name]
        status, v = f['status'], f['value']
        if status == VALUE and v in ('', [], None):
            status = NOT_DISCLOSED
            notes.append(f"{name}: coded as a value but empty; recorded as {NOT_DISCLOSED}")
        if name == 'population_coverage' and status == VALUE and (v['pct'] is None or not v['definition']):
            status = NOT_DISCLOSED
            notes.append(f"population_coverage: no figure with a stated definition; recorded as {NOT_DISCLOSED}")
        has = status == VALUE
        miss = status  # what a missing cell holds
        if not has:
            v = empty_value(FIELDS[name][1])
        cited += [labels[x] for x in f['evidence_results'] if x in labels] if has else []

        def cell(x, fmt=lambda y: y):
            """A field's sub-value: the status code when the field has no value, not_disclosed
            when this part of an otherwise-coded value is empty."""
            if not has:
                return miss
            return NOT_DISCLOSED if x in ('', None, []) else fmt(x)

        if name in SPECTRUM_BANDS:
            out[f'{name}_mhz'] = cell(v['mhz'], fmt_num)
            out[f'{name}_label'] = cell(v['regulator_band_labels'])
        elif name == 'licenses':
            for key, col in (('award_date', 'license_award_date'), ('expiry_date', 'license_expiry_date'),
                             ('renewal_condition', 'license_renewal_condition')):
                out[col] = '; '.join(f"{l['band_label']}: {l[key] or NOT_DISCLOSED}" for l in v) if has else miss
        elif name == 'population_coverage':
            out['population_coverage_pct'] = cell(v['pct'], fmt_num)
            out['coverage_definition'] = cell(v['definition'])
        elif name == 'state_equity':
            out['state_equity_pct'] = cell(v['pct'], fmt_num)
            holders = v['holders'] if has else []
            out['state_holders'] = '; '.join(
                f"{h['holder']} {fmt_num(h['pct']) + '%' if h['pct'] is not None else '(share not stated)'} "
                f"({h['state']}; state link: {'reference list' if h['state_link'] == 'reference_list' else 'source'})"
                for h in holders) or (NOT_APPLICABLE if has and v['pct'] == 0 else cell(''))
            # Mechanical split of evidence-based from reference-list state findings (cf.
            # owner_parent_inferred in the data-center enrichment): a yes/no column, plus a
            # fixed-wording note per list-based holder.
            listed = [h for h in holders if h['state_link'] == 'reference_list']
            out['state_equity_from_reference_list'] = ('yes' if listed else 'no') if has else miss
            for h in listed:
                notes.append(f"state_holder_list: {h['holder']} classified as state-controlled per reviewed "
                             f"reference list, not from this row's own source material")
                if h['reference_entry'] not in STATE_HOLDER_ENTRIES:
                    notes.append(f"state_holder_list: {h['holder']} cites reference entry "
                                 f"'{h['reference_entry']}', which is not on the list; check by hand")
        elif name == 'parent_company_origin':
            out['parent_company'] = cell(v['parent_company'])
            out['parent_company_origin'] = cell(v['country'], canonical_country)
        elif name == 'legacy_4g_carryover':
            out['legacy_4g_carryover'] = cell(v['carryover'], lambda b: str(b).lower())
            out['legacy_4g_vendor'] = cell(v['vendor'])
        elif name == 'cable_landing_dependency':
            by_hand = RESEARCHER_CABLE_MATCHES.get(op['operator_id'], {})
            match = lambda c: by_hand.get(c) or match_cable(c, cables)
            matched = [match(c) for c in v if match(c)] if has else []
            unmatched = [c for c in v if not match(c)] if has else []
            out['cable_landing_dependency'] = '; '.join(dict.fromkeys(matched)) or (NOT_DISCLOSED if has else miss)
            out['cable_landing_unmatched'] = '; '.join(unmatched) or (NOT_APPLICABLE if has else miss)
        elif name in VENDOR_ELEMENTS or name == 'core_vendor_4g_legacy':
            out[name] = fmt_vendors(v) if has else miss
            if has:
                origins = [vendor_origin(e['vendor'], parent_origin) for e in v]
                unknown = [e['vendor'] for e, o in zip(v, origins) if o is None]
                if unknown:
                    notes.append(f"{name}: no vendor-origin record yet for {', '.join(unknown)}")
                # One origin per vendor, in the same order, so the two columns line up.
                out[f'{name}_origin'] = '; '.join(o or NOT_YET_COLLECTED for o in origins)
            else:
                out[f'{name}_origin'] = miss
            if name in VENDOR_ELEMENTS:
                h = hhi(v) if has else None
                out[f'{name}_hhi'] = str(h) if h is not None else (NOT_DISCLOSED if has else miss)
        elif name == 'rip_and_replace_deadline':
            out[name] = '; '.join(f"{d['element']}: {d['deadline']} (funding: {d['funding_mechanism'] or 'none stated'})"
                                  for d in v) if has else miss
        elif isinstance(v, list):
            out[name] = '; '.join(v) if has else miss
        elif name == 'ixp_count':
            out[name] = cell(v, fmt_num)
        else:
            out[name] = cell(v)
        out[f'{name}_tier'] = cell(f['tier'] if f['tier'] != 'none' else '')
        out[f'{name}_source'] = cell(f['source'])

    # State equity decides ownership_type, listed or not (STATE_BACKED_PCT / STATE_OWNED_PCT).
    se = fields['state_equity']
    if se['status'] == VALUE and se['value']['pct'] is not None and se['value']['pct'] > STATE_BACKED_PCT:
        expected = 'state_owned' if se['value']['pct'] >= STATE_OWNED_PCT else 'state_backed_minority'
        if out['ownership_type'] != expected:
            notes.append(f"ownership_type: {out['ownership_type']} recoded {expected} from state equity "
                         f"{fmt_num(se['value']['pct'])}%")
            out['ownership_type'] = expected
            out['ownership_type_tier'], out['ownership_type_source'] = se['tier'], se['source']
    provisional = out['ownership_type'] in STATE_TYPES
    out['ownership_type_provisional'] = 'yes' if provisional else 'no'
    notes += [PROVISIONAL_NOTE] if provisional else []

    out['market_vendor_shares'] = '; '.join(
        f"{s['element']}: {s['vendor']} {fmt_num(s['share_pct'])}% of {s['share_basis']} ({s['analyst_house']}, {s['year']})"
        for s in fields['market_vendor_shares']) or NOT_DISCLOSED
    out['notes'] = ' | '.join(notes) or 'none'
    out['source_urls'] = '; '.join(dict.fromkeys(cited)) or NOT_DISCLOSED
    assert all(out[c] != '' for c in PANEL_COLUMNS), [c for c in PANEL_COLUMNS if out[c] == '']
    return {c: out[c] for c in PANEL_COLUMNS}

# ============================================================================
# ESTIMATE
# ============================================================================


def estimate(n_markets, n_operators, cache, output):
    """Cost of a full current-year run, from measured averages where they exist."""
    search_rate = average(cache.costs(), SEARCH_ESTIMATE)
    disc = [json.loads(l)['cost'] for l in open(DISCOVERY_LOG)] if os.path.exists(DISCOVERY_LOG) else []
    ops = []
    for path in (output, DRY_RUN_OUTPUT):
        if os.path.exists(path + '.raw.jsonl'):
            ops += [json.loads(l)['claude'] for l in open(path + '.raw.jsonl')]
    sync = [c['cost'] for c in ops if not c.get('batch')]
    batched = [(c['cost'], c['usage']) for c in ops if c.get('batch')]
    disc_rate, op_rate = average(disc, DISCOVERY_ESTIMATE), average(sync, OPERATOR_ESTIMATE)
    batch_rate, _ = worst_case_batch_rate(MODEL, batched, op_rate, PREFIX_TOKENS)
    searches = n_markets * 2 + n_operators * len(LAYERS)
    basis = lambda xs: f"measured over {len(xs)}" if xs else 'prior, not yet measured'
    lines = [
        ('Perplexity searches', f"{searches} ({n_markets} discovery + {n_markets} regulatory + {n_operators} x {len(LAYERS)})",
         searches * search_rate, f"${search_rate:.4f}/search, {basis(cache.costs())}"),
        ('Claude discovery', f"{n_markets} calls", n_markets * disc_rate, f"${disc_rate:.4f}/market, {basis(disc)}"),
        ('Claude extraction (batch)', f"{n_operators} operators", n_operators * op_rate * 0.5,
         f"${op_rate * 0.5:.4f}/operator expected; sized at worst case ${batch_rate:.4f}"),
        ('Claude extraction (sync)', f"{n_operators} operators", n_operators * op_rate,
         f"${op_rate:.4f}/operator, {basis(sync)}"),
    ]
    for label, what, cost, how in lines:
        print(f"  {label:28} {what:48} ${cost:6.2f}   ({how})")
    batch_total = lines[0][2] + lines[1][2] + lines[2][2]
    print(f"  {'Total with batch extraction':28} {'':48} ${batch_total:6.2f}")
    print(f"  {'Total, all synchronous':28} {'':48} ${lines[0][2] + lines[1][2] + lines[3][2]:6.2f}")

# ============================================================================
# RUN
# ============================================================================


def main():
    parser = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    parser.add_argument('--markets', help='comma-separated market names (default: Germany for a dry run)')
    parser.add_argument('--full', action='store_true', help=f'every market -> {FULL_OUTPUT}')
    parser.add_argument('--year', type=int, default=date.today().year, help='observation year (phase 1: current)')
    parser.add_argument('--estimate', action='store_true', help='print a cost estimate and exit (no API calls)')
    parser.add_argument('--operators', type=int, default=100, help='--estimate: operator count to price')
    parser.add_argument('--perplexity-cap', type=float, help='USD; required for any API run')
    parser.add_argument('--claude-cap', type=float, help='USD; required for any API run')
    parser.add_argument('--batch', action='store_true', help='extract via the Message Batches API (half price)')
    parser.add_argument('--batch-rows', type=int, default=50, help='--batch: rows per submitted batch')
    parser.add_argument('--effort', default='medium', choices=['low', 'medium', 'high'])
    parser.add_argument('--workers', type=int, default=4, help='concurrent Perplexity searches')
    parser.add_argument('--discover-only', action='store_true', help='stop after building the operator list')
    parser.add_argument('--rediscover', help='comma-separated markets whose operator list is rebuilt '
                                             '(from the cached discovery search)')
    parser.add_argument('--searches-only', action='store_true',
                        help='build operator lists and run every search, then stop before extraction')
    parser.add_argument('--output', help='panel CSV path (default: the dry-run or full output)')
    parser.add_argument('--operator-ids', help='comma-separated operator_ids to code (default: all in the markets)')
    args = parser.parse_args()

    cache = SearchCache()
    output = args.output or (FULL_OUTPUT if args.full else DRY_RUN_OUTPUT)
    if args.estimate:
        known = load_operators()
        n_ops = int((known['included'] == 'yes').sum()) if args.full and len(known) else args.operators
        print(f"\nEstimate for {len(MARKETS)} markets, ~{n_ops} operators, observation year {args.year}:")
        estimate(len(MARKETS), n_ops, cache, output)
        return
    if args.perplexity_cap is None or args.claude_cap is None:
        sys.exit('Set --perplexity-cap and --claude-cap (USD): every step stops before it could exceed them.')

    markets = list(MARKETS) if args.full else [m.strip() for m in (args.markets or 'Germany').split(',')]
    unknown = [m for m in markets if m not in MARKETS]
    if unknown:
        sys.exit(f"Not in the panel: {', '.join(unknown)}")
    pplx_key = env_key('PERPLEXITY_API_KEY') or sys.exit('Missing PERPLEXITY_API_KEY in .env')
    client = anthropic_client()
    spend = Spend(args.perplexity_cap, args.claude_cap)

    discover(markets, args.year, cache, client, pplx_key, spend, args)
    ops = load_operators()
    ops = ops[ops['market'].isin(markets) & (ops['included'] == 'yes')]
    if args.operator_ids:
        ops = ops[ops['operator_id'].isin(args.operator_ids.split(','))]
    print(f"\n{len(ops)} included operator(s) in {', '.join(markets)}: "
          + ', '.join(ops['operator_name']))
    if args.discover_only:
        print(f"\n{spend.summary()}")
        return

    writer, out_f, done = open_resumable_csv(output, PANEL_COLUMNS, 'row_id')
    todo = ops[~ops['operator_id'].map(lambda i: f"{i}-{args.year}").isin(done)]
    print(f"{len(ops) - len(todo)} already in {output}, {len(todo)} to code.")

    jobs = [(search_key('regulatory', MARKETS[m]), LAYER_QUESTIONS['regulatory'].format(market=m, year=args.year))
            for m in sorted(set(todo['market']))]
    for _, op in todo.iterrows():
        name = op['operator_name'] + (f" ({op['brands']})" if op['brands'] and op['brands'] != NOT_DISCLOSED else '')
        jobs += [(search_key(layer, f"{op['operator_id']}|{args.year}"),
                  LAYER_QUESTIONS[layer].format(operator=name, market=op['market'], year=args.year)) for layer in LAYERS]
    print(f"\nSearches: {len(jobs)} needed, {sum(1 for k, p in jobs if cache.fresh(k, p))} cached.")
    missing = run_searches(jobs, cache, pplx_key, spend, args.workers)
    if args.searches_only:
        print(f"\nSearches only: {len(jobs) - len(missing)} of {len(jobs)} cached, {len(missing)} missing. "
              f"No extraction run. {spend.summary()}.")
        return

    def searches_for(op):
        found = {layer: cache.get(search_key(layer, f"{op['operator_id']}|{args.year}")) for layer in LAYERS}
        found['regulatory'] = cache.get(search_key('regulatory', op['market_iso']))
        return found if all(found.values()) else None

    ready = [op for _, op in todo.iterrows() if searches_for(op)]
    if len(ready) < len(todo):
        print(f"{len(todo) - len(ready)} operator(s) lack a search and wait for the next run.")
    cables = load_cable_names()
    raw_f, err_f = open(output + '.raw.jsonl', 'a'), open(output + '.errors.jsonl', 'a')

    def content(op):
        found = searches_for(op)
        return operator_content(op, args.year, {k: e['search'] for k, e in found.items()})

    def write(op, fields, message, cost, batch_id=None):
        writer.writerow(build_row(op, args.year, fields, searches_for(op), cables))
        out_f.flush()
        raw_f.write(json.dumps({'row_id': f"{op['operator_id']}-{args.year}", 'claude': {
            'model': message.model, 'fields': fields, 'usage': message.usage.to_dict(), 'cost': cost,
            'batch': batch_id is not None, 'batch_id': batch_id}}, default=str) + '\n')
        raw_f.flush()

    def log_error(op_id, e, batch_id=None):
        err_f.write(json.dumps({'row_id': op_id, 'error': f"{type(e).__name__}: {e}", 'batch_id': batch_id}) + '\n')
        err_f.flush()
        print(f"  ✗ {op_id}: {type(e).__name__}: {e}")

    prior = []
    if os.path.exists(output + '.raw.jsonl'):
        prior = [json.loads(l)['claude'] for l in open(output + '.raw.jsonl')]
    sync_costs = [c['cost'] for c in prior if not c.get('batch')]

    if args.batch:
        by_row = {f"{op['operator_id']}-{args.year}": op for op in ready}
        p90 = float(np.percentile(sync_costs, 90)) if sync_costs else OPERATOR_ESTIMATE
        spent = run_capped_batches(
            client, MODEL, list(by_row.items()),
            lambda op: request_params(CLAUDE_SYSTEM, None, content(op), args.effort, '1h'),
            lambda rid, message, cost, bid: write(by_row[rid], parse_response(message, EXTRACTION_VALIDATOR),
                                                   message, cost, bid),
            lambda rid, e, bid: log_error(rid, e, bid),
            output + '.batches.jsonl', spend.cap['claude'] - spend.spent['claude'], args.batch_rows,
            lambda: worst_case_batch_rate(MODEL, [(c['cost'], c['usage']) for c in prior if c.get('batch')],
                                          p90, PREFIX_TOKENS),
            PREFIX_TOKENS)
        spend.add('claude', spent)
    else:
        for op in ready:
            rate = max(sync_costs) if sync_costs else OPERATOR_ESTIMATE * 1.5
            if not spend.allows('claude', rate):
                print(f"  Claude cap reached: stopping before {op['operator_name']}.")
                break
            params = request_params(CLAUDE_SYSTEM, None, content(op), args.effort, '5m')
            try:
                fields, message, cost = call_claude(client, params, EXTRACTION_VALIDATOR)
            except Exception as e:
                # A billed but unusable reply still counts against the cap.
                spend.add('claude', getattr(e, 'cost', 0))
                log_error(f"{op['operator_id']}-{args.year}", e)
                continue
            spend.add('claude', cost)
            sync_costs.append(cost)
            write(op, fields, message, cost)
            u = message.usage
            print(f"  coded {op['operator_name']:32} ${cost:.3f} (in {u.input_tokens}, cache read "
                  f"{u.cache_read_input_tokens or 0}, out {u.output_tokens})")
    out_f.close(), raw_f.close(), err_f.close()
    print(f"\nSpend this run: {spend.summary()}. Output: {output}. Nothing was written to Supabase.")


if __name__ == '__main__':
    main()
