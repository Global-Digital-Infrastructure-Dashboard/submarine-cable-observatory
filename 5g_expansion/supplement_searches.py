"""Targeted follow-up searches for gaps found while coding the first-10 batch. Same cache and cap as
research_searches.py. Run from repo root: python3 5g_expansion/supplement_searches.py --cap 1.00"""
import argparse, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.getcwd(), '5g_expansion')); sys.path.insert(0, os.getcwd())
from research_searches import CACHE, EST, SYSTEM
from enrich_5g_operators import SearchCache
from pipeline_common import env_key, perplexity_search

NBIM = ("Norges Bank Investment Management (Government Pension Fund Global) holding in {co}: the percentage of "
        "{co}'s shares (ownership %) held at 31 December 2025 (or the latest year-end), as published in NBIM's "
        "holdings list or in {co}'s own shareholder disclosures. Give the exact figure and its source URL.")
SUPP = {
    'lu-shares': "Luxembourg mobile market shares by operator (POST, Tango/Proximus Luxembourg, Orange Luxembourg) "
                 "in the latest ILR (Institut Luxembourgeois de Régulation) statistical report, 2024 or 2025: percent of "
                 "mobile subscriptions for each operator and the year.",
    'sg-launch': "Commercial 5G launch dates in Singapore for Singtel, M1 and SIMBA (TPG): the date each operator first "
                 "made commercial 5G service available to customers (NSA or SA), from operator press releases or IMDA.",
    'simba-ran': "SIMBA Telecom (formerly TPG Telecom Singapore) mobile network equipment vendors: who supplies its 4G "
                 "and 5G radio access network and core network? Contract announcements with dates.",
    'ooredoo-owners': "Ooredoo Q.P.S.C. (Qatar) major shareholders: percentage held by the State of Qatar / Qatar "
                      "Investment Authority (QIA) / Qatar Holding and any other government entities, per Ooredoo's latest "
                      "annual report or Qatar Stock Exchange disclosure.",
    'il-partner-hot-ran': "Partner Communications and HOT Mobile (Israel) shared radio network (PHI Networks): which "
                          "vendor supplies the 5G RAN and 4G RAN (Nokia, Ericsson)? Did Partner replace Nokia with "
                          "Ericsson in 2023-2024, and who supplies Partner's and HOT Mobile's 5G standalone core? "
                          "Dates and sources.",
    'il-pelephone-core': "Pelephone (Bezeq group, Israel) 5G standalone core network vendor and launch date; Pelephone "
                         "5G RAN vendor; Bezeq annual report disclosure of Pelephone's equipment suppliers.",
    'ucell-owner': "Ucell (COSCOM LLC, Uzbekistan) current ownership in 2025-2026: who owns Ucell now? Did the 2021 "
                   "Digital Holding transaction with MegaFon/USM complete? Percentages held by the Uzbek state "
                   "(State Assets Management Agency or other) and dates.",
    'uz-shares': "Uzbekistan mobile operator market shares by subscribers, 2024 or 2025: Ucell, Beeline Uzbekistan, "
                 "Uzmobile (Uzbektelecom), Mobiuz. Percent share for each and the source (regulator, Ministry of "
                 "Digital Technologies, BMI, or operator).",
    'millicom-owners': "Millicom International Cellular (Tigo) major shareholders 2025-2026: list every holder above 3%, "
                       "and any government, sovereign wealth fund or state-owned company holding shares, with percentages "
                       "and the filing date.",
    'uy-claro': "Claro Uruguay (AM Wireless Uruguay): date of commercial 5G launch in Uruguay, and its share of "
                "Uruguay's mobile subscriptions per URSEC statistics (latest year).",
    'vodacom-owners': "Vodacom Group Limited (South Africa) major shareholders per its latest integrated annual report: "
                      "Vodafone Group's percentage, the Public Investment Corporation (PIC) / Government Employees Pension "
                      "Fund percentage, and any other government or state entity, with dates.",
    'airtel-africa-owners': "Airtel Africa plc major shareholders per the latest annual report (2025 or 2026): "
                            "percentages for Airtel Africa Mauritius / Bharti Airtel, Singapore Telecom International, "
                            "Qatar Holding LLC, and any other government, sovereign wealth fund or state-owned holder.",
    'nbim-cellcom': NBIM.format(co='Cellcom Israel'),
    'nbim-partner': NBIM.format(co='Partner Communications Company'),
    'nbim-bezeq': NBIM.format(co='Bezeq The Israel Telecommunication Corp'),
    'nbim-singtel': NBIM.format(co='Singapore Telecommunications (Singtel)'),
    'nbim-starhub': NBIM.format(co='StarHub'),
    'nbim-safaricom': NBIM.format(co='Safaricom PLC'),
    'nbim-americamovil': NBIM.format(co='America Movil'),
    'nbim-orange-proximus': ("Norges Bank Investment Management holdings at 31 December 2025 in Orange S.A. and in "
                             "Proximus: ownership percentage in each, from NBIM's holdings list."),
}

ap = argparse.ArgumentParser(); ap.add_argument('--cap', type=float, required=True); a = ap.parse_args()
cache = SearchCache(CACHE)
todo = [(f'exp|supp|{k}', p) for k, p in SUPP.items() if not cache.fresh(f'exp|supp|{k}', p)]
spent = sum(cache.costs())
print(f'{len(todo)} supplementary searches; spent so far ${spent:.4f}; cap ${a.cap:.2f}')
if spent + len(todo) * EST > a.cap: sys.exit('would exceed cap')
key = env_key('PERPLEXITY_API_KEY')
def run(j):
    k, p = j
    if sum(cache.costs()) + EST > a.cap: return k, 'skipped: cap'
    try: cache.put(k, perplexity_search(SYSTEM, p, key), p); return k, 'ok'
    except Exception as e: return k, f'error: {e}'
with ThreadPoolExecutor(4) as ex:
    for k, s in ex.map(run, todo):
        if s != 'ok': print(k, s)
print(f'done; spent from cache file ${sum(SearchCache(CACHE).costs()):.4f}')
