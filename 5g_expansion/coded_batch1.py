"""Researcher coding of the first-10 expansion batch (Prof. Shen's reduced schema), coded in-session on
2026-11-15 from the cached searches in data/5g_expansion_searches.jsonl plus NBIM's 31 Dec 2025 equity
holdings file. Values come only from the cited source; anything a source didn't state is not_disclosed.

Source-type mapping (the schema allows three types):
  company_report : the operator's, its parent's, a vendor's or a shareholder's own publication (press release,
                   annual report, filing, NBIM's holdings list)
  regulator      : national regulators and other official government or intergovernmental bodies
                   (ministries, statistics agencies, parliament papers, ITU)
  news_article   : news media and other third-party publications (trade press, NGOs, academic books, GSMA)
Not cited at all: Wikipedia, personal LinkedIn profiles, eSIM/aggregator sites.

Government stakes: one row per holder; never summed. pct_of names the company the percentage is of, so
a stake in a parent is recorded at the parent level and never multiplied down the chain.
"""

NBIM = 'https://www.nbim.no/api/investments/v2/report/?assetType=eq&date=2025-12-31&fileType=xlsx'
CO, REG, NEWS = 'company_report', 'regulator', 'news_article'


def V(value, url, stype, note='', year=None):
    return dict(status='value', value=value, year=year, source_url=url, source_type=stype, note=note)


def ND(note=''):
    return dict(status='not_disclosed', value=None, year=None, source_url='', source_type='', note=note)


def R(vendor, share, url, stype, note=''):
    assert share in ('all', 'most', 'some', 'small', 'not_disclosed'), share
    return dict(vendor=vendor, share_category=share, source_url=url, source_type=stype, note=note)


def G(government, holder, pct, pct_of, basis, as_of, url, stype, note=''):
    assert basis in ('direct', 'via_parent'), basis
    return dict(government=government, holder=holder, pct=pct, pct_of=pct_of, basis=basis, as_of=as_of,
                source_url=url, source_type=stype, note=note)


# Israel shares: one consistent source for all four operators.
IL_SHARE = 'https://investors.cellcom.co.il/wp-content/uploads/2026/06/Cellcom-Israel-Ltd.-Periodic-Report-for-2025.pdf'
IL_SHARE_NOTE = "Cellcom's own estimate of the market at 31 Dec 2025 (Cellcom 32, Partner 23, Pelephone 23, HOT 14)"
LU_ILR = 'https://www.ilr.lu/wp-content/uploads/ilr-stat-10062026-Rapport-telecom-2025.pdf'
UY_SHARE = 'https://www.telcobrief.com/en/market-data/uruguay'
UY_NOTE = ("Dec 2025 URSEC subscription counts via TelcoBrief: ANTEL 2,448,826; Movistar 1,344,705; Claro 1,139,384; "
           "total 4,932,915. Other measures conflict: la diaria (citing URSEC) gives ANTEL 62 / Movistar 20 / Claro 18 "
           "for 'mobile services' (measure unstated); TeleSemana gives Claro 16.5% of subscriptions in Dec 2024.")
UZ_SHARE = 'https://freedomhouse.org/country/uzbekistan/freedom-net/2024'
UZ_NOTE = 'Freedom House citing Dec 2023 operator data (Ucell 25, Beeline 25, Uzbektelecom 23, Mobiuz 22)'
TJ_SHARE = 'https://tadviser.com/index.php/Article:Communications_(Tajik_market)'
TJ_NOTE = ('computed from 2024 subscriber counts for all six operators: Tcell 2.66m, Babilon-Mobile 1.88m, '
           'MegaFon 1.80m, Zet-Mobile 1.00m, Tajiktelecom 0.275m, O Mobile 0.241m (total 7.856m)')
ORANGE_XLSX = 'https://assets.orange.com/pm_12751_545_545865-jr7yvi3osw.xlsx'
PROXIMUS_AR = 'https://www.proximus-cdn.com/dam/jcr:44041fd1-b790-497d-b397-cb03869fab27/proximus-integrated-annual-report-2026-v1.1_en.pdf'
VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
OOREDOO_AR = 'https://www.ooredoo.com/wp-content/uploads/2026/03/2025-Ooredoo-Annual-Report_English_FINAL.pdf'
OOREDOO_OWN = 'https://www.ooredoo.com/wp-content/uploads/2026/07/Ownership-Structure-Top-Shareholders.pdf'
E_AND_NOTE = ('state link for e& comes from the data/state_holders.csv reference list (pending Prof. Shen review); '
              'the Vodafone filing names e& but does not call it state-owned')
PHI_DISPUTE = ('DISPUTED: the 2020 Partner/HOT (PHI shared network) 5G deployment is attributed to Ericsson by INSS '
               'and by Israelpedia, but to Nokia by a Bezeq/Pelephone-related report; secondary sources also say '
               'Partner signed an Ericsson MoU in Jan 2023 to make Ericsson its "primary supplier". Coded Ericsson '
               'with no share category.')

