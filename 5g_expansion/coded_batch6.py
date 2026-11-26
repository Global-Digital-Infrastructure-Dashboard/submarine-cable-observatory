"""Researcher coding of expansion batch 6 (Zambia, Benin, Laos, Thailand, Bangladesh, Brunei; 9 operators), coded
in-session on 2026-11-26 from the cached v2 searches in data/5g_expansion_searches.jsonl (plus core-panel cache entries
for Telenor's and Singtel's shareholders), under Prof. Shen's revised schema (see schema.py). Values come only from the
cited source; anything a source didn't state is not_disclosed. Government stake percentages, computed figures and
share-category claims were checked against the primary page at coding time (Prof. Shen's rule 11); the per-fact log is
5g_expansion/verify_2026-11-26_batch6.csv, with fetched copies in data/5g_direct/ (named by sha1(url)[:12]).
Not cited at all: Wikipedia, personal LinkedIn profiles, Scribd, eSIM/aggregator sites, Reddit.

Batch notes:
- MTN opcos (Zambia, Benin): MTN Group's percentage of each opco is from the group-composition chart in MTN's FY2025
  annual financial statements (p.107-108 printed, PDF p.109-110: MTN Zambia Limited 78%, effective 89.8% for
  accounting; Spacetel Benin SA 75%). The GEPF row (19.94% of MTN Group) is coded exactly as batch 4's MTN Irancell row.
- Airtel Zambia follows batch 1's Airtel Kenya row: no state holder at 5% or more in the Airtel Africa / Bharti chain;
  the same below-threshold holders are listed.
- Thailand: no NBTC operator statistics newer than Q1 2015 were found, so neither operator's share is coded. True's
  chain includes two state holders (China Mobile Communications Group via China Mobile Limited, coded as in batch 3's
  Zong row; the Norwegian state via Telenor ASA, coded as in the core panel's Telenor rows). True's own major-shareholder
  page could not be fetched (true.listedcompany.com returned an empty response; the SET page is script-rendered), so the
  True-level percentages in those chains are UNVERIFIED and come from a research database quoting True's 7 Mar 2025 list.
- Robi follows batch 3's Dialog rows (Khazanah + EPF of Axiata; EPF is a registered pension fund).
- Brunei: UNN is the single wholesale network (retail providers DST, imagine and Progresif ride on it), so it has no
  retail market share.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-26'

register(
    domains={
        'company': ['mtn.com', 'mtn-investor.com', 'mtn.zm', 'huawei.com', 'truecorp.co.th', 'true.listedcompany.com',
                    'ais.co.th', 'ais.th', 'grameenphone.com', 'robi.com.bd', 'axiata.com', 'axiata.listedcompany.com',
                    'unn.com.bn', 'laotel.com', 'telenor.com', 'airtel.co.zm'],
        'government': ['apt.int', 'aiti.gov.bn', 'btrc.gov.bd', 'nbtc.go.th'],
        'research_industry_group': ['mordorintelligence.com', 'mpmonitor.org'],
        'news': ['itweb.africa', 'itnewsafrica.com', 'teletimesinternational.com', 'laotiantimes.com', 'internetlaos.com',
                 'scandasia.com', 'digitalmag.theceomagazine.com'],
    },
    overrides={
        # China Mobile filings hosted on irasia (as registered in batch 3)
        'https://doc.irasia.com/listco/hk/chinamobile/interim/2025/intrep.pdf': 'company',
        'https://doc.irasia.com/listco/hk/chinamobile/annual/2023/ar2023.pdf': 'company',
    },
    vendors=['NuRAN Wireless'],
)

# ------------------------------------------------------------------ shared: MTN Group (GEPF), Airtel Africa, Telenor, Axiata
MTN_AFS = 'https://www.mtn.com/wp-content/uploads/2026/03/MTN-Group-FY-25-Annual-Financial-Statements.pdf'
MTN_DATA25 = 'https://mtn-investor.com/reporting/annuals-2025/pdf/data-sheets-spreads.pdf'
GEPF_NOTE = ("MTN FY2025 annual financial statements, p.146, beneficial shareholders of 5% or more (19.44% in 2024; GEPF's own "
             "report gave 22% at 31 Mar 2022). Coded under Prof. Shen's pension rule (2026-11-26): GEPF is governed by the "
             "Government Employees Pension Law 1996 and manages pensions for government employees (GEPF website). Its investment "
             "manager, the PIC, is government-owned (GEPF annual report 2022)")


def gepf(parent_pct, chain):
    return G('South Africa', 'Government Employees Pension Fund (GEPF)', 'pension_fund', 19.94, 'MTN Group Limited', 'via_parent',
             '2025-12-31', MTN_AFS, GEPF_NOTE, parent_pct=parent_pct, chain=chain)


AIRTEL_DROPPED = ["Qatar Holding LLC 3.67% of Airtel Africa plc (2025-03-31; no Qatar nominee on the Airtel Africa board per the 2025 annual report and leadership page)",
                  'Norges Bank Investment Management 0.39% of Airtel Africa plc (2025-12-31; board seat not checked)',
                  'Norges Bank Investment Management 1.06% of Bharti Airtel Ltd (2025-12-31; board seat not checked)']
BHARTI_OPEN = ("OPEN (as for Airtel Kenya): Bharti Airtel's 30 Jun 2025 BSE pattern shows a 10.79% foreign promoter group without "
               "naming its members, so a Singtel stake in Bharti could not be coded")

TELENOR_SHARE = 'https://www.telenor.com/who-we-are/corporate-governance/telenors-share-and-shareholders/'
FOLKETRYGD_DROP = 'Folketrygdfondet (Government Pension Fund Norway) 4.35-4.76% of Telenor ASA (2025-26; meets the pension rule; board seat not checked)'


def norway(chain, parent_pct=None, note=''):
    """Same row as the core panel's Telenor operators (coded_batch_core3.telenor_gov)."""
    return G('Norway', 'Government of Norway', 'government_ministry', 53.97, 'Telenor ASA', 'via_parent', '2026-02-27', TELENOR_SHARE,
             "the Norwegian state's holding is managed by the Ministry of Trade, Industry and Fisheries. " + note,
             parent_pct=parent_pct, chain=chain)


