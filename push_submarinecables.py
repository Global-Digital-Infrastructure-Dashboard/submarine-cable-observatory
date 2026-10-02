"""
Push the full cable dataset (plus computed supplier_bloc / owner_bloc) to the
Supabase submarinecables table.

Usage:
  python push_submarinecables.py          # preview old vs new submarinecables (writes nothing)
  python push_submarinecables.py --push   # replace all submarinecables rows
"""

from collections import Counter

import pandas as pd

from pipeline_common import (load_dataset, should_push, get_supabase, get_read_client,
                             fetch_all, replace_rows, print_count_diff, print_key_diff)

DATASET_COLUMNS = [
    'cable_name', 'rfs_year', 'length_km', 'status', 'landing_countries',
    'landing_stations', 'suppliers', 'suppliers_country', 'chinese_supplier',
    'owners', 'owner_country', 'chinese_owner', 'regions', 'source', 'notes',
    'revised', 'revision_status', 'revision_detail', 'financier',
    'chinese_financier', 'hk_linked', 'financier_type', 'financier_nationality',
    'financing_confidence', 'financing_note',
]
COLUMNS = DATASET_COLUMNS + ['supplier_bloc', 'owner_bloc']

df = load_dataset()
missing = [c for c in DATASET_COLUMNS if c not in df.columns]
if missing:
    raise SystemExit(f"Dataset is missing columns: {missing}")

rows = df[COLUMNS].astype(object).where(df[COLUMNS].notna(), None).to_dict('records')
print(f"Loaded {len(rows)} cables with {len(COLUMNS)} columns")

if should_push():
    replace_rows(get_supabase(), 'submarinecables', rows)
else:
    old = fetch_all(get_read_client(), 'submarinecables')

    print("\n" + "="*80)
    print("PREVIEW: submarinecables (old = live Supabase, new = this run)")
    print("="*80)
    print(f"Rows: {len(old)} old → {len(rows)} new")

    old_columns = set(old[0]) - {'id', 'created_at'} if old else set()
    if old and old_columns != set(COLUMNS):
        print(f"  Columns only in live table: {sorted(old_columns - set(COLUMNS)) or 'none'}")
        print(f"  Columns only in new data:   {sorted(set(COLUMNS) - old_columns) or 'none'}")

    print_key_diff('Cables (by cable_name)', [r['cable_name'] for r in old], [r['cable_name'] for r in rows], limit=25)
    print_count_diff('supplier_bloc:', Counter(r['supplier_bloc'] for r in old), Counter(r['supplier_bloc'] for r in rows))
    print_count_diff('owner_bloc:', Counter(r['owner_bloc'] for r in old), Counter(r['owner_bloc'] for r in rows))

    old_by_name = {r['cable_name']: r for r in old}
    for col in ('supplier_bloc', 'owner_bloc'):
        moves = Counter(
            (old_by_name[r['cable_name']][col], r[col]) for r in rows
            if r['cable_name'] in old_by_name and old_by_name[r['cable_name']][col] != r[col]
        )
        print(f"\n{col} reclassified (kept cables): {sum(moves.values())}")
        for (o, n), count in moves.most_common(10):
            print(f"  {o:>8} → {n:<8}{count:>5}")

    print("\n(preview only — nothing written. Pass --push to replace Supabase submarinecables)")
