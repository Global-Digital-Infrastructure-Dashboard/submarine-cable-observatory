"""Researcher coding of expansion batch 3 (Pakistan, Latvia, Ukraine, Zimbabwe, Sri Lanka), coded in-session on
2026-11-23 from the cached v2 searches in data/5g_expansion_searches.jsonl (plus core-panel cache entries for
Telia's shareholders). Values come only from the cited source; anything a source didn't state is not_disclosed.
Schema, source types and the 5% rule: schema.py. Primary-source checks made while coding (Prof. Shen's rule 11):
5g_expansion/verify_2026-11-23_batch3.csv.

Batch notes:
- Ukraine: only 5G pilots were found (Lviv 2025, Kyiv Jul 2026), so launch is not_disclosed and pilot vendors
  are noted, not coded (as for MobiFone's Open RAN pilot in batch 1). Prof. Shen (2026-11-26): kept out of the main
  sample, rows flagged sample_status = pilot_only; no replacement country.
- Pakistan: PTA authorised phased commercial 5G for Jazz, Ufone and Zong on 19 Mar 2026; only Zong states a launch.
  PTA's annual report (operator counts) timed out on every fetch, so computed shares are not coded.
- Sri Lanka: Khazanah (36.69% of Axiata) is coded on Axiata's own wording ('the sovereign wealth fund of the
  Government of Malaysia'), the same basis as batch 4's XLSmart row; EPF and PNB are not, because Axiata's report
  does not describe them as state entities and they are not on data/state_holders.csv.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-23'

register(
    domains={
        'company': ['jazz.com.pk', 'veon.com', 'zong.com.pk', 'ufone.com', 'lmt.lv', 'tele2.com', 'econet.co.zw',
                    'ewzinvestor.com', 'dialog.lk', 'axiata.com', 'lifecell.ua', 'vodafone.ua', 'teliacompany.com',
                    'bitegroup.net'],
        'government': ['pta.gov.pk', 'potraz.gov.zw', 'trc.gov.lk', 'digital-strategy.ec.europa.eu', 'nkrzi.gov.ua',
                       'moitt.gov.pk', 'investinlatvia.org'],
        'research_industry_group': ['vis.com.pk', 'mtn-c.com', 'cepa.org', '5g-routes.eu'],
        'news': ['dawn.com', 'tribune.com.pk', 'techjuice.pk', 'pakistangulfeconomist.com', 'eng.lsm.lv', 'bnn-news.com',
                 'teleinfotoday.com', 'dev.ua', 'techtimes.com', 'itnewsafrica.com', 'themorning.lk', 'ft.lk',
                 'odessa-journal.com', 'open4business.com.ua', 'mobileeurope.co.uk', 'baltic-course.com',
                 'profit.pakistantoday.com.pk'],
        'other': ['sorainen.com'],
    },
    overrides={
        # company documents hosted elsewhere
        'https://doc.irasia.com/listco/hk/chinamobile/interim/2025/intrep.pdf': 'company',
        'https://doc.irasia.com/listco/hk/chinamobile/annual/2023/ar2023.pdf': 'company',
        'https://s3.ap-southeast-1.amazonaws.com/dlg.dialog.lk/s3fs-public/2026-05/Dialog-Integrated-Annual-Report-2025.pdf': 'company',
        'https://stocks.observer-reporter.com/observerreporter/article/gnwcq-2024-8-28-bite-group-selects-nokias-packet-core-to-drive-5g-evolution-and-to-simplify-and-enhance-network-capacity': 'company',
    },
)

E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
PTA_5G = ('https://pta.gov.pk/category/pta-granted-ngms-5g-licenses-to-cmos:-cmos-will-commence-phase-wise-5g-commercial-'
          'services-across-pakistan-40050183-2026-03-22')
PK_SHARE_NOTE = ("PTA Annual Report 2023 counts at Jun 2023 (via searches incl. exp|supp|pta-shares): Jazz 71,334,141; Telenor "
                 "46,921,677; Zong 46,512,493; Ufone 24,503,956; SCO 1,676,367; total 190,948,634. PTA's 2024-25 report and indicators "
                 "pages give no operator counts. The searches also report conflicting rounded shares from the same report (Zong 29% vs "
                 "~24% from the counts; Ufone 11% vs 12.7%). UNVERIFIED: the PTA PDF timed out on every fetch (last tried 2026-11-23), "
                 "so no share is computed. Telenor Pakistan's later combination with PTCL/Ufone is not covered by these figures")
PK_LAUNCH_NOTE = 'PTA authorised Jazz, Ufone and Zong on 19 Mar 2026 to begin phase-wise commercial 5G'
LV_SHARE = 'https://eng.lsm.lv/article/economy/economy/09.05.2023-latvians-call-and-text-less-browse-internet-more.a507915/'
LV_SHARE_NOTE = ("share of mobile INTERNET connections in 2022 (regulator SPRK data via LSM, 9 May 2023): LMT 38.31, Tele2 38.28, "
                 "Bite 23.4; verified on the LSM page. No regulator share of all mobile subscriptions found")
UA_PILOT = 'https://digital-strategy.ec.europa.eu/en/miscellaneous/ukraine-kyivstar-vodafone-ukraine-and-lifecell-launch-5g-pilot-kyiv'
UA_LAUNCH = ND("only 5G pilots found (Lviv 2025; Kyiv, Jul 2026, all three operators); no commercial launch")
# Prof. Shen (2026-11-26): pilots don't count as a launch, so Ukraine is outside the main sample. Its rows are kept,
# flagged pilot_only, so the country can be reintroduced if commercial 5G launches; no replacement country is drawn.
UA_SAMPLE = dict(sample_status='pilot_only',
                 sample_status_note=('outside the main sample (Prof. Shen, 2026-11-26): only 5G pilots, no commercial launch; '
                                     'data kept for reintroduction if commercial service launches; no replacement drawn'))
UA_SHARE = ND('the regulator (NKEK) site returned no operator-level subscription data')
LMT_OWN = 'https://eng.lsm.lv/article/economy/business/15.07.2025-latvian-state-wants-to-buy-out-telias-stakes-in-two-telecoms-companies.a606911/'
LMT_BNN = 'https://bnn-news.com/money/latvia-seeks-strategic-investors-for-tet-and-lmt-several-dozens-already-identified-s7rwe5n'
TELIA_OWN = 'https://www.teliacompany.com/en/articles/shareholdings'

DIALOG_CHAIN = ("Axiata Group Berhad -> Axiata Investments (Labuan) 73.75% of Dialog Axiata PLC (31 Dec 2025); Axiata's percentage of "
                "the Labuan entity not stated")

OPERATORS = [
    # ------------------------------------------------------------------ Pakistan
    dict(region='Asia-Pacific', country='Pakistan', operator_name='Jazz',
         name_note='JazzWorld Pakistan Limited, formerly Pakistan Mobile Communications Limited (PMCL)',
         share=ND('Jazz ~38% of mobile subscriptions in FY2022-23 per PTA AR 2023 (via search). ' + PK_SHARE_NOTE),
         launch=V(2026, 'https://profit.pakistantoday.com.pk/2026/03/20/jazz-launches-5g-services-after-securing-pta-licence-rollout-begins-in-major-cities',
                  "'Jazz launches 5G services after securing PTA licence, rollout begins in major cities' (Profit, 20 Mar 2026; verified); "
                  "Dawn dates the launch announcement 19 Mar 2026. " + PK_LAUNCH_NOTE),
         ran5=[], ran5_note='no 5G RAN vendor named, also not in the launch reports (ZTE 5G work appears only in a personal profile)',
         ran4=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/jazz-signs-five-year-4g-network-expansion-deal-with-nokia-to-boost-network-capacity-and-coverage/',
                 '5-year 4G expansion deal (11 Mar 2019): AirScale in central and southern Punjab, Sindh and Baluchistan; no network-wide share')],
         ran4_note=("a 2017 Pakistan & Gulf Economist article lists Huawei, ZTE, Nokia-Siemens and Alcatel as 'primary vendors for networking "
                    "equipment' incl. radio base stations but names no generation, so not coded as 4G. Swaps (Ericsson->ZTE, Huawei->Ericsson, "
                    "2,300 Nokia LTE sites) appear only in personal profiles and are not coded"),
         gov=[], gov_note='no state holder: IWCPL 84.71% and VEON Pakistan Holdings 15% (both VEON group, private) per the FY2025 directors report',
         gov_dropped=[],
         core=ND("Nokia supplies subscriber data management (HLR/HSS, Aug 2022), not shown to be the 5G core"),
         first_contract=ND('Ericsson microwave frame contract (Dec 2025) is transmission, not a 5G RAN/core contract'),
         vendor_operates=ND("Ericsson announced (24 Mar 2021) a 3-year renewal for nationwide multivendor performance management and "
                            "optimisation of the 2G/3G/4G network; UNVERIFIED: ericsson.com returned 403, and optimisation alone is not "
                            "shown to be network operation")),
    dict(region='Asia-Pacific', country='Pakistan', operator_name='Ufone',
         name_note='Pak Telecom Mobile Limited (PTML)',
         share=ND('Ufone 12.7% (2023) per PTA AR 2023 summary via search, but another search gives 11%. ' + PK_SHARE_NOTE),
         launch=ND(PK_LAUNCH_NOTE + "; Express Tribune (20 Mar 2026) says Ufone would launch 'in the coming days' and ProPakistani "
                   "(20 Apr 2026) that it was 'set to launch'; TechJuice (23 Oct 2026) reports 127 Ufone 5G sites in 24 cities; no "
                   "confirmed launch date (exp|supp|jazz-ufone-launch)"),
         ran5=[], ran5_note='no 5G RAN vendor named',
         ran4=[], ran4_note='Huawei, Nokia, Ericsson and ZTE appear only in personal project profiles (not cited)',
         gov=[G('Pakistan', 'Government of Pakistan', 'government_ministry', 62.18, 'Pakistan Telecommunication Company Limited (PTCL)', 'via_parent',
                '2025-04-30', 'https://docs.vis.com.pk/RatingReports/OP_0530003001_0005300.pdf',
                "VIS rating report: the Government of Pakistan is PTCL's majority shareholder; government nominees sit on the PTML board "
                "(per the rating disclosure and Dawn); Dawn (May 2024) says PTCL holds 'close to 100%' of Ufone",
                parent_pct=100.0, chain='PTCL 100% of PTML (Ufone)', board_seat='yes'),
              G('United Arab Emirates', 'e& (via Etisalat International Pakistan)', 'state_owned_company', 26.0, 'Pakistan Telecommunication Company Limited (PTCL)',
                'via_parent', '2025-04-30', 'https://docs.vis.com.pk/RatingReports/OP_0530003001_0005300.pdf',
                "e&'s 2025 integrated annual report gives the Emirates Investment Authority 60%, ultimately controlled by the UAE Federal Government",
                link_url=E_AND_AR, parent_pct=100.0, chain='Etisalat International Pakistan (e& subsidiary) 26% of PTCL -> PTCL 100% of PTML')],
         gov_dropped=[],
         core=ND(), first_contract=ND('only the PTA spectrum licence (19 Mar 2026); no vendor contract found'),
         vendor_operates=ND('Huawei managed services for Ufone appear only in a personal profile (not cited)')),
    dict(region='Asia-Pacific', country='Pakistan', operator_name='Zong',
         name_note='CMPak Limited (China Mobile Pakistan)',
         share=ND('no current PTA operator figure found. ' + PK_SHARE_NOTE),
         launch=V(2026, 'https://www.zong.com.pk/press-release/zong-5g-is-live-leading-pakistans-digital-journey-into-a-new-era-with-commercial-5g-launch',
                  "commercially launched in 16+ cities on 19 Mar 2026 (Zong release, verified); 2019 5G use was trials only"),
         ran5=[], ran5_note="no 5G RAN vendor named; a 2019 consultancy note only expected ZTE 5G equipment",
         ran4=[R('Huawei', 'not_disclosed', 'https://www.zong.com.pk/press-release/cmpak-and-huawei-conduct-pakistans-first-commercial-use-of-smart-8t8r',
                 "'Zong 4G' existing 4T4R network upgraded to Smart 8T8R with Huawei in Lahore (12 Mar 2021); verified")],
         ran4_note="MTN Consulting (2019) calls ZTE Zong's long-standing supplier without naming a generation, so not coded",
         gov=[G('China', 'China Mobile Communications Group Co., Ltd. (CMCC)', 'state_owned_company', 69.09, 'China Mobile Limited', 'via_parent', '2025-06-30',
                'https://doc.irasia.com/listco/hk/chinamobile/interim/2025/intrep.pdf',
                "ultimate controlling shareholder; China Mobile's 2023 annual report calls CMCC a central state-owned enterprise under SASAC",
                link_url='https://doc.irasia.com/listco/hk/chinamobile/annual/2023/ar2023.pdf',
                chain='CMCC -> China Mobile (Hong Kong) Group -> China Mobile Hong Kong (BVI) -> China Mobile Limited -> China Mobile International Holdings -> CMPak; intermediate percentages not stated')],
         gov_dropped=[],
         core=ND(), first_contract=ND('first 5G trial 23 Aug 2019 (MoITT); no vendor contract named'), vendor_operates=ND()),
    # ------------------------------------------------------------------ Latvia
    dict(region='Central Asia & Eastern Europe', country='Latvia', operator_name='LMT',
         name_note='Latvijas Mobilais Telefons',
         share=V(38.31, LV_SHARE, LV_SHARE_NOTE, 2022),
         launch=V(2019, 'https://www.lmt.lv/en/innovations/news/lmt-becomes-the-first-in-the-baltics-to-launch-5g-commercially',
                  'commercial 5G from 19 Jul 2019; 5G SA (5G+) from Jul 2025'),
         ran5=[], ran5_note=("no nationwide 5G RAN vendor named: Nokia supplied the 2018 live demo and a 2025 tactical-defence system; Nokia "
                             "and Ericsson built a defence testbed"),
         ran4=[R('Nokia', 'all', 'https://www.lightreading.com/2g-3g-4g/lmt-does-lte-with-nsn',
                 "supplier named as Nokia Siemens Networks: 'exclusive partner to LMT for its LTE network' (1800 MHz LTE, Sep 2011), also "
                 "supplying the EPC; verified. A 5G-ROUTES report also describes long-term Nokia use for 2G/3G/4G")],
         gov=[G('Latvia', 'VAS Latvijas Valsts radio un televīzijas centrs (LVRTC)', 'state_owned_company', 23.0, 'LMT', 'direct', '2025-07-22', LMT_BNN,
                "BNN: 28% of LMT held 'by the state through LVRTC and Possessor (5%)'; verified"),
              G('Latvia', 'SIA Publisko aktīvu pārvaldītājs Possessor', 'state_holding_company', 5.0, 'LMT', 'direct', '2025-07-22', LMT_BNN,
                'state public-asset manager; verified'),
              G('Latvia', 'SIA Publisko aktīvu pārvaldītājs Possessor', 'state_holding_company', 51.0, 'Tet', 'via_parent', '2025-07-22', LMT_BNN,
                "BNN: 'The state, through Possessor, owns 51% of Tet' (LSM 15 Jul 2025: the Latvian state owns 51% of Tet); verified",
                parent_pct=23.0, chain='Tet 23% of LMT'),
              G('Sweden', 'Swedish State', 'government_ministry', 41.1, 'Telia Company AB', 'via_parent', '2026-06-30', TELIA_OWN,
                'from the core-panel cache (Telia shareholdings, 30 Jun 2026)',
                parent_pct=49.0, chain="Telia Company -> Sonera Holding 49% of LMT (LSM 15 Jul 2025); Telia's Tilts Communications also holds 49% of Tet (23% of LMT)")],
         gov_note=("LSM (15 Jul 2025) puts the Latvian state's look-through share at 39.7%; the government's plan to buy out Telia's "
                   "stakes was not completed (LSM, 10 Jul 2026: no decision; 17 Nov 2026: bids being readied)"),
         gov_dropped=[],
         core=V('Nokia', 'https://www.nokia.com/newsroom/nokia-5g-standalone-core-selected-by-lmt-to-deliver-advanced-5g-services-in-latvia/',
                "Nokia 5G SA core selected 6 Jun 2022; LMT already used Nokia Cloud Packet Core. Ericsson's 2025 deal modernises subscriber "
                "infrastructure (UDM), not the packet core"),
         first_contract=ND('2018 Nokia live demo was cooperation, not a contract; the 2022 SA-core deal post-dates the 2019 launch'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Latvia', operator_name='Tele2',
         name_note='Tele2 Latvia SIA (100% Tele2 Sverige AB, owned by Tele2 AB)',
         share=V(38.28, LV_SHARE, LV_SHARE_NOTE, 2022),
         launch=V(2020, 'https://resources.telegeography.com/scandinavian-skirmishes-and-baltic-battlegrounds-reviewing-regional-rivalries',
                  "Jan 2020 per TeleGeography; Tele2's nationwide rollout followed the Dec 2021 700 MHz auction"),
         ran5=[R('Nokia', 'all', 'https://www.nokia.com/newsroom/nokia-and-tele2-expand-5g-partnership-in-the-baltics/',
                 "Baltic 5G RAN deal (4 Jan 2022): 'Nokia is the incumbent and sole supplier in the deal'; verified")],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-and-tele2-expand-5g-partnership-in-the-baltics/',
                 "Nokia described as the incumbent; it will 'modernize Tele2's nationwide radio network' and Tele2 says the existing 4G "
                 "networks will be upgraded in the same rollout; verified")],
         gov=[], gov_note='no state holder at 5% or more in Tele2 AB (Freya Investissement 19.8%, BlackRock 6.2%)',
         gov_dropped=['Norges Bank Investment Management 1.69% of Tele2 AB (Aug 2026; board seat not checked)',
                      'Third Swedish National Pension Fund (AP3) 0.69% of Tele2 AB (Oct 2026; meets the pension rule: state fund, board appointed by the government, ap3.se; board seat not checked)'],
         core=V('Nokia', 'https://www.nokia.com/newsroom/nokia-to-accelerate-tele2s-digitalization-with-distributed-cloud-core/',
                'SA 5G core, Voice over 5G and Cloud Packet Core for Sweden and the Baltics incl. Latvia (11 Jan 2021)'),
         first_contract=ND('Nokia core (Jan 2021) and RAN (Jan 2022) deals post-date the Jan 2020 launch'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Latvia', operator_name='Bite',
         name_note='BITE Latvija SIA (Bitė Group)',
         share=V(23.4, LV_SHARE, LV_SHARE_NOTE, 2022),
         launch=V(2023, 'https://www.sorainen.com/deals/bite-latvija-receives-green-light-to-use-frequencies-enabling-its-5g-services/',
                  'regulator authorised 3.6 GHz sharing with Unistars on 9 Feb 2023, enabling 5G; an industry directory gives Feb 2023'),
         ran5=[R('Ericsson', 'all', 'https://developingtelecoms.com/telecom-business/operator-news/13506-ericsson-takes-a-bite-of-baltics-5g-networks.html',
                 "2022-2028 deal: Ericsson 'will be the sole provider of nationwide RAN for Bite' (Latvia and Lithuania); verified")],
         ran4=[R('Huawei', 'not_disclosed', 'https://www.mobileeurope.co.uk/6026/', "Jun 2010: Huawei to deploy a nationwide 2G/3G/4G network (SingleRAN)"),
               R('Ericsson', 'not_disclosed', 'https://investinlatvia.org/en/news/5g-technology-takes-several-steps-forward-in-latvia',
                 'May 2022 agreement also covers upgrading the existing 2G/3G/4G networks')],
         ran4_note=("Huawei's legacy equipment presumably replaced by Ericsson, but that is stated only in a personal profile, so no "
                    "vendor-switch row is recorded"),
         gov=[], gov_note='100% UAB Bite group; consolidating parent PLT VII Finance S.à r.l. (Providence Equity, private)', gov_dropped=[],
         core=V('Nokia', 'https://stocks.observer-reporter.com/observerreporter/article/gnwcq-2024-8-28-bite-group-selects-nokias-packet-core-to-drive-5g-evolution-and-to-simplify-and-enhance-network-capacity',
                "Nokia appliance-based Packet Core incl. 5G SA for Latvia and Lithuania (Nokia release via GlobeNewswire, 28 Aug 2024); earlier NSA EPC vendor not named"),
         first_contract=V('2022-05-17', 'https://www.ericsson.com/en/news/3/2022/bit-group-selects-ericsson-as-sole-network-supplier--bringing-5g-to-the-baltics',
                          'Ericsson framework agreement for 5G in Latvia and Lithuania; an earlier Huawei 5G MoU (2019) was not a supply contract'),
         vendor_operates=ND('Nokia MantaRay network management software is a product, not managed operations')),
    # ------------------------------------------------------------------ Ukraine
    dict(region='Central Asia & Eastern Europe', country='Ukraine', operator_name='Kyivstar', **UA_SAMPLE,
         share=UA_SHARE, launch=UA_LAUNCH,
         ran5=[], ran5_note=("Kyiv pilot (Jul 2026) used 'a mix of Ericsson and Huawei equipment', Huawei the 'basic supplier for Kyiv' "
                             "(dev.ua); pilot only, not coded"),
         ran4=[], ran4_note=("CEPA (2023): Kyivstar 'relies on Chinese vendors Huawei and ZTE'; Light Reading (Jul 2024): equipment from "
                             "Ericsson and ZTE and 'a broader mix of vendors for RAN'. No generation or share stated, so not coded"),
         gov=[], gov_note='VEON Amsterdam B.V. 83.6% of Kyivstar Group (1 Mar 2026); VEON not state-controlled per the filings', gov_dropped=[],
         core=ND('Ericsson and ZTE are in the existing core; no 5G core vendor named'),
         first_contract=ND('Rakuten Symphony letter of intent for 4G/5G Open RAN (28 Feb 2024) is not a contract'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Ukraine', operator_name='Vodafone', **UA_SAMPLE,
         name_note='Vodafone Ukraine (PrJSC VF Ukraine; Vodafone brand partner, owned by NEQSOL)',
         share=UA_SHARE, launch=UA_LAUNCH,
         ran5=[], ran5_note=("5G testing with Huawei (Kropyvnytskyi, Ivano-Frankivsk) and Nokia (Vynnyky) from 14 May 2025; Nokia equipment "
                             "in the Kyiv pilot (Jul 2026). Pilots only, not coded"),
         ran4=[], ran4_note="Strand Consult (via Light Reading, Jul 2024): 75% of Vodafone Ukraine's RAN kit from Chinese vendors, not split by vendor or generation",
         gov=[], gov_note='Telco Investments B.V. 99% (ultimate parent NEQSOL Holding, beneficial owner Nasib Hasanov); no state holder (H1 2025 statements)',
         gov_dropped=[],
         core=ND(), first_contract=ND('only 5G trials with Nokia (2024) and Huawei/Nokia testing (2025)'), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Ukraine', operator_name='lifecell', **UA_SAMPLE,
         share=UA_SHARE, launch=UA_LAUNCH,
         ran5=[], ran5_note="Kyiv pilot (Jul 2026): 'lifecell built its network on Ericsson stations' (dev.ua); pilot only, not coded",
         ran4=[], ran4_note=("Odessa Journal (Nov 2025): 11,755 Huawei and 11,473 Ericsson base stations in lifecell's network, generation not "
                             "stated; Huawei cooperation since 2010 (lifecell history). Not coded as 4G"),
         gov=[], gov_note=("NJJ Holding (Xavier Niel) via DVL Telecom since 9 Sep 2024. Before that Turkcell owned 100%, with the Türkiye "
                           "Wealth Fund holding 26.2% of Turkcell (via TVF BTIH); no longer in the chain"),
         gov_dropped=[],
         core=V('Ericsson', 'https://m.lifecell.ua/en/about_lifecell/pressroom/press-releases/?chosen_period=2026-02',
                'agreement (10 Feb 2026) to move the core to Ericsson cloud-native Packet Core and UDM, preparing for 5G SA; no commercial 5G yet'),
         first_contract=V('2026-02-10', 'https://m.lifecell.ua/en/about_lifecell/pressroom/press-releases/?chosen_period=2026-02',
                          'Ericsson core agreement; earlier Ericsson work (2019 demo, 2020 Massive MIMO test) was testing'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Zimbabwe
    dict(region='Africa', country='Zimbabwe', operator_name='Econet',
         name_note='Econet Wireless Zimbabwe',
         share=V(72.85, 'https://www.potraz.gov.zw/wp-content/uploads/2025/09/2025-1st-Quarter-Abridged-Sector-Performance-Report-HMed.pdf',
                 'POTRAZ Q1 2025 active mobile subscriptions: Econet 11,578,890 / 15,893,626 (NetOne 3,978,177; Telecel 336,559); verified in the PDF', 2025),
         launch=V(2022, 'https://www.econet.co.zw/econet-5g/', '24 Feb 2022'),
         ran5=[R(v, 'not_disclosed', 'https://ewzinvestor.com/wp-content/uploads/2026/07/zw-eco-2023-ar-00.pdf',
                 "2023 annual report: 'We partnered with Ericsson, ZTE and Huawei to launch 5G services' (RAN and 5G EPC); no split")
               for v in ('Ericsson', 'ZTE', 'Huawei')],
         ran4=[], ran4_note='Ericsson, ZTE and Huawei are listed as network-infrastructure key suppliers only in a Scribd copy of the 2022 report (not cited)',
         gov=[], gov_note=("no state holder at 5% or more: Econet Global Limited 42.9% (Mauritius) and nominee accounts (FY2025 report). "
                           "Older reports show an unnamed 'government and parastatals' category of 0.5-0.6%"),
         gov_dropped=[],
         core=V('Ericsson', 'https://www.itnewsafrica.com/2022/03/econet-ericsson-launch-5g-in-zimbabwe/',
                'Ericsson 5G EPC for the Harare launch (1 Mar 2022); dual-mode 5G Core modernisation (Feb 2023); SA core functions added (Mar 2025)'),
         first_contract=ND('Ericsson announcement (1 Mar 2022) post-dates the 24 Feb 2022 launch; contract date not stated'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Sri Lanka
    dict(region='Asia-Pacific', country='Sri Lanka', operator_name='Dialog',
         name_note='Dialog Axiata PLC',
         share=V(62.1, 'https://www.trc.gov.lk/content/files/news/comments_MAR/2.%20Retail%20Cellular%20Mobile%20Voice%20and%20Broadband%20Markets_Public%20V1.pdf',
                 "TRCSL market analysis, end-Sep 2025: Dialog 62.1, Mobitel 24.6, Hutch 13.4. Dialog's 2025 report says 64% citing TRCSL Q4 2025", 2025),
         launch=V(2025, 'https://www.themorning.lk/articles/RNDVfJgHgj0GvJNVhdvD', 'commercial 5G 19 Dec 2025, with SLT-Mobitel the same day'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2/2026/ericsson-to-deploy-5g-ran-in-sri-lanka-with-dialog-axiata',
                 '5G RAN agreement announced 5 Mar 2026 (AIR 3219 Massive MIMO, software, rollout); no share wording. The vendor of the Dec 2025 launch network is not named')],
         ran4=[], ran4_note='Huawei, Ericsson and ZTE supplied the 3G/HSPA network (2009); no 4G vendor named',
         gov=[G('Malaysia', 'Khazanah Nasional Berhad', 'sovereign_wealth_fund', 36.69, 'Axiata Group Berhad', 'via_parent', '2026-03-31',
                'https://www.axiata.com/2025IAR/documents/Axiata-Integrated-Annual-Report-2025-Overview.pdf',
                "Axiata's audited statements call Khazanah 'the sovereign wealth fund of the Government of Malaysia' (36.71% direct in the "
                "narrative; 36.69% in the 31 Mar 2026 shareholding table); same basis as batch 4 (XLSmart)",
                link_url='https://www.axiata.com/2025IAR/documents/Axiata-Governance-and-Audited-Financial-Statements-2025.pdf',
                chain=DIALOG_CHAIN),
              G('Malaysia', 'Employees Provident Fund Board (EPF)', 'pension_fund', 19.36, 'Axiata Group Berhad', 'via_parent', '2026-03-31',
                'https://www.axiata.com/2025IAR/documents/Axiata-Integrated-Annual-Report-2025-Overview.pdf',
                "Axiata IAR2025 shareholding structure as at 31 Mar 2026 (Overview document, PDF p.2; read 2026-11-26); an EPF representative "
                "director sits on Axiata's board (exp|supp|axiata-holders). Pension rule: established by the Employees Provident Fund Act "
                "1991 (Act 452), Board appointed by the Minister", chain=DIALOG_CHAIN, board_seat='yes')],
         gov_note=("EPF coded under Prof. Shen's pension rule (2026-11-26); before it, EPF was left out because Axiata's report does "
                   "not call it state-owned. Permodalan Nasional Berhad 18.28% of Axiata is not coded: a unit-trust manager, not a "
                   "pension fund, and not described as state-owned. Also direct in Dialog: Bharti Airtel 10.36% (private)"),
         gov_dropped=["Employees' Provident Fund (Sri Lanka) 2.58% of Dialog Axiata PLC (direct; meets the pension rule: established "
                      "under EPF Act No. 15 of 1958, assets managed by the Central Bank of Sri Lanka, epf.lk; board seat not checked)"],
         core=ND(), first_contract=ND('Ericsson RAN agreement (5 Mar 2026) post-dates the Dec 2025 launch'),
         vendor_operates=ND('Ericsson Managed Enterprise Cloud (2015) is an enterprise-cloud service, not network operation')),
]
