"""Print everything needed to re-code one core-panel market in the expansion format (migration, Prof. Shen 2026-11):
the core panel's relevant fields per operator, its discovery row, the core vendor/ownership search answers
(data/5g_searches.jsonl) and the new migration searches (mig|share, mig|ran in data/5g_expansion_searches.jsonl).

  python3 5g_expansion/show_core.py Germany
"""
import json, re, sys
import pandas as pd

market = sys.argv[1]
FIELDS = ['ran_vendor', 'ran_vendor_tier', 'ran_vendor_source', 'core_vendor', 'core_vendor_source', 'core_vendor_4g_legacy',
          'core_vendor_4g_legacy_source', 'legacy_4g_carryover', 'legacy_4g_vendor', 'legacy_4g_carryover_source',
          'vendor_restriction_exists', 'restriction_instrument_type', 'restriction_scope', 'rip_and_replace_deadline',
          'rip_and_replace_deadline_source', 'market_vendor_shares', 'parent_company', 'notes', 'source_urls']
panel = pd.read_csv('data/5g_operator_panel.csv')
ops = pd.read_csv('data/5g_operators.csv')
stakes = pd.read_csv('data/5g_operator_gov_stakes.csv')
rows = panel[panel.market == market]


def answers(path, keep):
    latest = {}  # the core cache repeats some keys (re-searched ownership); show only the last answer per key
    for e in map(json.loads, open(path)):
        if keep(e['key']):
            latest[e['key']] = e
    for e in latest.values():
        if True:
            a = re.sub(r'\n{2,}', '\n', e['search']['answer'])
            urls = ' '.join(f"[{i + 1}]{r.get('url')}" for i, r in enumerate(e['search']['results']))
            yield e['key'], a, urls


for k, a, urls in answers('data/5g_expansion_searches.jsonl', lambda k: k == f'mig|mktshare|{market}'):
    print(f'======== {k} (market-level shares)\n{a}\nURLS: {urls}')

for r in rows.itertuples():
    oid = r.operator_id
    print(f'\n################ {oid} ({r.operator_name})')
    for f in FIELDS:
        print(f'{f}: {getattr(r, f)}')
    d = ops[ops.operator_id == oid]
    if len(d):
        d = d.iloc[0]
        print(f"discovery: five_g_status={d.five_g_status}; five_g_launch_date={d.five_g_launch_date}; sources={d.source_urls}")
    s = stakes[stakes.operator_id == oid]
    print('gov stakes (gov_stakes_core.py):', '; '.join(f"{x.holder} {x.pct}% of {x.pct_of} ({x.basis}, {x.state_link_basis})" for x in s.itertuples()) or 'none')
    for path, keep in (('data/5g_searches.jsonl', lambda k: k.split('|')[0] in ('vendor', 'ownership') and k.split('|')[1] == oid),
                       ('data/5g_expansion_searches.jsonl', lambda k: k.startswith('mig|') and k.split('|')[2] == oid)):
        for k, a, urls in answers(path, keep):
            print(f'\n======== {k}\n{a}\nURLS: {urls}')
