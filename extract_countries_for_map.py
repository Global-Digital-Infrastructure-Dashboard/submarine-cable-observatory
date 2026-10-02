"""
Extract country list with cable counts for map visualization

Usage:
  python extract_countries_for_map.py          # preview old vs new countries_map (writes nothing)
  python extract_countries_for_map.py --push   # sync Supabase countries_map + write local JSON
"""

import json
from pathlib import Path

from pipeline_common import (load_dataset, should_push, get_supabase, get_read_client,
                             fetch_all, sync_rows, print_key_diff)

df = load_dataset()

# Count cables per country
country_cables = {}
for idx, row in df.iterrows():
    for country in row['landing_countries_list']:
        if country:
            country_cables[country] = country_cables.get(country, 0) + 1

# Sort by cable count
sorted_countries = sorted(country_cables.items(), key=lambda x: x[1], reverse=True)

output = {
    'countries': [
        {'name': country, 'cables': count}
        for country, count in sorted_countries
    ],
    'total_countries': len(sorted_countries),
    'total_cables': len(df)
}

print(f"✓ Extracted {len(sorted_countries)} countries")
print(f"\nTop 10 countries by cable count:")
for country, count in sorted_countries[:10]:
    print(f"  {country}: {count} cables")

# ============================================================================
# SUPABASE
# ============================================================================

if should_push():
    sync_rows(get_supabase(), 'countries_map', output['countries'], key='name')

    output_path = Path('public/data')
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path / 'countries_for_map.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("✓ Exported public/data/countries_for_map.json")
else:
    old = {r['name']: r['cables'] for r in fetch_all(get_read_client(), 'countries_map', 'id,name,cables')}
    new = dict(sorted_countries)

    print("\n" + "="*80)
    print("PREVIEW: countries_map (old = live Supabase, new = this run)")
    print("="*80)
    print(f"Total cable landings: {sum(old.values())} old → {sum(new.values())} new")
    print_key_diff('Countries', old, new)

    changed = sorted(set(old) & set(new), key=lambda k: -abs(new[k] - old[k]))
    print("\nLargest count changes (kept countries):")
    for name in changed[:15]:
        print(f"  {name:28}{old[name]:>5} → {new[name]:<5}")
    print("\n(preview only — nothing written. Pass --push to sync Supabase countries_map)")
