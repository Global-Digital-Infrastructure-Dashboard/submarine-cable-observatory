"""
Comprehensive Data Processing for All Dashboard Modules
BLOC-NEUTRAL METHODOLOGY: Independence = domestic control, not anti-Chinese
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from collections import defaultdict
import re

print("="*80)
print("COMPREHENSIVE DATA PROCESSING - BLOC-NEUTRAL METHODOLOGY")
print("="*80)

# Load the dataset
df = pd.read_excel('data/global_submarine_dataset V1_2026.xlsx')
print(f"\nLoaded {len(df)} cables")

# ============================================================================
# BLOC CLASSIFICATION
# ============================================================================

def classify_bloc(country_str):
    """Classify countries into geopolitical blocs"""
    if pd.isna(country_str) or country_str == '':
        return 'Unknown'
    
    country_str = str(country_str).lower()
    
    china_keywords = ['china', 'chinese', 'prc', 'hong kong']
    us_keywords = ['united states', 'usa', 'us ', 'american']
    europe_keywords = ['france', 'uk', 'united kingdom', 'britain', 'germany', 'italy', 
                       'spain', 'netherlands', 'belgium', 'sweden', 'finland',
                       'denmark', 'norway', 'ireland', 'portugal', 'austria', 'alcatel']
    japan_keywords = ['japan', 'japanese', 'nec']
    india_keywords = ['india', 'indian']
    
    blocs_present = []
    
    if any(keyword in country_str for keyword in china_keywords):
        blocs_present.append('China')
    if any(keyword in country_str for keyword in us_keywords):
        blocs_present.append('US')
    if any(keyword in country_str for keyword in europe_keywords):
        blocs_present.append('Europe')
    if any(keyword in country_str for keyword in japan_keywords):
        blocs_present.append('Japan')
    if any(keyword in country_str for keyword in india_keywords):
        blocs_present.append('India')
    
    if len(blocs_present) == 0:
        return 'Other'
    elif len(blocs_present) == 1:
        return blocs_present[0]
    else:
        return 'Mixed'

df['supplier_bloc'] = df['suppliers_country'].apply(classify_bloc)
df['owner_bloc'] = df['owner_country'].apply(classify_bloc)

print("Bloc Classification Complete")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_hhi(series):
    """Calculate Herfindahl-Hirschman Index"""
    if len(series) == 0:
        return 0
    counts = series.value_counts(normalize=True)
    hhi = (counts ** 2).sum() * 10000
    return round(hhi, 2)

def parse_list_field(field_str):
    """Parse comma/semicolon separated fields"""
    if pd.isna(field_str):
        return []
    return [item.strip() for item in re.split(r'[,;]', str(field_str)) if item.strip()]

df['regions_list'] = df['regions'].apply(parse_list_field)
df['landing_countries_list'] = df['landing_countries'].apply(parse_list_field)

# ============================================================================
# MODULE 1: MAIN CABLES DATA
# ============================================================================

cables_data = {
    'version': '1.0',
    'updated': '2026-03-28',
    'total_cables': len(df),
    'cables': df.replace({np.nan: None}).to_dict('records')
}

# ============================================================================
# MODULE 2: SOVEREIGNTY & DEPENDENCY (REVISED)
# ============================================================================

print("\n" + "="*80)
print("PROCESSING: SOVEREIGNTY MODULE (BLOC-NEUTRAL)")
print("="*80)

# Create country-level dataset
country_cables = []
for idx, row in df.iterrows():
    for country in row['landing_countries_list']:
        if country:
            country_cables.append({
                'country': country,
                'supplier_bloc': row['supplier_bloc'],
                'owner_bloc': row['owner_bloc'],
                'chinese_supplier': row['chinese_supplier'],
                'chinese_owner': row['chinese_owner'],
                'suppliers_country': row['suppliers_country'],
                'owner_country': row['owner_country']
            })

country_df = pd.DataFrame(country_cables)

country_metrics = []

for country in country_df['country'].unique():
    country_data = country_df[country_df['country'] == country]
    total_cables = len(country_data)
    
    # SUPPLIER PERSPECTIVE
    supplier_counts = country_data['supplier_bloc'].value_counts()
    supplier_shares = supplier_counts / total_cables
    
    # Diversification (Shannon entropy)
    supplier_entropy = -sum(supplier_shares * np.log(supplier_shares.replace(0, 1)))
    max_entropy = np.log(len(supplier_counts)) if len(supplier_counts) > 1 else 1
    supplier_diversification = supplier_entropy / max_entropy if max_entropy > 0 else 0
    
    # Independence (BLOC-NEUTRAL: domestic suppliers)
    domestic_supplier_count = 0
    for _, cable in country_data.iterrows():
        supplier_country_str = str(cable.get('suppliers_country', ''))
        if country.lower() in supplier_country_str.lower():
            domestic_supplier_count += 1
    
    supplier_independence = domestic_supplier_count / total_cables if total_cables > 0 else 0
    
    # No dominance
    supplier_no_dominance = 1 - supplier_shares.max() if len(supplier_shares) > 0 else 0
    
    # Redundancy
    supplier_redundancy = min(len(supplier_counts) / 5, 1)
    
    # SOVEREIGNTY INDEX
    supplier_sovereignty = (
        0.40 * supplier_diversification +
        0.30 * supplier_independence +
        0.20 * supplier_no_dominance +
        0.10 * supplier_redundancy
    )
    
    # OWNER PERSPECTIVE (same logic)
    owner_counts = country_data['owner_bloc'].value_counts()
    owner_shares = owner_counts / total_cables
    
    owner_entropy = -sum(owner_shares * np.log(owner_shares.replace(0, 1)))
    max_entropy = np.log(len(owner_counts)) if len(owner_counts) > 1 else 1
    owner_diversification = owner_entropy / max_entropy if max_entropy > 0 else 0
    
    domestic_owner_count = 0
    for _, cable in country_data.iterrows():
        owner_country_str = str(cable.get('owner_country', ''))
        if country.lower() in owner_country_str.lower():
            domestic_owner_count += 1
    
    owner_independence = domestic_owner_count / total_cables if total_cables > 0 else 0
    
    owner_no_dominance = 1 - owner_shares.max() if len(owner_shares) > 0 else 0
    owner_redundancy = min(len(owner_counts) / 5, 1)
    
    owner_sovereignty = (
        0.40 * owner_diversification +
        0.30 * owner_independence +
        0.20 * owner_no_dominance +
        0.10 * owner_redundancy
    )
    
    # Bloc percentages - ALL blocs
    pct_chinese_supplier = (supplier_counts.get('China', 0) / total_cables * 100)
    pct_chinese_owner = (owner_counts.get('China', 0) / total_cables * 100)
    pct_us_supplier = (supplier_counts.get('US', 0) / total_cables * 100)
    pct_us_owner = (owner_counts.get('US', 0) / total_cables * 100)
    pct_eu_supplier = (supplier_counts.get('Europe', 0) / total_cables * 100)
    pct_eu_owner = (owner_counts.get('Europe', 0) / total_cables * 100)
    pct_japan_supplier = (supplier_counts.get('Japan', 0) / total_cables * 100)
    pct_japan_owner = (owner_counts.get('Japan', 0) / total_cables * 100)
    pct_india_supplier = (supplier_counts.get('India', 0) / total_cables * 100)
    pct_india_owner = (owner_counts.get('India', 0) / total_cables * 100)
    pct_mixed_supplier = (supplier_counts.get('Mixed', 0) / total_cables * 100)
    pct_mixed_owner = (owner_counts.get('Mixed', 0) / total_cables * 100)
    pct_other_supplier = (supplier_counts.get('Other', 0) / total_cables * 100)
    pct_other_owner = (owner_counts.get('Other', 0) / total_cables * 100)
    
    country_metrics.append({
        'country': country,
        'total_cables': total_cables,
        'supplier_sovereignty_index': round(supplier_sovereignty, 3),
        'owner_sovereignty_index': round(owner_sovereignty, 3),
        'supplier_diversification': round(supplier_diversification, 3),
        'owner_diversification': round(owner_diversification, 3),
        'supplier_independence': round(supplier_independence, 3),
        'owner_independence': round(owner_independence, 3),
        'pct_chinese_supplier': round(pct_chinese_supplier, 1),
        'pct_chinese_owner': round(pct_chinese_owner, 1),
        'pct_us_supplier': round(pct_us_supplier, 1),
        'pct_us_owner': round(pct_us_owner, 1),
        'pct_eu_supplier': round(pct_eu_supplier, 1),
        'pct_eu_owner': round(pct_eu_owner, 1),
        'pct_japan_supplier': round(pct_japan_supplier, 1),
        'pct_japan_owner': round(pct_japan_owner, 1),
        'pct_india_supplier': round(pct_india_supplier, 1),
        'pct_india_owner': round(pct_india_owner, 1),
        'pct_mixed_supplier': round(pct_mixed_supplier, 1),
        'pct_mixed_owner': round(pct_mixed_owner, 1),
        'pct_other_supplier': round(pct_other_supplier, 1),
        'pct_other_owner': round(pct_other_owner, 1),
        'pct_domestic_supplier': round(supplier_independence * 100, 1),
        'pct_domestic_owner': round(owner_independence * 100, 1)
    })

country_metrics_sorted = sorted(country_metrics, key=lambda x: x['owner_sovereignty_index'], reverse=True)

sovereignty_data = {
    'countries': country_metrics_sorted,
    'global_stats': {
        'supplier_perspective': {
            'avg_sovereignty_index': round(np.mean([c['supplier_sovereignty_index'] for c in country_metrics]), 3),
            'avg_diversification': round(np.mean([c['supplier_diversification'] for c in country_metrics]), 3),
            'avg_independence': round(np.mean([c['supplier_independence'] for c in country_metrics]), 3),
            'single_supplier_dependent': sum(c['supplier_diversification'] < 0.5 for c in country_metrics)
        },
        'owner_perspective': {
            'avg_sovereignty_index': round(np.mean([c['owner_sovereignty_index'] for c in country_metrics]), 3),
            'avg_diversification': round(np.mean([c['owner_diversification'] for c in country_metrics]), 3),
            'avg_independence': round(np.mean([c['owner_independence'] for c in country_metrics]), 3),
            'single_owner_dependent': sum(c['owner_diversification'] < 0.5 for c in country_metrics)
        }
    },
    'methodology_note': 'Independence = % domestic suppliers/owners (bloc-neutral). Updated 2026-03-28.'
}

print(f"✓ Sovereignty data ready")

# Show China's new scores
china = next((c for c in country_metrics if c['country'] == 'China'), None)
if china:
    print("\nCHINA (BLOC-NEUTRAL METHODOLOGY):")
    print(f"  Cables: {china['total_cables']}")
    print(f"  Owner sovereignty: {china['owner_sovereignty_index']} (was penalized before)")
    print(f"  Domestic owners: {china['pct_domestic_owner']}%")
    print(f"  Owner independence component: {china['owner_independence']}")

# ============================================================================
# EXPORT
# ============================================================================

output_path = Path('../dashboard/public/data')
output_path.mkdir(parents=True, exist_ok=True)

with open(output_path / 'sovereignty_dependency.json', 'w') as f:
    json.dump(sovereignty_data, f, indent=2, default=str)

print(f"\n✓ Exported sovereignty_dependency.json")
print("✓ Complete!")