"""Validate the in-session coding and write the expansion-panel CSVs.

  data/5g_expansion_panel.csv            one row per operator (scalar fields: value/status/source/type/note)
  data/5g_expansion_ran_vendors.csv      one row per operator x generation x vendor
  data/5g_expansion_gov_stakes.csv       one row per government holder at 5% or more, or with a board seat (never summed)
  data/5g_expansion_vendor_switches.csv  one row per vendor switch found while coding (opportunistic, not searched for)

Coding comes from every 5g_expansion/coded_batch*.py module (OPERATORS list each). The schema, source types,
holder types and the 5% rule are in schema.py.

Provenance check: every source_url (and state_link_url, owner_body_url) must appear in the cached search evidence
(answers or result lists in data/5g_expansion_searches.jsonl, or data/5g_searches.jsonl for reused core-panel facts),
or be a primary source read directly: NBIM's holdings file, or any URL logged as 'confirmed' with a quote in a
5g_expansion/verify_*.csv file (fund statutes, Lyse's annual report; copies kept locally in data/5g_direct/).

Sample status (Prof. Shen, 2026-11-26): an operator with sample_status = pilot_only (Ukraine: pilots only, no commercial
launch) stays in all four files but is outside the main sample; counts are printed for the main sample and pilots.

Spot-check: random.Random(SEED).sample over the non-European operators of batch 1 (kept as drawn on 2026-11-15).
Run from the repo root: python3 5g_expansion/build_panel.py [--check]   (--check validates without writing)
"""
import csv, glob, importlib, json, os, random, sys
sys.path.insert(0, os.path.join(os.getcwd(), '5g_expansion'))
from schema import SAMPLE_STATUS, VENDORS, source_type

SEED = 20261115
NBIM = 'https://www.nbim.no/api/investments/v2/report/?assetType=eq&date=2025-12-31&fileType=xlsx'
SCALARS = {'share': 'mobile_customer_share_pct', 'launch': 'fiveg_launch_year', 'core': '5g_core_vendor',
           'first_contract': 'first_5g_contract_date', 'vendor_operates': 'vendor_also_operates_network'}


def batches():
    for path in sorted(glob.glob('5g_expansion/coded_batch*.py')):
        mod = importlib.import_module(os.path.basename(path)[:-3])
        yield mod


def core_ids(value):
    return [c for c in (x.strip() for x in value.split(';')) if c]


def evidence_text():
    text = []
    for path in ('data/5g_expansion_searches.jsonl', 'data/5g_searches.jsonl'):
        for line in open(path):
            s = json.loads(line)['search']
            text.append(s['answer'])
            text.extend(str(r.get('url')) for r in s['results'])
    return '\n'.join(text)


def direct_sources():
    """URLs read directly and logged as confirmed, with the quote relied on, in a verify CSV."""
    urls = set()
    for path in glob.glob('5g_expansion/verify_*.csv'):
        with open(path) as f:
            urls |= {r['url'] for r in csv.DictReader(f) if r['result'] == 'confirmed'}
    return urls


