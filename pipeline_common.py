"""
Shared helpers for the data-processing scripts:
dataset loading, bloc classification, the Supabase client, and paid-API helpers
(Perplexity search, Claude client, spend tracking, capped batch runs, resumable CSVs).
"""

import os
import re
import sys
from collections import Counter

import numpy as np
import pandas as pd

DATASET_PATH = 'data/global_submarine_dataset_2026.xlsx'
SUPABASE_URL = 'https://nvlvwmkpaunoudvoivrz.supabase.co'

BLOCS = ['China', 'US', 'Europe', 'Japan', 'India', 'Mixed', 'Other', 'Unknown']

# ============================================================================
# BLOC CLASSIFICATION
# ============================================================================

# Country tokens are matched exactly (after splitting on ';' / ','), so 'US'
# no longer falls through to 'Other' and 'Niger' can't match 'Nigeria'.
BLOC_COUNTRIES = {
    'China': {'china', 'prc', "people's republic of china", 'hong kong'},
    'US': {'us', 'usa', 'u.s.', 'united states', 'united states of america'},
    'Europe': {
        # EU-27
        'austria', 'belgium', 'bulgaria', 'croatia', 'cyprus', 'czechia',
        'czech republic', 'denmark', 'estonia', 'finland', 'france', 'germany',
        'greece', 'hungary', 'ireland', 'italy', 'latvia', 'lithuania',
        'luxembourg', 'malta', 'netherlands', 'poland', 'portugal', 'romania',
        'slovakia', 'slovenia', 'spain', 'sweden',
        # EEA / EFTA + UK
        'iceland', 'liechtenstein', 'norway', 'switzerland',
        'uk', 'united kingdom', 'great britain', 'britain',
    },
    'Japan': {'japan'},
    'India': {'india'},
}
UNKNOWN_TOKENS = {'', 'unknown', 'n/a', 'na', 'none', 'tbd'}


def split_list_field(field_str):
    """Parse comma/semicolon separated fields"""
    if pd.isna(field_str):
        return []
    return [item.strip() for item in re.split(r'[,;]', str(field_str)) if item.strip()]


# The dataset mixes codes and full names ('US' vs 'United States'). Normalize to
# the full names the frontend map keys on, so each country is counted once and
# domestic-ownership checks can use exact matching.
COUNTRY_ALIASES = {
    'us': 'United States',
    'usa': 'United States',
    'u.s.': 'United States',
    'united states of america': 'United States',
    'us (incl. us virgin islands)': 'United States',
    'uk': 'United Kingdom',
    'great britain': 'United Kingdom',
    'britain': 'United Kingdom',
    'uae': 'United Arab Emirates',
    'cape verde': 'Cabo Verde',
    'virgin islands (u.k.)': 'Virgin Islands (British)',
}


def canonical_country(name):
    return COUNTRY_ALIASES.get(name.strip().lower(), name.strip())


def country_list(field_str):
    """Split a country field and normalize each name (order kept, duplicates dropped)."""
    return list(dict.fromkeys(canonical_country(c) for c in split_list_field(field_str)))


def classify_bloc(country_str):
    """
    Classify a ';'-separated country list into one of BLOCS.

    - No known countries (blank / 'Unknown')  -> Unknown
    - Exactly one named bloc present         -> that bloc
    - More than one named bloc present       -> Mixed
    - Only countries outside the named blocs -> Other
    Countries outside the named blocs don't make a cable Mixed (same as before).
    """
    tokens = [t.lower() for t in split_list_field(country_str)]
    known = [t for t in tokens if t not in UNKNOWN_TOKENS]
    if not known:
        return 'Unknown'

    blocs_present = {
        bloc for bloc, countries in BLOC_COUNTRIES.items()
        if any(t in countries for t in known)
    }
    if not blocs_present:
        return 'Other'
    if len(blocs_present) == 1:
        return blocs_present.pop()
    return 'Mixed'


# ============================================================================
# DATA LOADING
# ============================================================================

def load_dataset():
    df = pd.read_excel(DATASET_PATH)
    df['supplier_bloc'] = df['suppliers_country'].apply(classify_bloc)
    df['owner_bloc'] = df['owner_country'].apply(classify_bloc)
    df['landing_countries_list'] = df['landing_countries'].apply(country_list)
    return df


