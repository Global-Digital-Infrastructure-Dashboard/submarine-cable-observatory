"""
Comprehensive Data Processing for All Dashboard Modules
BLOC-NEUTRAL METHODOLOGY: Independence = domestic control, not anti-Chinese

Usage:
  python process_all_modules.py          # preview old vs new temporal_dynamics (writes nothing)
  python process_all_modules.py --push   # replace Supabase temporal_dynamics rows + write local JSON
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
from collections import defaultdict

from pipeline_common import (load_dataset, split_list_field, is_domestic, should_push, get_supabase,
                             get_read_client, fetch_all, replace_rows, print_count_diff)

print("="*80)
print("COMPREHENSIVE DATA PROCESSING - BLOC-NEUTRAL METHODOLOGY")
print("="*80)

# Load the dataset (bloc classification applied in pipeline_common.classify_bloc)
df = load_dataset()
print(f"\nLoaded {len(df)} cables")
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

df['regions_list'] = df['regions'].apply(split_list_field)

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
    domestic_supplier_count = sum(is_domestic(country, c) for c in country_data['suppliers_country'])
    
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
    
    domestic_owner_count = sum(is_domestic(country, c) for c in country_data['owner_country'])
    
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
# MODULE 3: TEMPORAL DYNAMICS
# ============================================================================

print("\n" + "="*80)
print("PROCESSING: TEMPORAL DYNAMICS")
print("="*80)

SUPPLIER_COLUMNS = {
    'China': 'china_count', 'US': 'us_count', 'Europe': 'europe_count',
    'Japan': 'japan_count', 'India': 'india_count', 'Mixed': 'mixed_count',
    'Other': 'other_count', 'Unknown': 'unknown_count',
}
OWNER_COLUMNS = {
    'China': 'owner_chinese_count', 'US': 'owner_us_count', 'Europe': 'owner_europe_count',
    'Japan': 'owner_japan_count', 'India': 'owner_india_count', 'Mixed': 'owner_mixed_count',
    'Other': 'owner_other_count', 'Unknown': 'owner_unknown_count',
}

temporal_rows = []
cumulative_total = 0
for year, year_df in df.dropna(subset=['rfs_year']).groupby(df['rfs_year'].astype('Int64')):
    supplier_counts = year_df['supplier_bloc'].value_counts()
    owner_counts = year_df['owner_bloc'].value_counts()
    cumulative_total += len(year_df)

    row = {'year': int(year), 'total_cables': len(year_df), 'cumulative_total': cumulative_total}
    row.update({col: int(supplier_counts.get(bloc, 0)) for bloc, col in SUPPLIER_COLUMNS.items()})
    row.update({col: int(owner_counts.get(bloc, 0)) for bloc, col in OWNER_COLUMNS.items()})
    # Kept for backward compatibility: Western = US + Europe + Japan
    row['western_count'] = row['us_count'] + row['europe_count'] + row['japan_count']
    row['owner_western_count'] = row['owner_us_count'] + row['owner_europe_count'] + row['owner_japan_count']
    # Any Chinese owner stake (chinese_owner flag), including cables classified Mixed
    row['owner_chinese_any_count'] = int(year_df['chinese_owner'].fillna(0).astype(int).gt(0).sum())
    temporal_rows.append(row)

temporal_data = {'years': temporal_rows}

print(f"✓ Temporal data ready: {len(temporal_rows)} years "
      f"({temporal_rows[0]['year']}–{temporal_rows[-1]['year']}), {cumulative_total} cables")

# ============================================================================
# EXPORT
# ============================================================================

TEMPORAL_COUNT_COLUMNS = list(SUPPLIER_COLUMNS.values()) + ['western_count'] + \
    list(OWNER_COLUMNS.values()) + ['owner_western_count', 'owner_chinese_any_count']

if should_push():
    replace_rows(get_supabase(), 'temporal_dynamics', temporal_rows)

    output_path = Path('public/data')
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path / 'sovereignty_dependency.json', 'w') as f:
        json.dump(sovereignty_data, f, indent=2, default=str)
    with open(output_path / 'temporal_dynamics.json', 'w') as f:
        json.dump(temporal_data, f, indent=2, default=str)
    print("✓ Exported public/data/sovereignty_dependency.json, temporal_dynamics.json")
else:
    old = fetch_all(get_read_client(), 'temporal_dynamics')

    print("\n" + "="*80)
    print("PREVIEW: temporal_dynamics (old = live Supabase, new = this run)")
    print("="*80)
    print(f"Rows: {len(old)} old → {len(temporal_rows)} new; "
          f"years {min(r['year'] for r in old)}–{max(r['year'] for r in old)} old → "
          f"{temporal_rows[0]['year']}–{temporal_rows[-1]['year']} new")
    print_count_diff('Cables summed over all years, per column:',
                     {'total_cables': sum(r['total_cables'] for r in old),
                      **{c: sum(r.get(c) or 0 for r in old) for c in TEMPORAL_COUNT_COLUMNS}},
                     {'total_cables': sum(r['total_cables'] for r in temporal_rows),
                      **{c: sum(r[c] for r in temporal_rows) for c in TEMPORAL_COUNT_COLUMNS}})

    missing = sorted(set(temporal_rows[0]) - set(old[0])) if old else []
    if missing:
        print(f"\n⚠ Columns not on the live table yet (the push will fail until they're added): {missing}")
    print("\n(preview only — nothing written. Pass --push to replace Supabase temporal_dynamics)")

print("✓ Complete!")