OPERATORS = [
    # ------------------------------------------------------------------ Libya
    dict(region='Africa', country='Libya', operator_name='Al-madar',
         share=ND("only 'more than 3 million subscribers' (Oct 2020, Operator Watch) found; no market total for that date"),
         launch=V(2019, 'https://www.libyaherald.com/2019/10/al-madar-launches-libyas-first-5g-mobile-internet-service-first-in-north-africa/', NEWS,
                  "29 Oct 2019, limited areas. DISPUTED: Libya Herald (Jan 2026) also reports Almadar launching 'Libya's first 5G "
                  "service in Tripoli'; coded the 2019 launch"),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.libyaherald.com/2021/11/10/libya-needs-5g-and-5g-is-ready-for-libya-andrea-missori-country-manager-ericsson-libya/', NEWS,
                 "Nov 2021: Al-Madar 5G service 'powered by Ericsson' over its commercial 4G network")],
         ran4=[R('Huawei', 'not_disclosed', 'https://freedomhouse.org/country/libya/freedom-net/2019', NEWS, 'Huawei worked on introducing 4G (Oct 2018)'),
               R('Nokia', 'small', 'https://www.linkedin.com/posts/nokia-for-service-providers_al-madar-leverages-nokias-innovative-capacity-activity-7399779199722553344-gluF', CO,
                 "Nokia's own post (Nov 2025): one C-RAN LTE deployment at Benghazi National Stadium")],
         ran4_note='Huawei/ZTE/Ericsson LTE work is also described in personal LinkedIn profiles, which are not cited',
         gov=[G('Libya', 'Government of Libya (through LPTIC, the state holding company)', None, 'Al-madar', 'via_parent', '2026-01-25',
                'https://almadar.ly/en/Pages/Who-we-are.aspx', CO, "Al-Madar describes itself as government-owned; LPTIC is its parent; percentage not disclosed")],
         core=ND('Ericsson-powered 5G ran over the existing 4G network (NSA), but no source names the EPC/5GC vendor'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Kenya
    dict(region='Africa', country='Kenya', operator_name='Safaricom',
         share=V(65.3, 'http://www.ca.go.ke/sites/default/files/2025-12/Sector%20Statistics%20Report%20Q1%202025-2026_0.pdf', REG,
                 'Communications Authority, mobile subscriptions at 30 Sep 2025', 2025),
         launch=V(2022, 'https://www.safaricom.co.ke/media-center-landing/press-releases/safaricom-announces-commercial-launch-of-5g-services', CO, 'commercial launch 27 Oct 2022'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.safaricom.co.ke/media-center-landing/press-releases/safaricom-switches-on-5g-across-kenya', CO, 'one of two named 5G technology partners'),
               R('Nokia', 'not_disclosed', 'https://www.safaricom.co.ke/media-center-landing/press-releases/safaricom-switches-on-5g-across-kenya', CO, 'one of two named 5G technology partners')],
         ran4=[], ran4_note='no 4G RAN vendor named in the annual reports searched',
         gov=[G('Kenya', 'Government of Kenya (Cabinet Secretary to the National Treasury)', 20.0, 'Safaricom PLC', 'direct', '2026-06-30',
                'https://www.safaricom.co.ke/annualreport_2026/pdf/Safaricom_IAR_20431_2026_12h00_Interactive.pdf', CO,
                '35.00% at 31 Mar 2025 (FY2025 financial statements); the government sold 15% to Vodacom, completed 30 Jun 2026'),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 0.82, 'Safaricom PLC', 'direct', '2025-12-31', NBIM, CO),
              G('United Arab Emirates', 'e& (Emirates Telecommunications Group)', 17.005026, 'Vodafone Group Plc', 'via_parent', '2026-03-31', VODAFONE_AR, CO,
                'ownership chain: Vodafone Group -> Vodacom (65.10%) -> Vodafone Kenya (Vodacom majority since 30 Jun 2026) -> 55% of Safaricom. ' + E_AND_NOTE),
              G('Norway', 'Norges Bank', 3.0004, 'Vodafone Group Plc', 'via_parent', '2026-03-31', VODAFONE_AR, CO,
                "NBIM's holdings file shows 1.56% at 31 Dec 2025; Vodafone's later filing coded")],
         gov_note='Vodacom-level state holders not found in a current filing (an older report gave GEPF 12.9% in 2017); NBIM held no Vodacom shares at 31 Dec 2025',
         core=ND('Nokia and Huawei are the named 5G partners; the core vendor is not specified'),
         first_contract=ND("Huawei/Nokia partner selection was announced in the 'switches on 5G' release; the searches disagree on its date (19 Mar 2021 vs 20 Oct 2022)"),
         vendor_operates=ND()),
    dict(region='Africa', country='Kenya', operator_name='Airtel',
         share=V(29.6, 'https://www.ca.go.ke/increased-smartphone-adoption-and-mobile-money-drive-growth-telecoms-sector-report-shows', REG,
                 'Communications Authority, quarter to 30 Sep 2024 (FY2023/24 annual: 29.5%)', 2024),
         launch=V(2023, 'https://www.ca.go.ke/sites/default/files/CA/Speeches/Remarks%20byDirector%20General,%20CA%20During%20the%20Launch%20of%205G%20By%20Airtel%20Network%20on%206th%20July%202023.pdf', REG, 'launched 6 Jul 2023'),
         ran5=[R('Nokia', 'not_disclosed', 'https://techtrendske.co.ke/2020/12/01/nokia-and-airtel-kenya-lay-5g-foundations-in-kenya/', NEWS,
                 'Dec 2020 three-year deal for 5G-ready AirScale Single RAN; no source confirms the vendor of the 5G network launched in 2023')],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.airtelkenya.com/Airtel-selects-Ericsson-to-modernize-its-4G-network-in-Kenya', CO, '4G RAN modernisation, signed Aug 2020'),
               R('Nokia', 'not_disclosed', 'https://techtrendske.co.ke/2020/12/01/nokia-and-airtel-kenya-lay-5g-foundations-in-kenya/', NEWS, '2G/3G/4G modernisation in Nairobi and other areas (Dec 2020)')],
         gov=[G('Qatar', 'Qatar Holding LLC', 3.67, 'Airtel Africa plc', 'via_parent', '2025-03-31',
                'https://cdn-webportal.airtelstream.net/website/investor/main/AR2025/reports/p054-directors-report-13853.html', CO,
                "Airtel Africa owns Airtel Kenya via Bharti Airtel Kenya B.V. (99.99975%). Qatar Holding's state link: Ooredoo's ownership disclosure labels it 'State of Qatar / Qatar Holding' (" + OOREDOO_OWN + ')'),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 0.39, 'Airtel Africa plc', 'via_parent', '2025-12-31', NBIM, CO),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 1.06, 'Bharti Airtel Ltd (ultimate parent)', 'via_parent', '2025-12-31', NBIM, CO, 'ownership 1.06%, voting 0.90%')],
         core=ND('Nokia deal laid groundwork for 5G; no core/EPC vendor named'),
         first_contract=ND('Ericsson (Aug 2020) and Nokia (Dec 2020) deals were for "5G-ready" 4G equipment, not explicitly 5G contracts'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Singapore
    dict(region='Asia-Pacific', country='Singapore', operator_name='Singtel',
         share=V(50.7, 'https://cdn2.singteldigital.com/content/dam/singtel/investorRelations/annualReports/2025/Singtel-AR25.pdf', CO, 'at 31 Mar 2025', 2025),
         launch=V(2020, 'https://cdn1.singteldigital.com/content/dam/singtel/business/sb/articles/transforming-singapores-future-with-5g.pdf', CO, 'NSA commercial Sep 2020; SA May 2021'),
         ran5=[R('Ericsson', 'all', 'https://cdn2.singteldigital.com/content/dam/singtel/investorRelations/annualReports/2020/agm2020-responses-to-questions.pdf', CO,
                 "Singtel chose 'Ericsson's equipment solely' for its 5G network (2020 AGM responses)")],
         ran4=[], ran4_note='4G RAN vendor not named in the sources found',
         gov=[G('Singapore', 'Temasek Holdings', 50.56, 'Singtel', 'direct', '2026-06-30',
                'https://cdn1.singteldigital.com/content/dam/singtel/investorRelations/annualReports/2026/Letter-to-Shareholders.pdf', CO,
                'computed from share counts: 8,304,071,181 direct shares within a 51.99% combined interest'),
              G('Singapore', 'Temasek Holdings (deemed, via subsidiaries/associates)', 1.43, 'Singtel', 'via_parent', '2026-06-30',
                'https://cdn1.singteldigital.com/content/dam/singtel/investorRelations/annualReports/2026/Letter-to-Shareholders.pdf', CO,
                'computed from 235,133,564 deemed shares within the 51.99% combined interest'),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 0.76, 'Singtel', 'direct', '2025-12-31', NBIM, CO)],
         core=V('Ericsson', 'https://www.ericsson.com/en/cases/2022/singtel-and-ericsson', CO, 'dual-mode 5G Core; NSA used an upgraded Ericsson EPC'),
         first_contract=ND('Ericsson 5G pilot network launched July 2018; contract date not found'),
         vendor_operates=ND()),
    dict(region='Asia-Pacific', country='Singapore', operator_name='StarHub',
         share=ND('no overall share found; an IMDA filing gives Dec 2024 prepaid 22.2% / postpaid 22.8%'),
         launch=V(2020, 'https://www.starhub.com/about-us/newsroom/2020/august/first-to-say-hello-5g-with-starhub.html', CO, 'early-access 5G from 18 Aug 2020; SA in 2021'),
         ran5=[R('Nokia', 'not_disclosed', 'https://ir.starhub.com/misc/ar2020.pdf', CO, 'launched 5G Aug 2020 with Nokia as technology partner (3.5 GHz SA RAN shared with M1)')],
         ran4=[R('Huawei', 'not_disclosed', 'https://ir.starhub.com/misc/ar2015.pdf', CO, 'HetNet/LTE infrastructure partner (2015)'),
               R('Nokia', 'not_disclosed', 'https://ir.starhub.com/misc/ar2016.pdf', CO, 'LTE-Advanced technology (2016)')],
         gov=[G('Singapore', 'Temasek Holdings', 56.13, 'StarHub Ltd', 'via_parent', '2025-12-31',
                'https://links.sgx.com/FileOpen/StarHub%20Annual%20Report%202025.ashx?App=Announcement&FileID=882452', CO,
                'deemed interest through ST Telemedia -> STT Communications -> Asia Mobile Holding Co -> Asia Mobile Holdings (55.959% direct after 27 Mar 2026 share issue)'),
              G('Qatar', 'Qatar Investment Authority', 53.0, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', OOREDOO_AR, CO,
                "Ooredoo (via OIH Investment LLC) owns ~25% of Asia Mobile Holdings, StarHub's 55.96% holder"),
              G('Qatar', 'General Retirement & Social Insurance Authority', 13.0, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', OOREDOO_AR, CO, 'same chain as QIA'),
              G('Qatar', 'General Military Retirement and Social Insurance Authority', 2.0, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', OOREDOO_AR, CO, 'same chain as QIA'),
              G('United Arab Emirates', 'Abu Dhabi Investment Authority', 4.99, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', OOREDOO_AR, CO, 'same chain as QIA'),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 1.88, 'Ooredoo Q.P.S.C.', 'via_parent', '2025-12-31', NBIM, CO, 'same chain as QIA'),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 0.57, 'StarHub Ltd', 'direct', '2025-12-31', NBIM, CO)],
         core=ND(), first_contract=ND('Nokia 5G NR pilot in 2018; no dated 5G contract found'), vendor_operates=ND()),
    dict(region='Asia-Pacific', country='Singapore', operator_name='M1',
         share=ND('no overall share found; an IMDA filing gives Dec 2024 prepaid 13.5% / postpaid 23.9%'),
         launch=V(2020, 'https://www.m1.com.sg/about-us/news-releases/2020/m1-enables-5g-for-everyone', CO, 'commercial NSA 24 Sep 2020; SA 2021'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.m1.com.sg/about-us/news-releases/2020/m1-granted-final-5g-network-license-from-imda', CO,
                 'Nokia selected for the nationwide 3.5 GHz SA RAN; Ericsson/Nokia/Huawei named only as possible mmWave vendors')],
         ran4=[], ran4_note='Huawei appears only as an LTE-Advanced trial partner (Jan 2016), not as a confirmed supplier',
         gov=[G('Singapore', 'Temasek Holdings', 33.38, 'M1 Limited', 'via_parent', '2025',
                'https://www.imda.gov.sg/-/media/imda/files/regulations-and-licensing/regulations/consultations/2025/simba-and-m1/annex-b-non-confidential-abbreviated-statement-submitted-by-simba-and-m1.pdf', CO,
                "indirect interest as filed with IMDA by SIMBA/M1; Keppel Ltd holds 83.86% indirect; Keppel's sale of M1 to SIMBA/Tuas pending. Fullerton Management 8.07% indirect listed but not identified as state in the source"),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 1.36, 'Keppel Ltd', 'via_parent', '2025-12-31', NBIM, CO)],
         core=V('Nokia', 'https://www.nokia.com/newsroom/nokia-and-m1-partner-with-5g-standalone-core-to-drive-singapores-5g-ecosystem/', CO, 'cloud-native 5G SA core, partnership announced 13 Jan 2021'),
         first_contract=V('2020-06', 'https://www.datacenterdynamics.com/en/news/singapore-finalizes-5g-contract-winners-nokia-and-ericsson-named-suppliers/', NEWS,
                          "Nokia named as M1/StarHub 5G SA RAN supplier when IMDA finalised licences (June 2020). The searches date M1's own Nokia release to both 24 Jun and 24 Sep 2020"),
         vendor_operates=ND()),
    dict(region='Asia-Pacific', country='Singapore', operator_name='Simba',
         share=V(10.0, 'https://www.imda.gov.sg/-/media/imda/files/regulations-and-licensing/regulations/consultations/2025/simba-and-m1/annex-b-non-confidential-abbreviated-statement-submitted-by-simba-and-m1.pdf', CO,
                 "SIMBA's own submission to IMDA, early 2023; Business Times cites BMI at 11% for 2025", 2023),
         launch=ND('5G NSA market trial 10 Sep 2021; IMDA 5G rights from 1 Jan 2022; all plans 5G-capable Sep 2023; commercial launch date not found'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.businesstimes.com.sg/companies-markets/telcos-media-tech/key-considerations-hanging-over-approval-simba-m1s-merger', NEWS,
                 "Business Times (11 Mar 2026): SIMBA's 5G network is 'built on' Huawei technology")],
         ran4=[], ran4_note='4G vendor not named; follow-up search also found none',
         gov=[G('Norway', 'Norges Bank Investment Management (GPFG)', 0.65, 'Tuas Ltd (100% parent)', 'via_parent', '2025-12-31', NBIM, CO)],
         core=ND("Business Times says the network is built on Huawei technology but doesn't say whether that includes the core"),
         first_contract=ND(),
         vendor_operates=V(False, 'https://support.simba.sg/hc/en-us/articles/26550149956505-Whose-infrastructure-does-SIMBA-use', CO,
                           "equipment above the end-user fibre layer is 'built, managed, and owned by SIMBA'")),
    # ------------------------------------------------------------------ Uzbekistan
    dict(region='Central Asia & Eastern Europe', country='Uzbekistan', operator_name='Ucell',
         share=V(25.0, UZ_SHARE, NEWS, UZ_NOTE, 2023),
         launch=V(2021, 'https://ucell.uz/en/company_news/ucell_launches_5g_in_tashkent', CO, 'Tashkent, 14 Apr 2021'),
         ran5=[R('Huawei', 'not_disclosed', 'https://ucell.uz/en/company_news/ucell_launches_5g_in_tashkent', CO, 'equipment for the first commercial 5G in Tashkent (2021); also central Tashkent sites (2022)'),
               R('Nokia', 'not_disclosed', 'https://ucell.uz/en/company_news/ucell_5g_in_tashkent_and_samarkand_is_real_now', CO, 'central Tashkent sites (Aug 2022)'),
               R('ZTE', 'not_disclosed', 'https://ucell.uz/en/company_news/ucell_5g_in_tashkent_and_samarkand_is_real_now', CO, 'central Samarkand NSA sites (Aug 2022)')],
         ran4=[R('ZTE', 'most', 'https://www.zte.com.cn/global/about/magazine/zte-technologies/2012/1/en_595/283276.html', CO, "'main LTE equipment supplier' (ZTE case study, 2012); UzDaily (Sep 2024) repeats ZTE as 4G supplier")],
         gov=[G('Uzbekistan', 'Agency for State Assets Management (ASAM)', 49.0, 'Digital Holding (100% owner of COSCOM/Ucell)', 'via_parent', '2021-09-30',
                'https://ucell.uz/uz/company_news/digital_holding', CO, 'Digital Holding formed 30 Sep 2021: Digital Invest (MegaFon/USM JV) 51%, ASAM 49%')],
         core=ND('SA environment is multivendor (Nokia, Huawei, ZTE interoperate); core vendor not named'),
         first_contract=ND('5G testing began 2019; no dated vendor contract'), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Uzbekistan', operator_name='Uzbektelecom',
         share=V(23.0, UZ_SHARE, NEWS, UZ_NOTE + '; brand Uzmobile', 2023),
         launch=V(2022, 'https://uztelecom.uz/en/news/news/for-the-first-time-in-the-cis-uztelecom-launched-5g-network-in-all-regional-centres-of-uzbekistan/', CO, 'Tashkent Mar 2022; all regional centres Sep 2024'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/uzbektelecom-pens-huawei-and-zte-deals-worth-506m-for-major-network-expansion/', NEWS, 'Huawei and ZTE contracts (US$506.8m) incl. 388 + 325 5G base stations, not split by vendor; Huawei 5.5G launch Sep 2024'),
               R('ZTE', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/uzbektelecom-pens-huawei-and-zte-deals-worth-506m-for-major-network-expansion/', NEWS, 'same contracts, not split by vendor')],
         ran4=[R('Huawei', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/uzbektelecom-pens-huawei-and-zte-deals-worth-506m-for-major-network-expansion/', NEWS, 'thousands of 3G/4G base stations under Huawei+ZTE contracts, not split by vendor'),
               R('ZTE', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/uzbektelecom-pens-huawei-and-zte-deals-worth-506m-for-major-network-expansion/', NEWS, 'same')],
         gov=[G('Uzbekistan', 'Ministry of Economy and Finance', 67.17, 'Uzbektelecom JSC', 'direct', '2025-12-31',
                'https://openinfo.uz/media/int_report/08c4d98a-95e7-4ee7-8771-8093b193f1f5.pdf', CO, '2025 consolidated financial statements'),
              G('Uzbekistan', 'National Investment Fund of Uzbekistan (UzNIF; 100% owned by the Ministry of Economy and Finance)', 25.0, 'Uzbektelecom JSC', 'direct', '2025-12-31',
                'https://openinfo.uz/media/int_report/08c4d98a-95e7-4ee7-8771-8093b193f1f5.pdf', CO, '25% transferred from the Ministry'),
              G('Uzbekistan', 'State Assets Management Agency', 2.033, 'Uzbektelecom JSC', 'direct', '2026-08-28',
                'https://uztelecom.uz/uploads/media/2024/%D0%AF%D0%BD%D0%B2%D0%B0%D1%80%D1%8C/STRUCTURE%20OF%20SHARE%20CAPITAL.pdf', CO,
                "DISPUTED: the search dates this share-structure file to 28 Aug 2026, but its URL path says 2024/January, and the FY2025 statements say the remaining 7.83% is held by entities each under 1%"),
              G('Uzbekistan', 'SUE Center of Radio Communication, Broadcasting and Television', 0.34, 'Uzbektelecom JSC', 'direct', '2026-08-28',
                'https://uztelecom.uz/uploads/media/2024/%D0%AF%D0%BD%D0%B2%D0%B0%D1%80%D1%8C/STRUCTURE%20OF%20SHARE%20CAPITAL.pdf', CO, 'same file as the State Assets Management Agency row'),
              G('Uzbekistan', 'SUE Unicon.uz', 0.002, 'Uzbektelecom JSC', 'direct', '2026-08-28',
                'https://uztelecom.uz/uploads/media/2024/%D0%AF%D0%BD%D0%B2%D0%B0%D1%80%D1%8C/STRUCTURE%20OF%20SHARE%20CAPITAL.pdf', CO, 'same file')],
         core=ND('network is NSA; EPC vendor not named'),
         first_contract=ND('Huawei pre-trial 5G tests in 2019; Huawei supply agreement 1 May 2021 not stated to cover 5G'), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Uzbekistan', operator_name='Mobiuz',
         share=V(22.0, UZ_SHARE, NEWS, UZ_NOTE + '; BMI (via Times of Central Asia) gives 20.9% at end-2024', 2023),
         launch=V(2022, 'https://developingtelecoms.com/telecom-technology/wireless-networks/13947-mobiuz-goes-live-with-5g-services-in-uzbek-capital.html', NEWS, 'Tashkent, Sep 2022'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/mobiuz-launches-5g-services-in-uzbek-capital', NEWS, 'Huawei supplied the equipment for the Sep 2022 launch')],
         ran4=[R('Huawei', 'not_disclosed', 'https://www.uzdaily.uz/en/mobiuz-expands-its-technical-capabilities/', NEWS, 'Huawei shipments under a US$150m modernisation project (Nov 2020)'),
               R('ZTE', 'not_disclosed', 'https://www.zte.com.cn/global/about/news/Mobiuz-and-ZTE-drive-digital-transformation-in-Uzbekistan-with-successful-network-modernization-project.html', CO, 'modernisation in Karakalpakstan and Khorezm, 1,200+ base stations (Sep 2025); generation not stated')],
         gov=[G('Uzbekistan', 'Digital Economy Development Support Fund "Digital Trust" (state fund)', 100.0, 'Universal Mobile Systems LLC (Mobiuz)', 'direct', '2025-06-09',
                'https://gov.uz/en/davaktiv/news/view/59663', REG, "state sale of 100% launched 9 Jun 2025; a US-led consortium was selected 4 Jun 2026, closing not confirmed")],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Uruguay
    dict(region='Latin America & Caribbean', country='Uruguay', operator_name='ANTEL',
         share=V(49.64, UY_SHARE, NEWS, UY_NOTE, 2025),
         launch=V(2023, 'https://antel.com.uy/institucional/sala-de-prensa/eventos/antel-lanzo-la-tecnologia-5g-en-uruguay', CO,
                  "national launch 28 Jun 2023. DISPUTED: Nokia (10 Apr 2019) describes ANTEL's 'first commercial 5G network' in Maldonado; coded ANTEL's own launch"),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/antel-and-nokia-make-the-first-5g-call-on-a-commercial-network-in-latin-america/', CO, 'Nokia 5G radio network, initial deployment Apr 2019')],
         ran4=[R('Alcatel-Lucent (now Nokia)', 'not_disclosed', 'https://www.prnewswire.com/news-releases/antel-and-alcatel-lucent-launch-4glte-services-in-uruguay-and-establish-the-first-commercial-4glte-wireless-network-in-a-latin-american-country-135501863.html', CO, 'end-to-end LTE incl. base stations (Dec 2011)')],
         gov=[G('Uruguay', 'State of Uruguay', 100.0, 'ANTEL', 'direct', '2026-10-31',
                'https://www.uruguayxxi.gub.uy/uploads/informacion/a2ed35ca0ef7e73184e708515899e831f9bf565c.pdf', REG, 'state enterprise (Uruguay XXI, government agency); no share register')],
         core=ND('Nokia supplied radio, transport and services; core not stated'),
         first_contract=V('2019-04-10', 'https://www.nokia.com/newsroom/antel-and-nokia-make-the-first-5g-call-on-a-commercial-network-in-latin-america/', CO, 'announcement of the completed Nokia 5G network; signing date not disclosed'),
         vendor_operates=ND()),
    dict(region='Latin America & Caribbean', country='Uruguay', operator_name='Movistar',
         share=V(27.26, UY_SHARE, NEWS, 'computed 1,344,705 / 4,932,915. ' + UY_NOTE, 2025),
         launch=V(2023, 'https://portal.powertec.com.au/industry-resources/companies/movistar-uruguay', NEWS, 'Sep 2023 (weak source: industry directory)'),
         ran5=[R('Nokia', 'not_disclosed', 'https://library.oapen.org/bitstream/handle/20.500.12657/99202/9781003489450_10.4324_9781003489450-11.pdf?sequence=1&isAllowed=y', NEWS, 'academic book (2025): Nokia partner for the 2023 5G tender')],
         ran4=[], ran4_note='Ericsson was sole GSM supplier (2005) and 3G supplier (2007); no LTE vendor found',
         gov=[G('Sweden', 'Tredje AP-fonden (AP3, state pension buffer fund)', 0.62, 'Millicom International Cellular', 'via_parent', '2026',
                'https://www.marketbeat.com/instant-alerts/filing-millicom-international-cellular-sa-tigo-shares-purchased-by-calamos-advisors-llc-2026-11-09/', NEWS,
                'aggregator shareholder data, not an official filing'),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 0.69, 'Millicom International Cellular', 'via_parent', '2026',
                'https://www.marketbeat.com/instant-alerts/filing-millicom-international-cellular-sa-tigo-shares-purchased-by-calamos-advisors-llc-2026-11-09/', NEWS,
                "aggregator data; NBIM's own file shows no Millicom holding at 31 Dec 2025"),
              G('United States (State of Wyoming)', 'State of Wyoming', None, 'Millicom International Cellular', 'via_parent', '2026',
                'https://www.marketbeat.com/instant-alerts/filing-millicom-international-cellular-sa-tigo-shares-purchased-by-calamos-advisors-llc-2026-11-09/', NEWS,
                '2,241 shares; percentage negligible and not stated')],
         gov_note=("Telefonica sold 100% of Telefonica Moviles del Uruguay to Millicom on 7 Oct 2025 (Telefonica disclosure), so SEPI and PIF no longer reach it. "
                   "Millicom's holders above 3%: Niel family 44.1%, Dodge & Cox, BlackRock; no state holder (2025 SEC annual filing)"),
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    dict(region='Latin America & Caribbean', country='Uruguay', operator_name='Claro',
         share=V(23.10, UY_SHARE, NEWS, 'computed 1,139,384 / 4,932,915. ' + UY_NOTE, 2025),
         launch=ND('3.5 GHz spectrum won May 2023; commercial launch date not found in two searches'),
         ran5=[R('Nokia', 'not_disclosed', 'https://developingtelecoms.com/telecom-technology/wireless-networks/11321-claro-uruguay-begins-5g-network-trials.html', NEWS, 'Nokia access network in 28 GHz trials (Jun 2021); an academic book names Nokia for the 2023 deployment')],
         ran4=[], ran4_note='only a personal LinkedIn profile mentions Nokia LTE work (not cited)',
         gov=[G('Norway', 'Norges Bank Investment Management (GPFG)', 0.07, 'America Movil (100% parent)', 'via_parent', '2025-12-31', NBIM, CO)],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Israel
    dict(region='Middle East', country='Israel', operator_name='Cellcom',
         share=V(32.0, IL_SHARE, CO, IL_SHARE_NOTE, 2025),
         launch=V(2020, IL_SHARE, CO, '5G launched 2020 per 2025 periodic report'),
         ran5=[], ran5_note='5G RAN vendor not named in filings; 4G/5G network shared with Wecom',
         ran4=[R('Nokia (NSN Israel)', 'not_disclosed', IL_SHARE, CO, 'LTE/LTE-A framework agreement since Apr 2014')],
         gov=[], gov_note="no state holder in filings (controlling holder FF6-Cell LP, private); NBIM held no Israeli telecoms at 31 Dec 2025",
         core=ND('NSN framework covers 4G/5G and associated core equipment; the SA core vendor is not named'),
         first_contract=ND(), vendor_operates=ND('Amdocs runs IT/billing operations (since 2010), not the network')),
    dict(region='Middle East', country='Israel', operator_name='Partner',
         share=V(23.0, IL_SHARE, CO, IL_SHARE_NOTE, 2025),
         launch=V(2020, 'https://www.itu.int/en/ITU-D/Regional-Presence/Europe/Documents/Events/2020/5G_EUR_CIS/5G_Israel-final.pdf', REG, 'Sep 2020'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.inss.org.il/wp-content/uploads/2020/11/no.-1403.pdf', NEWS, PHI_DISPUTE)],
         ran4=[R('Ericsson', 'all', 'https://www.partner.co.il/contentassets/db3c9f1868834974925401ebe917bccb/pdfs/20f_2018_isa.pdf', CO, 'sole radio and core equipment supplier (2018 20-F); 4G deployed with Ericsson from 2010')],
         gov=[], gov_note='controlling holder Amphissa (Phoenix-linked, private); no state holder; NBIM none at 31 Dec 2025',
         core=V('Ericsson', 'https://www.partner.co.il/contentassets/db3c9f1868834974925401ebe917bccb/pdfs/20f_2018_isa.pdf', CO,
                'PROVISIONAL: Ericsson was sole core supplier (2018 20-F); only secondary sources say the 5G SA core is Ericsson-built (announced early 2023, migration done Jul 2025)'),
         first_contract=ND(), vendor_operates=ND('PHI Networks (Partner/HOT JV) runs the shared RAN; no vendor-managed operations')),
    dict(region='Middle East', country='Israel', operator_name='Pelephone',
         share=V(23.0, IL_SHARE, CO, IL_SHARE_NOTE, 2025),
         launch=V(2020, 'https://www.datacenterdynamics.com/en/news/israel-awards-5g-contracts-pelephone-hot-mobile-and-partner-comms/', NEWS, 'launched commercially by 1 Oct 2020'),
         ran5=[R('Ericsson', 'all', 'https://ir.bezeq.co.il/static-files/770b7f6a-96d1-4b0d-92c2-e4cb0a15bc9e', CO, "Bezeq annual report: Ericsson supplied Pelephone's UMTS, LTE and 5G infrastructure")],
         ran4=[R('Ericsson', 'all', 'https://en.globes.co.il/en/article-pelephone-picks-ericsson-as-sole-4g-vendor-1000972189', NEWS, 'sole 4G vendor (2014); Bezeq annual report confirms')],
         gov=[], gov_note='100% owned by Bezeq (no controlling shareholder); no state holder found; NBIM held no Bezeq at 31 Dec 2025',
         core=V('Ericsson', 'https://ir.bezeq.co.il/news-releases/news-release-details/pelephone-expects-reach-100-thousand-5g-max-customers-and-will/', CO, 'independent SA core built with Ericsson (NIS 50m); 5G MAX launched Sep 2024'),
         first_contract=ND('Siklu mmWave backhaul deal dated 3 Sep 2020, but Ericsson 5G sites existed by Aug 2020; Ericsson contract date not found'),
         vendor_operates=ND()),
    dict(region='Middle East', country='Israel', operator_name='HOT',
         share=V(14.0, IL_SHARE, CO, IL_SHARE_NOTE + "; Keystone's Jul 2026 presentation says 15%", 2025),
         launch=V(2020, 'https://www.datacenterdynamics.com/en/news/israel-awards-5g-contracts-pelephone-hot-mobile-and-partner-comms/', NEWS, 'launched commercially by 1 Oct 2020'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.inss.org.il/wp-content/uploads/2020/11/no.-1403.pdf', NEWS, PHI_DISPUTE)],
         ran4=[], ran4_note='shared PHI network with Partner; 4G vendor not found',
         gov=[], gov_note='controlled by Altice/Drahi (private); no state holder found',
         core=ND('INSS names Ericsson as the Partner-HOT 5G equipment vendor without saying whether that covers the core'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Luxembourg
    dict(region='Western Europe', country='Luxembourg', operator_name='Post',
         share=V(50.3, LU_ILR, REG, 'ILR 2025 report, subscribers excl. M2M', 2025),
         launch=V(2020, 'https://www.ericsson.com/en/press-releases/2020/10/post-luxembourg-chooses-ericsson-as-5g-core-and-ran-vendor', CO, 'Ericsson-powered 5G live 16 Oct 2020'),
         ran5=[R('Ericsson', 'all', 'https://www.post.lu/en/particuliers/support/telephonie-mobile/5g/strategie-5g-de-post/quel-est-votre-fournisseur-pour-le-reseau-5g-de-post', CO, "POST: 5G 'deployed on the Ericsson network infrastructure'")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2020/10/post-luxembourg-chooses-ericsson-as-5g-core-and-ran-vendor', CO, '2020 deal includes modernising the existing 2G/3G/4G network; Ericsson described as legacy provider')],
         gov=[G('Luxembourg', 'State of Luxembourg', 100.0, 'POST Luxembourg', 'direct', '2025-12-31', 'https://www.postgroup.lu/documents/1846390/5402177/RA_2025_EN.pdf', CO, 'sole shareholder since 1992 (Annual Report 2025, published 12 May 2026)')],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/2020/10/post-luxembourg-chooses-ericsson-as-5g-core-and-ran-vendor', CO, 'cloud-native dual-mode 5G Core'),
         first_contract=V('2020-10-26', 'https://www.ericsson.com/en/press-releases/2020/10/post-luxembourg-chooses-ericsson-as-5g-core-and-ran-vendor', CO, 'announcement date of the multi-year 5G Core+RAN contract (after the 16 Oct launch); signing date not disclosed'),
         vendor_operates=ND('Ericsson provides rollout and support services; no managed operations stated')),
    dict(region='Western Europe', country='Luxembourg', operator_name='Tango',
         share=V(32.9, LU_ILR, REG, 'ILR 2025 report (Proximus Luxembourg)', 2025),
         launch=V(2020, 'https://www.proximusnxt.lu/en/5g-beyond-borders', CO, '23 Oct 2020'),
         ran5=[R('Nokia', 'all', 'https://www.proximusnxt.lu/en/partnerships-finnish-company-nokia-and-swedish-company-ericsson', CO, "Nokia selected for 5G RAN and to replace the incumbent radio vendor (7-year deal, 15 Dec 2020)")],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.proximusnxt.lu/en/tango-and-proximus-nxt-partner', CO, 'progressive modernisation of 2G/3G/4G by 2023'),
               R('Huawei', 'not_disclosed', 'https://www.lightreading.com/5g/proximus-dumps-huawei-in-luxembourg-too', NEWS, '100% of 4G RAN as of Dec 2020 (Strand Consult); replacement by Nokia under way, completion not confirmed')],
         gov=[G('Belgium', 'Belgian State (via SFPIM)', 53.51, 'Proximus PLC', 'via_parent', '2025-12-31', PROXIMUS_AR, CO,
                "from the core-panel cache (Proximus 2025 integrated annual report); Proximus's percentage in Proximus Luxembourg not stated"),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 1.22, 'Proximus PLC', 'via_parent', '2025-12-31', NBIM, CO)],
         core=V('Ericsson', 'https://www.proximusnxt.lu/en/partnerships-finnish-company-nokia-and-swedish-company-ericsson', CO, 'dual-mode 5G core (Dec 2020)'),
         first_contract=ND('Nokia/Ericsson deals announced 15 Dec 2020, after the Oct 2020 launch, so they were not the first 5G vendor arrangement'),
         vendor_operates=ND()),
    dict(region='Western Europe', country='Luxembourg', operator_name='Orange',
         share=V(15.8, LU_ILR, REG, "ILR 2025 report chart (Orange's 2024 URD cites 15.3% for Jun 2024)", 2025),
         launch=V(2020, 'https://www.orange.lu/en/news/orange-luxembourg-launches-its-5g-network-and-deploys-a-support-programme-for-its-customers/', CO, '23 Nov 2020'),
         ran5=[R('Nokia', 'all', 'https://www.orange.lu/en/news/orange-luxembourg-chooses-european-equipment-manufacturer-nokia-to-deploy-its-5g-network/', CO, "Nokia the 'only radio supplier' (9 Oct 2020)")],
         ran4=[R('Huawei', 'not_disclosed', 'https://www.lightreading.com/5g/proximus-dumps-huawei-in-luxembourg-too', NEWS, "'fully reliant' on Huawei for 4G RAN as of Dec 2020 (Strand Consult); Orange said the 5G rollout renews all 4G equipment, vendor not named")],
         gov=[G('France', 'French State', 13.39, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX, CO, '21.04% of voting rights; chain Orange S.A. -> Orange Belgium -> Orange Luxembourg'),
              G('France', 'Bpifrance Participations', 9.56, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX, CO, '8.00% of voting rights'),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 1.76, 'Orange S.A.', 'via_parent', '2025-12-31', NBIM, CO, 'voting 0.00%'),
              G('Norway', 'Norges Bank Investment Management (GPFG)', 1.28, 'Orange Belgium SA (direct parent)', 'via_parent', '2025-12-31', NBIM, CO)],
         core=V('Ericsson', 'https://www.orange.com/en/press-release/orange-selects-suppliers-for-its-5g-stand-alone-5g-sa-networks-in-europe-234893', CO, '5G SA core for Luxembourg (21 Feb 2022)'),
         first_contract=V('2020-10-09', 'https://www.orange.lu/en/news/orange-luxembourg-chooses-european-equipment-manufacturer-nokia-to-deploy-its-5g-network/', CO, 'Nokia selected after a 2019 tender (announcement date)'),
         vendor_operates=ND('Nokia agreement includes deployment and maintenance, not network operation')),
    # ------------------------------------------------------------------ Vietnam
    dict(region='Asia-Pacific', country='Vietnam', operator_name='Viettel',
         share=V(40.0, 'https://www.gsma.com/connectivity-for-good/spectrum/wp-content/uploads/2024/11/GSMA_Accelerating-5G-in-Vietnam-2024.pdf', NEWS,
                 'GSMA report (Nov 2024): ~40% of mobile connections; VinaPhone 30, MobiFone 16, Vietnamobile 12, Gmobile 2', 2024),
         launch=V(2024, 'https://english.mst.gov.vn/viettel-launches-vietnams-first-5g-network-197241016083258314.htm', REG, '15 Oct 2024'),
         ran5=[R('Ericsson', 'most', 'https://www.ericsson.com/en/press-releases/2024/9/viettel-vietnam-extends-ericsson-partnership-through-major-5g-network-award', CO, "awarded 30 Sep 2024; 'majority of provinces' incl. Hanoi, northern and central Vietnam"),
               R('Nokia', 'some', 'https://www.nokia.com/asset/i/215526/', CO, '22 provinces, ~2,500 sites (2024)'),
               R('Viettel High Tech (in-house)', 'small', 'https://www.vietnam.vn/en/2-800-tram-goc-5g-do-viettel-phat-trien-duoc-dua-vao-mang-luoi', NEWS,
                 '2,800 own-made gNodeBs (Oct 2026), compared with >20,000 new 5G sites by end-2025 (Developing Telecoms)')],
         ran5_note="excluded: Qualcomm (chipsets/L1 software inside Viettel's own radios); a Huawei-led group's US$23m '5G equipment' contract and ZTE antenna contracts with unclear year and scope",
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2024/9/viettel-vietnam-extends-ericsson-partnership-through-major-5g-network-award', CO, '4G modernisation in the same areas as its 5G award')],
         gov=[G('Vietnam', 'State of Vietnam (owner rights exercised by the Ministry of National Defence)', 100.0, 'Viettel Group', 'direct', '2018-01-11',
                'https://vpcp.chinhphu.vn/chi-dao-dieu-hanh-cua-chinh-phu-thu-tuong-chinh-phu-ngay-11-1-2018-11519405.htm', REG, 'Decree 05/2018/ND-CP: state holds 100% of charter capital')],
         core=V('Viettel High Tech (in-house)', 'https://viettel.com.vn/en/news-events/news/viettel-telecommunications-equipment-on-gartners-prestigious-list/', CO, 'own cloud-native 4G EPC/5G core in network since 2022'),
         first_contract=ND('first 5G call with Ericsson in May 2019; contract date not found'),
         vendor_operates=ND('vertically integrated: its own subsidiary Viettel High Tech makes the core and some gNodeBs; no external vendor runs the network')),
    # ------------------------------------------------------------------ Tajikistan
    dict(region='Central Asia & Eastern Europe', country='Tajikistan', operator_name='Tcell',
         share=V(33.9, TJ_SHARE, NEWS, TJ_NOTE, 2024),
         launch=V(2020, 'https://www.telecompaper.com/news/tcell-launches-5g-network--1349663', NEWS, 'Dushanbe, Aug 2020'),
         ran5=[], ran5_note='5G RAN vendor not named', ran4=[], ran4_note='only GSM-era Huawei (2002) found',
         gov=[], gov_note='100% owned by AKFED (Aga Khan Fund for Economic Development) via CATD BV since 2017; AKFED is not a government',
         core=ND(), first_contract=ND(),
         vendor_operates=ND('a personal LinkedIn profile claims Huawei managed services in 2012-2014 (not cited)')),
    dict(region='Central Asia & Eastern Europe', country='Tajikistan', operator_name='MegaFon',
         share=V(22.9, TJ_SHARE, NEWS, TJ_NOTE, 2024),
         launch=V(2020, 'https://megafon.tj/about', CO, 'central Dushanbe from 21 Feb 2020'),
         ran5=[], ran5_note='vendor not named', ran4=[], ran4_note='vendor not named',
         gov=[G('Tajikistan', 'OJSC Tojiktelecom (state-owned national operator)', 25.0, 'TT Mobile (MegaFon Tajikistan)', 'direct', '2021-10-26',
                'https://asiaplus.news/en/2021/10/26/tajikistan-has-expensive-and-slow-internet-connection/', NEWS, 'MegaFon PJSC holds the other 75%')],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Trinidad and Tobago
    dict(region='Latin America & Caribbean', country='Trinidad and Tobago', operator_name='bmobile',
         share=ND("TATT: the two MNOs' shares were 'approximately comparable' at end-2023; figures redacted"),
         launch=V(2019, 'https://trinidadexpress.com/features/local/5g-is-here/article_96af41c0-1ade-11ea-a888-4b2424e4ff02.html', NEWS, '4 Dec 2019'),
         ran5=[R('Huawei', 'not_disclosed', 'https://technewstt.com/bd1227/', NEWS, 'Huawei technology partner, Massive MIMO for 5G (Dec 2019)')],
         ran4=[R('Huawei', 'not_disclosed', 'https://technewstt.com/bd1227/', NEWS, 'TDD 4G LTE equipment (Dec 2019)')],
         gov=[G('Trinidad and Tobago', 'National Enterprises Limited (state holding company)', 51.0, 'TSTT', 'direct', '2026', 'https://www.tstt.co.tt/company-overview', CO, 'Cable & Wireless (Liberty Latin America) holds the other 49%'),
              G('Trinidad and Tobago', 'Corporation Sole (Minister of Finance)', 51.0, 'National Enterprises Limited', 'via_parent', '2023-09-30',
                'https://papers.ttparliament.org/document-category/administrative-reports/', REG, 'NEL annual administrative report FY2023, laid 13 Jan 2025')],
         core=ND('5G launched in partnership with Huawei; core scope not stated'),
         first_contract=V('2019-12', 'https://oxfordbusinessgroup.com/reports/trinidad-tobago/2020-report/economy/bright-prospects-investors-take-steps-to-position-the-country-as-a-regional-centre-for-business-process-outsourcing', NEWS, 'TSTT announced a Huawei 5G deal in Dec 2019'),
         vendor_operates=V(False, 'https://bmobile.co.tt/covid-response/our-network/', CO, "TSTT's own team monitors, optimises and protects the network")),
]
