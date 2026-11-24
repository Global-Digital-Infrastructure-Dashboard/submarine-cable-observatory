"""Targeted follow-up searches for gaps found while coding the first-10 batch. Same cache and cap as
research_searches.py. Run from repo root: python3 5g_expansion/supplement_searches.py --cap 1.00"""
import argparse, os, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.join(os.getcwd(), '5g_expansion')); sys.path.insert(0, os.getcwd())
from research_searches import CACHE, EST, SYSTEM, spent_on_disk
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

# Retrofit after Prof. Shen's 2026-11 review: direct state-link source for e&, board seats for sub-5% holders,
# operators possibly missing from the first 10, Tajik vendors, regulator-published customer shares.
REG_SHARE = ("{country} mobile market shares by operator from the national regulator ({reg}): the latest published "
             "number of mobile subscriptions (or SIMs/customers) per operator and the percent share, with the "
             "report title, date and URL. Only regulator or government statistics; say 'not found' otherwise.")
SUPP_2026_11 = {
    'e&-owners': "e& (Emirates Telecommunications Group Company PJSC, formerly Etisalat) major shareholders: the "
                 "percentage held by the Emirates Investment Authority (EIA) or other UAE government entities, as "
                 "stated in e&'s latest annual report, integrated report or ADX disclosure, with the date and URL.",
    'airtel-africa-board': "Airtel Africa plc board of directors (2025 or 2026): does Qatar Holding LLC or the Qatar "
                           "Investment Authority have a nominee or representative director on the board? Name the "
                           "director and source, or say not found.",
    'ooredoo-board': "Ooredoo Q.P.S.C. board of directors (2025 or 2026): which directors represent the Abu Dhabi "
                     "Investment Authority (ADIA), the General Military Retirement and Social Insurance Authority, "
                     "or other shareholders? Per Ooredoo's annual report or governance report, with sources.",
    'libyana-5g': "Has Libyana (Libyana Mobile Phone, Libya) launched commercial 5G service? Give the date, the "
                  "cities, the network vendor, and sources (2019-2026). Say not found if there is no launch.",
    'vinaphone-5g': "Has VinaPhone (VNPT, Vietnam) launched commercial 5G service? Give the launch date, the 5G RAN "
                    "and core vendors, and sources (2024-2026).",
    'mobifone-5g': "Has MobiFone (Vietnam) launched commercial 5G service? Give the launch date, the 5G RAN and "
                   "core vendors, and sources (2024-2026).",
    'digicel-tt-5g': "Has Digicel Trinidad and Tobago launched commercial 5G service? Give the launch date, the "
                     "network vendor, and sources (2019-2026). Say not found if there is no launch.",
    'tcell-vendor': "Tcell (Tajikistan, Aga Khan / AKFED) 5G and 4G LTE network equipment vendor: which company "
                    "(Huawei, ZTE, Ericsson, Nokia) supplied Tcell's 5G network launched in Dushanbe in 2020 and its "
                    "LTE network? Include Russian- or Tajik-language sources, with URLs.",
    'megafon-tj-vendor': "MegaFon Tajikistan (TT Mobile) 5G and 4G LTE network equipment vendor: which company "
                         "(Huawei, ZTE, Ericsson, Nokia) supplied the 5G network launched in Dushanbe in February "
                         "2020 and the LTE network? Include Russian-language sources, with URLs.",
    'reg-share-uy': REG_SHARE.format(country='Uruguay', reg='URSEC'),
    'reg-share-vn': REG_SHARE.format(country='Vietnam', reg='Ministry of Information and Communications / Ministry of Science and Technology, VNTA'),
    'reg-share-il': REG_SHARE.format(country='Israel', reg='Ministry of Communications'),
    'reg-share-uz': REG_SHARE.format(country='Uzbekistan', reg='Ministry of Digital Technologies'),
    'reg-share-tj': REG_SHARE.format(country='Tajikistan', reg='Communications Service under the Government'),
    'reg-share-sg': REG_SHARE.format(country='Singapore', reg='IMDA'),
    'bharti-owners': "Bharti Airtel Limited (India) shareholding pattern, latest quarter of 2025 or 2026: percentage "
                     "held by Singapore Telecommunications (Singtel) and its subsidiaries (e.g. Pastel Limited), by "
                     "Bharti Telecom, and by any government, sovereign wealth fund or state-owned company holding 5% "
                     "or more; also Bharti Airtel's percentage of Airtel Africa plc. Dates and URLs (BSE/NSE filings).",
}
SUPP.update(SUPP_2026_11)