def main():
    evidence, direct, problems = evidence_text(), direct_sources(), []

    def sourced(url, where):
        """Source type for a cited URL, after checking it is in the evidence."""
        if url and url != NBIM and url not in direct and url not in evidence:
            problems.append(f'{where}: URL not in cached evidence: {url}')
        try:
            return source_type(url)
        except KeyError as e:
            problems.append(f'{where}: {e}')
            return ''

    panel, ran, gov, switches, not_added, migrated = [], [], [], [], {}, {}
    for mod in batches():
        batch = mod.__name__
        not_added.update(getattr(mod, 'CHECKED_NOT_ADDED', {}))
        for op in mod.OPERATORS:
            oid = f"{op['country']}|{op['operator_name']}"
            # One row may carry several core ids ('a; b') when core operators have merged (Fastweb + Vodafone Italia).
            for cid in core_ids(op.get('core_operator_id', '')):
                if cid in migrated:
                    problems.append(f'{oid}: core_operator_id {cid} migrated twice (also {migrated[cid]})')
                migrated[cid] = oid
            if any(r['operator_id'] == oid for r in panel):
                problems.append(f'{oid}: coded twice')
            row = dict(operator_id=oid, region=op['region'], country=op['country'], operator_name=op['operator_name'],
                       name_note=op.get('name_note', ''), core_operator_id=op.get('core_operator_id', ''),
                       sample_status=op.get('sample_status', 'main'), sample_status_note=op.get('sample_status_note', ''))
            if row['sample_status'] not in SAMPLE_STATUS:
                problems.append(f"{oid}: sample_status {row['sample_status']}")
            for field, name in SCALARS.items():
                f = op[field]
                if f['status'] == 'value' and not f['source_url']:
                    problems.append(f'{oid} {field}: value without a source')
                if field == 'core' and f['status'] == 'value' and f['value'] not in VENDORS:
                    problems.append(f'{oid} core: non-canonical vendor {f["value"]}')
                row[name] = f['value'] if f['status'] == 'value' else ''
                row[f'{name}_status'] = f['status']
                if field == 'share':
                    row['mobile_customer_share_year'] = f['year'] or ''
                row[f'{name}_source_url'] = f['source_url']
                row[f'{name}_source_type'] = sourced(f['source_url'], f'{oid} {field}')
                row[f'{name}_note'] = f['note']
            for gen in ('ran5', 'ran4'):
                label = '5G' if gen == 'ran5' else '4G'
                row[f'{label.lower()}_ran_vendors'] = '; '.join(f"{r['vendor']} ({r['share_category']})" for r in op[gen])
                row[f'{label.lower()}_ran_status'] = 'value' if op[gen] else 'not_disclosed'
                row[f'{label.lower()}_ran_note'] = op.get(f'{gen}_note', '')
                for r in op[gen]:
                    stype = sourced(r['source_url'], f'{oid} {gen} {r["vendor"]}')
                    ran.append(dict(operator_id=oid, country=op['country'], operator_name=op['operator_name'], generation=label,
                                    vendor=r['vendor'], share_category=r['share_category'], source_url=r['source_url'],
                                    source_type=stype, note=r['note']))
            row['government_stakes'] = '; '.join(
                f"{g['government']}: {g['holder']} {g['pct'] if g['pct'] is not None else 'n/d'}% of {g['pct_of']} ({g['basis']})"
                for g in op['gov'])
            row['government_stakes_status'] = 'value' if op['gov'] else 'none_found'
            row['government_stakes_note'] = op.get('gov_note', '')
            if 'gov_dropped' not in op:
                problems.append(f'{oid}: gov_dropped missing (list holders below 5%, or [])')
            row['government_stakes_below_threshold'] = '; '.join(op.get('gov_dropped', []))
            for g in op['gov']:
                stype = sourced(g['source_url'], f'{oid} gov {g["holder"]}')
                if g['state_link_url'] and g['state_link_url'] != g['source_url']:
                    sourced(g['state_link_url'], f'{oid} gov {g["holder"]} state link')
                if g['owner_body_url']:
                    sourced(g['owner_body_url'], f'{oid} gov {g["holder"]} owner body')
                if g['holder_type'] == 'pension_fund' and source_type(g['state_link_url']) not in ('company', 'government'):
                    problems.append(f'{oid} gov {g["holder"]}: pension-fund basis must come from the fund itself or its law')
                gov.append(dict(operator_id=oid, country=op['country'], operator_name=op['operator_name'],
                                government=g['government'], government_level=g['government_level'], holder=g['holder'],
                                holder_type=g['holder_type'],
                                pct=g['pct'] if g['pct'] is not None else '', pct_status='value' if g['pct'] is not None else 'not_disclosed',
                                pct_of=g['pct_of'], basis=g['basis'],
                                parent_ownership_pct_of_operator=g['parent_ownership_pct_of_operator'] if g['parent_ownership_pct_of_operator'] is not None else '',
                                ownership_chain=g['ownership_chain'], board_seat=g['board_seat'], as_of=g['as_of'],
                                source_url=g['source_url'], source_type=stype, state_link_basis=g['state_link_basis'],
                                state_link_url=g['state_link_url'], pension_rule=g['pension_rule'],
                                owner_body=g['owner_body'], owner_body_url=g['owner_body_url'], note=g['note']))
            for s in op.get('switches', []):
                stype = sourced(s['source_url'], f'{oid} switch')
                switches.append(dict(operator_id=oid, country=op['country'], operator_name=op['operator_name'], **{**s, 'source_type': stype}))
            row['vendor_switches'] = '; '.join(f"{s['generation']} {s['element']}: {s['old_vendor']} -> {s['new_vendor']} ({s['announced']})"
                                               for s in op.get('switches', []))
            row['coded_at'] = getattr(mod, 'CODED_AT', '')
            row['retrofit_at'] = getattr(mod, 'RETROFIT_AT', '')
            row['added_at'] = op.get('added', '')
            row['batch'] = batch
            panel.append(row)

    first = sorted(r['operator_id'] for r in panel if r['batch'] == 'coded_batch1' and r['region'] != 'Western Europe'
                   and not r['added_at'])
    # Widened from 2 to 6 on 2026-11-15; the same seed extends the sample. Results: 5g_expansion/spotcheck_2026-11-15.csv.
    # Drawn over the 2026-11-15 operator ids; the 2026-11-23 renames (Al-madar -> Al-Madar, Simba -> SIMBA) touch no pick.
    old_ids = [o.replace('Libya|Al-Madar', 'Libya|Al-madar').replace('Singapore|SIMBA', 'Singapore|Simba') for o in first]
    picks = set(random.Random(SEED).sample(sorted(old_ids), 6))
    for r in panel:
        r['spot_check'] = r['operator_id'] in picks

    # Every core-panel operator is migrated exactly once (Prof. Shen, 2026-11).
    with open('data/5g_operator_panel.csv') as f:
        core = {r['operator_id'] for r in csv.DictReader(f)}
    missing, extra = sorted(core - set(migrated)), sorted(set(migrated) - core)
    problems += [f'core operator {c} not migrated' for c in missing] + [f'core_operator_id {c} not in the core panel' for c in extra]
    print(f'core panel: {len(core)} operators; migrated {len(migrated)} ids into '
          f'{sum(1 for r in panel if r["core_operator_id"])} rows; missing {missing}; extra {extra}')

    if problems:
        print('\n'.join(problems))
        sys.exit(f'{len(problems)} problem(s); nothing written')
    main_ids = {r['operator_id'] for r in panel if r['sample_status'] == 'main'}
    for label, keep in (('main sample', lambda i: i in main_ids), ('pilot_only', lambda i: i not in main_ids)):
        n = [r for r in panel if keep(r['operator_id'])]
        g = [r for r in gov if keep(r['operator_id'])]
        print(f"{label}: {len(n)} operators in {len({r['country'] for r in n})} countries; {len(g)} stakes "
              f"({sum(1 for r in g if r['government_level'] == 'local')} local); "
              f"{sum(1 for r in ran if keep(r['operator_id']))} RAN rows; {sum(1 for r in switches if keep(r['operator_id']))} switches")
    if '--check' in sys.argv:
        print(f'check passed: {len(panel)} operators, {len(gov)} stakes, {len(ran)} RAN rows, {len(switches)} switches; nothing written')
        return
    for path, rows in (('data/5g_expansion_panel.csv', panel), ('data/5g_expansion_ran_vendors.csv', ran),
                       ('data/5g_expansion_gov_stakes.csv', gov), ('data/5g_expansion_vendor_switches.csv', switches)):
        with open(path, 'w', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        print(f'{path}: {len(rows)} rows')
    print('spot-check picks (batch 1):', sorted(picks))
    print('checked, not added:', '; '.join(not_added) or 'none')


if __name__ == '__main__':
    main()
