"""Researcher coding of the first-10 expansion batch (Prof. Shen's reduced schema), coded in-session on
2026-11-15 from the cached searches in data/5g_expansion_searches.jsonl plus NBIM's 31 Dec 2025 equity
holdings file. Values come only from the cited source; anything a source didn't state is not_disclosed.

Retrofitted 2026-11-23 to Prof. Shen's review (see schema.py): source types from the URL; government stakes
at 5% or more (or with a board seat), with holder_type, state_link_basis, parent_ownership_pct_of_operator and
ownership_chain; canonical operator and vendor names with the original in name_note / the fact note; vendor
switches; VinaPhone and MobiFone added after the data-gap check. Holders below the threshold are listed in
gov_dropped. Not cited at all: Wikipedia, personal LinkedIn profiles, eSIM/aggregator sites.
"""
from schema import G, ND, R, S, V

CODED_AT = '2026-11-15'
RETROFIT_AT = '2026-11-23'
NBIM = 'https://www.nbim.no/api/investments/v2/report/?assetType=eq&date=2025-12-31&fileType=xlsx'
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
OOREDOO_GOV = 'https://www.ooredoo.com/2025-annual-report/pdfs/Ooredoo_English_2025_Corporate-Governance.pdf'
GSMA_VN = 'https://www.gsma.com/connectivity-for-good/spectrum/wp-content/uploads/2024/11/GSMA_Accelerating-5G-in-Vietnam-2024.pdf'
GSMA_VN_NOTE = 'GSMA report (Nov 2024): share of mobile connections: Viettel ~40, VinaPhone 30, MobiFone 16, Vietnamobile 12, Gmobile 2'
TELEGEO_VN = 'https://resources.telegeography.com/5g-comes-to-vietnam'

# Data-gap check (Prof. Shen, 2026-11): operators looked for and not added, with the search that settled it.
CHECKED_NOT_ADDED = {
    'Libya|Libyana': 'no commercial 5G launch found 2019-2026; ZTE core/VAS modernisation (2020) only (exp|supp|libyana-5g)',
    'Trinidad and Tobago|Digicel': 'no 5G launch: not ready in Nov 2019, still none per Ookla 2025 (exp|supp|digicel-tt-5g)',
}

# Israel shares: one consistent source for all four operators.
IL_SHARE = 'https://investors.cellcom.co.il/wp-content/uploads/2026/06/Cellcom-Israel-Ltd.-Periodic-Report-for-2025.pdf'
IL_SHARE_NOTE = ("Cellcom's own estimate of the market at 31 Dec 2025 (Cellcom 32, Partner 23, Pelephone 23, HOT 14), p.67; "
                 "verified against the PDF in the 2026-11-15 spot-check (HOT 14% confirmed visually by the researcher)")
LU_ILR = 'https://www.ilr.lu/wp-content/uploads/ilr-stat-10062026-Rapport-telecom-2025.pdf'
UY_SHARE = 'https://www.telcobrief.com/en/market-data/uruguay'
UY_NOTE = ("Dec 2025 URSEC subscription counts via TelcoBrief: ANTEL 2,448,826; Movistar 1,344,705; Claro 1,139,384; "
           "total 4,932,915. Other measures conflict: la diaria (citing URSEC) gives ANTEL 62 / Movistar 20 / Claro 18 "
           "for 'mobile services' (measure unstated); TeleSemana gives Claro 16.5% of subscriptions in Dec 2024.")
UZ_SHARE = 'https://freedomhouse.org/country/uzbekistan/freedom-net/2024'
UZ_NOTE = 'Freedom House citing Dec 2023 operator data (Ucell 25, Beeline 25, Uzbektelecom 23, Mobiuz 22)'
TJ_SHARE = 'https://tadviser.com/index.php/Article:Communications_(Tajik_market)'
TJ_NOTE = ('computed from 2024 subscriber counts for all six operators: Tcell 2.66m, Babilon-Mobile 1.88m, '
           'MegaFon 1.80m, Zet-Mobile 1.00m, Tojiktelecom 0.275m, O Mobile 0.241m (total 7.856m); Tojiktelecom spelled Tajiktelecom in the source')
ORANGE_XLSX = 'https://assets.orange.com/pm_12751_545_545865-jr7yvi3osw.xlsx'
PROXIMUS_AR = 'https://www.proximus-cdn.com/dam/jcr:44041fd1-b790-497d-b397-cb03869fab27/proximus-integrated-annual-report-2026-v1.1_en.pdf'
VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
OOREDOO_AR = 'https://www.ooredoo.com/wp-content/uploads/2026/03/2025-Ooredoo-Annual-Report_English_FINAL.pdf'
E_AND_NOTE = ("the Vodafone filing names e& but does not call it state-owned; e&'s 2025 integrated annual report gives the "
              "Emirates Investment Authority 60% and says the EIA is ultimately controlled by the UAE Federal Government")
TEMASEK_TYPE_NOTE = ('holder_type is a researcher classification: the sources name Temasek as the holding company but do not '
                     'describe it; the state link comes from data/state_holders.csv (wholly owned by the Minister for Finance)')
PHI_DISPUTE = ("SPOT-CHECK 2026-11-15: INSS p.1 verified: 'Partner-Hot Mobile and Pelephone would use Ericsson equipment'. The "
               "Nokia attribution below comes from an unidentified Bezeq/Pelephone-related report and was not verified. "
               'DISPUTED: the 2020 PHI (Partner-HOT shared network) 5G deployment is attributed to Ericsson by INSS '
               'and by Israelpedia, but to Nokia by a Bezeq/Pelephone-related report; secondary sources also say '
               'Partner signed an Ericsson MoU in Jan 2023 to make Ericsson its "primary supplier". Coded Ericsson '
               'with no share category.')

