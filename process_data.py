import pandas as pd
import json
from pathlib import Path
import numpy as np

print("Starting data processing...")

# Read your submarine cables data
df = pd.read_excel('data/global_submarine_dataset_V1_2026.xlsx')
print(f"Loaded {len(df)} cables")

# Simple bloc classification
def classify_bloc(country_str):
    if pd.isna(country_str):
        return 'Unknown'
    country_str = str(country_str).lower()
    
    if 'china' in country_str: return 'China'
    if 'united states' in country_str or 'usa' in country_str: return 'US'
    if any(word in country_str for word in ['france', 'uk', 'united kingdom', 'germany', 'italy', 'spain']): 
        return 'Europe'
    if 'japan' in country_str: return 'Japan'
    if 'india' in country_str: return 'India'
    return 'Other'

print("Classifying blocs...")
df['supplier_bloc'] = df['suppliers_country'].apply(classify_bloc)
df['owner_bloc'] = df['owner_country'].apply(classify_bloc)

print("Bloc distribution:")
print(df['supplier_bloc'].value_counts())

# Convert DataFrame to dict and handle NaN/None values
cables_list = df.replace({np.nan: None}).to_dict('records')

# Export to JSON for React app
output = {
    'version': '1.0',
    'updated': '2026-02-26',
    'total_cables': len(df),
    'cables': cables_list
}

# Save to dashboard's public/data directory
output_path = Path('../dashboard/public/data')
output_path.mkdir(parents=True, exist_ok=True)

output_file = output_path / 'cables_data.json'
with open(output_file, 'w') as f:
    json.dump(output, f, indent=2, default=str)

print(f"\n✓ Successfully processed {len(df)} cables")
print(f"✓ Saved to: {output_file}")
print("\nYou can now run your React dashboard!")