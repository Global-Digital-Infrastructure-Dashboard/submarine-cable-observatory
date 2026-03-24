"""
Comprehensive Data Processing for All Dashboard Modules
Generates JSON files for: Market Structure, Geographic, Sovereignty, Temporal, Policy
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from collections import defaultdict
import re

print("="*80)
print("COMPREHENSIVE SUBMARINE CABLE DATA PROCESSING")
print("="*80)

# Load the dataset
df = pd.read_excel('data/global_submarine_dataset_V1_2026.xlsx')
print(f"\nLoaded {len(df)} cables")

# ============================================================================
# BLOC CLASSIFICATION
# ============================================================================

def classify_bloc(country_str):
    """Classify countries into geopolitical blocs"""
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

print("\nBloc Classification Complete")
print(f"Supplier blocs: {df['supplier_bloc'].value_counts().to_dict()}")

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
    """Parse comma/semicolon separated fields into lists"""
    if pd.isna(field_str):
        return []
    return [item.strip() for item in re.split(r'[,;]', str(field_str)) if item.strip()]

# Parse regions and countries
df['regions_list'] = df['regions'].apply(parse_list_field)
df['landing_countries_list'] = df['landing_countries'].apply(parse_list_field)

# ============================================================================
# MODULE 1: MAIN CABLES DATA (for all modules)
# ============================================================================

cables_data = {
    'version': '1.0',
    'updated': '2026-02-26',
    'total_cables': len(df),
    'cables': df.replace({np.nan: None}).to_dict('records')
}

# ============================================================================
# MODULE 2: MARKET STRUCTURE DATA
# ============================================================================

print("\n" + "="*80)
print("PROCESSING: MARKET STRUCTURE MODULE")
print("="*80)

# A. Supplier Competition
supplier_share = df['supplier_bloc'].value_counts().to_dict()
owner_share = df['owner_bloc'].value_counts().to_dict()

# Market share over time
df_with_year = df[df['rfs_year'].notna()].copy()

market_share_over_time = []
for year in range(int(df_with_year['rfs_year'].min()), int(df_with_year['rfs_year'].max()) + 1):
    year_data = df_with_year[df_with_year['rfs_year'] == year]
    if len(year_data) > 0:
        year_blocs = year_data['supplier_bloc'].value_counts().to_dict()
        market_share_over_time.append({
            'year': year,
            'blocs': year_blocs,
            'total': len(year_data)
        })

# HHI over time
hhi_over_time = []
for year in range(1990, 2029):
    year_data = df_with_year[df_with_year['rfs_year'] == year]
    if len(year_data) > 0:
        hhi = calculate_hhi(year_data['supplier_bloc'])
        hhi_over_time.append({
            'year': year,
            'supplier_hhi': hhi,
            'count': len(year_data)
        })

# Entry timing
entry_timing = df_with_year.groupby('supplier_bloc')['rfs_year'].min().to_dict()

# B. Ownership Structure
# State-owned vs private (we'll need to code this manually or from external data)
# For now, create placeholder structure

# C. Supplier-Owner Divergence
divergence_matrix = {
    'chinese_supplier_western_owner': 0,
    'western_supplier_chinese_owner': 0,
    'fully_chinese': 0,
    'fully_western': 0
}

for _, cable in df.iterrows():
    supplier = cable['supplier_bloc']
    owner = cable['owner_bloc']
    
    if supplier == 'China' and owner in ['US', 'Europe']:
        divergence_matrix['chinese_supplier_western_owner'] += 1
    elif supplier in ['US', 'Europe'] and owner == 'China':
        divergence_matrix['western_supplier_chinese_owner'] += 1
    elif supplier == 'China' and owner == 'China':
        divergence_matrix['fully_chinese'] += 1
    elif supplier in ['US', 'Europe'] and owner in ['US', 'Europe']:
        divergence_matrix['fully_western'] += 1

market_structure_data = {
    'supplier_competition': {
        'market_share': supplier_share,
        'market_share_over_time': market_share_over_time,
        'hhi_over_time': hhi_over_time,
        'entry_timing': entry_timing
    },
    'ownership_structure': {
        'market_share': owner_share,
        'global_hhi': calculate_hhi(df['owner_bloc'])
    },
    'supplier_owner_divergence': divergence_matrix
}

print(f"✓ Market share trends: {len(market_share_over_time)} years")
print(f"✓ HHI time series: {len(hhi_over_time)} data points")
print(f"✓ Entry timing: {len(entry_timing)} blocs")

# ============================================================================
# MODULE 3: GEOGRAPHIC DISTRIBUTION DATA
# ============================================================================

print("\n" + "="*80)
print("PROCESSING: GEOGRAPHIC DISTRIBUTION MODULE")
print("="*80)

# Regional clustering
regional_data = {}
for region in ['Asia-Pacific', 'Europe', 'Americas', 'Africa', 'Middle East']:
    # Find cables with this region
    region_cables = df[df['regions_list'].apply(lambda x: region in x if isinstance(x, list) else False)]
    
    if len(region_cables) > 0:
        regional_data[region] = {
            'total_cables': len(region_cables),
            'supplier_distribution': region_cables['supplier_bloc'].value_counts().to_dict(),
            'pct_chinese_supplier': (region_cables['chinese_supplier'].sum() / len(region_cables) * 100),
            'pct_us_supplier': (region_cables[region_cables['supplier_bloc'] == 'US'].shape[0] / len(region_cables) * 100),
            'supplier_hhi': calculate_hhi(region_cables['supplier_bloc'])
        }

geographic_data = {
    'regional_clustering': regional_data,
    'total_regions': len(regional_data)
}

print(f"✓ Regional analysis: {len(regional_data)} regions")

# ============================================================================
# MODULE 4: SOVEREIGNTY & DEPENDENCY DATA
# ============================================================================

print("\n" + "="*80)
print("PROCESSING: SOVEREIGNTY & DEPENDENCY MODULE")
print("="*80)

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

# Compute country-level metrics
country_metrics = []
for country in country_df['country'].unique():
    country_data = country_df[country_df['country'] == country]
    
    total_cables = len(country_data)
    chinese_supplier_count = country_data['chinese_supplier'].sum()
    us_supplier_count = len(country_data[country_data['supplier_bloc'] == 'US'])
    eu_supplier_count = len(country_data[country_data['supplier_bloc'] == 'Europe'])
    
    # Supplier diversification
    supplier_hhi = calculate_hhi(country_data['supplier_bloc'])
    diversification = 1 - (supplier_hhi / 10000)
    
    # Single supplier dominance
    supplier_counts = country_data['supplier_bloc'].value_counts()
    max_supplier_share = supplier_counts.max() / total_cables if len(supplier_counts) > 0 else 0
    single_supplier_dominance = 1 if max_supplier_share > 0.5 else 0
    
    # Route redundancy (number of distinct suppliers)
    distinct_suppliers = country_data['supplier_bloc'].nunique()
    
    # Calculate sovereignty index (simplified)
    # Formula: weighted combination of diversification, foreign ownership, bloc dominance, redundancy
    sovereignty_index = (
        diversification * 0.4 +  # Supplier diversification
        (1 - (chinese_supplier_count / total_cables)) * 0.3 +  # Low Chinese dependence
        (1 - single_supplier_dominance) * 0.2 +  # No single supplier dominance
        (min(distinct_suppliers / 5, 1)) * 0.1  # Route redundancy (normalized to max 5)
    )
    
    country_metrics.append({
        'country': country,
        'total_cables': total_cables,
        'pct_chinese_supplier': round((chinese_supplier_count / total_cables) * 100, 2),
        'pct_us_supplier': round((us_supplier_count / total_cables) * 100, 2),
        'pct_eu_supplier': round((eu_supplier_count / total_cables) * 100, 2),
        'supplier_diversification': round(diversification, 3),
        'single_supplier_dominance': single_supplier_dominance,
        'distinct_suppliers': distinct_suppliers,
        'sovereignty_index': round(sovereignty_index, 3),
        'supplier_hhi': round(supplier_hhi, 2)
    })

# Sort by total cables
country_metrics_sorted = sorted(country_metrics, key=lambda x: x['total_cables'], reverse=True)

sovereignty_data = {
    'countries': country_metrics_sorted,
    'global_stats': {
        'total_countries': len(country_metrics),
        'avg_sovereignty_index': round(np.mean([c['sovereignty_index'] for c in country_metrics]), 3),
        'avg_diversification': round(np.mean([c['supplier_diversification'] for c in country_metrics]), 3)
    }
}

print(f"✓ Country-level metrics: {len(country_metrics)} countries")

# ============================================================================
# MODULE 5: TEMPORAL DYNAMICS DATA
# ============================================================================

print("\n" + "="*80)
print("PROCESSING: TEMPORAL DYNAMICS MODULE")
print("="*80)

# Cables per year by bloc
cables_per_year = []
for year in range(int(df_with_year['rfs_year'].min()), int(df_with_year['rfs_year'].max()) + 1):
    year_data = df_with_year[df_with_year['rfs_year'] == year]
    
    bloc_counts = {}
    for bloc in ['China', 'US', 'Europe', 'Japan', 'India', 'Other', 'Mixed', 'Unknown']:
        bloc_counts[bloc] = len(year_data[year_data['supplier_bloc'] == bloc])
    
    cables_per_year.append({
        'year': year,
        **bloc_counts,
        'total': len(year_data)
    })

# Pre-2013 vs Post-2013 comparison
pre_2013 = df_with_year[df_with_year['rfs_year'] < 2013]
post_2013 = df_with_year[df_with_year['rfs_year'] >= 2013]

comparison_2013 = {
    'pre_2013': {
        'total': len(pre_2013),
        'blocs': pre_2013['supplier_bloc'].value_counts().to_dict(),
        'avg_per_year': len(pre_2013) / (2013 - pre_2013['rfs_year'].min())
    },
    'post_2013': {
        'total': len(post_2013),
        'blocs': post_2013['supplier_bloc'].value_counts().to_dict(),
        'avg_per_year': len(post_2013) / (post_2013['rfs_year'].max() - 2013 + 1)
    }
}

# Post-2020 analysis
post_2020 = df_with_year[df_with_year['rfs_year'] >= 2020]
comparison_2020 = {
    'total': len(post_2020),
    'blocs': post_2020['supplier_bloc'].value_counts().to_dict(),
    'chinese_share': len(post_2020[post_2020['supplier_bloc'] == 'China']) / len(post_2020) * 100
}

# Status breakdown
status_breakdown = df['status'].value_counts().to_dict()

temporal_data = {
    'cables_per_year': cables_per_year,
    'comparison_2013': comparison_2013,
    'comparison_2020': comparison_2020,
    'status_breakdown': status_breakdown,
    'year_range': {
        'min': int(df_with_year['rfs_year'].min()),
        'max': int(df_with_year['rfs_year'].max())
    }
}

print(f"✓ Temporal data: {len(cables_per_year)} years")
print(f"✓ Pre-2013: {len(pre_2013)} cables, Post-2013: {len(post_2013)} cables")

# ============================================================================
# MODULE 6: POLICY & REGULATION DATA
# ============================================================================

print("\n" + "="*80)
print("PROCESSING: POLICY & REGULATION MODULE")
print("="*80)

# Extract policy events from regulation_notes
policy_events = []
for idx, row in df.iterrows():
    if pd.notna(row['regulation_notes']):
        policy_events.append({
            'cable_name': row['cable_name'],
            'year': row['rfs_year'],
            'note': row['regulation_notes'],
            'supplier_bloc': row['supplier_bloc'],
            'owner_bloc': row['owner_bloc']
        })

policy_data = {
    'events': policy_events,
    'total_events': len(policy_events),
    'cables_with_notes': len(df[df['regulation_notes'].notna()])
}

print(f"✓ Policy events: {len(policy_events)} regulatory notes")

# ============================================================================
# EXPORT ALL DATA
# ============================================================================

print("\n" + "="*80)
print("EXPORTING DATA FILES")
print("="*80)

output_path = Path('../dashboard/public/data')
output_path.mkdir(parents=True, exist_ok=True)

# Export each module's data
files_to_export = {
    'cables_data.json': cables_data,
    'market_structure.json': market_structure_data,
    'geographic_distribution.json': geographic_data,
    'sovereignty_dependency.json': sovereignty_data,
    'temporal_dynamics.json': temporal_data,
    'policy_regulation.json': policy_data
}

for filename, data in files_to_export.items():
    filepath = output_path / filename
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"✓ Exported {filename}")

# Also create metadata
metadata = {
    'version': '1.0',
    'updated': '2026-02-26',
    'infrastructure_type': 'submarine_cables',
    'total_cables': len(df),
    'year_range': {
        'min': int(df_with_year['rfs_year'].min()),
        'max': int(df_with_year['rfs_year'].max())
    },
    'blocs': list(df['supplier_bloc'].unique()),
    'files': list(files_to_export.keys())
}

with open(output_path / 'metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"✓ Exported metadata.json")

print("\n" + "="*80)
print("PROCESSING COMPLETE!")
print("="*80)
print(f"\nGenerated {len(files_to_export)} data files for all dashboard modules")
print(f"Location: {output_path}")