OPERATORS = [
    # ------------------------------------------------------------------ Libya
    dict(region='Africa', country='Libya', operator_name='Al-Madar',
         name_note='Wikipedia list name Al-madar; also written Almadar, Almadar Aljadid, Al-Madar Al-Jadeed',
         share=ND("only 'more than 3 million subscribers' (Oct 2020, Operator Watch) found; no market total for that date"),
         launch=V(2019, 'https://www.libyaherald.com/2019/10/al-madar-launches-libyas-first-5g-mobile-internet-service-first-in-north-africa/',
                  "29 Oct 2019, limited areas. DISPUTED: Libya Herald (Jan 2026) also reports Almadar launching 'Libya's first 5G "
                  "service in Tripoli'; coded the 2019 launch"),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.libyaherald.com/2021/11/10/libya-needs-5g-and-5g-is-ready-for-libya-andrea-missori-country-manager-ericsson-libya/',
                 "Nov 2021: Al-Madar 5G service 'powered by Ericsson' over its commercial 4G network")],
         ran4=[R('Huawei', 'not_disclosed', 'https://freedomhouse.org/country/libya/freedom-net/2019', 'Huawei worked on introducing 4G (Oct 2018)'),
               R('Nokia', 'small', 'https://www.linkedin.com/posts/nokia-for-service-providers_al-madar-leverages-nokias-innovative-capacity-activity-7399779199722553344-gluF',
                 "Nokia's own post (Nov 2025): one C-RAN LTE deployment at Benghazi National Stadium")],
         ran4_note='Huawei/ZTE/Ericsson LTE work is also described in personal LinkedIn profiles, which are not cited',
         gov=[G('Libya', 'Libyan Post, Telecommunications and Information Technology Company (LPTIC)', 'state_holding_company', None, 'Al-Madar', 'direct', '2013-09-18',
                'https://www.telecompaper.com/news/libyan-govt-plans-to-list-mobile-operator-libyana-in-2014--967615',
                "LPTIC named as parent of Al-Madar and Libyana; percentage not disclosed", link_url='https://almadar.ly/en/Pages/Who-we-are.aspx'),
              G('Libya', 'Government of Libya', 'government_ministry', None, 'LPTIC', 'via_parent', '2026-01-25',
                'https://almadar.ly/en/Pages/Who-we-are.aspx', "Al-Madar describes itself as government-owned; the state's percentage of LPTIC is not disclosed")],
         gov_dropped=[],
         core=ND('Ericsson-powered 5G ran over the existing 4G network (NSA), but no source names the EPC/5GC vendor'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Kenya
    dict(region='Africa', country='Kenya', operator_name='Safaricom',
         share=V(65.3, 'http://www.ca.go.ke/sites/default/files/2025-12/Sector%20Statistics%20Report%20Q1%202025-2026_0.pdf',
                 'Communications Authority, mobile subscriptions at 30 Sep 2025', 2025),
         launch=V(2022, 'https://www.safaricom.co.ke/media-center-landing/press-releases/safaricom-announces-commercial-launch-of-5g-services', 'commercial launch 27 Oct 2022'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.safaricom.co.ke/media-center-landing/press-releases/safaricom-switches-on-5g-across-kenya', 'one of two named 5G technology partners'),
               R('Nokia', 'not_disclosed', 'https://www.safaricom.co.ke/media-center-landing/press-releases/safaricom-switches-on-5g-across-kenya', 'one of two named 5G technology partners')],
         ran4=[], ran4_note='no 4G RAN vendor named in the annual reports searched',
         gov=[G('Kenya', 'Government of Kenya (Cabinet Secretary to the National Treasury)', 'government_ministry', 20.0, 'Safaricom PLC', 'direct', '2026-06-30',
                'https://www.safaricom.co.ke/annualreport_2026/pdf/Safaricom_IAR_20431_2026_12h00_Interactive.pdf',
                '35.00% at 31 Mar 2025 (FY2025 financial statements); the government sold 15% to Vodacom, completed 30 Jun 2026'),
              G('United Arab Emirates', 'e& (Emirates Telecommunications Group)', 'state_owned_company', 17.005026, 'Vodafone Group Plc', 'via_parent', '2026-03-31', VODAFONE_AR,
                E_AND_NOTE, link_url=E_AND_AR,
                chain='Vodafone Group Plc -> Vodacom Group 65.10% -> Vodafone Kenya (Vodacom majority since 30 Jun 2026; % not stated) -> Safaricom PLC 55%'),
              G('South Africa', 'Government Employees Pension Fund (GEPF)', 'pension_fund', 12.24, 'Vodacom Group Limited', 'via_parent',
                '2025-03-31', 'https://www.vodacom.com/pdf/agm/2025/notice-of-annual-general-meeting-2025.pdf',
                "Vodacom notice of AGM 2025, p.11 major shareholders: 'Government Employee Pension Fund (GEPF) 254 385 551 12.24' "
                "(verified in batch 5, 2026-11-26). Added under Prof. Shen's pension rule (2026-11-26)",
                chain='Vodacom Group -> Vodafone Kenya (Vodacom majority since 30 Jun 2026; % not stated) -> Safaricom PLC 55%')],
         gov_dropped=['Norges Bank Investment Management 0.82% of Safaricom PLC (2025-12-31; board seat not checked)',
                      "Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; NBIM's file shows 1.56% at 2025-12-31; board seat not checked)"],
         gov_note=('GEPF added 2026-11-26 from the Vodacom 2025 AGM notice (an older report gave 12.9% in 2017); NBIM held no Vodacom '
                   'shares at 31 Dec 2025'),
         core=ND('Nokia and Huawei are the named 5G partners; the core vendor is not specified'),
         first_contract=ND("Huawei/Nokia partner selection was announced in the 'switches on 5G' release; the searches disagree on its date (19 Mar 2021 vs 20 Oct 2022)"),
         vendor_operates=ND()),
    dict(region='Africa', country='Kenya', operator_name='Airtel',
         share=V(29.6, 'https://www.ca.go.ke/increased-smartphone-adoption-and-mobile-money-drive-growth-telecoms-sector-report-shows',
                 'Communications Authority, quarter to 30 Sep 2024 (FY2023/24 annual: 29.5%)', 2024),
         launch=V(2023, 'https://www.ca.go.ke/sites/default/files/CA/Speeches/Remarks%20byDirector%20General,%20CA%20During%20the%20Launch%20of%205G%20By%20Airtel%20Network%20on%206th%20July%202023.pdf', 'launched 6 Jul 2023'),
         ran5=[R('Nokia', 'not_disclosed', 'https://techtrendske.co.ke/2020/12/01/nokia-and-airtel-kenya-lay-5g-foundations-in-kenya/',
                 'Dec 2020 three-year deal for 5G-ready AirScale Single RAN; no source confirms the vendor of the 5G network launched in 2023')],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.airtelkenya.com/Airtel-selects-Ericsson-to-modernize-its-4G-network-in-Kenya', '4G RAN modernisation, signed Aug 2020'),
               R('Nokia', 'not_disclosed', 'https://techtrendske.co.ke/2020/12/01/nokia-and-airtel-kenya-lay-5g-foundations-in-kenya/', '2G/3G/4G modernisation in Nairobi and other areas (Dec 2020)')],
         gov=[],
         gov_note=("no state holder at 5% or more found. Airtel Africa owns Airtel Kenya via Bharti Airtel Kenya B.V. (99.99975%). OPEN: "
                   "Bharti Airtel's 30 Jun 2025 BSE pattern shows a 10.79% foreign promoter group without naming its members "
                   "(Singtel/Pastel not identified; the filing link returned 404), so a Singtel stake in Bharti could not be coded"),
         gov_dropped=["Qatar Holding LLC 3.67% of Airtel Africa plc (2025-03-31; no Qatar nominee on the Airtel Africa board per the 2025 annual report and leadership page)",
                      'Norges Bank Investment Management 0.39% of Airtel Africa plc (2025-12-31; board seat not checked)',
                      'Norges Bank Investment Management 1.06% of Bharti Airtel Ltd (2025-12-31; board seat not checked)'],
         core=ND('Nokia deal laid groundwork for 5G; no core/EPC vendor named'),
         first_contract=ND('Ericsson (Aug 2020) and Nokia (Dec 2020) deals were for "5G-ready" 4G equipment, not explicitly 5G contracts'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Singapore
    dict(region='Asia-Pacific', country='Singapore', operator_name='Singtel',
         share=ND("Singtel AR FY25 gives 4.5m Singapore mobile customers (p.5) but no Singapore market-share %. SPOT-CHECK FIX: the "
                  "50.7% coded earlier was Telkomsel's Indonesian share (AR25 p.118 associates table)"),
         launch=V(2020, 'https://cdn1.singteldigital.com/content/dam/singtel/business/sb/articles/transforming-singapores-future-with-5g.pdf', 'NSA commercial Sep 2020; SA May 2021'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/cases/2022/singtel-and-ericsson',
                 "Ericsson case study (Feb 2022, updated Oct 2024) lists 'Ericsson 5G RAN' among solutions deployed in Singtel's 5G SA; "
                 "no exclusivity wording and no other vendor named. SPOT-CHECK FIX: 'Ericsson solely' in the 2020 AGM document is a "
                 "shareholder's question (Q21); Singtel's answer ('vendor agnostic… most optimal solution') neither confirms nor "
                 "denies sole supply, so no share category is coded")],
         ran4=[], ran4_note='4G RAN vendor not named in the sources found',
         gov=[G('Singapore', 'Temasek Holdings', 'state_holding_company', 50.55, 'Singtel', 'direct', '2026-06-30',
                'https://cdn1.singteldigital.com/content/dam/singtel/investorRelations/annualReports/2026/Letter-to-Shareholders.pdf',
                'computed: 8,304,071,181 direct shares / 16,426,070,100 issued (5% = 821,303,505 shares, letter s.2.7); combined 51.99% (p.13). ' + TEMASEK_TYPE_NOTE,
                link='reference_list'),
              G('Singapore', 'Temasek Holdings (deemed, via subsidiaries/associates)', 'state_holding_company', 1.43, 'Singtel', 'via_parent', '2026-06-30',
                'https://cdn1.singteldigital.com/content/dam/singtel/investorRelations/annualReports/2026/Letter-to-Shareholders.pdf',
                'computed: 235,133,564 deemed shares / 16,426,070,100 issued. Kept below 5% because it is the same holder as the 50.55% direct stake '
                '(its board control comes with that stake); the intermediate holders are not named',
                link='reference_list', board_seat='yes')],
         gov_dropped=['Norges Bank Investment Management 0.76% of Singtel (2025-12-31; board seat not checked)'],
         core=V('Ericsson', 'https://www.ericsson.com/en/cases/2022/singtel-and-ericsson', 'dual-mode 5G Core; NSA used an upgraded Ericsson EPC'),
         first_contract=ND('Ericsson 5G pilot network launched July 2018; contract date not found'),
         vendor_operates=ND()),
    dict(region='Asia-Pacific', country='Singapore', operator_name='StarHub',
         share=ND('no overall share found; an IMDA filing gives Dec 2024 prepaid 22.2% / postpaid 22.8%'),
         launch=V(2020, 'https://www.starhub.com/about-us/newsroom/2020/august/first-to-say-hello-5g-with-starhub.html', 'early-access 5G from 18 Aug 2020; SA in 2021'),
         ran5=[R('Nokia', 'not_disclosed', 'https://ir.starhub.com/misc/ar2020.pdf', 'launched 5G Aug 2020 with Nokia as technology partner (3.5 GHz SA RAN shared with M1)')],
         ran4=[R('Huawei', 'not_disclosed', 'https://ir.starhub.com/misc/ar2015.pdf', 'HetNet/LTE infrastructure partner (2015)'),
               R('Nokia', 'not_disclosed', 'https://ir.starhub.com/misc/ar2016.pdf', 'LTE-Advanced technology (2016)')],
         gov=[G('Singapore', 'Temasek Holdings', 'state_holding_company', 56.13, 'StarHub Ltd', 'via_parent', '2025-12-31',
                'https://links.sgx.com/FileOpen/StarHub%20Annual%20Report%202025.ashx?App=Announcement&FileID=882452',
                'deemed interest as filed (a percentage of StarHub itself, not multiplied by us). ' + TEMASEK_TYPE_NOTE, link='reference_list',
                parent_pct=55.959,
                chain='Temasek -> ST Telemedia -> STT Communications -> Asia Mobile Holding Co -> Asia Mobile Holdings 55.959% of StarHub (after the 27 Mar 2026 share issue); intermediate percentages not stated'),
              G('Qatar', 'Qatar Investment Authority', 'sovereign_wealth_fund', 53.0, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', OOREDOO_AR,
                "Ooredoo's annual report calls QIA the State of Qatar's sovereign wealth fund",
                chain='Ooredoo Q.P.S.C. (via OIH Investment LLC) ~25% of Asia Mobile Holdings -> 55.959% of StarHub'),
              G('Qatar', 'General Retirement & Social Insurance Authority', 'pension_fund', 13.0, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', OOREDOO_AR,
                "Ooredoo lists it as a Qatari government-related entity; board member H.E. Ahmed Ali Al Hammadi represents it (2025 corporate governance report)",
                chain='Ooredoo Q.P.S.C. (via OIH Investment LLC) ~25% of Asia Mobile Holdings -> 55.959% of StarHub', board_seat='yes')],
         gov_dropped=['General Military Retirement and Social Insurance Authority 2% of Ooredoo Q.P.S.C. (2025-12-31; no board representative in the 2025 governance report)',
                      'Abu Dhabi Investment Authority 4.99% of Ooredoo Q.P.S.C. (2025-12-31; no board representative; sold shares in a 2025 secondary offering)',
                      'Norges Bank Investment Management 1.88% of Ooredoo Q.P.S.C. (2025-12-31; board seat not checked)',
                      'Norges Bank Investment Management 0.57% of StarHub Ltd (2025-12-31; board seat not checked)'],
         core=ND(), first_contract=ND('Nokia 5G NR pilot in 2018; no dated 5G contract found'), vendor_operates=ND()),
    dict(region='Asia-Pacific', country='Singapore', operator_name='M1',
         share=ND('no overall share found; an IMDA filing gives Dec 2024 prepaid 13.5% / postpaid 23.9%'),
         launch=V(2020, 'https://www.m1.com.sg/about-us/news-releases/2020/m1-enables-5g-for-everyone', 'commercial NSA 24 Sep 2020; SA 2021'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.m1.com.sg/about-us/news-releases/2020/m1-granted-final-5g-network-license-from-imda',
                 'Nokia selected for the nationwide 3.5 GHz SA RAN; Ericsson/Nokia/Huawei named only as possible mmWave vendors')],
         ran4=[], ran4_note='Huawei appears only as an LTE-Advanced trial partner (Jan 2016), not as a confirmed supplier',
         gov=[G('Singapore', 'Temasek Holdings', 'state_holding_company', 33.38, 'M1 Limited', 'via_parent', '2025',
                'https://www.imda.gov.sg/-/media/imda/files/regulations-and-licensing/regulations/consultations/2025/simba-and-m1/annex-b-non-confidential-abbreviated-statement-submitted-by-simba-and-m1.pdf',
                "indirect interest as filed with IMDA by SIMBA/M1 (a percentage of M1 itself); Keppel's sale of M1 to SIMBA/Tuas pending. "
                "Fullerton Management 8.07% indirect listed but not identified as state in the source. " + TEMASEK_TYPE_NOTE,
                link='reference_list', parent_pct=83.86,
                chain='Keppel Ltd 83.86% indirect of M1 (Keppel Konnect 19.31% direct + Konnectivity 80.69% direct)')],
         gov_dropped=['Norges Bank Investment Management 1.36% of Keppel Ltd (2025-12-31; board seat not checked)'],
         core=V('Nokia', 'https://www.nokia.com/newsroom/nokia-and-m1-partner-with-5g-standalone-core-to-drive-singapores-5g-ecosystem/', 'cloud-native 5G SA core, partnership announced 13 Jan 2021'),
         first_contract=V('2020-06', 'https://www.datacenterdynamics.com/en/news/singapore-finalizes-5g-contract-winners-nokia-and-ericsson-named-suppliers/',
                          "Nokia named as M1/StarHub 5G SA RAN supplier when IMDA finalised licences (June 2020). The searches date M1's own Nokia release to both 24 Jun and 24 Sep 2020"),
         vendor_operates=ND()),
    dict(region='Asia-Pacific', country='Singapore', operator_name='SIMBA',
         name_note='Wikipedia list name Simba; SIMBA Telecom, formerly TPG Telecom Singapore',
         share=V(10.0, 'https://www.imda.gov.sg/-/media/imda/files/regulations-and-licensing/regulations/consultations/2025/simba-and-m1/annex-b-non-confidential-abbreviated-statement-submitted-by-simba-and-m1.pdf',
                 "SIMBA's own submission to IMDA, early 2023; Business Times cites BMI at 11% for 2025", 2023),
         launch=ND('5G NSA market trial 10 Sep 2021; IMDA 5G rights from 1 Jan 2022; all plans 5G-capable Sep 2023; commercial launch date not found'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.businesstimes.com.sg/companies-markets/telcos-media-tech/key-considerations-hanging-over-approval-simba-m1s-merger',
                 "Business Times (11 Mar 2026): SIMBA's 5G network is 'built on' Huawei technology")],
         ran4=[], ran4_note='4G vendor not named; follow-up search also found none',
         gov=[], gov_note='no state holder at 5% or more found in Tuas Ltd (100% parent)',
         gov_dropped=['Norges Bank Investment Management 0.65% of Tuas Ltd (100% parent) (2025-12-31; board seat not checked)'],
         core=ND("Business Times says the network is built on Huawei technology but doesn't say whether that includes the core"),
         first_contract=ND(),
         vendor_operates=V(False, 'https://support.simba.sg/hc/en-us/articles/26550149956505-Whose-infrastructure-does-SIMBA-use',
                           "equipment above the end-user fibre layer is 'built, managed, and owned by SIMBA'")),
    # ------------------------------------------------------------------ Uzbekistan
    dict(region='Central Asia & Eastern Europe', country='Uzbekistan', operator_name='Ucell',
         share=V(25.0, UZ_SHARE, UZ_NOTE, 2023),
         launch=V(2021, 'https://ucell.uz/en/company_news/ucell_launches_5g_in_tashkent', 'Tashkent, 14 Apr 2021'),
         ran5=[R('Huawei', 'not_disclosed', 'https://ucell.uz/en/company_news/ucell_launches_5g_in_tashkent', 'equipment for the first commercial 5G in Tashkent (2021); also central Tashkent sites (2022)'),
               R('Nokia', 'not_disclosed', 'https://ucell.uz/en/company_news/ucell_5g_in_tashkent_and_samarkand_is_real_now', 'central Tashkent sites (Aug 2022)'),
               R('ZTE', 'not_disclosed', 'https://ucell.uz/en/company_news/ucell_5g_in_tashkent_and_samarkand_is_real_now', 'central Samarkand NSA sites (Aug 2022)')],
         ran4=[R('ZTE', 'most', 'https://www.zte.com.cn/global/about/magazine/zte-technologies/2012/1/en_595/283276.html', "'main LTE equipment supplier' (ZTE case study, 2012); UzDaily (Sep 2024) repeats ZTE as 4G supplier")],
         gov=[G('Uzbekistan', 'Agency for State Assets Management (ASAM)', 'government_ministry', 49.0, 'Digital Holding', 'via_parent', '2021-09-30',
                'https://ucell.uz/uz/company_news/digital_holding', 'Digital Holding formed 30 Sep 2021: Digital Invest (MegaFon/USM JV) 51%, ASAM 49%',
                parent_pct=100.0, chain='Digital Holding 100% of COSCOM (Ucell)')],
         gov_dropped=[],
         core=ND('SA environment is multivendor (Nokia, Huawei, ZTE interoperate); core vendor not named'),
         first_contract=ND('5G testing began 2019; no dated vendor contract'), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Uzbekistan', operator_name='Uzbektelecom',
         name_note='also Uztelecom; mobile brand Uzmobile',
         share=V(23.0, UZ_SHARE, UZ_NOTE + '; brand Uzmobile', 2023),
         launch=V(2022, 'https://uztelecom.uz/en/news/news/for-the-first-time-in-the-cis-uztelecom-launched-5g-network-in-all-regional-centres-of-uzbekistan/', 'Tashkent Mar 2022; all regional centres Sep 2024'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/uzbektelecom-pens-huawei-and-zte-deals-worth-506m-for-major-network-expansion/', 'Huawei and ZTE contracts (US$506.8m) incl. 388 + 325 5G base stations, not split by vendor; Huawei 5.5G launch Sep 2024'),
               R('ZTE', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/uzbektelecom-pens-huawei-and-zte-deals-worth-506m-for-major-network-expansion/', 'same contracts, not split by vendor')],
         ran4=[R('Huawei', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/uzbektelecom-pens-huawei-and-zte-deals-worth-506m-for-major-network-expansion/', 'thousands of 3G/4G base stations under Huawei+ZTE contracts, not split by vendor'),
               R('ZTE', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/uzbektelecom-pens-huawei-and-zte-deals-worth-506m-for-major-network-expansion/', 'same')],
         gov=[G('Uzbekistan', 'Ministry of Economy and Finance', 'government_ministry', 67.17, 'Uzbektelecom JSC', 'direct', '2025-12-31',
                'https://openinfo.uz/media/int_report/08c4d98a-95e7-4ee7-8771-8093b193f1f5.pdf', '2025 consolidated financial statements'),
              G('Uzbekistan', 'National Investment Fund of Uzbekistan (UzNIF; 100% owned by the Ministry of Economy and Finance)', 'state_holding_company', 25.0, 'Uzbektelecom JSC', 'direct', '2025-12-31',
                'https://openinfo.uz/media/int_report/08c4d98a-95e7-4ee7-8771-8093b193f1f5.pdf', '25% transferred from the Ministry')],
         gov_note=("SPOT-CHECK FIX (2026-11-15): three rows removed (State Assets Management Agency 2.033%, Center of Radio Communication "
                   "0.34%, Unicon.uz 0.002%). They came from a share-structure file the search dated 28 Aug 2026, but the file itself "
                   "shows the Ministry at 92.174%, i.e. the pre-2025 structure. The FY2025 statements (p.15), the latest official filing, "
                   "list only the Ministry 67.17%, UzNIF 25.00% and 'other legal entities and individuals (individually hold less than "
                   "1%)' 7.83%."),
         gov_dropped=[],
         core=ND('network is NSA; EPC vendor not named'),
         first_contract=ND('Huawei pre-trial 5G tests in 2019; Huawei supply agreement 1 May 2021 not stated to cover 5G'), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Uzbekistan', operator_name='Mobiuz',
         share=V(22.0, UZ_SHARE, UZ_NOTE + '; BMI (via Times of Central Asia) gives 20.9% at end-2024', 2023),
         launch=V(2022, 'https://developingtelecoms.com/telecom-technology/wireless-networks/13947-mobiuz-goes-live-with-5g-services-in-uzbek-capital.html', 'Tashkent, Sep 2022'),
         ran5=[R('Huawei', 'not_disclosed', 'https://developingtelecoms.com/telecom-technology/wireless-networks/13947-mobiuz-goes-live-with-5g-services-in-uzbek-capital.html',
                 "Developing Telecoms (7 Sep 2022), citing TeleGeography: the US$150m Chinese loan funds 'the implementation of 5G - all using "
                 "equipment provided by Huawei'. SPOT-CHECK: the originally cited DCD article was blocked (403) under both fetch methods, so it was re-cited here")],
         ran4=[R('Huawei', 'not_disclosed', 'https://developingtelecoms.com/telecom-technology/wireless-networks/13947-mobiuz-goes-live-with-5g-services-in-uzbek-capital.html',
                 "same article: 'nationwide 3G & 4G coverage expansion… all using equipment provided by Huawei'. SPOT-CHECK FIX: the "
                 "originally cited UzDaily piece mentions Huawei equipment but no network generation")],
         ran4_note=("SPOT-CHECK FIX: ZTE removed from 4G. ZTE's Sep 2025 release covers replacing base stations and 1,200+ new ones in "
                    "Karakalpakstan and Khorezm, but never names a generation"),
         gov=[G('Uzbekistan', 'State of Uzbekistan (state share managed by the State Assets Management Agency, UzSAMA)', 'government_ministry', 100.0, 'Universal Mobile Systems LLC (Mobiuz)', 'direct', '2025-06-09',
                'https://gov.uz/en/davaktiv/news/view/59663',
                "UzSAMA announced privatisation of '100% of the state-owned share'. SPOT-CHECK FIX: the holder was previously coded as 'Digital "
                "Trust', a name this page doesn't use (it came from Gazeta.uz, which isn't cited). A US-led consortium was selected 4 Jun 2026; closing not confirmed")],
         gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Uruguay
    dict(region='Latin America & Caribbean', country='Uruguay', operator_name='ANTEL',
         share=V(49.64, UY_SHARE, UY_NOTE, 2025),
         launch=V(2023, 'https://antel.com.uy/institucional/sala-de-prensa/eventos/antel-lanzo-la-tecnologia-5g-en-uruguay',
                  "national launch 28 Jun 2023. DISPUTED: Nokia (10 Apr 2019) describes ANTEL's 'first commercial 5G network' in Maldonado; coded ANTEL's own launch"),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/antel-and-nokia-make-the-first-5g-call-on-a-commercial-network-in-latin-america/', 'Nokia 5G radio network, initial deployment Apr 2019')],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.prnewswire.com/news-releases/antel-and-alcatel-lucent-launch-4glte-services-in-uruguay-and-establish-the-first-commercial-4glte-wireless-network-in-a-latin-american-country-135501863.html', 'supplier named as Alcatel-Lucent (now part of Nokia); end-to-end LTE incl. base stations (Dec 2011)')],
         gov=[G('Uruguay', 'State of Uruguay', 'government_ministry', 100.0, 'ANTEL', 'direct', '2026-10-31',
                'https://www.uruguayxxi.gub.uy/uploads/informacion/a2ed35ca0ef7e73184e708515899e831f9bf565c.pdf', 'state enterprise (Uruguay XXI, government agency); no share register')],
         gov_dropped=[],
         core=ND('Nokia supplied radio, transport and services; core not stated'),
         first_contract=V('2019-04-10', 'https://www.nokia.com/newsroom/antel-and-nokia-make-the-first-5g-call-on-a-commercial-network-in-latin-america/', 'announcement of the completed Nokia 5G network; signing date not disclosed'),
         vendor_operates=ND()),
    dict(region='Latin America & Caribbean', country='Uruguay', operator_name='Movistar',
         share=V(27.26, UY_SHARE, 'computed 1,344,705 / 4,932,915. ' + UY_NOTE, 2025),
         launch=V(2023, 'https://portal.powertec.com.au/industry-resources/companies/movistar-uruguay', 'Sep 2023 (weak source: industry directory)'),
         ran5=[R('Nokia', 'not_disclosed', 'https://library.oapen.org/bitstream/handle/20.500.12657/99202/9781003489450_10.4324_9781003489450-11.pdf?sequence=1&isAllowed=y', 'academic book (2025): Nokia partner for the 2023 5G tender')],
         ran4=[], ran4_note='Ericsson was sole GSM supplier (2005) and 3G supplier (2007); no LTE vendor found',
         gov=[],
         gov_dropped=['Tredje AP-fonden (AP3) 0.62% of Millicom (2026; aggregator data; meets the pension rule, ap3.se; board seat not checked)',
                      "Norges Bank Investment Management 0.69% of Millicom (2026; aggregator data; NBIM's own file shows none at 2025-12-31)",
                      'State of Wyoming, 2,241 Millicom shares (2026; aggregator data; percentage negligible)'],
         gov_note=("Telefonica sold 100% of Telefonica Moviles del Uruguay to Millicom on 7 Oct 2025 (Telefonica disclosure), so SEPI and PIF no longer reach it. "
                   "Millicom's holders above 3%: Niel family 44.1%, Dodge & Cox, BlackRock; no state holder (2025 SEC annual filing)"),
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    dict(region='Latin America & Caribbean', country='Uruguay', operator_name='Claro',
         share=V(23.10, UY_SHARE, 'computed 1,139,384 / 4,932,915. ' + UY_NOTE, 2025),
         launch=ND('3.5 GHz spectrum won May 2023; commercial launch date not found in two searches'),
         ran5=[R('Nokia', 'not_disclosed', 'https://developingtelecoms.com/telecom-technology/wireless-networks/11321-claro-uruguay-begins-5g-network-trials.html', 'Nokia access network in 28 GHz trials (Jun 2021); an academic book names Nokia for the 2023 deployment')],
         ran4=[], ran4_note='only a personal LinkedIn profile mentions Nokia LTE work (not cited)',
         gov=[], gov_note='no state holder at 5% or more found in America Movil (100% parent)',
         gov_dropped=['Norges Bank Investment Management 0.07% of America Movil (2025-12-31; board seat not checked)'],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Israel
    dict(region='Middle East', country='Israel', operator_name='Cellcom',
         share=V(32.0, IL_SHARE, IL_SHARE_NOTE, 2025),
         launch=V(2020, IL_SHARE, '5G launched 2020 per 2025 periodic report'),
         ran5=[R('Nokia', 'not_disclosed', IL_SHARE,
                 "contract counterparty NSN Israel (Nokia Solutions and Networks). SPOT-CHECK FIX: p.90 framework agreement with NSN Israel covers purchase of 'advanced 4th Generation and 5th Generation technology'; network shared with Wecom")],
         ran4=[R('Nokia', 'not_disclosed', IL_SHARE, 'contract counterparty NSN Israel; LTE/LTE-A framework agreement (p.90), since Apr 2014')],
         gov=[], gov_note="no state holder in filings (controlling holder FF6-Cell LP, private); NBIM held no Israeli telecoms at 31 Dec 2025", gov_dropped=[],
         core=ND("NSN framework covers 4G/5G and associated core equipment (p.90); p.91: Cellcom 'entered into an agreement to build "
                 "and operate a 5th Generation network core (standalone)' with an UNNAMED counterparty"),
         first_contract=ND(),
         vendor_operates=ND("p.91: an agreement to 'build and operate' the SA 5G core exists, but the counterparty is not named, so "
                            "it can't be shown to be an equipment vendor; Amdocs runs IT/billing operations (since 2010), not the network")),
    dict(region='Middle East', country='Israel', operator_name='Partner',
         share=V(23.0, IL_SHARE, IL_SHARE_NOTE, 2025),
         launch=V(2020, 'https://www.itu.int/en/ITU-D/Regional-Presence/Europe/Documents/Events/2020/5G_EUR_CIS/5G_Israel-final.pdf', 'Sep 2020'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.inss.org.il/wp-content/uploads/2020/11/no.-1403.pdf', PHI_DISPUTE)],
         ran4=[R('Ericsson', 'all', 'https://www.partner.co.il/contentassets/db3c9f1868834974925401ebe917bccb/pdfs/20f_2018_isa.pdf', 'sole radio and core equipment supplier (2018 20-F); 4G deployed with Ericsson from 2010')],
         gov=[], gov_note='controlling holder Amphissa (Phoenix-linked, private); no state holder; NBIM none at 31 Dec 2025', gov_dropped=[],
         core=V('Ericsson', 'https://www.partner.co.il/contentassets/db3c9f1868834974925401ebe917bccb/pdfs/20f_2018_isa.pdf',
                'PROVISIONAL: Ericsson was sole core supplier (2018 20-F); only secondary sources say the 5G SA core is Ericsson-built (announced early 2023, migration done Jul 2025)'),
         first_contract=ND(), vendor_operates=ND('PHI Networks (Partner-HOT shared network JV) runs the shared RAN; no vendor-managed operations')),
    dict(region='Middle East', country='Israel', operator_name='Pelephone',
         share=V(23.0, IL_SHARE, IL_SHARE_NOTE, 2025),
         launch=V(2020, 'https://www.datacenterdynamics.com/en/news/israel-awards-5g-contracts-pelephone-hot-mobile-and-partner-comms/', 'launched commercially by 1 Oct 2020'),
         ran5=[R('Ericsson', 'all', 'https://ir.bezeq.co.il/static-files/770b7f6a-96d1-4b0d-92c2-e4cb0a15bc9e',
                 "Bezeq annual report: Ericsson supplied Pelephone's UMTS, LTE and 5G infrastructure. SPOT-CHECK: UNVERIFIED, because the Bezeq file "
                 "returned 403 under both fetch methods. INSS (verified) says Pelephone 'would use Ericsson equipment' but has no sole-supplier wording")],
         ran4=[R('Ericsson', 'all', 'https://en.globes.co.il/en/article-pelephone-picks-ericsson-as-sole-4g-vendor-1000972189', 'sole 4G vendor (2014); Bezeq annual report confirms')],
         gov=[], gov_note='100% owned by Bezeq (no controlling shareholder); no state holder found; NBIM held no Bezeq at 31 Dec 2025', gov_dropped=[],
         core=V('Ericsson', 'https://ir.bezeq.co.il/news-releases/news-release-details/pelephone-expects-reach-100-thousand-5g-max-customers-and-will/', 'independent SA core built with Ericsson (NIS 50m); 5G MAX launched Sep 2024'),
         first_contract=ND('Siklu mmWave backhaul deal dated 3 Sep 2020, but Ericsson 5G sites existed by Aug 2020; Ericsson contract date not found'),
         vendor_operates=ND()),
    dict(region='Middle East', country='Israel', operator_name='HOT',
         share=V(14.0, IL_SHARE, IL_SHARE_NOTE + "; Keystone's Jul 2026 presentation says 15%", 2025),
         launch=V(2020, 'https://www.datacenterdynamics.com/en/news/israel-awards-5g-contracts-pelephone-hot-mobile-and-partner-comms/', 'launched commercially by 1 Oct 2020'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.inss.org.il/wp-content/uploads/2020/11/no.-1403.pdf', PHI_DISPUTE)],
         ran4=[], ran4_note='PHI (Partner-HOT shared network); 4G vendor not found',
         gov=[], gov_note='controlled by Altice/Drahi (private); no state holder found', gov_dropped=[],
         core=ND('INSS names Ericsson as the PHI (Partner-HOT shared network) 5G equipment vendor without saying whether that covers the core'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Luxembourg
    dict(region='Western Europe', country='Luxembourg', operator_name='Post',
         share=V(50.3, LU_ILR, 'ILR 2025 report, subscribers excl. M2M', 2025),
         launch=V(2020, 'https://www.ericsson.com/en/press-releases/2020/10/post-luxembourg-chooses-ericsson-as-5g-core-and-ran-vendor', 'Ericsson-powered 5G live 16 Oct 2020'),
         ran5=[R('Ericsson', 'all', 'https://www.post.lu/en/particuliers/support/telephonie-mobile/5g/strategie-5g-de-post/quel-est-votre-fournisseur-pour-le-reseau-5g-de-post', "POST: 5G 'deployed on the Ericsson network infrastructure'")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2020/10/post-luxembourg-chooses-ericsson-as-5g-core-and-ran-vendor', '2020 deal includes modernising the existing 2G/3G/4G network; Ericsson described as legacy provider')],
         gov=[G('Luxembourg', 'State of Luxembourg', 'government_ministry', 100.0, 'POST Luxembourg', 'direct', '2025-12-31', 'https://www.postgroup.lu/documents/1846390/5402177/RA_2025_EN.pdf', 'sole shareholder since 1992 (Annual Report 2025, published 12 May 2026)')],
         gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/2020/10/post-luxembourg-chooses-ericsson-as-5g-core-and-ran-vendor', 'cloud-native dual-mode 5G Core'),
         first_contract=V('2020-10-26', 'https://www.ericsson.com/en/press-releases/2020/10/post-luxembourg-chooses-ericsson-as-5g-core-and-ran-vendor', 'announcement date of the multi-year 5G Core+RAN contract (after the 16 Oct launch); signing date not disclosed'),
         vendor_operates=ND('Ericsson provides rollout and support services; no managed operations stated')),
    dict(region='Western Europe', country='Luxembourg', operator_name='Tango',
         share=V(32.9, LU_ILR, 'ILR 2025 report (Proximus Luxembourg)', 2025),
         launch=V(2020, 'https://www.proximusnxt.lu/en/5g-beyond-borders', '23 Oct 2020'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.proximusnxt.lu/en/partnerships-finnish-company-nokia-and-swedish-company-ericsson',
                 "Nokia 'selected both to actively participate in the deployment of the 5G network and to progressively modernize the existing "
                 "2G, 3G and 4G networks by 2023' (15 Dec 2020). SPOT-CHECK FIX: previously 'all', but the release has no sole-supplier wording")],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.proximusnxt.lu/en/tango-and-proximus-nxt-partner', 'progressive modernisation of 2G/3G/4G by 2023'),
               R('Huawei', 'not_disclosed', 'https://www.lightreading.com/5g/proximus-dumps-huawei-in-luxembourg-too', '100% of 4G RAN as of Dec 2020 (Strand Consult); replacement by Nokia under way, completion not confirmed')],
         gov=[G('Belgium', 'Belgian State (via SFPIM)', 'government_ministry', 53.51, 'Proximus PLC', 'via_parent', '2025-12-31', PROXIMUS_AR,
                "from the core-panel cache (Proximus 2025 integrated annual report); Proximus's percentage of Proximus Luxembourg not stated")],
         gov_dropped=['Norges Bank Investment Management 1.22% of Proximus PLC (2025-12-31; board seat not checked)'],
         switches=[S('RAN', '4G', 'Huawei', 'Nokia', '2020-12-15', 'not_confirmed', 'https://www.lightreading.com/5g/proximus-dumps-huawei-in-luxembourg-too',
                     "Strand Consult (via Light Reading): Huawei supplied 100% of Proximus Luxembourg's 4G RAN; Nokia to replace the incumbent "
                     "radio vendor and modernise 2G/3G/4G by 2023 (Proximus NXT release, 15 Dec 2020); completion not confirmed")],
         core=V('Ericsson', 'https://www.proximusnxt.lu/en/partnerships-finnish-company-nokia-and-swedish-company-ericsson', 'dual-mode 5G core (Dec 2020)'),
         first_contract=ND('Nokia/Ericsson deals announced 15 Dec 2020, after the Oct 2020 launch, so they were not the first 5G vendor arrangement'),
         vendor_operates=ND()),
    dict(region='Western Europe', country='Luxembourg', operator_name='Orange',
         share=V(15.8, LU_ILR, "ILR 2025 report chart (Orange's 2024 URD cites 15.3% for Jun 2024)", 2025),
         launch=V(2020, 'https://www.orange.lu/en/news/orange-luxembourg-launches-its-5g-network-and-deploys-a-support-programme-for-its-customers/', '23 Nov 2020'),
         ran5=[R('Nokia', 'all', 'https://www.orange.lu/en/news/orange-luxembourg-chooses-european-equipment-manufacturer-nokia-to-deploy-its-5g-network/', "Nokia the 'only radio supplier' (9 Oct 2020)")],
         ran4=[R('Huawei', 'not_disclosed', 'https://www.lightreading.com/5g/proximus-dumps-huawei-in-luxembourg-too', "'fully reliant' on Huawei for 4G RAN as of Dec 2020 (Strand Consult); Orange said the 5G rollout renews all 4G equipment, vendor not named")],
         gov=[G('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX, '21.04% of voting rights',
                chain='Orange S.A. -> Orange Belgium SA -> Orange Luxembourg; percentages not stated'),
              G('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX,
                "8.00% of voting rights; Orange's file groups it with the French State as the public sector",
                chain='Orange S.A. -> Orange Belgium SA -> Orange Luxembourg; percentages not stated')],
         gov_dropped=['Norges Bank Investment Management 1.76% of Orange S.A. (2025-12-31; voting 0.00%; board seat not checked)',
                      'Norges Bank Investment Management 1.28% of Orange Belgium SA (2025-12-31; board seat not checked)'],
         switches=[S('RAN', '4G', 'Huawei', 'not_disclosed', '2020-10-09', 'not_confirmed', 'https://www.lightreading.com/5g/proximus-dumps-huawei-in-luxembourg-too',
                     "Strand Consult: 'fully reliant' on Huawei for 4G RAN (Dec 2020); Orange Luxembourg said its Nokia 5G rollout renews all "
                     "4G equipment but did not name the 4G vendor")],
         core=V('Ericsson', 'https://www.orange.com/en/press-release/orange-selects-suppliers-for-its-5g-stand-alone-5g-sa-networks-in-europe-234893', '5G SA core for Luxembourg (21 Feb 2022)'),
         first_contract=V('2020-10-09', 'https://www.orange.lu/en/news/orange-luxembourg-chooses-european-equipment-manufacturer-nokia-to-deploy-its-5g-network/', 'Nokia selected after a 2019 tender (announcement date)'),
         vendor_operates=ND('Nokia agreement includes deployment and maintenance, not network operation')),
    # ------------------------------------------------------------------ Vietnam
    dict(region='Asia-Pacific', country='Vietnam', operator_name='Viettel',
         share=V(40.0, 'https://www.gsma.com/connectivity-for-good/spectrum/wp-content/uploads/2024/11/GSMA_Accelerating-5G-in-Vietnam-2024.pdf',
                 GSMA_VN_NOTE + ". DISPUTED: the ministry (MIC, 10 Jan 2024) says Viettel has 'more than 50%' of mobile subscriptions "
                 "(~57m) but publishes no operator table; GSMA coded because it gives a figure for every operator", 2024),
         launch=V(2024, 'https://english.mst.gov.vn/viettel-launches-vietnams-first-5g-network-197241016083258314.htm', '15 Oct 2024'),
         ran5=[R('Ericsson', 'most', 'https://www.ericsson.com/en/press-releases/2024/9/viettel-vietnam-extends-ericsson-partnership-through-major-5g-network-award', "awarded 30 Sep 2024; 'majority of provinces' incl. Hanoi, northern and central Vietnam"),
               R('Viettel High Tech', 'small', 'https://www.vietnam.vn/en/2-800-tram-goc-5g-do-viettel-phat-trien-duoc-dua-vao-mang-luoi',
                 'in-house (Viettel subsidiary): 2,800 own-made gNodeBs (Oct 2026), compared with >20,000 new 5G sites by end-2025 (Developing Telecoms)')],
         ran5_note="SPOT-CHECK FIX: Nokia ('some', 22 provinces / ~2,500 sites) removed. The cited nokia.com asset is an Omdia report on core-network vendors and doesn't mention Nokia's Viettel RAN; no other source was checked. Ericsson 'most' was verified against Ericsson's 30 Sep 2024 release ('majority share of Viettel's nationwide 5G deployment'). Viettel High Tech's 2,800 gNodeBs were verified; 'small' is a researcher judgment against >20,000 sites. Also excluded: Qualcomm (chipsets/L1 software inside Viettel's own radios); a Huawei-led group's US$23m '5G equipment' contract and ZTE antenna contracts with unclear year and scope",
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2024/9/viettel-vietnam-extends-ericsson-partnership-through-major-5g-network-award', '4G modernisation in the same areas as its 5G award')],
         gov=[G('Vietnam', 'State of Vietnam (owner rights exercised by the Ministry of National Defence)', 'government_ministry', 100.0, 'Viettel Group', 'direct', '2018-01-11',
                'https://vpcp.chinhphu.vn/chi-dao-dieu-hanh-cua-chinh-phu-thu-tuong-chinh-phu-ngay-11-1-2018-11519405.htm', 'Decree 05/2018/ND-CP: state holds 100% of charter capital')],
         gov_dropped=[],
         core=V('Viettel High Tech', 'https://viettel.com.vn/en/news-events/news/viettel-telecommunications-equipment-on-gartners-prestigious-list/', 'in-house (Viettel subsidiary): own cloud-native 4G EPC/5G core in network since 2022'),
         first_contract=ND('first 5G call with Ericsson in May 2019; contract date not found'),
         vendor_operates=ND('vertically integrated: its own subsidiary Viettel High Tech makes the core and some gNodeBs; no external vendor runs the network')),
    dict(region='Asia-Pacific', country='Vietnam', operator_name='VinaPhone', added=RETROFIT_AT,
         name_note='VNPT-VinaPhone Corporation (VNPT group)',
         share=V(30.0, GSMA_VN, GSMA_VN_NOTE + "; the ministry publishes no current operator table (exp|supp|reg-share-vn)", 2024),
         launch=V(2024, TELEGEO_VN, "commercial 5G from 20 Dec 2024 on 3.7-3.8 GHz (TeleGeography); VNPT's release reproduced by SAMENA "
                  "(25 Dec 2024) says 63 provinces and cities"),
         ran5=[R('Nokia', 'not_disclosed', TELEGEO_VN, 'working with Nokia on its 5G rollout under a contract signed in Oct 2024; no share wording')],
         ran4=[], ran4_note=("EIAS says 'much of Vietnam's preexisting 4G infrastructure was built by Ericsson and Nokia', not specific to "
                             "VinaPhone, so not coded"),
         gov=[G('Vietnam', 'Vietnam Posts and Telecommunications Group (VNPT)', 'state_owned_company', 100.0, 'VNPT-VinaPhone', 'direct', '2015-05-19',
                'https://english.mst.gov.vn/vnpt-launches-3-corporations-197114517.htm',
                'one-member limited company; VNPT holds 100% of its charter capital',
                link_url='https://vnpt.com.vn/file/808080809b97b1bb019b9b3d370b02a9/upload/xdata/202602/20260225103734vnpt_presentation_update_112025_eng.pdf'),
              G('Vietnam', 'Government of Vietnam', 'government_ministry', 100.0, 'VNPT', 'via_parent', '2013',
                'https://via.org.vn/datafiles/files/14778988677027_vietnam-telecommunications-report-q1-2013.pdf',
                "VNPT described as wholly owned by the government (BMI report, Q1 2013); VNPT's Nov 2025 presentation labels it a "
                "'State-Owned Enterprise' without a percentage", parent_pct=100.0)],
         gov_dropped=[],
         core=ND('2020 trial ran on the existing core; core vendor not named'),
         first_contract=V('2024-10', TELEGEO_VN, 'Nokia contract signed Oct 2024; day and scope not stated'),
         vendor_operates=ND('Nokia is the rollout vendor; no managed operations stated')),
    dict(region='Asia-Pacific', country='Vietnam', operator_name='MobiFone', added=RETROFIT_AT,
         share=V(16.0, GSMA_VN, GSMA_VN_NOTE + "; the ministry publishes no current operator table", 2024),
         launch=V(2025, 'https://beta-en.mic.gov.vn/5g-expansion-in-vietnam-mobifone-joins-the-race-to-accelerate-connectivity-197250328092041599.htm',
                  "MIC (28 Mar 2025): officially launched, Vietnam's third 5G operator; Vietnam News dates it 26 Mar 2025. A later MIC "
                  "article (20 Mar 2026) gives 23 Jun 2025; all three dates are in 2025"),
         ran5=[R('Huawei', 'not_disclosed', 'https://economictimes.indiatimes.com/industry/telecom/vietnam-eyes-new-5g-deals-with-chinese-tech-firms-sources-say-despite-us-warnings/printarticle/129131443.cms',
                 "Reuters (via Economic Times, 6 Mar 2026): a Huawei 5G base station seen on a MobiFone-branded tower in Ho Chi Minh City; "
                 "scope not established. UNVERIFIED: the fetch tool refuses this site")],
         ran5_note=("not coded: Rakuten Symphony 4G/5G Open RAN pilot (MoU 5 Jun 2025; a pilot, not the commercial network); Samsung "
                    "equipment linked to MobiFone in a 2019 SCMP article (trial era)"),
         ran4=[], ran4_note='4G vendor not named in the sources',
         gov=[G('Vietnam', 'State of Vietnam (ownership representative: Ministry of Public Security)', 'government_ministry', None, 'MobiFone', 'direct', '2025-02-28',
                'https://news.tuoitre.vn/vietnams-mobifone-now-under-umbrella-of-public-security-ministry-10384901.htm',
                "state ownership transferred from CMSC to the Ministry of Public Security on 28 Feb 2025 (verified 2026-11-23); the "
                "article gives no percentage, and the '100% state-owned' wording in the search comes from a wiki-style site that is not cited")],
         gov_dropped=[],
         core=ND('Ericsson EPC/EPG appears only in the Nov 2020 4G/5G trial document (a Scribd copy, not cited); operational 5G core vendor not named'),
         first_contract=ND('Ericsson trial agreement (19 Nov 2020) and Nokia 5G collaboration agreement (27 Feb 2023, MST) are not supply contracts'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Tajikistan
    dict(region='Central Asia & Eastern Europe', country='Tajikistan', operator_name='Tcell',
         share=V(33.9, TJ_SHARE, TJ_NOTE, 2024),
         launch=V(2020, 'https://www.telecompaper.com/news/tcell-launches-5g-network--1349663', 'Dushanbe, Aug 2020'),
         ran5=[], ran5_note='5G RAN vendor not named; a second pass on 2026-11-23 (exp|supp|tcell-vendor) found none',
         ran4=[], ran4_note=("only GSM-era Huawei (2002) found. China Index's 'Huawei already provides 4G to Tcell' was checked on "
                             "2026-11-23: it links only to a Huawei 4G modem product page on tcell.tj, so it is not coded as a network supplier"),
         gov=[], gov_note='100% owned by AKFED (Aga Khan Fund for Economic Development) via CATD BV since 2017; AKFED is not a government', gov_dropped=[],
         core=ND(), first_contract=ND(),
         vendor_operates=ND('a personal LinkedIn profile claims Huawei managed services in 2012-2014 (not cited)')),
    dict(region='Central Asia & Eastern Europe', country='Tajikistan', operator_name='MegaFon',
         share=V(22.9, TJ_SHARE, TJ_NOTE, 2024),
         launch=V(2020, 'https://megafon.tj/about', 'central Dushanbe from 21 Feb 2020'),
         ran5=[], ran5_note='vendor not named; a second pass on 2026-11-23 (exp|supp|megafon-tj-vendor) found none',
         ran4=[], ran4_note='vendor not named (also none in the second pass)',
         gov=[G('Tajikistan', 'OJSC Tojiktelecom', 'state_owned_company', 25.0, 'TT Mobile (MegaFon Tajikistan)', 'direct', '2021-10-26',
                'https://asiaplus.news/en/2021/10/26/tajikistan-has-expensive-and-slow-internet-connection/',
                "MegaFon PJSC holds the other 75%. Also written Tajiktelecom. State link: Asia-Plus (2007) and SAMENA describe it as state-owned",
                link_url='https://asiaplus.news/en/2007/03/10/tajikistan-doesnt-need-megafon/')],
         gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Trinidad and Tobago
    dict(region='Latin America & Caribbean', country='Trinidad and Tobago', operator_name='bmobile',
         share=ND("TATT: the two MNOs' shares were 'approximately comparable' at end-2023; figures redacted"),
         launch=V(2019, 'https://trinidadexpress.com/features/local/5g-is-here/article_96af41c0-1ade-11ea-a888-4b2424e4ff02.html', '4 Dec 2019'),
         ran5=[R('Huawei', 'not_disclosed', 'https://technewstt.com/bd1227/', 'Huawei technology partner, Massive MIMO for 5G (Dec 2019)')],
         ran4=[R('Huawei', 'not_disclosed', 'https://technewstt.com/bd1227/', 'TDD 4G LTE equipment (Dec 2019)')],
         gov=[G('Trinidad and Tobago', 'National Enterprises Limited', 'state_holding_company', 51.0, 'TSTT', 'direct', '2026', 'https://www.tstt.co.tt/company-overview',
                'Cable & Wireless (Liberty Latin America) holds the other 49%', link_url='https://papers.ttparliament.org/document-category/administrative-reports/'),
              G('Trinidad and Tobago', 'Corporation Sole (Minister of Finance)', 'government_ministry', 51.0, 'National Enterprises Limited', 'via_parent', '2023-09-30',
                'https://papers.ttparliament.org/document-category/administrative-reports/', 'NEL annual administrative report FY2023, laid 13 Jan 2025',
                parent_pct=51.0)],
         gov_dropped=[],
         core=ND('5G launched in partnership with Huawei; core scope not stated'),
         first_contract=V('2019-12', 'https://oxfordbusinessgroup.com/reports/trinidad-tobago/2020-report/economy/bright-prospects-investors-take-steps-to-position-the-country-as-a-regional-centre-for-business-process-outsourcing', 'TSTT announced a Huawei 5G deal in Dec 2019'),
         vendor_operates=V(False, 'https://bmobile.co.tt/covid-response/our-network/', "TSTT's own team monitors, optimises and protects the network")),
]
