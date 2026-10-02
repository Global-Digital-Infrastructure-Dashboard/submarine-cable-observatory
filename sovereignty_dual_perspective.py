"""
Enhanced Sovereignty Analysis - Supplier vs Owner Perspectives
BLOC-NEUTRAL METHODOLOGY: Independence now measures domestic vs foreign control

Usage:
  python sovereignty_dual_perspective.py          # preview old vs new sovereignty_countries (writes nothing)
  python sovereignty_dual_perspective.py --push   # sync Supabase sovereignty_countries + write local JSON
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path

from pipeline_common import (load_dataset, is_domestic, should_push, get_supabase, get_read_client,
                             fetch_all, sync_rows, print_key_diff)

print("="*80)
print("SOVEREIGNTY ANALYSIS: SUPPLIER VS OWNER PERSPECTIVES")
print("="*80)

# Load dataset with bloc classification applied
df = load_dataset()

print("\nBloc Classification Complete")

def calculate_hhi(series):
    if len(series) == 0:
        return 0
    counts = series.value_counts(normalize=True)
    hhi = (counts ** 2).sum() * 10000
    return round(hhi, 2)

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
    domestic_count = sum(is_domestic(country_name, c) for c in country_data[country_column])
    
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
    supplier_counts = country_data['supplier_bloc'].value_counts()
    owner_counts = country_data['owner_bloc'].value_counts()

    def pct(counts, bloc):
        return round((counts.get(bloc, 0) / total_cables) * 100, 1)
    
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
        'pct_us_supplier': pct(supplier_counts, 'US'),
        'pct_eu_supplier': pct(supplier_counts, 'Europe'),
        'pct_japan_supplier': pct(supplier_counts, 'Japan'),
        'pct_india_supplier': pct(supplier_counts, 'India'),
        'pct_mixed_supplier': pct(supplier_counts, 'Mixed'),
        'pct_other_supplier': pct(supplier_counts, 'Other'),
        
        # Owner perspective
        'owner_sovereignty_index': owner_metrics['sovereignty_index'],
        'owner_diversification': owner_metrics['diversification'],
        'owner_independence': owner_metrics['independence'],
        'owner_hhi': owner_metrics['hhi'],
        'owner_distinct_blocs': owner_metrics['distinct_blocs'],
        'pct_domestic_owner': owner_metrics['domestic_percentage'],
        'pct_chinese_owner': round((chinese_owner_count / total_cables) * 100, 1),
        'pct_us_owner': pct(owner_counts, 'US'),
        'pct_eu_owner': pct(owner_counts, 'Europe'),
        'pct_japan_owner': pct(owner_counts, 'Japan'),
        'pct_india_owner': pct(owner_counts, 'India'),
        'pct_mixed_owner': pct(owner_counts, 'Mixed'),
        'pct_other_owner': pct(owner_counts, 'Other'),
        
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

# ============================================================================
# SUPABASE
# ============================================================================

# Columns that exist on the sovereignty_countries table
SOVEREIGNTY_COLUMNS = [
    'country', 'total_cables',
    'supplier_sovereignty_index', 'owner_sovereignty_index',
    'supplier_diversification', 'owner_diversification',
    'pct_domestic_supplier', 'pct_domestic_owner',
    'pct_chinese_supplier', 'pct_chinese_owner',
    'pct_us_supplier', 'pct_us_owner',
    'pct_eu_supplier', 'pct_eu_owner',
    'pct_japan_supplier', 'pct_japan_owner',
    'pct_india_supplier', 'pct_india_owner',
    'pct_mixed_supplier', 'pct_mixed_owner',
    'pct_other_supplier', 'pct_other_owner',
]

rows = [{col: c[col] for col in SOVEREIGNTY_COLUMNS} for c in country_metrics_sorted]

if should_push():
    sync_rows(get_supabase(), 'sovereignty_countries', rows, key='country')

    output_path = Path('public/data')
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path / 'sovereignty_dependency.json', 'w') as f:
        json.dump(sovereignty_data, f, indent=2, default=str)
    print("✓ Exported public/data/sovereignty_dependency.json")
else:
    old = {r['country']: r for r in fetch_all(get_read_client(), 'sovereignty_countries')}
    new = {r['country']: r for r in rows}

    print("\n" + "="*80)
    print("PREVIEW: sovereignty_countries (old = live Supabase, new = this run)")
    print("="*80)
    print_key_diff('Countries', old, new)

    print(f"\nAverage across countries:")
    print(f"  {'column':24}{'old':>8}{'new':>8}")
    for col in SOVEREIGNTY_COLUMNS[2:]:
        o = np.mean([r[col] or 0 for r in old.values()]) if old else 0
        n = np.mean([r[col] for r in new.values()])
        print(f"  {col:24}{o:>8.2f}{n:>8.2f}")

    print(f"\nKey countries (old → new):")
    print(f"  {'country':22}{'cables':>12}{'domestic owner %':>20}{'owner sovereignty':>20}")
    for name in ['United States', 'United Kingdom', 'China', 'Japan', 'India', 'France', 'Singapore', 'Nigeria', 'Niger']:
        o, n = old.get(name), new.get(name)
        if not (o or n):
            continue
        f = lambda r, k: '—' if r is None else r[k]
        print(f"  {name:22}{f(o,'total_cables'):>5} → {f(n,'total_cables'):<5}"
              f"{f(o,'pct_domestic_owner'):>9} → {f(n,'pct_domestic_owner'):<9}"
              f"{f(o,'owner_sovereignty_index'):>9} → {f(n,'owner_sovereignty_index'):<9}")
    print("\n(preview only — nothing written. Pass --push to sync Supabase sovereignty_countries)")

print("\n✓ Complete!")