def is_domestic(country, country_field):
    """True if `country` is one of the (normalized) countries in `country_field` — exact match, no substrings."""
    return canonical_country(country) in country_list(country_field)


# ============================================================================
# SUPABASE
# ============================================================================

def should_push():
    """Scripts only write (Supabase + local JSON) when run with --push; otherwise they preview."""
    return '--push' in sys.argv


def env_key(var):
    """From the environment, else from the gitignored .env file. Never hardcoded."""
    key = os.environ.get(var)
    if not key and os.path.exists('.env'):
        for line in open('.env'):
            name, _, value = line.strip().partition('=')
            if name.strip() == var:
                key = value.strip().strip('"\'')
    return key


def _service_role_key():
    return env_key('SUPABASE_SERVICE_ROLE_KEY')


def get_supabase():
    """Service-role client for backend writes."""
    from supabase import create_client

    key = _service_role_key()
    if not key:
        sys.exit('SUPABASE_SERVICE_ROLE_KEY is not set (env or .env); refusing to push.')
    return create_client(os.environ.get('SUPABASE_URL', SUPABASE_URL), key)


def _anon_key():
    """The public anon key the frontend already ships."""
    frontend = open('src/lib/supabase.js').read()
    return re.search(r"supabaseKey\s*=\s*'([^']+)'", frontend).group(1)


def get_read_client():
    """Client for previews: service key if set, else the anon key."""
    from supabase import create_client

    return create_client(os.environ.get('SUPABASE_URL', SUPABASE_URL), _service_role_key() or _anon_key())


def get_anon_client():
    """Anon-key client for read-only lookups that must never hold write credentials."""
    from supabase import create_client

    return create_client(os.environ.get('SUPABASE_URL', SUPABASE_URL), _anon_key())


def fetch_all(client, table, columns='*', page_size=1000):
    """Read every row (PostgREST caps a single response at 1000 rows)."""
    rows, start = [], 0
    while True:
        page = client.table(table).select(columns).order('id').range(start, start + page_size - 1).execute().data
        rows.extend(page)
        if len(page) < page_size:
            return rows
        start += page_size


def _delete_ids(table, ids, chunk=200):
    for i in range(0, len(ids), chunk):
        table.delete().in_('id', ids[i:i + chunk]).execute()


def replace_rows(client, table_name, rows):
    """
    Replace a table's contents without a window where it is empty or half-written:
    insert the new rows first, then delete the old ids. If the insert fails nothing
    changed; if deleting the old rows fails, the new rows are removed again.
    """
    table = client.table(table_name)
    old_ids = [r['id'] for r in fetch_all(client, table_name, 'id')]
    inserted = table.insert(clean_rows(rows)).execute().data
    new_ids = [r['id'] for r in inserted]
    try:
        _delete_ids(table, old_ids)
    except Exception:
        _delete_ids(table, new_ids)
        raise
    print(f"✓ Replaced {table_name}: inserted {len(new_ids)} rows, deleted {len(old_ids)} old rows")


def sync_rows(client, table_name, rows, key):
    """
    For tables with a UNIQUE constraint on `key` (insert-first would collide):
    upsert every new row in one statement (all-or-nothing), then delete rows
    whose key is no longer in the dataset.
    """
    table = client.table(table_name)
    table.upsert(clean_rows(rows), on_conflict=key).execute()
    new_keys = {r[key] for r in rows}
    stale_ids = [r['id'] for r in fetch_all(client, table_name, f'id,{key}') if r[key] not in new_keys]
    _delete_ids(table, stale_ids)
    print(f"✓ Synced {table_name}: upserted {len(rows)} rows, deleted {len(stale_ids)} stale rows")


# ============================================================================
# PREVIEW HELPERS
# ============================================================================

def print_count_diff(title, old_counts, new_counts):
    old_counts, new_counts = Counter(old_counts), Counter(new_counts)
    keys = sorted(set(old_counts) | set(new_counts), key=lambda k: -new_counts.get(k, 0))
    print(f"\n{title}")
    print(f"  {'':24}{'old':>8}{'new':>8}{'Δ':>8}")
    for k in keys:
        o, n = old_counts.get(k, 0), new_counts.get(k, 0)
        print(f"  {str(k):24}{o:>8}{n:>8}{n - o:>+8}")


