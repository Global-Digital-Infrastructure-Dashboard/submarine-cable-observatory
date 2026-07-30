"""
Enhanced Sovereignty Analysis - Supplier vs Owner Perspectives
BLOC-NEUTRAL METHODOLOGY: Independence now measures domestic vs foreign control
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

print("="*80)
print("SOVEREIGNTY ANALYSIS: SUPPLIER VS OWNER PERSPECTIVES")
print("="*80)

# Load processed data
df = pd.read_excel('data/global_submarine_dataset V1_2026.xlsx')

# Apply bloc classification
def classify_bloc(country_str):
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

print("\nBloc Classification Complete")

def calculate_hhi(series):
    if len(series) == 0:
        return 0
    counts = series.value_counts(normalize=True)
    hhi = (counts ** 2).sum() * 10000
    return round(hhi, 2)

def parse_list_field(field_str):
    if pd.isna(field_str):
        return []
    import re
    return [item.strip() for item in re.split(r'[,;]', str(field_str)) if item.strip()]

df['landing_countries_list'] = df['landing_countries'].apply(parse_list_field)

# Create country-level dataset
country_cables = []
for idx, row in df.iterrows():
    for country in row['landing_countries_list']:
        if country:
            country_cables.append({
                'country': country,
                'cable_name': row['cable_name'],
                'supplier_bloc': row['supplier_bloc'],
                'owner_bloc': row['owner_bloc'],
                'chinese_supplier': row['chinese_supplier'],
                'chinese_owner': row['chinese_owner'],
                'suppliers_country': row['suppliers_country'],
                'owner_country': row['owner_country'],
                'rfs_year': row['rfs_year']
            })

country_df = pd.DataFrame(country_cables)

print(f"\nAnalyzing {len(country_df['country'].unique())} countries...")

# ============================================================================
# FUNCTION: Calculate Sovereignty Index (BLOC-NEUTRAL)
# ============================================================================

def calculate_sovereignty_index(country_data, bloc_column, country_column, country_name):
    """
    Calculate sovereignty index with BLOC-NEUTRAL independence measure
    
    Independence now = % domestic suppliers/owners (not anti-Chinese)
    """
    total_cables = len(country_data)
    
    # 1. Diversification (40%) - Shannon entropy
    bloc_counts = country_data[bloc_column].value_counts()
    bloc_shares = bloc_counts / total_cables
    
    # Calculate entropy
    entropy = -sum(bloc_shares * np.log(bloc_shares.replace(0, 1)))
    max_entropy = np.log(len(bloc_counts)) if len(bloc_counts) > 1 else 1
    diversification = entropy / max_entropy if max_entropy > 0 else 0
    
    # 2. Independence (30%) - BLOC-NEUTRAL: % domestic suppliers/owners
    domestic_count = 0
    for _, cable in country_data.iterrows():
        country_str = str(cable.get(country_column, ''))
        if country_name.lower() in country_str.lower():
            domestic_count += 1
    
    independence = domestic_count / total_cables if total_cables > 0 else 0
    
    # 3. No single-bloc dominance (20%)
    max_bloc_share = bloc_shares.max()
    no_dominance = 1 - max_bloc_share if max_bloc_share < 1 else 0
    
    # 4. Route redundancy (10%)
    distinct_blocs = len(bloc_counts)
    redundancy = min(distinct_blocs / 5, 1)
    
    # Weighted combination
    sovereignty_index = (
        diversification * 0.4 +
        independence * 0.3 +
        no_dominance * 0.2 +
        redundancy * 0.1
    )
    
    return {
        'diversification': round(diversification, 3),
        'independence': round(independence, 3),
        'no_dominance': round(no_dominance, 3),
        'redundancy': round(redundancy, 3),
        'sovereignty_index': round(sovereignty_index, 3),
        'hhi': round(calculate_hhi(country_data[bloc_column]), 2),
        'distinct_blocs': distinct_blocs,
        'domestic_percentage': round(independence * 100, 1)
    }

# ============================================================================
# COMPUTE BOTH PERSPECTIVES
# ============================================================================

country_metrics = []

for country in country_df['country'].unique():
    country_data = country_df[country_df['country'] == country]
    total_cables = len(country_data)
    
    # Calculate supplier-based metrics
    supplier_metrics = calculate_sovereignty_index(
        country_data, 
        'supplier_bloc',
        'suppliers_country',
        country
    )
    
    # Calculate owner-based metrics
    owner_metrics = calculate_sovereignty_index(
        country_data,
        'owner_bloc',
        'owner_country',
        country
    )
    
    # Count by bloc (for additional analysis)
    chinese_supplier_count = country_data['chinese_supplier'].sum()
    chinese_owner_count = country_data['chinese_owner'].sum()
    us_supplier_count = len(country_data[country_data['supplier_bloc'] == 'US'])
    us_owner_count = len(country_data[country_data['owner_bloc'] == 'US'])
    eu_supplier_count = len(country_data[country_data['supplier_bloc'] == 'Europe'])
    eu_owner_count = len(country_data[country_data['owner_bloc'] == 'Europe'])
    
    country_metrics.append({
        'country': country,
        'total_cables': total_cables,
        
        # Supplier perspective
        'supplier_sovereignty_index': supplier_metrics['sovereignty_index'],
        'supplier_diversification': supplier_metrics['diversification'],
        'supplier_independence': supplier_metrics['independence'],
        'supplier_hhi': supplier_metrics['hhi'],
        'supplier_distinct_blocs': supplier_metrics['distinct_blocs'],
        'pct_domestic_supplier': supplier_metrics['domestic_percentage'],
        'pct_chinese_supplier': round((chinese_supplier_count / total_cables) * 100, 1),
        'pct_us_supplier': round((us_supplier_count / total_cables) * 100, 1),
        'pct_eu_supplier': round((eu_supplier_count / total_cables) * 100, 1),
        
        # Owner perspective
        'owner_sovereignty_index': owner_metrics['sovereignty_index'],
        'owner_diversification': owner_metrics['diversification'],
        'owner_independence': owner_metrics['independence'],
        'owner_hhi': owner_metrics['hhi'],
        'owner_distinct_blocs': owner_metrics['distinct_blocs'],
        'pct_domestic_owner': owner_metrics['domestic_percentage'],
        'pct_chinese_owner': round((chinese_owner_count / total_cables) * 100, 1),
        'pct_us_owner': round((us_owner_count / total_cables) * 100, 1),
        'pct_eu_owner': round((eu_owner_count / total_cables) * 100, 1),
        
        # Dominance flags
        'single_supplier_dominance': supplier_metrics['no_dominance'] == 0,
        'single_owner_dominance': owner_metrics['no_dominance'] == 0,
    })

# Sort by total cables
country_metrics_sorted = sorted(country_metrics, key=lambda x: x['total_cables'], reverse=True)

print(f"\n✓ Calculated sovereignty for {len(country_metrics)} countries")

# Global statistics
sovereignty_data = {
    'countries': country_metrics_sorted,
    'global_stats': {
        'total_countries': len(country_metrics),
        'supplier_perspective': {
            'avg_sovereignty_index': round(np.mean([c['supplier_sovereignty_index'] for c in country_metrics]), 3),
            'avg_diversification': round(np.mean([c['supplier_diversification'] for c in country_metrics]), 3),
            'avg_independence': round(np.mean([c['supplier_independence'] for c in country_metrics]), 3),
            'single_supplier_dependent': sum(1 for c in country_metrics if c['single_supplier_dominance'])
        },
        'owner_perspective': {
            'avg_sovereignty_index': round(np.mean([c['owner_sovereignty_index'] for c in country_metrics]), 3),
            'avg_diversification': round(np.mean([c['owner_diversification'] for c in country_metrics]), 3),
            'avg_independence': round(np.mean([c['owner_independence'] for c in country_metrics]), 3),
            'single_owner_dependent': sum(1 for c in country_metrics if c['single_owner_dominance'])
        }
    },
    'methodology_note': 'Independence component measures domestic vs foreign control (bloc-neutral), not specifically Chinese independence. Updated 2026-03-28.'
}

# Export
output_path = Path('../dashboard/public/data')
output_path.mkdir(parents=True, exist_ok=True)

with open(output_path / 'sovereignty_dependency.json', 'w') as f:
    json.dump(sovereignty_data, f, indent=2, default=str)

print(f"✓ Exported sovereignty_dependency.json")

# Show China's data specifically
china_data = next((c for c in country_metrics if c['country'] == 'China'), None)
if china_data:
    print("\n" + "="*80)
    print("CHINA'S SOVEREIGNTY SCORES (BLOC-NEUTRAL METHODOLOGY)")
    print("="*80)
    print(f"Total cables: {china_data['total_cables']}")
    print(f"Supplier sovereignty: {china_data['supplier_sovereignty_index']}")
    print(f"Owner sovereignty: {china_data['owner_sovereignty_index']}")
    print(f"Domestic suppliers: {china_data['pct_domestic_supplier']}%")
    print(f"Domestic owners: {china_data['pct_domestic_owner']}%")
    print(f"Chinese suppliers: {china_data['pct_chinese_supplier']}%")
    print(f"Chinese owners: {china_data['pct_chinese_owner']}%")

print("\n" + "="*80)
print("COMPARISON: SUPPLIER VS OWNER SOVEREIGNTY")
print("="*80)

print(f"\nSupplier Perspective:")
print(f"  Avg Sovereignty: {sovereignty_data['global_stats']['supplier_perspective']['avg_sovereignty_index']}")
print(f"  Avg Independence (domestic control): {sovereignty_data['global_stats']['supplier_perspective']['avg_independence']}")

print(f"\nOwner Perspective:")
print(f"  Avg Sovereignty: {sovereignty_data['global_stats']['owner_perspective']['avg_sovereignty_index']}")
print(f"  Avg Independence (domestic control): {sovereignty_data['global_stats']['owner_perspective']['avg_independence']}")

print("\n✓ Complete!")