# Follow-ups from coding batches 2-4 (user-approved 2026-11-23, ~$0.07).
SUPP.update({
    'mtel-me-5g': "Mtel (Montenegro, Telekom Srbija group): has it launched commercial 5G? Launch date, 5G RAN and core "
                  "vendors, and its ownership (Telekom Srbija's percentage and Telekom Srbija's state owner), with sources.",
    'jazz-ufone-launch': "Jazz (Pakistan) and Ufone (PTCL, Pakistan) commercial 5G launch: the date each launched commercial 5G "
                         "service after the 2026 spectrum auction, and each operator's 5G RAN vendor. Sources with dates.",
    'altice-do-launch': "Altice Dominicana (Dominican Republic) commercial 5G launch date, per INDOTEL or an Altice press release.",
    'xl-axiata-launch': "XL Axiata (now XLSmart, Indonesia) commercial 5G launch: the first date and city XL Axiata (or Smartfren) "
                        "launched commercial 5G, 2021-2022, per operator press releases.",
    'pta-shares': "PTA (Pakistan Telecommunication Authority) annual report 2024-25 or latest telecom indicators: cellular "
                  "subscribers by operator (Jazz, Zong, Telenor/Ufone, SCO) with the date. Regulator figures only.",
    'axiata-holders': "Axiata Group Berhad annual report 2025: how does it describe Khazanah Nasional, the Employees Provident "
                      "Fund (EPF) and Permodalan Nasional Berhad (PNB)? Does it say they are government-owned or "
                      "state-controlled? Exact wording, percentages and page.",
    'monaco-telecom-owners': "Monaco Telecom shareholders: the percentage held by the Government of Monaco (or a Monaco state "
                             "entity) and by NJJ Holding, latest filing or official statement.",
    'tci-iran-owners': "Telecommunication Company of Iran (TCI) shareholders 2025: percentages held by Etemad Mobin, the "
                       "government, Social Security Organization or other state entities, and how sources describe its status.",
    'jordan-ssc': "Social Security Corporation of Jordan (SSC / Social Security Investment Fund): legal status - is it a "
                  "government body or state-owned? Its shareholding in Orange Jordan (Jordan Telecom), with sources.",
    'gepf-status': "Government Employees Pension Fund (South Africa, managed by the PIC) holding in MTN Group: percentage, "
                   "and whether MTN or the PIC describes it as a government or state pension fund.",
})

ap = argparse.ArgumentParser(); ap.add_argument('--cap', type=float, required=True); a = ap.parse_args()
cache = SearchCache(CACHE)
todo = [(f'exp|supp|{k}', p) for k, p in SUPP.items() if cache.get(f'exp|supp|{k}') is None]
spent = spent_on_disk()
print(f'{len(todo)} supplementary searches; spent so far ${spent:.4f}; cap ${a.cap:.2f}')
if spent + len(todo) * EST > a.cap: sys.exit('would exceed cap')
key = env_key('PERPLEXITY_API_KEY')
def run(j):
    k, p = j
    if spent_on_disk() + EST > a.cap: return k, 'skipped: cap'
    try: cache.put(k, perplexity_search(SYSTEM, p, key), p); return k, 'ok'
    except Exception as e: return k, f'error: {e}'
with ThreadPoolExecutor(4) as ex:
    for k, s in ex.map(run, todo):
        if s != 'ok': print(k, s)
print(f'done; spent from cache file ${spent_on_disk():.4f}')