def print_key_diff(label, old_keys, new_keys, limit=40):
    old_keys, new_keys = set(old_keys), set(new_keys)
    added, removed = sorted(new_keys - old_keys), sorted(old_keys - new_keys)
    print(f"\n{label}: {len(old_keys)} old → {len(new_keys)} new "
          f"({len(added)} added, {len(removed)} removed, {len(old_keys & new_keys)} kept)")
    if added:
        print(f"  + {', '.join(added[:limit])}{' …' if len(added) > limit else ''}")
    if removed:
        print(f"  - {', '.join(removed[:limit])}{' …' if len(removed) > limit else ''}")


def to_native(value):
    """Convert numpy scalars to plain Python so supabase-py can JSON-encode them."""
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.floating):
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def clean_rows(rows):
    return [{k: to_native(v) for k, v in row.items()} for row in rows]


# ============================================================================
# PAID API HELPERS (Perplexity search, Claude extraction, spend tracking)
# ============================================================================

# USD per token. Perplexity responses usually report their own cost (usage.cost.total_cost);
# its table is only the fallback when they don't.
CLAUDE_PRICE = {
    'claude-opus-5-5': {'input': 4.00 / 1e6, 'output': 20.00 / 1e6, 'cache_read': 0.20 / 1e6},
    'claude-sonnet-5-5': {'input': 2.00 / 1e6, 'output': 10.00 / 1e6, 'cache_read': 0.20 / 1e6},
}
BATCH_DISCOUNT = 0.5  # Message Batches: half price on every token, cache reads/writes included
BATCH_SAFETY = 1.05  # margin on the worst-case per-row batch rate (output length varies)
PERPLEXITY_URL = 'https://api.perplexity.ai/chat/completions'
PERPLEXITY_MODEL = 'sonar-pro'
PERPLEXITY_PRICE = {'input': 3.00 / 1e6, 'output': 15.00 / 1e6, 'request': 10.00 / 1000}


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


def average(costs, default):
    return sum(costs) / len(costs) if costs else default


def anthropic_client():
    """Claude client from ANTHROPIC_API_KEY. Keys not scoped to a workspace (e.g. an org-level
    research key) must name one per request, from ANTHROPIC_WORKSPACE_ID. Retries aren't
    logged, and a request that fails after Anthropic processes it is still billed - keep them
    to one so unlogged spend stays small."""
    import anthropic

    key = env_key('ANTHROPIC_API_KEY')
    if not key:
        sys.exit('Missing ANTHROPIC_API_KEY: add it to .env (gitignored) as NAME=value, or export it.')
    workspace = env_key('ANTHROPIC_WORKSPACE_ID')
    return anthropic.Anthropic(api_key=key, max_retries=1,
                               default_headers={'anthropic-workspace-id': workspace} if workspace else None)


def perplexity_search(system, prompt, api_key, context_size='medium'):
    """One sonar-pro search: {'answer', 'results', 'usage', 'cost'}, cost as Perplexity reports it."""
    import time
    import requests

    body = {
        'model': PERPLEXITY_MODEL,
        'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': prompt}],
        'web_search_options': {'search_context_size': context_size},
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


def open_resumable_csv(path, columns, key):
    """Append-mode DictWriter on `path` plus the `key` values already written, so a re-run skips
    completed rows. Exits if an existing file has different columns."""
    import csv

    done = set()
    if os.path.exists(path):
        header = next(csv.reader(open(path)), None)
        if header and header != columns:
            sys.exit(f"{path} has different columns than this version writes: "
                     f"missing {sorted(set(columns) - set(header))}, extra {sorted(set(header) - set(columns))}.")
        done = set(pd.read_csv(path, usecols=[key], dtype=str)[key]) if header else set()
    new_file = not os.path.exists(path) or os.path.getsize(path) == 0
    out_f = open(path, 'a', newline='')
    writer = csv.DictWriter(out_f, fieldnames=columns)
    if new_file:
        writer.writeheader()
        out_f.flush()
    return writer, out_f, done


