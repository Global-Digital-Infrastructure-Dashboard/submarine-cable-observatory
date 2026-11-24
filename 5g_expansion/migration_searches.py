"""Backfill searches for migrating the core-94 panel into the expansion's three-file format (Prof. Shen, 2026-11):
customer share and 5G launch (QUESTIONS['share']) and RAN vendors with 4G, share wording and switches
(QUESTIONS['ran']), the same v2 prompts the expansion uses. Ownership comes from gov_stakes_core.py; the core
vendor, restrictions and deadlines come from the core panel itself, so no 'core' or 'gov' searches are run.

Keys: mig|share|<operator_id> and mig|ran|<operator_id>, in the expansion cache (data/5g_expansion_searches.jsonl),
so the cap counts every expansion search ever made (spent_on_disk). Approved 2026-11-23: 188 searches, phase cap
$1.40 on top of $2.357 already spent.

Run from the repo root: python3 5g_expansion/migration_searches.py --cap 3.76 [--dry] [--markets Germany]
"""
import argparse, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.getcwd(), '5g_expansion')); sys.path.insert(0, os.getcwd())
import pandas as pd
from research_searches import CACHE, QUESTIONS, SYSTEM, spent_on_disk
from enrich_5g_operators import SearchCache
from pipeline_common import env_key, perplexity_search

MARKET_SHARE = """{country} mobile market shares by operator: the share of mobile subscriptions (or SIMs/customers) held by \
each mobile network operator ({operators}) for the latest period available, with the period. Use the national \
regulator's market report first; if it publishes only totals, use a source that gives every operator on the same \
basis (an operator filing or results release with a market-share table, or an analyst report quoted with its date). \
Give the source URL next to each figure and say what is counted (SIMs, subscriptions, excluding M2M...)."""

EST = 0.0070  # measured 0.0062 per v2 search on 2026-11-23, plus a margin


def jobs(markets=None):
    panel = pd.read_csv('data/5g_operator_panel.csv', usecols=['operator_id', 'operator_name', 'market'])
    if markets:
        panel = panel[panel.market.isin(markets)]
    # Added 2026-11-24 after the calibration batch: regulators in Western Europe publish totals only, so one
    # market-level search per market (user-approved, cap +$0.25).
    for market, g in panel.groupby('market', sort=False):
        yield f'mig|mktshare|{market}', MARKET_SHARE.format(country=market, operators=', '.join(g.operator_name))
    for r in panel.itertuples():
        for layer in ('share', 'ran'):
            yield f'mig|{layer}|{r.operator_id}', QUESTIONS[layer].format(operator=r.operator_name, country=r.market)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cap', type=float, required=True, help='total expansion-cache spend cap, USD')
    ap.add_argument('--markets')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    cache = SearchCache(CACHE)
    todo = [(k, p) for k, p in jobs(a.markets.split(',') if a.markets else None) if cache.get(k) is None]
    spent = spent_on_disk()
    print(f'{len(todo)} uncached migration searches; spent so far ${spent:.4f}; cap ${a.cap:.2f}; estimate ${len(todo) * EST:.2f}')
    if a.dry:
        return
    if spent + len(todo) * EST > a.cap:
        sys.exit('would exceed the cap')
    key = env_key('PERPLEXITY_API_KEY')

    def run(job):
        k, p = job
        if spent_on_disk() + EST > a.cap:
            return k, 'skipped: cap'
        try:
            cache.put(k, perplexity_search(SYSTEM, p, key), p)
            return k, 'ok'
        except Exception as e:
            return k, f'error: {e}'

    with ThreadPoolExecutor(4) as ex:
        for k, status in ex.map(run, todo):
            if status != 'ok':
                print(k, status)
    print(f'done; spent from cache file ${spent_on_disk():.4f}')


if __name__ == '__main__':
    main()
