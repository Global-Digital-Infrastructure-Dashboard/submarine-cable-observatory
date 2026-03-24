"""
Enhanced Sovereignty Analysis - Supplier vs Owner Perspectives
Generates both supplier-based and owner-based sovereignty indices
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

print("="*80)
print("SOVEREIGNTY ANALYSIS: SUPPLIER VS OWNER PERSPECTIVES")
print("="*80)

# Load processed data
df = pd.read_excel('data/global_submarine_dataset_V1_2026.xlsx')

# Apply bloc classification (reuse from main script)
def classify_bloc(country_str):
    if pd.isna(country_str) or country_str == '':
        return 'Unknown'
    country_str = str(country_str).lower()
    
    china_keywords = ['china', 'chinese', 'prc']
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
                'rfs_year': row['rfs_year']
            })

country_df = pd.DataFrame(country_cables)

print(f"\nAnalyzing {len(country_df['country'].unique())} countries...")

# ============================================================================
# FUNCTION: Calculate Sovereignty Index (Generic)
# ============================================================================

def calculate_sovereignty_index(country_data, bloc_column, chinese_column):
    """
    Calculate sovereignty index based on either supplier or owner blocs
    
    Parameters:
    - country_data: DataFrame of cables for a specific country
    - bloc_column: 'supplier_bloc' or 'owner_bloc'
    - chinese_column: 'chinese_supplier' or 'chinese_owner'
    """
    total_cables = len(country_data)
    chinese_count = country_data[chinese_column].sum()
    
    # 1. Diversification (40%)
    bloc_hhi = calculate_hhi(country_data[bloc_column])
    diversification = 1 - (bloc_hhi / 10000)
    
    # 2. Independence from Chinese blocs (30%)
    independence = 1 - (chinese_count / total_cables)
    
    # 3. No single-bloc dominance (20%)
    bloc_counts = country_data[bloc_column].value_counts()
    max_bloc_share = bloc_counts.max() / total_cables if len(bloc_counts) > 0 else 0
    no_dominance = 0 if max_bloc_share > 0.5 else 1
    
    # 4. Route redundancy (10%)
    distinct_blocs = country_data[bloc_column].nunique()
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
        'no_dominance': no_dominance,
        'redundancy': round(redundancy, 3),
        'sovereignty_index': round(sovereignty_index, 3),
        'hhi': round(bloc_hhi, 2),
        'distinct_blocs': distinct_blocs,
        'max_bloc_share': round(max_bloc_share, 3)
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
        'chinese_supplier'
    )
    
    # Calculate owner-based metrics
    owner_metrics = calculate_sovereignty_index(
        country_data, 
        'owner_bloc', 
        'chinese_owner'
    )
    
    # Count by bloc
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
        'supplier_hhi': supplier_metrics['hhi'],
        'supplier_distinct_blocs': supplier_metrics['distinct_blocs'],
        'pct_chinese_supplier': round((chinese_supplier_count / total_cables) * 100, 2),
        'pct_us_supplier': round((us_supplier_count / total_cables) * 100, 2),
        'pct_eu_supplier': round((eu_supplier_count / total_cables) * 100, 2),
        
        # Owner perspective
        'owner_sovereignty_index': owner_metrics['sovereignty_index'],
        'owner_diversification': owner_metrics['diversification'],
        'owner_hhi': owner_metrics['hhi'],
        'owner_distinct_blocs': owner_metrics['distinct_blocs'],
        'pct_chinese_owner': round((chinese_owner_count / total_cables) * 100, 2),
        'pct_us_owner': round((us_owner_count / total_cables) * 100, 2),
        'pct_eu_owner': round((eu_owner_count / total_cables) * 100, 2),
        
        # Combined metrics
        'single_supplier_dominance': supplier_metrics['no_dominance'] == 0,
        'single_owner_dominance': owner_metrics['no_dominance'] == 0,
    })

# Sort by supplier sovereignty (default)
country_metrics_sorted = sorted(country_metrics, key=lambda x: x['supplier_sovereignty_index'], reverse=True)

print(f"\n✓ Calculated dual sovereignty indices for {len(country_metrics)} countries")

# Global statistics
sovereignty_data = {
    'countries': country_metrics_sorted,
    'global_stats': {
        'total_countries': len(country_metrics),
        'supplier_perspective': {
            'avg_sovereignty_index': round(np.mean([c['supplier_sovereignty_index'] for c in country_metrics]), 3),
            'avg_diversification': round(np.mean([c['supplier_diversification'] for c in country_metrics]), 3),
            'single_supplier_dependent': sum(1 for c in country_metrics if c['single_supplier_dominance'])
        },
        'owner_perspective': {
            'avg_sovereignty_index': round(np.mean([c['owner_sovereignty_index'] for c in country_metrics]), 3),
            'avg_diversification': round(np.mean([c['owner_diversification'] for c in country_metrics]), 3),
            'single_owner_dependent': sum(1 for c in country_metrics if c['single_owner_dominance'])
        }
    }
}

# Export
output_path = Path('../dashboard/public/data')
output_path.mkdir(parents=True, exist_ok=True)

with open(output_path / 'sovereignty_dependency.json', 'w') as f:
    json.dump(sovereignty_data, f, indent=2, default=str)

print(f"✓ Exported sovereignty_dependency.json with dual perspectives")

print("\n" + "="*80)
print("COMPARISON: SUPPLIER VS OWNER SOVEREIGNTY")
print("="*80)

print(f"\nSupplier Perspective:")
print(f"  Avg Sovereignty Index: {sovereignty_data['global_stats']['supplier_perspective']['avg_sovereignty_index']}")
print(f"  Avg Diversification: {sovereignty_data['global_stats']['supplier_perspective']['avg_diversification']}")
print(f"  Single-supplier dependent: {sovereignty_data['global_stats']['supplier_perspective']['single_supplier_dependent']} countries")

print(f"\nOwner Perspective:")
print(f"  Avg Sovereignty Index: {sovereignty_data['global_stats']['owner_perspective']['avg_sovereignty_index']}")
print(f"  Avg Diversification: {sovereignty_data['global_stats']['owner_perspective']['avg_diversification']}")
print(f"  Single-owner dependent: {sovereignty_data['global_stats']['owner_perspective']['single_owner_dependent']} countries")

print("\n✓ Complete!")