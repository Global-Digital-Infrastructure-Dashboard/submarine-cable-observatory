"""Researcher coding of expansion batch 5 (Africa: Uganda, Mozambique, Botswana, Madagascar, Nigeria; 10 operators), coded
in-session on 2026-11-26 from the cached v2 searches in data/5g_expansion_searches.jsonl under Prof. Shen's revised schema
(schema.py). Values come only from the cited source; anything a source didn't state is not_disclosed. Share categories,
computed figures and government stake percentages were checked against the primary page at coding time; the per-fact log
is 5g_expansion/verify_2026-11-26_batch5.csv (fetched copies in data/5g_direct/).
Not cited at all: Wikipedia, personal LinkedIn profiles, Scribd, eSIM/aggregator sites.

Batch notes:
- Shared parent groups follow the templates of the earlier batches: MTN opcos carry the GEPF row (19.94% of MTN Group,
  MTN FY2025 annual financial statements p.146) as in batch 4's MTN Irancell row, with MTN Group's own percentage of the
  opco from the same statements; Airtel opcos follow batch 1's Airtel Kenya row (no state holder at 5%; Qatar Holding and
  NBIM listed in gov_dropped); Vodacom Mozambique follows batch 1's Safaricom row (e& via Vodafone) and adds GEPF's 12.24%
  of Vodacom Group from Vodacom's 2025 AGM notice; Orange Botswana follows the Orange S.A. rows (French State + Bpifrance).
- Pension-style holders outside the PENSION_FUNDS registry are not coded (Prof. Shen's rule needs the fund's own site or
  law): Uganda's National Social Security Fund (10.547% of Airtel Uganda) and the Botswana Public Officers Pension Fund
  (controls Deci Investments, Mascom's 60% holder). Both are described in gov_note.
- Nigeria: NCC's 2025 annual report (Table 4.2) labels Airtel 22,225,610 (12.39%) and Glo 60,893,280 (33.94%), the reverse of
  every earlier NCC table (Dec 2024: Airtel 34.39%, Glo 12.23%); Airtel is coded from the Dec 2024 report, MTN from 2025.
- Mozambique: Tmcel only pre-launched 5G (25 Mar 2022) and INCM first awarded 5G spectrum to all three operators in Jun 2026,
  so Tmcel's launch is not_disclosed (sample status for a researcher decision).
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-26'

register(domains={
    'government': ['ncc.gov.ng', 'incm.gov.mz', 'bocra.org.bw', 'ucc.co.ug', 'worldbank.org'],
    'company': ['mtn.com', 'mtn-investor.com', 'mtn.co.ug', 'vodacom.com', 'yas.mg', 'airtel.in', 'airtel.co.ug', 'huawei.com',
                'innovis.in', 'mcom.ng'],
    'news': ['sdxcentral.com', 'techjaja.com', 'riotimesonline.com', '360mozambique.com', 'ecofinagency.com', 'connectingafrica.com',
             'technext24.com', 'techreviewafrica.com', 'techcabal.com', 'mobileworldlive.com'],
    'research_industry_group': ['hammergp.com'],
})

NBIM = 'https://www.nbim.no/api/investments/v2/report/?assetType=eq&date=2025-12-31&fileType=xlsx'
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
E_AND_NOTE = ("the Vodafone filing names e& but does not call it state-owned; e&'s 2025 integrated annual report gives the "
              "Emirates Investment Authority 60% and says the EIA is ultimately controlled by the UAE Federal Government")
ORANGE_XLSX = 'https://assets.orange.com/pm_12751_545_545865-jr7yvi3osw.xlsx'

# MTN Group (GEPF row as in batch 4's MTN Irancell; opco percentages from the same FY2025 statements).
MTN_AFS = 'https://www.mtn.com/wp-content/uploads/2026/03/MTN-Group-FY-25-Annual-Financial-Statements.pdf'
GEPF_NOTE = ("MTN FY2025 annual financial statements, p.146, beneficial shareholders of 5% or more (19.44% in 2024). Coded under "
             "Prof. Shen's pension rule (2026-11-26): GEPF is governed by the Government Employees Pension Law 1996 and manages "
             "pensions for government employees (GEPF website)")
MTN_DATA = 'https://www.mtn-investor.com/reporting/annuals-2025/pdf/data-sheets-spreads.pdf'
AIRTEL_DROPPED = ["Qatar Holding LLC 3.67% of Airtel Africa plc (2025-03-31; no Qatar nominee on the Airtel Africa board per the 2025 annual report and leadership page)",
                  'Norges Bank Investment Management 0.39% of Airtel Africa plc (2025-12-31; board seat not checked)',
                  'Norges Bank Investment Management 1.06% of Bharti Airtel Ltd (2025-12-31; board seat not checked)']
AIRTEL_SINGTEL = ("OPEN (as for batch 1's Airtel Kenya): Bharti Airtel's foreign promoter group (Singtel/Pastel) is not identified "
                  "in a current filing, so a Singtel stake in Bharti could not be coded")
# Uganda
UG_LAUNCH = 'https://www.sdxcentral.com/news/mtn-wins-5g-launch-race-in-uganda-with-airtel-not-far-behind/'
# Mozambique: INCM Communications Regulation Report 2024, p.41 (computed by the researcher).
MZ_SHARE = 'https://www.incm.gov.mz/wp-content/uploads/2026/10/Relatorio-de-Regulacao-2024-Versao-ENG.pdf'
MZ_NOTE = ('computed from INCM Communications Regulation Report 2024 (p.41), active mobile voice subscribers in 2024: Vodacom '
           '8,589,615; Movitel 7,156,826; Tmcel 1,373,456; total 17,119,897 (INCM rounds to ~50 / 42 / ~8%)')
MZ_SPECTRUM = ("INCM awarded 5G spectrum (700 MHz, 2.6 GHz, 3.5 GHz) to Tmcel, Vodacom and Movitel only in Jun 2026 (SAMENA/Extensia, "
               "29 Jun 2026: 'The country has until now relied primarily on 3G and 4G services')")
VODACOM_AGM = 'https://www.vodacom.com/pdf/agm/2025/notice-of-annual-general-meeting-2025.pdf'
VODACOM_MZ_CHAIN = ("Vodacom Group Limited -> Vodacom Mozambique (Vodacom Group's percentage not confirmed from a primary source; the "
                    "search gives 85%)")
TMCEL_GOV = 'https://www.riotimesonline.com/mozambique-tmcel-stake-sale-2026/'
TMCEL_GOV_NOTE = ("Rio Times (14 Aug 2026): 'The government holds about 66% of Tmcel directly, with the state asset institute IGEPE "
                  "holding a further 26% and former employees of the two predecessor companies the remaining 8%'; same split in "
                  "360 Mozambique / Diario Economico (25 Aug 2026). No official filing found; percentages are approximate")
# Botswana: BOCRA State of ICTs (March 2026), p.17.
BW_SHARE = 'https://www.bocra.org.bw/sites/default/files/sites/default/files/documents/State_of_ICTs,_2026_(v2.pdf'
BW_NOTE = ("BOCRA, State of ICTs in Botswana (Mar 2026) p.17, mobile telephony subscriptions at Sep 2025 (4,370,350 in total): "
           "Orange 45, Mascom 40, BTC Mobile 15. MTN's FY2025 data sheets give Mascom 40.8%")
ORANGE_URD = 'https://assets.orange.com/medias/domain12751/media101746/523989-ffp7njes6v-75.pdf'
ORANGE_BW_CHAIN = 'Orange S.A. -> 73.68% of Orange Botswana (2025 URD p.32; intermediate holding entities not stated)'
# Madagascar
TELMA_LAUNCH = 'https://www.connectingafrica.com/document.asp?doc_id=762095'
# Nigeria
NCC_2025 = 'https://ncc.gov.ng/sites/default/files/2026-11/2025-Annual-Report-and-Accounts.pdf'
NCC_2024 = 'https://ncc.gov.ng/media/3817/view'
NG_NOTE = ("NCC Annual Report 2025, Table 4.2 (p.18), share of mobile GSM subscriptions at Dec 2025: MTN 93,064,952 (51.87%). The "
           "same table labels Airtel 22,225,610 (12.39%) and Glo 60,893,280 (33.94%), the reverse of NCC's Dec 2024 figures "
           "(Airtel 34.39%, Glo 12.23%), so the Airtel/Glo columns look swapped")
MTN_NG_LAUNCH = 'https://www.lightreading.com/5g/mtn-nigeria-and-ericsson-launch-5g-services'
AIRTEL_NG_FS = 'https://assets.airtel.in/teams/simplycms/ADTECH/docs/Airtel_Networks_Limited.pdf'

CHECKED_NOT_ADDED = {}

OPERATORS = [
    # ------------------------------------------------------------------ Uganda
    dict(region='Africa', country='Uganda', operator_name='MTN', name_note='MTN Uganda Limited',
         share=V(63.0, MTN_DATA,
                 "MTN's own FY2025 data sheets (market analysis, p.35): MTN Uganda market share 63.0%, position 1 of 5 (measure not "
                 "defined; company figure, verified). UCC publishes only national totals (47.1m active mobile subscriptions, Dec 2025)", 2025),
         launch=V(2023, UG_LAUNCH,
                  "SDxCentral (31 Jul 2023): 'MTN launched the service first, doing so Friday, July 28, in the Kampala districts of Lugogo and "
                  "Bugoloobi' (verified); MTN Uganda's FY2023 earnings release: 'the first network to go live on 5G', 37 sites by year-end. "
                  "ZTE's Jan 2020 5G SA network was a trial"),
         ran5=[], ran5_note=("no 5G RAN vendor named: ZTE supplied the 2020 5G trial (MTN Uganda 2021 annual report); the 37 (2023) and "
                             "538 (2024) 5G sites have no named supplier"),
         ran4=[], ran4_note='no 4G RAN vendor named in MTN Uganda reports; Huawei appears only as the core-modernisation partner',
         gov=[G('South Africa', 'Government Employees Pension Fund (GEPF)', 'pension_fund', 19.94, 'MTN Group Limited', 'via_parent',
                '2025-12-31', MTN_AFS, GEPF_NOTE, parent_pct=76.02,
                chain=("MTN Group 76.02% of MTN Uganda Limited after the 2025 localisation sale (83.05% before; non-controlling "
                       "interests 23.98%; FY2025 statements note 9.4.1.4 and 9.5)"))],
         gov_note=("no Ugandan state holder found: MTN Uganda's FY2025 annual report says 94.5% of shareholders are local without "
                   "naming a state holder at 5% or more"),
         gov_dropped=[],
         core=V('Huawei', 'https://techjaja.com/huawei-to-build-mtn-ugandas-5g-core-network/',
                "Techjaja (10 Jan 2023): five-year strategic partnership with Huawei 'to transform and modernize its network towards a "
                "Cloud-native 5G-Capable Core network' (MUNA project), overseen by Huawei (verified); Hammer GP (2025) also says MTN "
                "engaged Huawei for a 5G-capable core. ZTE's 5G Common Core was for the 2020 trial only"),
         first_contract=V('2023-01-10', 'https://techjaja.com/huawei-to-build-mtn-ugandas-5g-core-network/',
                          "announcement of the Huawei 5G core partnership ('This 5G partnership dubbed MUNA project'); MTN Uganda's 2022 "
                          "annual report reports entering it during 2022 without a signing date. The ZTE 5G SA network (21 Jan 2020) was a trial"),
         vendor_operates=ND("Huawei 'oversees' the core-modernisation project (implementation, not network operation); ZTE's O&M "
                            "services since 2009 (ZTE, Jan 2020) are undated and unscoped; Ericsson's 2014 MTN managed-services deal "
                            "is not shown to cover Uganda")),
    dict(region='Africa', country='Uganda', operator_name='Airtel', name_note='Airtel Uganda Limited',
         share=ND("UCC publishes national totals only (47.1m active mobile subscriptions, Dec 2025), no operator shares; MTN's own "
                  "data sheets give MTN 63.0% of a five-operator market"),
         launch=V(2023, UG_LAUNCH,
                  "SDxCentral (31 Jul 2023): Airtel 'followed suit over the weekend' after MTN's 28 Jul 2023 launch (verified); Airtel's "
                  "5G FAQ and Watchdog Uganda give 7 Aug 2023 with 50 sites around Kampala"),
         ran5=[], ran5_note='Airtel Uganda annual reports give 50 5G sites (Aug 2023) and 150 more (2024) without naming suppliers',
         ran4=[R('Nokia', 'not_disclosed', 'https://www.hammergp.com/ugandas-telecom-landscape-in-the-era-of-402-tbps-gaps-gains-and-growth-potential/',
                 "Hammer GP (2025): 'Airtel Uganda's radio access network was built on a mix of Nokia, Huawei and ZTE equipment "
                 "(originally also Ericsson)' (verified); the RAN as a whole, no generation named"),
               R('Huawei', 'not_disclosed', 'https://www.hammergp.com/ugandas-telecom-landscape-in-the-era-of-402-tbps-gaps-gains-and-growth-potential/', 'same sentence'),
               R('ZTE', 'not_disclosed', 'https://www.hammergp.com/ugandas-telecom-landscape-in-the-era-of-402-tbps-gaps-gains-and-growth-potential/', 'same sentence')],
         ran4_note=("the source describes the whole RAN, so it is coded to 4G only (Airtel Uganda has been 100% 4G since 2019); "
                    "Ericsson 'originally' is not dated and no switch is stated, so no switch row"),
         gov=[G('Uganda', 'National Social Security Fund (Uganda)', 'pension_fund', 10.547, 'Airtel Uganda Limited', 'direct', '2024-12-31',
                'https://cdn-webportal.airtelstream.net/website/uganda/assets/pdf/Airtel-Annual-Report-2024.pdf',
                "Airtel Uganda annual report 2024, pp.28 and 53: 4,218,800,000 shares, 10.5470% (verified); the report calls NSSF 'a "
                "National savings scheme mandated by Government'. Pension rule (2026-11-26): the Minister of Gender, Labour and Social "
                "Development appoints the NSSF board (nssfug.org, Sep 2024)")],
         gov_note="Bharti Airtel Uganda Holdings B.V. holds 89.1102%. " + AIRTEL_SINGTEL,
         gov_dropped=AIRTEL_DROPPED,
         core=ND("Innovis says Airtel Uganda's core network was Huawei, but not the 5G core; no 5G core vendor named"),
         first_contract=ND('Airtel launched 5G days after its Jul 2023 spectrum award; no vendor or contract date named'),
         vendor_operates=V(True, 'https://www.economictimes.indiatimes.com/industry/telecom/bharti-airtel-in-pact-with-nokia-siemens-networks-for-network-expansion-in-africa/printarticle/10170059.cms',
                           "Bharti Airtel's 2011 agreement with Nokia Siemens Networks covers Uganda and six other African countries, with NSN "
                           "managing network operations; Innovis (Nokia's subcontractor) reports a five-year Airtel Uganda managed-services "
                           "contract from Mar 2013, extended four years in Mar 2018. Whether it continued after ~2022 is not found")),
    # ------------------------------------------------------------------ Mozambique
    dict(region='Africa', country='Mozambique', operator_name='Vodacom', name_note='Vodacom Mozambique (Vodacom Moçambique, S.A.)',
         share=V(50.17, MZ_SHARE, MZ_NOTE, 2024),
         launch=V(2023, 'https://www.samenacouncil.org/samena_daily_news?news=95230',
                  "SAMENA Daily (3 May 2023, from Developing Telecoms): 'Vodacom has become the first operator in Mozambique to launch "
                  "commercial 5G, with its network now available in Maputo City' (verified). " + MZ_SPECTRUM),
         ran5=[], ran5_note=("no Mozambique-specific 5G RAN vendor named; Nokia's Oct 2025 Vodafone/Vodacom AirScale extension and the "
                             "Vodafone-group RAN refresh (Ericsson, Huawei, Nokia, Samsung) are not attributed to Mozambique"),
         ran4=[], ran4_note=("the 4G Open RAN trial (Parallel Wireless, Mavenir, CrowdCell, Lime Microsystems) was a trial, not a "
                             "commercial deployment"),
         gov=[G('South Africa', 'Government Employees Pension Fund (GEPF)', 'pension_fund', 12.24, 'Vodacom Group Limited', 'via_parent',
                '2025-03-31', VODACOM_AGM,
                "Vodacom notice of AGM 2025 (dated 6 Jun 2025, JSE 11.26 major shareholders): 'Government Employee Pension Fund (GEPF) "
                "254 385 551 12.24' (verified). Coded under Prof. Shen's pension rule (2026-11-26): GEPF covers government employees "
                "under the Government Employees Pension Law 1996 (GEPF website)", chain=VODACOM_MZ_CHAIN),
              G('United Arab Emirates', 'e& (Emirates Telecommunications Group)', 'state_owned_company', 17.005026, 'Vodafone Group Plc',
                'via_parent', '2026-03-31', VODAFONE_AR, E_AND_NOTE, link_url=E_AND_AR,
                chain=("Vodafone Group Plc -> Vodacom Group 65.10% (Vodafone Investments SA 46.55% + Vodafone International Holdings "
                       "18.55%, Vodacom AGM notice 2025) -> Vodacom Mozambique (percentage not confirmed; the search gives 85%)"))],
         gov_note=("Vodacom Group's percentage of Vodacom Mozambique and the holders of the remainder were not found in a primary "
                   "source, so no Mozambican state holder could be checked. YeboYethu (5.51% of Vodacom Group) is a BEE vehicle, not "
                   "identified as a state entity. The batch-1 Safaricom row has no GEPF row; the same 12.24% applies to it (see report)"),
         gov_dropped=["Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; NBIM's file shows 1.56% at 2025-12-31; board seat not checked)"],
         core=ND("no Mozambique core vendor named; Vodacom's 'best technology' page says only that the group's mobile core is 5G-ready"),
         first_contract=ND('no 5G vendor contract date found'),
         vendor_operates=ND('the VMware case study covers virtualisation support, not network operation')),
    dict(region='Africa', country='Mozambique', operator_name='Tmcel',
         sample_status='pilot_only',
         sample_status_note=('outside the main sample (researcher decision 2026-11-26, same logic as Ukraine): only a 5G pre-launch '
                             '(25 Mar 2022), and INCM first awarded 5G spectrum in Jun 2026; data kept for reintroduction'),
         name_note='Moçambique Telecom, S.A. (Tmcel); the 5G list spells it Tmcell',
         share=V(8.02, MZ_SHARE, MZ_NOTE + '; Tmcel had 21% in 2020 and 3% in 2023 (INCM)', 2024),
         launch=ND("only a 5G 'pre-launch' in Maputo on 25 Mar 2022 with Huawei (360 Mozambique, verified); Ecofin (1 Apr 2022) says "
                   "commercial deployment would follow 'in the next few months' (verified), but no commercial launch date is found. "
                   + MZ_SPECTRUM),
         ran5=[R('Huawei', 'not_disclosed', 'https://360mozambique.com/business/companies/tmcel-launches-5g-technology-in-partnership-with-chinas-huawei/',
                 "360 Mozambique (28 Mar 2022): 5G pre-launch 'held in partnership with Huawei, a Chinese company that is implementing the "
                 "project' (verified); Ecofin: commercial 5G deployment 'with the technical expertise of China's Huawei'; pre-commercial, no share")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.ecofinagency.com/telecom/3101-43368-mozambique-tmcel-begins-phase-ii-of-the-telecom-network-upgrade-process',
                 "Ecofin (31 Jan 2022): phase II of the network modernisation will 'extend 4G and 4.5G technologies throughout the "
                 "country' relying on Ericsson, under a five-year agreement signed Nov 2020 (verified)")],
         ran4_note=("Huawei 2G-4G equipment appears only in a personal profile (not cited). WRONG IN SEARCH: samenacouncil news=111258 "
                    "(cited for the Ericsson phase II) is a 2026 spectrum-award story"),
         gov=[G('Mozambique', 'Government of the Republic of Mozambique', 'government_ministry', 66.0, 'Tmcel', 'direct', '2026-08-14',
                TMCEL_GOV, TMCEL_GOV_NOTE, board_seat='not_checked'),
              G('Mozambique', 'Instituto de Gestão das Participações do Estado (IGEPE)', 'state_holding_company', 26.0, 'Tmcel', 'direct',
                '2026-08-14', TMCEL_GOV,
                "described as 'the state asset institute' (Rio Times) and 'the Institute for State Shareholding Management' (360 "
                "Mozambique); IGEPE has run Tmcel under intervention since Mar 2023. " + TMCEL_GOV_NOTE)],
         gov_note=("never summed: 66% (state, direct) and 26% (IGEPE) are separate rows. In Aug 2026 the cabinet authorised talks on "
                   "selling a stake to a strategic investor (percentage not announced)"),
         gov_dropped=[],
         core=ND('Huawei implemented the 5G pre-launch project, but no source names the 5G core or NSA EPC vendor'),
         first_contract=ND("Ecofin: 'In June 2021, a USD 23 million expansion contract was signed with Huawei to test the 5G in Maputo' "
                           "(verified); a contract to test 5G is a trial, not a 5G deployment contract"),
         vendor_operates=ND("Ericsson's Oct 2024 OSS/BSS deal leaves Tmcel to self-manage the platforms; no managed-services contract found")),
    # ------------------------------------------------------------------ Botswana
    dict(region='Africa', country='Botswana', operator_name='Mascom', name_note='Mascom Wireless Botswana (Pty) Ltd',
         share=V(40.0, BW_SHARE, BW_NOTE, 2025),
         launch=V(2022, 'https://www.samenacouncil.org/samena_daily_news?news=88829',
                  "SAMENA Daily (27 Feb 2022): 'Mascom Botswana has launched its first 5G services in the capital Gaborone' with 111 "
                  "sites planned by year-end (verified)"),
         ran5=[], ran5_note=("no 5G RAN vendor named; the search's 'Ericsson preferred partner for Botswana' comes from a 2022 article "
                             "about MTN Nigeria and is not coded"),
         ran4=[], ran4_note="no 4G RAN vendor named ('Huawei LTE Wingle' on Mascom's site is a customer device)",
         gov=[G('South Africa', 'Government Employees Pension Fund (GEPF)', 'pension_fund', 19.94, 'MTN Group Limited', 'via_parent',
                '2025-12-31', MTN_AFS, GEPF_NOTE,
                chain=("MTN Group effective interest 53.1% in Mascom (joint venture, FY2025 statements p.113), held through Mobile "
                       "Botswana and MTN's 33.3% of Deci Investments, Mascom's holding company"))],
         gov_note=("Botswana Public Officers Pension Fund (BPOPF) controls Deci Investments (about 66.7%; Mobile Botswana, an MTN "
                   "subsidiary, holds about 33.3%), which holds 60% of Mascom (Competition and Consumer Authority merger notice "
                   "03/2023, via search). NOT CODED: checked 2026-11-26 against Prof. Shen's pension rule and it does not meet it as "
                   "written: BPOPF was 'created in accordance with the provisions of the Pensions and Provident Fund Act, 1987' (a "
                   "general registration law, not its own founding law), and the government nominates 5 of its 13 trustees, not the "
                   "board (bpopf.co.bw). Econet Wireless (about 40% of Mascom per the same notice) is not identified as a state entity"),
         gov_dropped=[],
         core=ND('no source names the 5G core vendor (Huawei core work appears only in a personal profile)'),
         first_contract=ND('launch Feb 2022; no vendor contract date'), vendor_operates=ND()),
    dict(region='Africa', country='Botswana', operator_name='Orange', name_note='Orange Botswana (Pty) Ltd',
         share=V(45.0, BW_SHARE, BW_NOTE + "; BOCRA's 2024 annual report gives Orange 43% at Mar 2024", 2025),
         launch=V(2022, 'https://www.orange.com/en/press-release/orange-launches-its-commercial-5g-network-in-botswana-the-first-orange-country-in-africa-to-launch-5g-technology-233585',
                  'commercial 5G launched 11 Nov 2022 in greater Gaborone and Francistown (~30% of the population); first Orange country in Africa'),
         ran5=[R('Huawei', 'not_disclosed', 'https://developingtelecoms.com/telecom-technology/wireless-networks/14205-botswana-becomes-orange-s-commercial-5g-launch-in-africa.html',
                 "Developing Telecoms on the 5G launch (Nov 2022), citing Orange MEA: 'Orange is uing RAN equipment from Huawei in Botswana "
                 "while tapping Ericsson for the core network' (verified); no share wording")],
         ran4=[], ran4_note='Huawei and Ericsson 4G equipment appear only in a personal profile (not cited)',
         gov=[G('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX,
                '21.04% of voting rights', chain=ORANGE_BW_CHAIN),
              G('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX,
                "8.00% of voting rights; Orange's file groups it with the French State as the public sector", chain=ORANGE_BW_CHAIN)],
         gov_note='the 26.32% outside Orange is described only as private investors; no Botswana state holder found',
         gov_dropped=['Norges Bank Investment Management 1.76% of Orange S.A. (2025-12-31; voting 0.00%; board seat not checked)'],
         core=V('Ericsson', 'https://developingtelecoms.com/telecom-technology/wireless-networks/14205-botswana-becomes-orange-s-commercial-5g-launch-in-africa.html',
                "same sentence: 'tapping Ericsson for the core network' at the 5G launch (verified); 5GC vs NSA EPC not stated"),
         first_contract=ND('commercial launch 11 Nov 2022; no vendor contract date'),
         vendor_operates=V(True, 'https://developingtelecoms.com/telecom-technology/customer-management/5507-orange-botswana-partners-with-ericsson-to-improve-quality-of-service.html',
                           'multi-year managed-services agreement announced 10 Oct 2014: Ericsson manages network operations and field '
                           'maintenance; end date not found')),
    # ------------------------------------------------------------------ Madagascar
    dict(region='Africa', country='Madagascar', operator_name='Telma', name_note='Telma (Telecom Malagasy; Axian group, brand Yas)',
         share=V(46.39, 'https://openknowledge.worldbank.org/server/api/core/bitstreams/edae10ff-b1ce-5507-981a-08abd91d70fc/content',
                 ("computed from the World Bank's Madagascar Digital Economy Assessment, footnote 10: 'There are 4.5 million Telma Mobile "
                  "subscribers, against 2.6 million for Orange and 2.6 million for Airtel in 2018 (Source: ARTEC)'; rounded millions, "
                  "three operators only. No newer ARTEC operator figures found"), 2018),
         launch=V(2020, TELMA_LAUNCH,
                  ("DISPUTED between Telma/Ericsson and ARTEC; coded Telma/Ericsson. Connecting Africa (1 Jul 2020): 'Telma Madagascar has "
                   "become the first operator to launch a 5G commercial network', live in Antananarivo and Toamasina (verified; Ericsson "
                   "says live 26 Jun 2020, page 403). Ecofin (27 Jul 2020): ARTEC suspended the network and sealed the equipment, saying "
                   "Telma had only 'a temporary authorization to experiment with the technology for one month', indoors (verified). "
                   "No later authorised relaunch date found")),
         ran5=[R('Ericsson', 'not_disclosed', TELMA_LAUNCH,
                 "'The 5G network is powered by Ericsson equipment'; 'using the latest radio access and transport products from the "
                 "Ericsson Radio System portfolio' on 3.6-3.7 GHz (verified); no share wording")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://services.yas.mg/data/corporate/2019_en.pdf',
                 "Telma corporate review 2019, p.25: contract signed 12 Jul 2019 with Ericsson 'for the purpose of covering the entire "
                 "country within 4 years', >700 new sites 'rapidly deployed in 4G+' (US$100m, 2019-2023; verified). Not coded 'all': "
                 "the source states a coverage goal, not that Ericsson supplies the whole RAN")],
         ran4_note='Feb 2023 Ericsson-AXIAN RAN, microwave and core modernisation for 4G and 5G (Ericsson release) confirms continuity',
         gov=[], gov_note=("no state holder found: Axian is a private, Hiridjee family-owned group (Axian brochure 2016); Axian Telecom's "
                           "stake in Telma is not confirmed from a primary source"),
         gov_dropped=[],
         core=V('Ericsson', TELMA_LAUNCH,
                "'Ericsson was selected by Telma in October 2019 to upgrade its core and radio network in Madagascar building on the two "
                "companies' existing 5G partnership' (verified); Ericsson's Oct 2019 release (403, UNVERIFIED) is titled a network "
                "upgrade 'towards 5G'. 5GC vs NSA EPC not stated"),
         first_contract=ND("the Ericsson contract (12 Jul 2019; announced 4 Oct 2019) deploys 4G+ sites 'to facilitate the rapid arrival "
                           "of 5G', i.e. 5G-ready, not explicitly a 5G contract (same rule as batch 1's Airtel Kenya)"),
         vendor_operates=ND("Ericsson's 2019 deal includes network optimisation services, which are not network operation")),
    # ------------------------------------------------------------------ Nigeria
    dict(region='Africa', country='Nigeria', operator_name='MTN', name_note='MTN Nigeria Communications Plc',
         share=V(51.87, NCC_2025, NG_NOTE, 2025),
         launch=V(2022, MTN_NG_LAUNCH,
                  "Ericsson/MTN release (19 Sep 2022, verified): 'successful launch of 5G services', first phase in parts of Lagos; DCD "
                  "dates the commercial launch 21 Sep 2022 (rollout began Aug 2022)"),
         ran5=[R('Ericsson', 'not_disclosed', MTN_NG_LAUNCH,
                 "'Ericsson's 5G technology - which includes 5G Radio Access Network & NSA Packet Core' for the launch phase (verified); "
                 "a 2022 article calls Ericsson MTN's 'preferred partner' in Nigeria, which is not a share category")],
         ran5_note="Huawei and ZTE are named only as MTN 'technology partners' for the 5G rollout (secondary repost, Jul 2022), so not coded",
         ran4=[R('Huawei', 'not_disclosed', 'https://www.huawei.com/en/news/2026/4/fdd-triplelowband-massivemimo',
                 "Huawei (22 Apr 2026): MTN Nigeria and Huawei deployed a commercial sub-1 GHz Massive MIMO site that 'increases low-band "
                 "LTE traffic by an impressive 104%' (verified); one site, no share")],
         ran4_note=("an Ericsson-to-Huawei swap of 3,000+ nodes (2012) and an NSN/Ericsson/ZTE multi-vendor LTE RAN appear only in "
                    "personal profiles (not cited), so no switch row"),
         gov=[G('South Africa', 'Government Employees Pension Fund (GEPF)', 'pension_fund', 19.94, 'MTN Group Limited', 'via_parent',
                '2025-12-31', MTN_AFS, GEPF_NOTE, parent_pct=76.27,
                chain=("MTN Group effective 76.27% of MTN Nigeria Communications Plc (FY2025 statements: non-controlling interests "
                       "23.73%); held via MTN International (Mauritius) Limited, 73.39% of issued shares (MTN Nigeria 2025 AFS, via search)"))],
         gov_note='no Nigerian state holder at 5% or more in MTN Nigeria\'s 2025 financial statements',
         gov_dropped=[],
         core=V('Ericsson', MTN_NG_LAUNCH,
                "5G launch used Ericsson's 'NSA Packet Core' (verified); MTN Group named Ericsson sole core strategic supplier for a "
                "cloud-native dual-mode 5G Core modernisation (28 Feb 2024)"),
         first_contract=ND('Ericsson 5G RAN and NSA core in place by the Sep 2022 launch; no contract date stated'),
         vendor_operates=V(True, 'https://www.lightreading.com/network-automation/mtn-nigeria-uses-ericsson-for-managed-services',
                           'five-year managed-services agreement (Feb 2014): Ericsson manages, optimises and maintains the network in Lagos, '
                           'Abuja, Enugu, Port Harcourt and Asaba (~75% of the network); renewal after ~2019 not found')),
    dict(region='Africa', country='Nigeria', operator_name='Airtel', name_note='Airtel Networks Limited (Airtel Nigeria)',
         share=V(34.39, NCC_2024,
                 ("NCC 2024 subscriber/network performance report (p.13), Dec 2024: MTN 51.39, Airtel 34.39 (56,619,381), Glo 12.23, EMTS "
                  "1.99 (verified). DISPUTED between NCC 2025 annual report (Airtel 12.39%) and NCC 2024 report (34.39%); coded 2024, "
                  "because the 2025 table appears to swap the Airtel and Glo columns (the search reported Airtel 33.94% for 2025)"), 2024),
         launch=V(2023, 'https://techreviewafrica.com/news/701/mtn-welcomes-airtel-into-nigerias-5g-network-league',
                  "TechReview Africa (19 Jun 2023): Airtel rolls out 5G in Lagos, Abuja, Ogun and Rivers, 'after MTN and Mafab' "
                  "(verified); Airtel's 3.5 GHz licence runs from 1 Mar 2023 (Airtel Networks 2022 statements)"),
         ran5=[], ran5_note='no 5G RAN vendor named outside personal profiles',
         ran4=[R('Nokia', 'not_disclosed', AIRTEL_NG_FS,
                 "Airtel Networks Limited 2022 financial statements: RAN modernisation upgrading 3G to 4G LTE, 'existing RAN equipment "
                 "were swapped with new LTE equipment from Nokia, ZTE and Huawei', 8,971 sites by 31 Dec 2022 (p.56; verified)"),
               R('ZTE', 'not_disclosed', AIRTEL_NG_FS, 'same statement (p.56)'),
               R('Huawei', 'not_disclosed', AIRTEL_NG_FS, 'same statement (p.56)')],
         ran4_note=("p.4 of the same report says 'new LTE equipment from Nokia post completion of ZTE and Huawei projects'; the old "
                    "vendor is not named, so no switch row"),
         gov=[],
         gov_note=("no state holder at 5% or more found. Airtel Africa owns Airtel Nigeria via Bharti Airtel Nigeria B.V. (91.74% of "
                   "Airtel Networks Limited). " + AIRTEL_SINGTEL),
         gov_dropped=AIRTEL_DROPPED,
         core=ND("Ericsson's Nov 2017 packet-core modernisation (EPC, '5G-ready') predates 5G; no 5G core vendor named"),
         first_contract=ND('no 5G vendor contract found; spectrum licence from 1 Mar 2023'),
         vendor_operates=V(True, 'https://www.huawei.com/en/news/2015/01/hw_412665',
                           'Huawei managed services for Airtel Nigeria since 2011 (2G/3G wireless, microwave and core across 60% of the '
                           'country), extended to Abuja/FCT on 28 Jan 2015; end date not found; 5G not covered')),
    dict(region='Africa', country='Nigeria', operator_name='MCOM', name_note='Mafab Communications Limited (brand MCOM)',
         share=ND("not listed in NCC's operator tables (2024: MTN, Airtel, Glo, EMTS; 2025: MTN, Airtel, Glo, T2)"),
         launch=V(2023, 'https://technext24.com/news/mafab-unveils-5g-network-in-lagos/',
                  ("Technext (26 Jan 2023): launch events in Abuja (24 Jan) and Lagos 'to launch its 5G mobile service, Mcom, formally', "
                   "'the second operator to launch 5G in Nigeria' (verified). DISPUTED between Technext (launched Jan 2023) and TechCabal "
                   "(26 Jan 2024: 'Mafab Communications to launch 5G later this year'; 403, UNVERIFIED); coded Technext. Mafab reportedly "
                   "sought to transfer its 5G spectrum to MTN in Sep 2026")),
         ran5=[], ran5_note="no RAN vendor named (NCC's Nokia 4G/5G training is unrelated to Mafab's network)",
         ran4=[], ran4_note='Mafab describes a 5G standalone network; no 4G RAN vendor named',
         gov=[], gov_note='no shareholder disclosure found; Mafab is chaired by its founder Musbahu Bashir (Althani Group), no state holder identified',
         gov_dropped=[],
         core=ND('Mafab says it operates a 5G SA core, but names no vendor'), first_contract=ND('spectrum licence Dec 2021; no vendor contract'),
         vendor_operates=ND()),
]
