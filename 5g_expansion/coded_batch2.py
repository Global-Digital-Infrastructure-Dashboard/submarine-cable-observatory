"""Researcher coding of expansion batch 2 (Turkey, Malta, Somalia, Jamaica, Jordan; 11 operators), coded in-session on
2026-11-23 from the cached v2 searches in data/5g_expansion_searches.jsonl under Prof. Shen's revised schema
(schema.py). Values come only from the cited source; anything a source didn't state is not_disclosed.
Share-category vendor claims were checked against the primary page at coding time (rule 11); the log is
5g_expansion/verify_2026-11-23_batch2.csv. No computed figures in this batch.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-23'

register(
    domains={
        'company': ['turkcell.com.tr', 'ttinvestorrelations.com', 'ttyatirimciiliskileri.com.tr', 'businesswire.com', 'huawei.com',
                    'i2i-systems.com', 'epic.com.mt', 'go.com.mt', 'melita.com', 'prnewswire.co.uk', 'cwc.com', 'orange.jo',
                    'telesom.com', 'somtelnetwork.net', 'hormuud.com', 'sec.gov', 'nec.com'],
        'government': ['digital-strategy.ec.europa.eu', 'btk.gov.tr', 'mca.org.mt', 'nca.gov.so', 'sdc.com.jo', 'trc.gov.jo'],
        'news': ['totaltele.com', 'computerweekly.com', 'devdiscourse.com', 'telecomlead.com', 'timesofmalta.com', 'pipelinepub.com',
                 'connectingafrica.com', 'sdxcentral.com', 'zawya.com', 'jamaicaobserver.com'],
        'other': ['somalilandbiz.com', 'rizzofarrugia.com'],
    },
    overrides={
        # Nokia's own presentation, hosted by ITU
        'https://www.itu.int/en/ITU-T/Workshops-and-Seminars/qos/201809/Documents/M_%20C_Presentation.pdf': 'company',
        # GO plc's annual report, hosted by a stockbroker
        'https://rizzofarrugia.com/wp-content/uploads/GO-2025-Annual-Report.pdf': 'company',
    },
    vendors=['ULAK', 'Juniper'],
)

TR_LAUNCH = 'https://digital-strategy.ec.europa.eu/en/miscellaneous/turkiye-three-mobile-operators-launch-nationwide-5g-services'
TR_LAUNCH_NOTE = 'all three operators launched nationwide 5G on 1 Apr 2026 after the 2025 spectrum auction (European Commission)'
TURKCELL_20F = 'https://www.sec.gov/Archives/edgar/data/1071321/000110465924060657/tkc-20231231x20f.htm'
TT_AR25 = 'https://www.ttinvestorrelations.com/media/dqsjlvxo/2025-annual-report.pdf'
VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
E_AND_SEC = 'https://www.sec.gov/Archives/edgar/data/839923/000120864626000022/0001208646-26-000022.txt'
MT_OIR = 'https://www.mca.org.mt/sites/default/files/pageattachments/MCA%20OIR%20Report%20-%20Final_2025.pdf'
MT_OIR_NOTE = ("MCA net-neutrality (OIR) report, published 1 Sep 2025: 769,805 mobile telephony subscriptions at end-Mar 2025, "
               "Epic 42.2 / GO 35.4 / Melita 22.4 (MCA Annual Report 2024 gives end-2024 Epic 42.4 / GO 35.0 / Melita 22.6)")
MT_MERGER = "Melita's announced acquisition of Epic (Sep 2026) is not shown as completed"
ORANGE_XLSX = 'https://assets.orange.com/pm_12751_545_545865-jr7yvi3osw.xlsx'
GO_AR25 = 'https://rizzofarrugia.com/wp-content/uploads/GO-2025-Annual-Report.pdf'
JO_AR25 = 'https://orange.jo/sites/default/files/documents/99730-Annual%20Report%202025%20EN.pdf'
SOMALILAND = 'operates in Somaliland (self-declared, internationally recognised as part of Somalia); listed under Somalia in the Wikipedia 5G list'

CHECKED_NOT_ADDED = {}

OPERATORS = [
    # ------------------------------------------------------------------ Turkey
    dict(region='Middle East', country='Turkey', operator_name='Turkcell',
         share=ND('BTK publishes national totals only (e.g. 90.8m mobile subscriptions); no operator shares found'),
         launch=V(2026, TR_LAUNCH, TR_LAUNCH_NOTE),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/5/2026/turkcell-selects-ericsson-to-accelerate-5g-advanced-innovation',
                 "4 Mar 2026: signed agreement for a 5G RAN rollout; no share wording")],
         ran5_note=("not coded: Huawei, Nokia, Samsung, ZTE, ULAK and Aselsan appear only as 5G trial/MoU partners in the 20-F filings; "
                    "Turkcell reports a 'significant installed base' of Chinese and Russian vendors' equipment without naming shares"),
         ran4=[], ran4_note='no 4G RAN vendor named in the filings searched',
         gov=[G('Turkey', 'TVF Bilgi Teknolojileri İletişim Hizmetleri (TVF BTIH)', 'state_holding_company', 26.2, 'Turkcell', 'direct', '2025-12-31',
                'https://www.turkcell.com.tr/en-en/about-us/investor-relations/corporate-governance/shareholder-structure/detail',
                'wholly owned by the Türkiye Wealth Fund; as sole holder of the relevant share class it appoints 5 of 9 directors incl. the chair',
                link_url=TURKCELL_20F, board_seat='yes'),
              G('Turkey', 'Türkiye Wealth Fund (TVF)', 'sovereign_wealth_fund', 100.0, 'TVF BTIH', 'via_parent', '2025-12-31', TURKCELL_20F,
                "Turkcell's filing calls TWF 'the wealth fund of the Republic of Türkiye' and its ultimate parent",
                parent_pct=26.2, board_seat='yes')],
         gov_note='IMTIS Holdings 19.8% is not identified as a state entity; 54.0% free float',
         gov_dropped=[],
         core=ND("Huawei 5G-oriented all-cloud core (Feb 2019) and Affirmed vEPC (2018) are both documented, a multi-vendor EPC; "
                 "the core used for the 2026 5G launch is not named"),
         first_contract=V('2018-09-10', 'https://totaltele.com/nokia-and-turkcell-sign-agreement-to-boost-connectivity-in-turkey/',
                          'Nokia agreement covering 5G and IoT rollout; the Ericsson 5G cooperation MoU followed on 15 Oct 2019'),
         vendor_operates=V(True, 'https://www.ericsson.com/en/press-releases/2016/11/turkcell-selects-ericsson-as-long-term-managed-services-partner',
                           'Ericsson long-term managed-services partner from Nov 2016, managing and operating the mobile and fixed network '
                           '(2G-4G; exclusive in the Marmara region incl. Istanbul); end date and 5G scope not stated')),
    dict(region='Middle East', country='Turkey', operator_name='Türk Telekom',
         share=ND("Türk Telekom reports 31.5m mobile subscribers at 31 Dec 2025 and says it became second-largest by subscribers "
                  "(Q3 2025 market data); no percentage, and BTK publishes no operator table"),
         launch=V(2026, TR_LAUNCH, TR_LAUNCH_NOTE),
         ran5=[], ran5_note='Huawei and Nokia appear only as strengthened partnerships in the 2024 annual report, with no 5G RAN scope',
         ran4=[R('ULAK', 'not_disclosed', 'https://www.ttinvestorrelations.com/media/ov4nhva0/2024-integrated-annual-report.pdf',
                 "domestic vendor: '830 base stations are operating entirely with locally produced ULAK LTE stations' and the whole "
                 "infrastructure in six provinces is ULAK (2024 report); the total LTE base-station count is not given")],
         ran4_note='other 4G vendors not named',
         gov=[G('Turkey', 'Türkiye Wealth Fund (TWF)', 'sovereign_wealth_fund', 61.68, 'Türk Telekom', 'direct', '2025-12-31', TT_AR25,
                '60% (55% Group A + 5% Group B) plus 1.68% bought in the free float; Group A nominates five directors',
                link_url=TURKCELL_20F, board_seat='yes'),
              G('Turkey', 'Ministry of Treasury and Finance (Turkish Treasury)', 'government_ministry', 25.0, 'Türk Telekom', 'direct', '2025-12-31', TT_AR25,
                'plus one Class C golden share; nominates two independent directors while holding 15-30%', board_seat='yes')],
         gov_dropped=[],
         core=ND('no 5G core vendor named; Ericsson is the IT provisioning partner (2021)'),
         first_contract=V('2021-01-13', 'https://www.businesswire.com/news/home/20210113005224/en/Juniper-Networks-and-Trk-Telekom-Create-Joint-Innovation-Path-for-Accelerated-Open-RAN-Development-and-Deployment',
                          'Juniper partnership covering Open RAN and 5G, with committed purchases for Open RAN and 5G deployment'),
         vendor_operates=V(True, 'https://www.itu.int/en/ITU-T/Workshops-and-Seminars/qos/201809/Documents/M_%20C_Presentation.pdf',
                           'Nokia presentation (ITU workshop, Sep 2018): five-year managed-service contract for Türk Telekom with Nokia and '
                           'IRIS Turkey; contract dates not given')),
    dict(region='Middle East', country='Turkey', operator_name='Vodafone', name_note='Vodafone Türkiye (Vodafone Turkey)',
         share=V(31.0, 'https://www.computerweekly.com/news/366641384/Turkey-launches-nationwide-5G-services-with-ambitious-domestic-production-targets',
                 "'roughly 31%' and about 25m subscribers (Computer Weekly, Apr 2026); approximate, not a regulator figure", 2026),
         launch=V(2026, TR_LAUNCH, TR_LAUNCH_NOTE),
         ran5=[], ran5_note=("Vodafone Group's 2025 RAN programme names Ericsson, Huawei, Nokia and Samsung at group level and "
                             "excludes Turkey from its site count; no Türkiye-specific 5G RAN vendor"),
         ran4=[R('NEC', 'not_disclosed', 'https://uk.nec.com/en_GB/press/201702/20170222_01.html',
                 'NEC/SpiderCloud Enterprise RAN for indoor LTE in buildings and business premises (22 Feb 2017), not the macro network')],
         ran4_note='a 2019 Parallel Wireless Open RAN pilot (2G/4G) is not coded; group-level Ericsson/Huawei statements are not Türkiye-specific',
         gov=[G('United Arab Emirates', 'e& (Emirates Telecommunications Group)', 'state_owned_company', 17.005026, 'Vodafone Group Plc', 'via_parent', '2026-03-31',
                VODAFONE_AR, 'held through wholly owned Atlas 2022 Holdings; e& is 60% owned by the Emirates Investment Authority (SEC filing, Jul 2026)',
                link_url=E_AND_SEC, chain="Vodafone Group Plc -> Vodafone Türkiye; the group's percentage is not stated in the sources")],
         gov_dropped=['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)'],
         core=ND('i2i Systems 5G core was tested for six months (reported 14 Nov 2024); production core vendor not named'),
         first_contract=ND('the i2i Systems collaboration (reported Nov 2024) gives no agreement date'),
         vendor_operates=ND('Ericsson Security Manager (Oct 2022) is a security product, not managed operations')),
    # ------------------------------------------------------------------ Malta
    dict(region='Western Europe', country='Malta', operator_name='Epic',
         share=V(42.2, MT_OIR, MT_OIR_NOTE, 2025),
         launch=V(2021, 'https://www.epic.com.mt/network/5g/', 'first commercial 5G in Sliema on 26 Nov 2021, then island-wide'),
         ran5=[R('Ericsson', 'all', 'https://www.devdiscourse.com/article/technology/1526233-epic-taps-ericsson-as-its-exclusive-5g-ran-provider-in-malta',
                 "'exclusive 5G radio access network (RAN) provider' (Apr 2021; verified 2026-11-23). Ericsson's 2025 'sole 5G RAN vendor' page returned 403")],
         ran4=[], ran4_note='4G RAN vendor not named',
         gov=[], gov_note=("Monaco Telecom's own page (checked 2026-11-23, https://monaco-telecom.mc/en/monaco-entreprise/) says it is "
                           "'co-owned by the Monegasque Government and NJJ Holding' and is 'the majority shareholder in Epic', but gives "
                           "no percentages. The 49.8% for the Government of Monaco (via Société Nationale de Financement) appears only "
                           "on Wikipedia, which is not cited, so no stake is coded (exp|supp|monaco-telecom-owners). " + MT_MERGER),
         gov_dropped=[],
         core=ND(), first_contract=V('2021-04-07', 'https://telecomlead.com/telecom-equipment/epic-selects-ericsson-for-supplying-5g-ran-99521',
                                     'Ericsson selected for 5G RAN and network modernisation'),
         vendor_operates=ND()),
    dict(region='Western Europe', country='Malta', operator_name='GO',
         share=V(35.4, MT_OIR, MT_OIR_NOTE, 2025),
         launch=ND('first 5G mobile sites set up in Dec 2021 (GO annual report 2021); commercial launch date not stated'),
         ran5=[R('Nokia', 'all', 'https://www.nokia.com/newsroom/nokia-selected-by-go-malta-for-nationwide-5g-deployment-in-seven-year-deal/',
                 "'sole strategic partner for a nationwide 5G RAN rollout'; AirScale 'will cover GO's network nationwide' (19 Jan 2022; verified 2026-11-23)")],
         ran4=[], ran4_note="Nokia calls itself the 'incumbent vendor', and the core search says GO's partner since 3G (2007), but no source names the 4G RAN vendor",
         gov=[G('Tunisia', 'Tunisie Telecom (through its wholly owned TT ML Limited)', 'state_owned_company', 65.42, 'GO p.l.c.', 'direct', '2025-12-31', GO_AR25,
                'TT ML Limited is the registered holder and is wholly owned by Tunisie Telecom'),
              G('Tunisia', 'Tunisian Government', 'government_ministry', 65.0, 'Tunisie Telecom', 'via_parent', '2025-12-31', GO_AR25,
                "GO's report: 'the Tunisian Government holds a 65% shareholding in Tunisie Telecom'",
                chain='Tunisie Telecom -> TT ML Limited (100%) -> 65.42% of GO')],
         gov_note=("Emirates International Telecommunications (a Dubai Holding subsidiary) owns the other 35% of Tunisie Telecom; the source "
                   "does not call it state-owned and it is not on data/state_holders.csv, so it is not coded"),
         gov_dropped=[],
         core=ND('5G core vendor not named'),
         first_contract=V('2021-12-15', 'https://www.go.com.mt/news/go-customers-to-enjoy-free-upgrade-to-5g-mobile-services/',
                          'GO announced the Nokia 5G network agreement (about EUR 16m); Nokia announced it as a seven-year deal on 19 Jan 2022'),
         vendor_operates=ND()),
    dict(region='Western Europe', country='Malta', operator_name='Melita',
         share=V(22.4, MT_OIR, MT_OIR_NOTE, 2025),
         launch=V(2021, 'https://www.melita.com/melita-launches-5g-with-endless-mobile-data-plans/', 'nationwide 5G launched 19 May 2021'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.samenacouncil.org/samena_daily_news?news=84546',
                 "May 2021 launch on 'the 5G Ericsson network' after a multi-million-euro Ericsson investment; no share wording")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.prnewswire.co.uk/news-releases/melita-chooses-ericsson-as-strategic-5g-partner-678011573.html',
                 'Mar 2018: Ericsson Radio System (multi-standard) to modernise and expand the mobile network; 4G portion not separated')],
         gov=[], gov_note='owned by Infrastructure at Goldman Sachs Alternatives (acquisition completed Jul 2025); no state holder. ' + MT_MERGER,
         gov_dropped=[],
         core=V('Ericsson', 'https://www.pipelinepub.com/news/Melita-picks-Ericsson-to-prepare-for-5G',
                'Ericsson to modernise and expand the virtual EPC as part of 5G preparation (27 Mar 2018), i.e. the NSA EPC; no SA core vendor named'),
         first_contract=V('2018-03-27', 'https://www.prnewswire.co.uk/news-releases/melita-chooses-ericsson-as-strategic-5g-partner-678011573.html',
                          'Ericsson chosen as strategic 5G partner (ERS and vEPC)'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Somalia
    dict(region='Africa', country='Somalia', operator_name='Hormuud Telecom',
         share=ND("Omdia (via Connecting Africa) puts Hormuud at 'over 39%' of the mobile market in Q3 2023, a lower bound only; the NCA publishes no operator shares"),
         launch=V(2024, 'https://nca.gov.so/hormuud-telecom-among-operators-spearheading-5g-revolution-in-somalia/', 'service from 21 Mar 2024; NCA report 23 Mar 2024'),
         ran5=[], ran5_note='no 5G RAN vendor named; Nokia and Samsung appear only as MWC 2023 discussions',
         ran4=[], ran4_note='no 4G RAN vendor named',
         gov=[], gov_note='privately owned by Somali shareholders (12,000+); no state holder found', gov_dropped=[],
         core=ND(), first_contract=ND("an HTG Solutions project listing ('Hormuud 5G Wireless Phase 1', Jan 2019) is not a vendor contract"),
         vendor_operates=ND('HTG Solutions describes technical support/managed services for Hormuud but is not shown to be an equipment vendor')),
    dict(region='Africa', country='Somalia', operator_name='Telesom', name_note=SOMALILAND,
         share=ND('no operator shares published by the NCA; the World Bank estimates Hormuud, Telesom and Golis together serve over 80%'),
         launch=V(2024, 'https://www.samenacouncil.org/samena_daily_news?news=98898', "commercial 5G (mobile and FWA) from 1 Jan 2024 per Telesom's announcement"),
         ran5=[], ran5_note='no 5G RAN vendor named', ran4=[], ran4_note='no 4G RAN vendor named',
         gov=[], gov_note='privately held (1,400+ shareholders; 49% retained by its founder per an academic source); no state holder found',
         gov_dropped=[], core=ND(), first_contract=ND(), vendor_operates=ND()),
    dict(region='Africa', country='Somalia', operator_name='Somtel',
         share=ND('no operator shares published by the NCA'),
         launch=V(2024, 'https://www.datacenterdynamics.com/en/news/somtel-launches-first-5g-network-in-somalia/', 'launched in the first week of Jan 2024 (DCD, 4 Jan 2024)'),
         ran5=[], ran5_note='no 5G RAN vendor named; a 2026 blog claim of Huawei equipment is not a citable source',
         ran4=[R('Nokia', 'not_disclosed', 'https://www.somalilandbiz.com/sector-guides/telecoms-2/',
                 "supplier named as Alcatel-Lucent (now part of Nokia): 'In 2014, Somtel contracted equipment vendor Alcatel-Lucent to deploy a 4G LTE network across Somaliland'")],
         gov=[], gov_note='owned by Dahabshiil Group (about 95%; the rest public shares); no state holder found', gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Jamaica
    dict(region='Latin America & Caribbean', country='Jamaica', operator_name='FLOW',
         name_note='Cable & Wireless Jamaica Limited (Liberty Latin America)',
         share=ND("the OUR's Q4 2025 report gives only total mobile subscriptions (3,310,790); Digicel is described as the market leader"),
         launch=V(2026, 'https://www.cwc.com/stories/flow-officially-introduces-5g-in-jamaica.html', "Jamaica's first commercial 5G, 11 Jun 2026"),
         ran5=[], ran5_note="no 5G RAN vendor named; Liberty Latin America's Ericsson deals cited are for Costa Rica and Puerto Rico",
         ran4=[], ran4_note='Huawei LTE overlay work (2018) appears only in a personal LinkedIn profile (not cited)',
         gov=[], gov_note=("Liberty Latin America (listed) owns Cable & Wireless Communications, which owns a majority of Cable & Wireless "
                           "Jamaica (92.3% in 2019; current % not stated); no state holder found"),
         gov_dropped=[], core=ND('Ericsson appears only in a 2017 5G prototype test'), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Jordan
    dict(region='Middle East', country='Jordan', operator_name='Orange', name_note='Orange Jordan (Jordan Telecommunications Company)',
         share=ND("Orange Jordan's 2025 annual report gives only a 30-35% range for its domestic mobile share; TRC's published operator shares are redacted"),
         launch=V(2023, 'https://www.orange.com/en/press-release/orange-jordan-officially-launches-5g-orange-5g-services-now-in-amman-and-irbid-with-continuous-expansion-233750',
                  'commercial launch 11 Jul 2023 in Amman and Irbid (pilot Nov 2022)'),
         ran5=[R('Nokia', 'all', 'https://www.nokia.com/newsroom/nokia-wins-nationwide-5g-ran-deal-with-orange-jordan/',
                 "supplies 5G RAN 'throughout the Kingdom of Jordan' and 'will replace Orange Jordan's entire existing RAN network' (4 May 2023; verified 2026-11-23)")],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-wins-nationwide-5g-ran-deal-with-orange-jordan/',
                 'Single RAN (2G-5G) replacing the entire existing RAN; completion not confirmed, so no 4G share is coded')],
         ran4_note='the replaced incumbent RAN vendor is not named, so no vendor-switch row (old vendor unknown)',
         gov=[G('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX, '21.04% of voting rights',
                chain='Orange S.A. -> Joint Investment Telecommunications Company (fully owned) -> 51.00% of Jordan Telecommunications Company'),
              G('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX,
                "8.00% of voting rights; Orange's file groups it with the French State as the public sector",
                chain='Orange S.A. -> Joint Investment Telecommunications Company (fully owned) -> 51.00% of Jordan Telecommunications Company'),
              G('Jordan', 'Government of the Hashemite Kingdom of Jordan', 'government_ministry', 0.0, 'Jordan Telecommunications Company', 'direct',
                '2026-11-19', 'https://www.sdc.com.jo/en/companyInfo?member_info=131206',
                'Securities Depository Center record: one board representative, no shareholding reported', board_seat='yes'),
              G('Jordan', 'Social Security Corporation (via its Social Security Investment Fund)', 'pension_fund', 28.88,
                'Jordan Telecommunications Company', 'direct', '2025-12-31',
                'https://orange.jo/sites/default/files/documents/Orange-Jordan-Annual-Report-2025-English.pdf',
                "Orange Jordan annual report 2025, p.13: 54,150,000 shares, 28.88% at 31 Dec 2024 and 2025; two board members "
                "represent the SSC (pp.16, 27); held via the Social Security Investment Fund (SSIF annual report 2023)", board_seat='yes')],
         gov_note=("Social Security Corporation coded under Prof. Shen's pension rule (2026-11-26): set up under the Social Security "
                   "Law to cover all laborers under the labor law (SSC website). Before that rule it was left uncoded because no "
                   "source calls it state-owned (exp|supp|jordan-ssc: a 'financially and administratively independent juridical "
                   "person'; the WTO Trade Policy Review, Aug 2023, says the government retained a 28.9% interest through the SSC)"),
         gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/5/2023/orange-jordan-selects-ericsson-to-bolster-5g-core-network-infrastructure-in-jordan',
                'cloud-native dual-mode 5G Core and 5G Charging (7 Aug 2023)'),
         first_contract=V('2023-05-04', 'https://www.nokia.com/newsroom/nokia-wins-nationwide-5g-ran-deal-with-orange-jordan/',
                          'nationwide 5G RAN deal with Nokia (Nokia release dated 4 May 2023; some reports give 5 May)'),
         vendor_operates=ND('Nokia provides design, deployment and technical support, not managed operations')),
]
