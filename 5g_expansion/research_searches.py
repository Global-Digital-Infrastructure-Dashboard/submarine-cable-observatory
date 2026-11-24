"""Perplexity searches for the 5G expansion batch (Prof. Shen's reduced schema).

Four searches per operator: share+launch, RAN vendors (5G and 4G), core vendor/contract, government stakes.
Results are cached in data/5g_expansion_searches.jsonl, one line per search with Perplexity's own billed cost.
The cap is checked against the cache file on disk, summing every line (so a repeated key still counts).

Prompt versions: QUESTIONS_V1 was used for the first-10 batch (2026-11-15). QUESTIONS (v2, 2026-11-23) follows
Prof. Shen's review: regulator shares first, vendor switches, and government holders of 5% or more (or with
a board seat) with holder type, the parent's stake at each step, and whether the source states the state
link. A key that is already cached is never searched again, whatever prompt it was asked with.

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


def spent_on_disk():
    """Every billed search ever made: one line per search, so a repeated key is still counted."""
    import json
    if not os.path.exists(CACHE):
        return 0.0
    return sum(json.loads(l)['search']['cost'] for l in open(CACHE))

SYSTEM = """You research mobile network operators for an academic dataset on telecom vendor \
dependence and state ownership. Use regulator statistics, operator annual reports and filings, \
stock-exchange disclosures, and reputable news. State only what sources say, with dates, and give \
the URL of each source next to each fact. Write "not found" for anything the sources don't cover; \
never estimate."""

QUESTIONS_V1 = {
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

QUESTIONS = {
    'share': """{operator} ({country}) - mobile market share and 5G launch.
1. The operator's share of mobile subscriptions/customers in {country} (percent), with the period it refers to. \
Use the national regulator's published market statistics first (name the report and date); only if the \
regulator publishes nothing by operator, use the operator's own report, then other sources. If only \
subscriber counts exist, give the counts for every operator in the market and their date.
2. The year (and date if known) {operator} launched commercial 5G service in {country}.""",
    'ran': """{operator} ({country}) - radio access network (RAN) equipment vendors for 5G and for 4G/LTE.
For each of 5G RAN and 4G RAN: name every supplier and how much of the network each supplies \
(sole supplier / most / some / small part / specific regions), quoting the source's own wording for any \
share. Include contract or deployment announcements with dates (e.g. Huawei, Ericsson, Nokia, ZTE, Samsung).
Also report any vendor switch: the operator replacing one vendor's equipment with another's (old vendor, \
new vendor, network element and generation, date or year announced and completed).""",
    'core': QUESTIONS_V1['core'],
    'gov': """{operator} ({country}) - shareholders that are governments or state entities.
List every government, ministry, state agency, state holding company, sovereign wealth fund, state \
pension fund or state-owned company that holds 5% or more of {operator} or of any parent company in its \
ownership chain, plus any smaller state holder that has a nominee or representative on that company's \
board. For each: the holder; its type (government/ministry, state holding company, sovereign wealth fund, \
pension fund, state-owned company); the country; the percentage and the company it is a percentage of; \
whether it is held directly in {operator} or through a parent, with each parent's percentage of the next \
company down to {operator}; any board seat; whether the source itself says the holder is state-owned or \
state-controlled; and the date and document. Prefer the latest annual report or official shareholder filing.""",
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
    todo = [(k, p) for k, p in jobs if cache.get(k) is None]
    spent = spent_on_disk()
    print(f"{len(ops)} operators, {len(jobs)} searches, {len(todo)} uncached; spent so far ${spent:.4f}; cap ${a.cap:.2f}")
    if a.dry:
        return
    if spent + len(todo) * EST > a.cap:
        sys.exit(f"Estimated ${spent + len(todo) * EST:.2f} would exceed the cap ${a.cap:.2f}.")
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

    with ThreadPoolExecutor(a.workers) as ex:
        for k, status in ex.map(run, todo):
            if status != 'ok':
                print(k, status)
    print(f"done; spent from cache file ${spent_on_disk():.4f}")


if __name__ == '__main__':
    main()