def worst_case_batch_rate(model, batched, fallback_rate, cache_prefix_tokens):
    """Per-row batch cost to size a chunk with, assuming every row writes the prompt cache.

    A big batch runs in parallel, so many rows miss the cache: on 2026-10-29 a third of a
    1,137-row batch wrote it (2x input price) instead of reading it, and the batch cost 21%
    over the average of earlier, mostly-cached rows. So take each logged batched row's cost
    (`batched`: (cost, usage) pairs) as if its cache read had been a 1h write, average that,
    and add a margin. With no batched rows yet, use `fallback_rate` (a synchronous per-row
    rate) at the batch discount plus a full cache write.
    """
    price = CLAUDE_PRICE[model]
    miss_premium = (price['input'] * 2 - price['cache_read']) * BATCH_DISCOUNT
    rates = [cost + (usage.get('cache_read_input_tokens') or 0) * miss_premium for cost, usage in batched]
    if rates:
        return average(rates, 0) * BATCH_SAFETY, f'worst case (every row a cache write) over {len(rates)} batched rows'
    return ((fallback_rate * BATCH_DISCOUNT + cache_prefix_tokens * miss_premium) * BATCH_SAFETY,
            'conservative: no batched rows yet')


def run_capped_batches(client, model, items, make_params, on_result, on_error, state_path, cap,
                       batch_rows, rate_fn, cache_prefix_tokens):
    """Extract via the Message Batches API without ever being able to exceed `cap` (USD).

    Collects any batch recorded in `state_path` but not yet collected, then submits `items`
    ((custom_id, payload) pairs) in chunks of at most `batch_rows`, one at a time. Each chunk
    is sized to what is left of the cap after the billed cost of the chunks before it, at the
    per-row rate `rate_fn()` returns ((rate, basis)): a chunk is billed in full even if it
    overruns the balance. For each result, on_result(custom_id, message, cost, batch_id) writes
    it, or on_error(custom_id, error, batch_id) logs it; the cost of an invalid but billed result
    is still counted. Returns the cost of everything collected this run.
    """
    import json
    import time

    state = [json.loads(line) for line in open(state_path)] if os.path.exists(state_path) else []
    collected = {s['batch_id'] for s in state if s.get('collected')}
    pending = [s for s in state if 'facility_ids' in s and s['batch_id'] not in collected]

    def collect(entry):
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
            cost = 0.0
            try:
                if result.result.type != 'succeeded':
                    raise RuntimeError(f"batch result {result.result.type}: {getattr(result.result, 'error', '')}")
                message = result.result.message
                cost = usage_cost(entry['model'], message.usage.to_dict(), batch=True)
                on_result(result.custom_id, message, cost, batch_id)
            except Exception as e:
                failed += 1
                on_error(result.custom_id, e, batch_id)
            else:
                done += 1
            spent += cost
        with open(state_path, 'a') as f:
            f.write(json.dumps({'batch_id': batch_id, 'collected': True}) + '\n')
        print(f"\nBatch {batch_id}: {done} rows written, {failed} failed. Claude cost ${spent:.2f} "
              f"(${spent / max(done, 1):.4f}/row at batch price, cache included).")
        return spent

    # A batch left from an earlier run was budgeted then; count it against this cap anyway.
    spent = sum(collect(entry) for entry in pending)
    submitted = {i for entry in pending for i in entry['facility_ids']}
    items = [(i, p) for i, p in items if i not in submitted]
    cache_write = cache_prefix_tokens * CLAUDE_PRICE[model]['input'] * 2 * BATCH_DISCOUNT
    while items:
        per_row, basis = rate_fn()
        left = cap - spent
        n = min(len(items), batch_rows, max(0, int((left - cache_write) // per_row)))
        if n == 0:
            print(f"${left:.2f} left of the ${cap:.2f} cap doesn't cover one row at "
                  f"${per_row:.4f}/row ({basis}); stopping with {len(items)} rows unsubmitted.")
            break
        chunk, items = items[:n], items[n:]
        print(f"Submitting {n} rows: at most ${n * per_row + cache_write:.2f} (${per_row:.4f}/row, {basis}); "
              f"${spent:.2f} spent so far this run, cap ${cap:.2f}.")
        batch = client.messages.batches.create(requests=[
            {'custom_id': i, 'params': make_params(p)} for i, p in chunk])
        # 'facility_ids' is the state file's historical name for the batch's custom_ids.
        entry = {'batch_id': batch.id, 'model': model, 'facility_ids': [i for i, _ in chunk],
                 'submitted_at': time.strftime('%Y-%m-%dT%H:%M:%S')}
        with open(state_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        print(f"Batch {batch.id} submitted; recorded in {state_path} so it can be collected if this exits.")
        spent += collect(entry)
    print(f"\nClaude cost this run: ${spent:.2f} of cap ${cap:.2f}.")
    return spent
