"""
Push the data-center enrichment (data/datacenter_enrichment.csv) to the private Supabase
datacenters table (create it first with sql/create_datacenters.sql), or write the same rows
as the shareable export CSV.

The export differs from the working CSV in four ways: the pipeline's tags in notes become
owner_parent_inferred / owner_origin_inferred and the landing note becomes nearest_landing;
the pre-field foreign_linked_entities placeholder reads "not extracted"; and two columns are
renamed with their units (cable_landing_km, facilities_within_50km).

Usage:
  python push_datacenters.py               # preview old vs new datacenters rows (writes nothing)
  python push_datacenters.py --push        # upsert every row by facility_id, delete stale rows
  python push_datacenters.py --csv PATH    # write the export CSV instead (no Supabase)
"""

import sys
from collections import Counter

import pandas as pd

from enrich_datacenters import FULL_OUTPUT, NOT_DISCLOSED, ORIGIN_NOTE
from pipeline_common import (fetch_all, get_read_client, get_supabase, print_count_diff, print_key_diff,
                             should_push, sync_rows)

PARENT_NOTE = 'owner_parent from public corporate structure, not facility-specific evidence (tier set to 3)'
LANDING_PREFIX = 'nearest in-service landing: '
NUMERIC = {'lat': float, 'lon': float, 'capacity_mw_coded': float, 'cable_landing_km': float,
           'facilities_within_50km': int}
BOOLEAN = ['owner_parent_inferred', 'owner_origin_inferred']


def split_notes(notes):
    segments = notes.split(' | ')
    landing = [s for s in segments if s.startswith(LANDING_PREFIX)]
    if len(landing) != 1:
        raise ValueError(f"expected one landing note, got {len(landing)}: {notes[:120]}")
    return {
        'notes': ' | '.join(s for s in segments
                            if s not in (PARENT_NOTE, ORIGIN_NOTE) and not s.startswith(LANDING_PREFIX)) or 'none',
        'nearest_landing': landing[0][len(LANDING_PREFIX):],
        'owner_parent_inferred': 'yes' if PARENT_NOTE in segments else 'no',
        'owner_origin_inferred': 'yes' if ORIGIN_NOTE in segments else 'no',
    }


def build_export(path=FULL_OUTPUT):
    """The shareable export as a DataFrame of strings, columns in export order."""
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    split = pd.DataFrame([split_notes(n) for n in df['notes']], index=df.index)
    out = df.drop(columns='notes').rename(columns={'cable_landing_proximity': 'cable_landing_km',
                                                   'interconnection_density': 'facilities_within_50km'})
    out['foreign_linked_entities'] = out['foreign_linked_entities'].replace(
        'not extracted (row predates this field)', 'not extracted')
    columns = []
    for c in out.columns:
        columns.append(c)
        if c == 'owner_parent':
            columns.append('owner_parent_inferred')
        elif c == 'owner_origin':
            columns.append('owner_origin_inferred')
        elif c == 'cable_landing_km':
            columns.append('nearest_landing')
    columns.insert(columns.index('foreign_linked_entities'), 'notes')
    return pd.concat([out, split], axis=1)[columns]


def to_db_rows(export):
    """Typed rows for the datacenters table: numbers as numbers (null when not disclosed), flags as booleans."""
    rows = []
    for record in export.to_dict('records'):
        for col, cast in NUMERIC.items():
            value = record[col]
            record[col] = None if value in (NOT_DISCLOSED, '') else cast(float(value))
        for col in BOOLEAN:
            record[col] = record[col] == 'yes'
        rows.append(record)
    return rows


if __name__ == '__main__':
    export = build_export()
    if '--csv' in sys.argv:
        path = sys.argv[sys.argv.index('--csv') + 1]
        export.to_csv(path, index=False)
        print(f"Wrote {len(export)} rows x {len(export.columns)} columns to {path}")
        sys.exit()

    rows = to_db_rows(export)
    print(f"Built {len(rows)} facilities with {len(export.columns)} columns from {FULL_OUTPUT}")
    if should_push():
        sync_rows(get_supabase(), 'datacenters', rows, key='facility_id')
    else:
        old = fetch_all(get_read_client(), 'datacenters')
        print(f"\nPREVIEW: datacenters (old = live Supabase, new = this run). Rows: {len(old)} old → {len(rows)} new")
        old_columns = set(old[0]) - {'id', 'created_at'} if old else set()
        if old and old_columns != set(export.columns):
            print(f"  Columns only in live table: {sorted(old_columns - set(export.columns)) or 'none'}")
            print(f"  Columns only in new data:   {sorted(set(export.columns) - old_columns) or 'none'}")
        print_key_diff('Facilities (by facility_id)', [r['facility_id'] for r in old], [r['facility_id'] for r in rows], limit=10)
        print_count_diff('owner_origin (top 6):', Counter(r['owner_origin'] for r in old),
                         Counter(dict(Counter(r['owner_origin'] for r in rows).most_common(6))))