AXIATA_OVERVIEW = 'https://www.axiata.com/2025IAR/documents/Axiata-Integrated-Annual-Report-2025-Overview.pdf'
AXIATA_AFS = 'https://www.axiata.com/2025IAR/documents/Axiata-Governance-and-Audited-Financial-Statements-2025.pdf'

# ------------------------------------------------------------------ Zambia
ZM_SHARE = 'https://itweb.africa/article/zambia-mobile-sector-exceeds-389-million/KWEBbvyLzKxqmRjO'
ZM_NOTE = ("ZICTA 2023 Annual Market Report for the ICT Sector, as reported by ITWeb Africa (2024): active mobile subscriptions "
           "21.1m at end-2023; Airtel 48.6%, MTN Zambia 32.6%, Zamtel 18.8% (verified on the ITWeb page). Not coded: MTN's "
           "FY2025 data sheets give MTN Zambia 42.3% (company figure, 2nd of 4 operators); the PwC Zambia 2025 telecoms report "
           "gives 2024 counts (Airtel 11,102,293, MTN 6,452,376, Zamtel 5,295,844; MTN 27.8%) but returned 403 (UNVERIFIED)")

# ------------------------------------------------------------------ Thailand
TH_SHARE_NOTE = ("no current NBTC operator statistics found (the NBTC Mobile Market document located is for Q1 2015: AIS 45.0, "
                 "DTAC 30.5, True 23.1)")
TRUE_HOLDERS = 'https://mpmonitor.org/p/th-t-00007-0/'
TRUE_HOLDERS_NOTE = ("True's 'Major Shareholders as of 7 March 2025' as quoted by the Media Pluralism Monitor database (read "
                     "2026-11-26): concert party 60.60% = Charoen Pokphand Group 28.60%, Telenor Thailand Investments 28.60%, "
                     "Citrine Global 3.39% (CPH Telco 50.99%, Telenor Asia 49.00%); China Mobile International Holdings Limited "
                     "7.81%; National Telecom 2.39%. UNVERIFIED against True's own list: true.listedcompany.com returned an "
                     "empty response and the SET major-shareholder page is script-rendered")

CHECKED_NOT_ADDED = {}

