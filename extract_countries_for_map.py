"""
Extract country list with cable counts for map visualization
"""

import pandas as pd
import json
from pathlib import Path

df = pd.read_excel('data/global_submarine_dataset_V1_2026.xlsx')

def parse_list_field(field_str):
    if pd.isna(field_str):
        return []
    import re
    return [item.strip() for item in re.split(r'[,;]', str(field_str)) if item.strip()]

df['landing_countries_list'] = df['landing_countries'].apply(parse_list_field)

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

output_path = Path('../dashboard/public/data')
output_path.mkdir(parents=True, exist_ok=True)

with open(output_path / 'countries_for_map.json', 'w') as f:
    json.dump(output, f, indent=2)

print(f"✓ Extracted {len(sorted_countries)} countries")
print(f"\nTop 10 countries by cable count:")
for country, count in sorted_countries[:10]:
    print(f"  {country}: {count} cables")
