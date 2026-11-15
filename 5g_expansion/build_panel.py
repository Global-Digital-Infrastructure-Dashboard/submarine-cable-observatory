"""Validate the in-session coding and write the expansion-panel CSVs.

  data/5g_expansion_panel.csv      one row per operator (scalar fields: value/status/source/note)
  data/5g_expansion_ran_vendors.csv one row per operator x generation x vendor
  data/5g_expansion_gov_stakes.csv  one row per government holder (never summed)

Provenance check: every source_url must appear in the cached search evidence (answers or result lists in
data/5g_expansion_searches.jsonl, or data/5g_searches.jsonl for reused core-panel facts), or be NBIM's
holdings file, which was downloaded and read directly.

Spot-check: random.Random(SEED).sample over the non-European operators, ~1 in 10.
Run from the repo root: python3 5g_expansion/build_panel.py
"""
import csv, json, math, os, random, sys
sys.path.insert(0, os.path.join(os.getcwd(), '5g_expansion'))
from coded_batch1 import NBIM, OPERATORS

SEED = 20261115
SOURCE_TYPES = {'company_report', 'regulator', 'news_article'}
CODED_AT = '2026-11-15'


def evidence_text():
    text = []
    for path in ('data/5g_expansion_searches.jsonl', 'data/5g_searches.jsonl'):
        for line in open(path):
            s = json.loads(line)['search']
            text.append(s['answer'])
            text.extend(str(r.get('url')) for r in s['results'])
    return '\n'.join(text)


def check(url, evidence, where, problems):
    if url and url != NBIM and url not in evidence:
        problems.append(f'{where}: URL not in cached evidence: {url}')


def main():
    evidence, problems = evidence_text(), []
    panel, ran, gov = [], [], []
    for op in OPERATORS:
        oid = f"{op['country']}|{op['operator_name']}"
        row = dict(operator_id=oid, region=op['region'], country=op['country'], operator_name=op['operator_name'])
        for field in ('share', 'launch', 'core', 'first_contract', 'vendor_operates'):
            f = op[field]
            if f['status'] == 'value':
                if f['source_type'] not in SOURCE_TYPES or not f['source_url']:
                    problems.append(f'{oid} {field}: value without a valid source')
                check(f['source_url'], evidence, f'{oid} {field}', problems)
            name = {'share': 'mobile_customer_share_pct', 'launch': 'fiveg_launch_year', 'core': '5g_core_vendor',
                    'first_contract': 'first_5g_contract_date', 'vendor_operates': 'vendor_also_operates_network'}[field]
            row[name] = f['value'] if f['status'] == 'value' else ''
            row[f'{name}_status'] = f['status']
            if field == 'share':
                row['mobile_customer_share_year'] = f['year'] or ''
            row[f'{name}_source_url'] = f['source_url']
            row[f'{name}_source_type'] = f['source_type']
            row[f'{name}_note'] = f['note']
        for gen in ('ran5', 'ran4'):
            label = '5G' if gen == 'ran5' else '4G'
            row[f'{label.lower()}_ran_vendors'] = '; '.join(f"{r['vendor']} ({r['share_category']})" for r in op[gen]) or ''
            row[f'{label.lower()}_ran_status'] = 'value' if op[gen] else 'not_disclosed'
            row[f'{label.lower()}_ran_note'] = op.get(f'{gen}_note', '')
            for r in op[gen]:
                if r['source_type'] not in SOURCE_TYPES:
                    problems.append(f'{oid} {gen} {r["vendor"]}: bad source_type')
                check(r['source_url'], evidence, f'{oid} {gen} {r["vendor"]}', problems)
                ran.append(dict(operator_id=oid, country=op['country'], operator_name=op['operator_name'], generation=label, **r))
        row['government_stakes'] = '; '.join(
            f"{g['government']}: {g['holder']} {g['pct'] if g['pct'] is not None else 'n/d'}% of {g['pct_of']} ({g['basis']})" for g in op['gov'])
        row['government_stakes_status'] = 'value' if op['gov'] else 'none_found'
        row['government_stakes_note'] = op.get('gov_note', '')
        for g in op['gov']:
            if g['source_type'] not in SOURCE_TYPES:
                problems.append(f'{oid} gov {g["holder"]}: bad source_type')
            check(g['source_url'], evidence, f'{oid} gov {g["holder"]}', problems)
            gov.append(dict(operator_id=oid, country=op['country'], operator_name=op['operator_name'], **g))
        row['coded_at'] = CODED_AT
        panel.append(row)

    non_european = sorted(r['operator_id'] for r in panel if r['region'] != 'Western Europe')
    k = max(1, round(len(non_european) / 10))
    picks = set(random.Random(SEED).sample(non_european, k))
    for r in panel:
        r['spot_check'] = r['operator_id'] in picks

    if problems:
        print('\n'.join(problems))
        sys.exit(f'{len(problems)} problem(s); nothing written')
    for path, rows in (('data/5g_expansion_panel.csv', panel), ('data/5g_expansion_ran_vendors.csv', ran),
                       ('data/5g_expansion_gov_stakes.csv', gov)):
        with open(path, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f'{path}: {len(rows)} rows')
    print(f'spot-check ({k} of {len(non_european)} non-European, seed {SEED}):', sorted(picks))


if __name__ == '__main__':
    main()
