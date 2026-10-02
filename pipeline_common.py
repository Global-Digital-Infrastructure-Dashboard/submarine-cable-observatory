"""
Shared helpers for the data-processing scripts:
dataset loading, bloc classification, and the Supabase client.
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


def _service_role_key():
    """From the environment, else from the gitignored .env file. Never hardcoded."""
    key = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')
    if not key and os.path.exists('.env'):
        for line in open('.env'):
            name, _, value = line.strip().partition('=')
            if name.strip() == 'SUPABASE_SERVICE_ROLE_KEY':
                key = value.strip().strip('"\'')
    return key


def get_supabase():
    """Service-role client for backend writes."""
    from supabase import create_client

    key = _service_role_key()
    if not key:
        sys.exit('SUPABASE_SERVICE_ROLE_KEY is not set (env or .env); refusing to push.')
    return create_client(os.environ.get('SUPABASE_URL', SUPABASE_URL), key)


def get_read_client():
    """Client for previews: service key if set, else the public anon key the frontend already ships."""
    from supabase import create_client

    key = _service_role_key()
    if not key:
        frontend = open('src/lib/supabase.js').read()
        key = re.search(r"supabaseKey\s*=\s*'([^']+)'", frontend).group(1)
    return create_client(os.environ.get('SUPABASE_URL', SUPABASE_URL), key)


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
