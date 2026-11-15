"""Perplexity searches for the 5G expansion batch (Prof. Shen's reduced schema).

Four searches per operator: share+launch, RAN vendors (5G and 4G), core vendor/contract, government stakes.
Results are cached in data/5g_expansion_searches.jsonl, one line per search with Perplexity's own billed cost.
The cap is checked against the cache file on disk, which counts every search ever made.

Run from the repo root:  python3 5g_expansion/research_searches.py --countries Libya,Kenya --cap 1.00 [--dry]
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.getcwd())
import pandas as pd

from enrich_5g_operators import SearchCache
from pipeline_common import env_key, perplexity_search

CACHE = 'data/5g_expansion_searches.jsonl'
OPERATORS = 'data/5g_expansion_operators.csv'
EST = 0.0075

SYSTEM = """You research mobile network operators for an academic dataset on telecom vendor \
dependence and state ownership. Use regulator statistics, operator annual reports and filings, \
stock-exchange disclosures, and reputable news. State only what sources say, with dates, and give \
the URL of each source next to each fact. Write "not found" for anything the sources don't cover; \
never estimate."""

QUESTIONS = {
    'share': """{operator} ({country}) - mobile market share and 5G launch.
1. The operator's share of mobile subscriptions/customers in {country} (percent), with the year it refers to. \
Prefer the national regulator's market statistics; otherwise the operator's own report. If only subscriber \
counts exist, give the counts for every operator in the market and their date.
2. The year (and date if known) {operator} launched commercial 5G service in {country}.""",
    'ran': """{operator} ({country}) - radio access network (RAN) equipment vendors for 5G and for 4G/LTE.
For each of 5G RAN and 4G RAN: name every supplier and how much of the network each supplies \
(sole supplier / most / some / small part / specific regions), as sources state it. Include contract or \
deployment announcements with dates (e.g. Huawei, Ericsson, Nokia, ZTE, Samsung).""",
    'core': """{operator} ({country}) - 5G core network.
1. Which vendor supplies the 5G core (5GC or NSA EPC used for 5G)?
2. The date of the operator's first 5G contract or agreement with any network vendor.
3. Does any equipment vendor also operate or manage the operator's network (managed services / \
outsourced network operations)? Name the vendor and the dates.""",
    'gov': """{operator} ({country}) - shareholders that are governments or state entities.
List EVERY government, state body, sovereign wealth fund, state pension fund or state-owned company \
that holds shares in {operator}, either directly or through a parent company (name the parent and the \
parent's stake). Include passive holdings such as Norges Bank Investment Management. For each: the \
holder, the country, the percentage, whether direct or via the parent, and the date and document it \
comes from. Prefer the latest annual report or official shareholder filing.""",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--countries', required=True)
    ap.add_argument('--cap', type=float, required=True)
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--workers', type=int, default=4)
    a = ap.parse_args()

    ops = pd.read_csv(OPERATORS)
    ops = ops[ops.country.isin(a.countries.split(','))]
    jobs = []
    for r in ops.itertuples():
        oid = f"{r.country}|{r.operator}"
        for layer, q in QUESTIONS.items():
            jobs.append((f"exp|{layer}|{oid}", q.format(operator=r.operator, country=r.country)))

    cache = SearchCache(CACHE)
    todo = [(k, p) for k, p in jobs if not cache.fresh(k, p)]
    spent = sum(cache.costs())
    print(f"{len(ops)} operators, {len(jobs)} searches, {len(todo)} uncached; spent so far ${spent:.4f}; cap ${a.cap:.2f}")
    if a.dry:
        return
    if spent + len(todo) * EST > a.cap:
        sys.exit(f"Estimated ${spent + len(todo) * EST:.2f} would exceed the cap ${a.cap:.2f}.")
    key = env_key('PERPLEXITY_API_KEY')

    def run(job):
        k, p = job
        if sum(cache.costs()) + EST > a.cap:
            return k, 'skipped: cap'
        try:
            cache.put(k, perplexity_search(SYSTEM, p, key), p)
            return k, 'ok'
        except Exception as e:
            return k, f'error: {e}'

    with ThreadPoolExecutor(a.workers) as ex:
        for k, status in ex.map(run, todo):
            if status != 'ok':
                print(k, status)
    print(f"done; spent from cache file ${sum(SearchCache(CACHE).costs()):.4f}")


if __name__ == '__main__':
    main()