OPERATORS = [
    # ------------------------------------------------------------------ Zambia
    dict(region='Africa', country='Zambia', operator_name='MTN',
         name_note='MTN Zambia Limited',
         share=V(32.6, ZM_SHARE, ZM_NOTE, 2023),
         launch=V(2022, 'https://www.mtn.com/mtn-zambia-launches-the-countrys-first-5g-network/',
                  "MTN (24 Nov 2022): 'MTN Zambia today launched our 5G network, becoming the first mobile operator in Zambia to "
                  "offer 5G services commercially after successfully undertaking trials ... over the past 11 months' (verified); "
                  "the Jan 2022 Huawei 5G pilot was a pilot"),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.huawei.com/en/news/2026/6/lampsite-mtn-zambia',
                 "Huawei (3 Jun 2026): MTN Zambia and Huawei completed the 'world's first commercial deployment' of the five-band "
                 "LampSite (incl. 3.5 GHz) at the Mulungushi centre, 'a new phase of upgraded 5G indoor connectivity' (verified); "
                 "indoor sites only. Huawei was also MTN Zambia's partner for the Jan 2022 5G pilot (IT News Africa) and for a "
                 "Meta-AAU 5G antenna (Apr 2025); no share wording")],
         ran5_note='no source names the vendor of the macro 5G network launched in Nov 2022 or any share',
         ran4=[R('Huawei', 'not_disclosed', 'https://www.itnewsafrica.com/2022/01/mtn-zambia-and-huawei-launch-5g',
                 "IT News Africa (11 Jan 2022), per the search: Huawei partnered with MTN Zambia in 2013 to build the country's first "
                 "4G network and in 2016 a 4.5G network. The page did not render on re-fetch (2026-11-26), so the wording is not "
                 "verified; no share stated")],
         gov=[gepf(78.0, "MTN Group 78% of MTN Zambia Limited (FY2025 AFS group-composition chart, p.107, under MTN International "
                         "(Mauritius); 'effective shareholding of 89.8%, for accounting purposes'; the FY2025 data sheets give 89.80% "
                         "effective)")],
         gov_note=("MTN's FY2025 sustainability report (via search) gives MTN Zambia as 78% MTN / 22% local shareholding without naming the local "
                   "holders; no Zambian state holder identified"),
         gov_dropped=[],
         core=ND('Huawei is named only as the 5G pilot partner (Jan 2022); no source names the 5G core or NSA EPC vendor'),
         first_contract=ND('the Huawei 5G pilot (11 Jan 2022) was a pilot partnership; no contract date'),
         vendor_operates=ND('China Comservice / Starlabs work appears only in a personal LinkedIn profile (not cited)')),
    dict(region='Africa', country='Zambia', operator_name='Airtel',
         name_note='Airtel Networks Zambia Plc',
         share=V(48.6, ZM_SHARE, ZM_NOTE, 2023),
         launch=V(2023, 'https://www.samenacouncil.org/samena_daily_news?news=96460',
                  "SAMENA Daily (27 Jul 2023, from CommsUpdate): 'Airtel Zambia has confirmed its commercial introduction of 5G "
                  "services', initially in select areas of Lusaka (verified); exact launch day not stated"),
         ran5=[], ran5_note=("no 5G RAN vendor named. Ericsson's Airtel Zambia RAN transformation (Mar 2016) covered 2G and a swap of "
                             "existing 3G sites 'on the road to 5G'; the search's '21 Mar 2025' MarketScreener date appears to be the "
                             "2016 announcement"),
         ran4=[], ran4_note=("Nokia and ZTE LTE work appears only in personal LinkedIn/Scribd profiles (not cited); ZTE's 2016-17 "
                             "virtualised gateways for Airtel Zambia are core/voice equipment, not RAN"),
         gov=[],
         gov_note=("no state holder at 5% or more found. Bharti Airtel Zambia Holdings B.V. 93.90% and Zambian public 6.10% at 31 Dec "
                   "2024 (Airtel Networks Zambia annual report 2024); ultimate controlling entity Bharti Enterprises (private family "
                   "trusts). Airtel Africa plc: Airtel Africa Mauritius 62.35%, Indian Continent Investment 16.22% (31 Mar 2025). "
                   + BHARTI_OPEN),
         gov_dropped=AIRTEL_DROPPED,
         core=ND('ZTE core-network work for Airtel Africa incl. Zambia appears only in a personal LinkedIn profile (not cited)'),
         first_contract=ND('no dated 5G vendor contract found'),
         vendor_operates=ND("Nokia Siemens Networks' managed-services deal for Airtel's network in Zambia and six other African "
                            "countries (Economic Times, 7 Sep 2011) covered 2G/3G and predates 5G; no current arrangement found")),
    # ------------------------------------------------------------------ Benin
    dict(region='Africa', country='Benin', operator_name='MTN',
         name_note='Spacetel Benin SA (MTN Benin)',
         share=V(43.5, MTN_DATA25,
                 ("MTN Group FY2025 data sheets, 'Market analysis' (p.24): Benin market share 43.5%, market position 1 of 3 operators, "
                  "MTN shareholding 75.00% (verified); company figure, no regulator (ARCEP Bénin) operator statistics found. The FY2024 "
                  "data sheets gave 47.5%; a secondary report cites ARCEP at about 50% for Q2 2024 without a linked publication"), 2025),
         launch=V(2024, 'https://www.mtn.com/mtn-group-extends-the-magic-of-5g-technology-to-benin-and-congo-brazzaville/',
                  "MTN Group (25 Nov 2024): 'the official commercial launch of 5G networks in Benin and the Republic of Congo' (verified); "
                  "an industry report dates the Benin launch 22 Nov 2024"),
         ran5=[], ran5_note='no source names a 5G RAN vendor',
         ran4=[R('NuRAN Wireless', 'not_disclosed', 'https://www.samenacouncil.org/samena_daily_news?news=101431',
                 "SAMENA Daily (19 Jul 2024): 'MTN Benin contracted NuRAN Wireless for 200 sites to deploy 2G, 3G and 4G in rural "
                 "locations', a five-year Network-as-a-Service agreement under MTN's 2022 group framework (verified); 200 rural sites only")],
         ran4_note=("Ericsson's 2015 five-year managed rural-coverage deal (low-power radio base stations, northern and central Benin) "
                    "names no generation. An Ericsson-to-Huawei 2G/3G/4G RAN modernisation (Apr 2024-Oct 2025) appears only in "
                    "personal LinkedIn profiles, so no Huawei row or vendor switch is recorded"),
         gov=[gepf(75.0, "MTN Group 75% of Spacetel Benin SA (FY2025 AFS group-composition chart, p.108, under MTN (Dubai) Limited; "
                         "the FY2025 data sheets give 75.00% effective)")],
         gov_note=("MTN's 2024 sustainability report (via search) gives MTN Benin as 75% MTN / 25% local shareholding without naming the local holders; "
                   "no Beninese state holder identified"),
         gov_dropped=[],
         core=ND("MTN's launch release names no core vendor; Ericsson's managed operations cover the existing core, not a named 5G core"),
         first_contract=ND('no dated 5G vendor contract found'),
         vendor_operates=V(True, 'https://teletimesinternational.com/2020/mtn-ericsson-managed-services/',
                           "Teletimes (26 Mar 2020): 'MTN Benin has extended its long-term relationship with Ericsson to provide managed "
                           "services, including Network Operations Center, Field Services in Radio, Core and Transmission' (verified); "
                           "Ericsson's own release returned 403. Huawei held a five-year managed-services contract from Sep 2014. "
                           "Current status after ~2025 not found")),
    # ------------------------------------------------------------------ Laos
    dict(region='Asia-Pacific', country='Laos', operator_name='LaoTel',
         name_note='Lao Telecommunications Public Company (Lao Telecom, LTC)',
         share=V(50.0, 'https://apt.int/sites/default/files/2022/05/APT_EM_2021_Laos_Report_Final.pdf',
                 ("APT Expert Mission 2021 report (May 2022), Table 8 'Mobile market share by operator', source MTC (the ministry): "
                  "LTC 54 (2019), 50 (2020); Unitel 36, ETL 11, Tplus 3 (verified, p.30). Tplus is 100% owned by LTC. The same report's "
                  "interview text gives LTC 48% and Unitel 57%, which do not reconcile with the ministry table; a secondary blog "
                  "gives LaoTel 34% for end-2020 (not coded)"), 2020),
         launch=V(2023, 'https://www.mordorintelligence.com/industry-reports/laos-telecom-mno-market',
                  ("DISPUTED between Mordor Intelligence ('Lao Telecom's February 2023 5G launch marked the country's first commercial "
                   "next-generation service'; verified) and the APT report (May 2022: 'LTC officially launched 5G services in September "
                   "2020' in parts of Vientiane); coded Mordor, because Lao Telecom's own history page lists '2019 - 2020 5G Trial "
                   "phase in VTE' and '2021 - 2024 5G Commercial launch'. Weak source (market-research summary)")),
         ran5=[], ran5_note=("no 5G RAN vendor named (a Huawei 'key supplier' claim appears only on Reddit; not cited). Lao Telecom "
                             "reported 56 5G stations in Nov 2026 (Laotian Times)"),
         ran4=[R('Huawei', 'not_disclosed', 'https://www.internetlaos.com/2012/11/ltc-to-launch-first-4g-commercial',
                 "Internet Laos (7 Nov 2012): 'The Chinese vendor Huawei was chosen for this project and installed 20 LTE mobile sites "
                 "in Vientiane' for LTC's first 4G service (verified); share of the national 4G network not stated")],
         gov=[G('Laos', 'Government of the Lao PDR', 'government_ministry', 51.0, 'Lao Telecommunications Public Company', 'direct', '2026-11-12',
                'https://laotiantimes.com/2026/11/12/lao-telecom-marks-30-years-of-growth-with-ceremony-in-vientiane/',
                ("Laotian Times (12 Nov 2026): 'The Lao Government and Shenington Investments (Singapore) set up the company as a joint "
                 "venture, with the government holding 51 percent and Shenington 49 percent' (verified); same split in the APT 2022 "
                 "report (Table 6, source MTC) and the ITU 2017 country profile. Holding body not named; board seat not checked"))],
         gov_note=("Shenington Investments (49%) is not identified as a state entity in the evidence. An intellinews headline 'Thailand's "
                   "AIS to acquire 24% stake in Lao Telecom' (undated) returned 403 and is UNVERIFIED; the Nov 2026 report still names "
                   "Shenington as the 49% holder, so no AIS/Singtel chain is coded"),
         gov_dropped=[],
         core=ND('no source names the 5G core or NSA EPC vendor'),
         first_contract=ND('a Huawei cooperation claim appears only on Reddit (not cited)'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Thailand
    dict(region='Asia-Pacific', country='Thailand', operator_name='True',
         name_note='True Corporation Public Company Limited (TrueMove H; merged with DTAC on 1 Mar 2023)',
         share=ND(TH_SHARE_NOTE + ". True's 2024 annual report gives 49,426,295 mobile customers at 31 Dec 2024 and a market of about "
                  "95.2m excluding NT and its MVNOs, but no percentage; that report could not be fetched (UNVERIFIED), so no share is computed"),
         launch=V(2020, 'https://investor.truecorp.co.th/misc/AR/20210326-true-ar2020-en.pdf',
                  "True annual report 2020: commercial 5G launched in 2020, exact date not stated (via search; the PDF host did not respond "
                  "on re-fetch). Ericsson's rollout for True began in Mar 2020 (ScandAsia)"),
         ran5=[R('Ericsson', 'not_disclosed', 'https://scandasia.com/thai-true-corporation-selected-ericsson-their-5g-radio-access-network-vendor/',
                 "ScandAsia (28 Apr 2020), citing Ericsson's 27 Apr 2020 statement: True 'has selected Ericsson as a 5G Radio Access Network "
                 "(RAN) vendor'; Ericsson Radio System for 700 MHz, 2.6 GHz and 26 GHz 'in the North, Central-West, and Upper South regions "
                 "of Thailand' (verified). A regional allocation is not one of the share categories")],
         ran5_note=("the vendor(s) for True's other regions are not named; an S&P 5G tracker lists True among ZTE's 5G customers "
                    "without saying RAN, so ZTE is not coded"),
         ran4=[], ran4_note="True's annual reports name no 4G RAN vendor ('multiple global suppliers')",
         gov=[G('China', 'China Mobile Communications Group Co., Ltd. (CMCC)', 'state_owned_company', 69.09, 'China Mobile Limited', 'via_parent', '2025-06-30',
                'https://doc.irasia.com/listco/hk/chinamobile/interim/2025/intrep.pdf',
                "as coded for Zong in batch 3; China Mobile's 2023 annual report calls CMCC a central state-owned enterprise under SASAC. "
                + TRUE_HOLDERS_NOTE,
                link_url='https://doc.irasia.com/listco/hk/chinamobile/annual/2023/ar2023.pdf',
                chain='CMCC -> China Mobile Limited -> China Mobile International Holdings Limited 7.81% of True Corporation (7 Mar 2025; UNVERIFIED)'),
              norway("Telenor ASA -> Telenor Thailand Investments 28.60% of True Corporation, plus Telenor Asia 49.00% of Citrine Global, "
                     "which holds 3.39% of True (7 Mar 2025; UNVERIFIED); Telenor's percentage of Telenor Thailand Investments not stated",
                     note=TRUE_HOLDERS_NOTE)],
         gov_note=("True's 2025 financial statements describe True as controlled by the CP Group and Telenor Group (via search). The "
                   "China Mobile holder's name differs between sources (China Mobile International Holdings Limited vs China Mobile "
                   "Communications Group Co., Ltd.); coded through China Mobile Limited as in batch 3"),
         gov_dropped=['National Telecom Public Company Limited (Thai state-owned) 2.39% of True Corporation (7 Mar 2025; UNVERIFIED; board seat not checked)',
                      FOLKETRYGD_DROP],
         core=ND("Ericsson's 100th-5G-agreement release does not say True's contract includes core; no 5G core vendor named"),
         first_contract=ND("Ericsson's selection was announced 27 Apr 2020, but the rollout began in Mar 2020 'immediately following "
                           "Ericsson's selection', so the selection/contract date is earlier and not stated"),
         vendor_operates=V(True, 'https://www.ericsson.com/496069/assets/local/managed-services/documents/ericsson-trueco.pdf',
                           "Ericsson case study (2025, via search): Ericsson is True's 'operations partner', covering network-operation "
                           "transformation and operations after the DTAC merger; Ericsson's managed-services page lists network and IT "
                           "operations and field maintenance for True. UNVERIFIED: ericsson.com returned 403; start date not stated")),
    dict(region='Asia-Pacific', country='Thailand', operator_name='AIS',
         name_note='Advanced Info Service Public Company Limited',
         share=ND(TH_SHARE_NOTE + ". AIS's FY2025 results say 'AIS achieved a market share of 50%' right after its mobile revenue figure "
                  "(verified), without saying the basis or period, so it is not coded as a subscription share; AIS reports 46 million mobile "
                  "subscribers (AGM 2026 minutes)"),
         launch=V(2020, 'https://investor.ais.co.th/en/our-company/milestones/2020-ongoing',
                  "AIS milestones: '5G NSA licensed service ... was launched in February 2020 nationwide in the 2600 MHz frequency band'; "
                  "5G SA from July 2020 (verified). AIS elsewhere dates the launch 21 Feb 2020"),
         ran5=[], ran5_note=("no 5G RAN vendor named. AIS's 2024 report says it 'primarily uses network equipment from ... Huawei and ZTE' "
                             "without a generation or network element; the ZTE strategic cooperation (A-Z Center, Jun 2022) is an "
                             "innovation partnership, not a RAN supply statement"),
         ran4=[], ran4_note="AIS's 2020-21 reports list Huawei, Nokia and ZTE as 'key network equipment' vendors without a generation",
         gov=[G('Singapore', 'Temasek Holdings', 'state_holding_company', 50.55, 'Singtel', 'via_parent', '2026-06-30',
                'https://cdn1.singteldigital.com/content/dam/singtel/investorRelations/annualReports/2026/Letter-to-Shareholders.pdf',
                ("same figure as coded for Singtel in batch 1 and for Telkomsel in batch 4. holder_type is a researcher classification; the "
                 "state link comes from data/state_holders.csv (wholly owned by the Minister for Finance)"),
                link='reference_list', parent_pct=23.32,
                chain=("Singtel 23.32% of AIS, 4.22% of it held under Raffles Nominees (Singtel SGX announcement, 28 Feb 2025: 'its "
                       "shareholding in AIS remains unchanged at 23.32%'; verified)"))],
         gov_note=("Gulf Development Public Company Limited (~40.44%, successor to Intouch from 1 Apr 2025) is not identified as a state "
                   "entity; no Thai state holder at 5% or more found"),
         gov_dropped=[],
         core=ND("AIS said on 14 Jul 2020 it was still choosing its 5G core supplier among Ericsson, Nokia, Huawei, ZTE and Samsung; the "
                 "winner is not named"),
         first_contract=ND('the ZTE comprehensive strategic cooperation agreement (10 Jun 2022) is a cooperation agreement and post-dates '
                           'the Feb 2020 launch; no earlier dated contract found'),
         vendor_operates=ND("Ericsson's 2006 GSM/EDGE turnkey build is network construction, not managed operations")),
    # ------------------------------------------------------------------ Bangladesh
    dict(region='Asia-Pacific', country='Bangladesh', operator_name='GP',
         name_note='Grameenphone Ltd.',
         share=V(45.3, 'https://cdn01da.grameenphone.com/sites/default/files/2026-03/16.%20Directors%E2%80%99%20Report.pdf',
                 ("Grameenphone annual report 2025, Directors' Report: end-of-year market share 45.3% (FY2025; 45.1% FY2024), 'Market "
                  "share based on BTRC published information'; 83.9m subscribers (verified). BTRC's own operator table could not be "
                  "fetched (timeouts)"), 2025),
         launch=V(2025, 'https://www.grameenphone.com/about/media-center/press-release/grameenphone-launches-5g-all-divisional-headquarters-first-telecom',
                  "Grameenphone (1 Sep 2025): 'commercial launch of its 5G services in all divisional headquarters' (verified); Robi "
                  "launched about two hours earlier the same day"),
         ran5=[], ran5_note=("no 5G RAN vendor named; Huawei (Dhaka) and ZTE (Chattogram) supported the Jul 2022 5G trials, and the 2025 "
                             "Rakuten Symphony Open RAN work is a pilot; neither is coded"),
         ran4=[], ran4_note="Nokia/Huawei RAN and a ZTE-over-Huawei SRAN swap appear only in a personal LinkedIn profile (not cited)",
         gov=[norway("Telenor ASA -> Telenor Mobile Communications AS 55.80% of Grameenphone (pattern of shareholding at 31 Dec 2025, GP "
                     "annual report 2025; verified); Telenor's percentage of Telenor Mobile Communications not stated",
                     note="Telenor's 2025 annual report rounds the state's stake to 54%")],
         gov_note="Grameen Telecom 34.20% (not-for-profit, not identified as a state entity); no Bangladeshi state holder found",
         gov_dropped=[FOLKETRYGD_DROP],
         core=ND('no source names the 5G core or NSA EPC vendor'),
         first_contract=ND('only the Jul 2022 trials (Huawei, ZTE) are dated; no vendor contract found'),
         vendor_operates=ND("Wipro's managed services (2017, 2021) cover IT and network management; Wipro is not a network-equipment vendor")),
    dict(region='Asia-Pacific', country='Bangladesh', operator_name='Robi',
         name_note='Robi Axiata PLC',
         share=ND("no BTRC operator figure retrieved (BTRC pages timed out); Robi had 57.40m subscriptions in Dec 2025 per an analyst site "
                  "(not cited), and Grameenphone's BTRC-based 45.3% is the only verified share for 2025"),
         launch=V(2025, 'https://www.samenacouncil.org/samena_daily_news?news=107225',
                  "SAMENA Daily (3 Sep 2025): 'Robi Axiata PLC has officially become the first mobile operator in Bangladesh to launch "
                  "commercial 5G services', live in parts of Dhaka, Chattogram and Sylhet (verified); Robi's company profile dates it 1 Sep 2025"),
         ran5=[R(v, 'not_disclosed', 'https://www.samenacouncil.org/samena_daily_news?news=107225',
                 "Acting CEO 'credited government support and partnerships with Ericsson and Huawei for enabling the rollout' (verified); "
                 "the network element is not stated and there is no split (coded as batch 3's Econet row)") for v in ('Ericsson', 'Huawei')],
         ran4=[], ran4_note=("Huawei/Ericsson 4G site counts and NSN-to-Ericsson / Alcatel-to-Ericsson BTS swaps appear only in personal "
                             "LinkedIn profiles (not cited)"),
         gov=[G('Malaysia', 'Khazanah Nasional Berhad', 'sovereign_wealth_fund', 36.69, 'Axiata Group Berhad', 'via_parent', '2026-03-31',
                AXIATA_OVERVIEW,
                "Axiata's audited statements call Khazanah 'the sovereign wealth fund of the Government of Malaysia' (36.71% direct in the "
                "narrative; 36.69% in the 31 Mar 2026 shareholding table); same basis as batch 3 (Dialog) and batch 4 (XLSmart)",
                link_url=AXIATA_AFS, parent_pct=61.82,
                chain='Axiata Group Berhad 61.82% of Robi Axiata PLC (Robi company profile, via search; the page is script-rendered, not re-verified)'),
              G('Malaysia', 'Employees Provident Fund Board (EPF)', 'pension_fund', 19.36, 'Axiata Group Berhad', 'via_parent', '2026-03-31',
                AXIATA_OVERVIEW,
                "Axiata IAR2025 shareholding structure as at 31 Mar 2026 (Overview document, PDF p.2); an EPF representative director "
                "sits on Axiata's board (exp|supp|axiata-holders). Pension rule: established by the Employees Provident Fund Act 1991 "
                "(Act 452), Board appointed by the Minister (as batch 3's Dialog row)",
                parent_pct=61.82, chain='Axiata Group Berhad 61.82% of Robi Axiata PLC (Robi company profile)', board_seat='yes')],
         gov_note=("Permodalan Nasional Berhad (18.28% of Axiata at 31 Mar 2026) and Amanah Saham Bumiputera (12.48%, 28 Nov 2025) are "
                   "not coded: unit-trust managers, not pension funds, and not described as state-owned. Bharti International "
                   "(Singapore) holds 28.18% of Robi; " + BHARTI_OPEN),
         gov_dropped=['Kumpulan Wang Persaraan (Diperbadankan) (KWAP) 2.49% of Axiata Group Berhad (2025-11-28; Malaysian public-service '
                      'pension fund, not in the pension-fund registry, rule not assessed; board seat not checked)',
                      'Lembaga Tabung Haji 1.09% of Axiata Group Berhad (2025-11-28; statutory pilgrims fund; board seat not checked)'],
         core=ND('the Ericsson/Huawei partnerships are not split between RAN and core; no 5G core vendor named'),
         first_contract=ND('no dated 5G vendor contract found'),
         vendor_operates=ND('a Robi managed-service project appears only in a personal LinkedIn profile; Route Mobile (2023) manages RCS '
                            'business messaging, not the network')),
    # ------------------------------------------------------------------ Brunei
    dict(region='Asia-Pacific', country='Brunei', operator_name='UNN',
         name_note='Unified National Networks Sdn Bhd (single wholesale mobile network; retail via DST, imagine and Progresif)',
         share=ND('not applicable: UNN is the single wholesale network and has no retail subscribers; AITI publishes no operator shares'),
         launch=V(2023, 'https://aiti.gov.bn/news/2023/5th-generation-5g-mobile-services-now-available-nationwide/',
                  "AITI/UNN/DST/imagine/Progresif joint press release (22 Jun 2023): '5G services is now available, starting on 22 June "
                  "2023' nationwide (verified)"),
         ran5=[R('Huawei', 'not_disclosed', 'https://digitalmag.theceomagazine.com/advertorial-huawei-technologies-brunei/',
                 "Huawei advertorial (CEO Magazine, undated), per the search: Huawei partners with UNN and supports the launch of Brunei's "
                 "5G network. UNVERIFIED: the page returned 403; RAN not stated explicitly and no share")],
         ran5_note="UNN's Single RAN rollout began Sep 2020; no source names the radio vendor",
         ran4=[],
         ran4_note="Juniper supplies IP/MPLS and RAN-aggregation routers, not radio equipment",
         gov=[G('Brunei', "His Majesty's Government of Brunei Darussalam", 'government_ministry', 100.0, 'Unified National Networks Sdn Bhd',
                'direct', '2026-11-26', 'https://unn.com.bn/index.php/about',
                ("UNN: 'an organization 100% wholly owned by His Majesty's Government of Brunei Darussalam, and recognized as a "
                 "Government-Linked company under Darussalam Assets Sdn Bhd' (verified)"))],
         gov_note=("held through Darussalam Assets Sdn Bhd, Brunei's state investment holding company, whose shareholder is the Minister "
                   "for Finance Corporation (US State Department 2026 Investment Climate Statement, via search; 403 on re-fetch); the "
                   "holding percentages along that chain are not stated, so Darussalam Assets is not coded as a separate row"),
         gov_dropped=[],
         core=ND("UNN calls Ericsson a 'major strategic supplier' for significant parts of its fixed and mobile core (IMS named), but no "
                 "source names the 5G core or NSA EPC vendor"),
         first_contract=ND('no dated 5G vendor contract found'),
         vendor_operates=ND('BICS manages roaming services (May 2021), not the network')),
]
