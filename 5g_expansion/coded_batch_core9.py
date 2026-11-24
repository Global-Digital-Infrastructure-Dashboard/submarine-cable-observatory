"""Core-94 migration, batch core9 (Prof. Shen, 2026-11): United States (5) and China (4) re-coded in the expansion's
three-file format, in-session on 2026-11-24, following the calibration batch (coded_batch_core1.py).

Inputs: the core panel and its cached vendor/ownership searches (data/5g_searches.jsonl), plus mig|mktshare, mig|share
and mig|ran (data/5g_expansion_searches.jsonl). Government stakes re-express gov_stakes_core.py. Share categories follow
the user's rules (stated % -> 100 all, >50 most, 10-50 some, <10 small; 'majority' -> most, 'roughly evenly' -> some),
each note stating the basis and date. Every share category and every share figure was checked on the primary page at
coding time (5g_expansion/verify_2026-11-24_core9.csv).

US-dish-wireless and US-uscellular are kept under the core panel's dated researcher decisions (consistent with GR-nova):
DISH was dismantling its network and in bankruptcy in 2026; UScellular's wireless operations were acquired by T-Mobile on
1 Aug 2025. Their rows describe the networks as built.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

register(domains={
    'company': ['verizon.com', 'att.com', 't-mobile.com', 'news.samsung.com', 'hkexnews.hk', 'chinaunicom.com.hk',
                'chinatelecom-h.com'],
    'government': ['floridapsc.com', 'fcc.gov', 'govinfo.gov'],
    'news': ['sdxcentral.com', 'fierce-network.com', 'fiercewireless.com', 'computerweekly.com', 'telecoms.com',
             'bignewsnetwork.com', 'rcrwireless.com', 'reuters.com'],
    'other': ['cafetele.com'],
})

US_REGION = 'North America (outside six regions)'
FLPSC = 'https://www.floridapsc.com/pscfiles/website-files/PDF/Publications/Reports/Telecommunication/TelecommunicationIndustry/2025.pdf'
FLPSC_NOTE = ("Florida Public Service Commission, 2025 telecommunications report, Figure 3-1 'U.S. Wireless Market Share, Fourth "
              "Quarter 2024' (T-Mobile 34.7, AT&T 31.5, Verizon 30.8, DISH 1.8, UScellular 1.2; basis: subscribers from the "
              "companies' 2025 10-K reports, about 374m in total; M2M treatment not stated). Verified on the PDF p.24-25, 2026-11-24. "
              "The FCC (national regulator) publishes year-end 2023 shares of postpaid+prepaid connections for four providers only "
              "(FCC 24-136, Fig. II.B.3: Verizon 38.6, T-Mobile 31.9, AT&T 28.3, UScellular 1.2; DISH absent; AT&T's ~135m "
              "connected-device/wholesale connections excluded), also verified; the state regulator's table is coded because it "
              "is newer and covers all five operators on one basis")
FCC = 'https://docs.fcc.gov/public/attachments/FCC-24-136A1.pdf'
TELEGEO_CN = 'https://resources.telegeography.com/china-the-worlds-biggest-5g-market'
TELEGEO_CN_NOTE = ("TeleGeography: share of China's 5G subscriptions at end-2025 (China Mobile 53, Telecom 24, Unicom 20, Broadnet 3); "
                   "basis: 5G subscriptions only, not all mobile subscriptions (MIIT publishes totals only). Verified on the page 2026-11-24")
REUTERS_CN = 'https://www.reuters.com/article/chinas-top-mobile-carriers-to-launch-commercial-5g-on-nov-1-tv-idUSB9N27700D/'
LR_US = 'https://www.lightreading.com/open-ran/floundering-in-open-ran-the-us-sniffs-around-rakuten'
SDX_VZ_2021 = 'https://www.sdxcentral.com/news/ericsson-lands-83b-for-verizon-5g-ran-expansion/'
SDX_VZ_2020 = 'https://www.sdxcentral.com/news/verizon-boots-nokia-samsung-gets-the-spoils/'
SDX_ATT = 'https://www.sdxcentral.com/news/att-claims-50-of-nokia-gear-has-been-ripped-from-its-network/'
SDX_TMO = 'https://www.sdxcentral.com/news/t-mobile-inks-5-year-multi-billion-dollar-5g-ran-deals-with-ericsson-nokia/'
DT_AR = 'https://report.telekom.com/annual-report-2025/_assets/downloads/sha-to-our-shareholders-dtag-ar25.pdf'
CM_TENDER = 'https://www.telecompaper.com/news/china-mobile-picks-huawei-zte-to-deploy-200-000-5g-base-stations--1333069'
CM_700 = 'https://www.telecomtv.com/content/5g/ericsson-takes-a-hit-in-china-mobile-s-latest-5g-contract-awards-and-nokia-gets-a-slice-of-the-pie-41994/'
CM_4G = 'https://www.lightreading.com/2g-3g-4g/report-huawei-zte-win-big-at-china-mobile'
CT_4G = 'https://www.lightreading.com/2g-3g-4g/alcatel-lucent-makes-4g-gains-in-china'
JOINT_TENDER = 'https://www.telecoms.com/5g-6g/huawei-and-zte-win-88-of-joint-china-telecom-unicom-5g-tender'
JOINT_NOTE = ("joint China Telecom-China Unicom 5G RAN tender (reported 7 Dec 2023): Huawei and ZTE together won '88% of the business', "
              "not split between them; Ericsson 'most of the rest'; Nokia 'totally frozen out'. UNVERIFIED: telecoms.com returned 403, "
              "so no share category is coded")
CN_RESTRICTION = 'no Chinese supplier restriction is described in the evidence'

OPERATORS = [
    # ------------------------------------------------------------------ United States
    dict(region=US_REGION, country='United States', operator_name='Verizon', core_operator_id='US-verizon-wireless',
         name_note='core panel name Verizon Wireless (Verizon Communications Inc.)',
         share=V(30.8, FLPSC, FLPSC_NOTE, 2024),
         launch=V(2019, 'https://www.verizon.com/about/our-company/5g/when-will-5g-arrive',
                  '5G Ultra Wideband from 3 Apr 2019 (Chicago, Minneapolis); matches the discovery list (2019-04-03)'),
         ran5=[R('Samsung', 'some', SDX_VZ_2021,
                 "about 50%: Verizon awarded Samsung 'nearly half of its 5G RAN budget' (basis: 5G RAN spend; SDxCentral, 15 Jul 2021); an "
                 "analyst had said 'roughly half of its radio access network (RAN) contract' (Rosenblatt via SDxCentral, 7 Jul 2020). Verified 2026-11-24"),
               R('Ericsson', 'not_disclosed', SDX_VZ_2021,
                 "the $8.3bn five-year deal 'positions Ericsson as Verizon's top RAN supplier' (15 Jul 2021); Light Reading calls it 'the biggest "
                 "supplier to Verizon'; no percentage. Verified 2026-11-24")],
         ran5_note='Nokia was dropped from the RAN in 2020 (see switches), so it is not coded as a 5G supplier',
         ran4=[R('Samsung', 'small', SDX_VZ_2020,
                 "about 5%: Samsung 'had about 5% of Verizon's 4G LTE RAN contract' (basis: 4G RAN contract; analyst via SDxCentral, 7 Jul 2020). Verified 2026-11-24"),
               R('Nokia', 'not_disclosed', SDX_VZ_2020, "Verizon to 'rip out and replace all of Nokia's equipment and services dating back to its 4G LTE network footprint' (7 Jul 2020)"),
               R('Ericsson', 'not_disclosed', 'https://www.fierce-network.com/financial/samsung-scores-6b-network-deal-verizon',
                 "an analyst described the network as 'half Ericsson and half Nokia gear' (Sep 2020). UNVERIFIED: the page returned 403, so no category")],
         gov=[], gov_note='no state holder: the proxy lists Vanguard, BlackRock and State Street above 5% of Verizon Communications',
         gov_dropped=[],
         core=ND('initial 5G was NSA on the existing LTE core; no 5G core vendor named'),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G/5G', 'Nokia', 'Samsung', '2020-07-07', 'not_confirmed', SDX_VZ_2020,
                     "Verizon goes 'from three RAN vendors to two', replacing all Nokia 4G LTE equipment (Samsung's $6.6bn contract disclosed "
                     "8 Sep 2020); Ookla (Jun 2026) still expected Nokia LTE decommissioning in H1 2026, so completion is not confirmed. Verified 2026-11-24")]),
    dict(region=US_REGION, country='United States', operator_name='AT&T', core_operator_id='US-at-t-mobility',
         name_note='core panel name AT&T Mobility (AT&T Mobility LLC; brands AT&T, Cricket)',
         share=V(31.5, FLPSC, FLPSC_NOTE, 2024),
         launch=V(2018, 'https://www.att.com/es-us/sdabout/story/2018/att_brings_5g_service_to_us.html',
                  'standards-based mobile 5G from 21 Dec 2018 in parts of 12 cities; matches the discovery list (2018-12-21)'),
         ran5=[R('Nokia', 'not_disclosed', LR_US,
                 "about 33%: Ericsson 'has replaced Finland's Nokia across a third of AT&T's network' once done (basis: share of the network, "
                 "not generation-specific; Light Reading, 2024); AT&T said 50% of the Nokia gear had been removed by 3 Mar 2026 (SDxCentral). Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Ericsson', 'not_disclosed', SDX_ATT,
                 "'the main equipment supplier and systems integrator' of AT&T's $14bn open RAN overhaul (3 Mar 2026); Light Reading: 'it will be "
                 "the sole supplier of RAN and management software' once Nokia is replaced (a future state, so not coded as 'all'). Verified 2026-11-24"),
               R('Fujitsu', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2023/12/att-to-accelerate-open-and-interoperable-radio-access-networks-ran-in-the-united-states-through-new-collaboration-with-ericsson',
                 'O-RAN radios in integrated Ericsson/Fujitsu sites from 2024 (4 Dec 2023)')],
         ran5_note="Samsung appears only as a 2018 'initial 5G radio partner' and CBRS supplier; Mavenir only as a radio developer, so neither is coded",
         ran4=[R('Nokia', 'some', LR_US, "about 33% of AT&T's network (same Light Reading figure; not generation-specific). Verified 2026-11-24")],
         ran4_note='Ericsson holds the rest of the legacy network but no percentage is stated',
         gov=[], gov_note='no state holder: Vanguard 7.5% is the only holder above 5% of AT&T Inc. found',
         gov_dropped=[],
         core=ND("Nokia supplies the 5G IMS voice core and Cloud Platform (Nokia competitive-landscape document); the packet-core vendor is not named"),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G/5G', 'Nokia', 'Ericsson', '2023-12-04', 'not_confirmed', SDX_ATT,
                     "Ericsson-led open RAN programme replacing legacy Nokia RAN across about a third of the network; 50% of Nokia gear removed "
                     "by 3 Mar 2026; 70% of traffic on open-capable platforms targeted for end-2026. Verified 2026-11-24")]),
    dict(region=US_REGION, country='United States', operator_name='T-Mobile US', core_operator_id='US-t-mobile-usa',
         name_note='core panel name T-Mobile USA (T-Mobile US, Inc.; brands Metro by T-Mobile, Mint Mobile)',
         share=V(34.7, FLPSC, FLPSC_NOTE, 2024),
         launch=V(2019, 'https://www.t-mobile.com/news/press/americas-first-nationwide-5g-network',
                  'nationwide 5G from 2 Dec 2019; matches the discovery list (2019-12-02)'),
         ran5=[R('Ericsson', 'some', LR_US,
                 "about 50%: Ericsson 'provides about half the 5G kit for T-Mobile' (basis: 5G equipment; Light Reading, 2024). Verified 2026-11-24"),
               R('Nokia', 'not_disclosed', SDX_TMO,
                 "the Jan 2021 five-year deals 'cement the Swedish and Finnish vendors as the exclusive RAN suppliers for T-Mobile' (SDxCentral, "
                 "14 Jan 2021); Nokia's share is not stated (the other half is not said to be Nokia's); Nokia extension Apr 2025. Verified 2026-11-24")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.t-mobile.com/news/press/ericsson-5g-agreement',
                 "'already installed base of Ericsson Radio System radios' upgradable to 5G NR by software (11 Sep 2018)"),
               R('Nokia', 'not_disclosed', 'https://www.telecompaper.com/news/t-mobile-us-inks-new-contracts-with-nokia-ericsson-for-5g-expansion--1368598',
                 "Nokia to continue upgrading T-Mobile's mid-band LTE network to 5G (Jan 2021)")],
         ran4_note='legacy Sprint sites used Nokia and Samsung per a blog (CafeTele), not coded',
         gov=[G('Germany', 'Federal Republic of Germany', 'government_ministry', 14.1, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
                '', parent_pct=52.6, chain='Deutsche Telekom AG 52.6% of T-Mobile US (itself listed; treasury shares taken into account)'),
              G('Germany', 'KfW', 'state_holding_company', 14.2, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
                'the annual report describes the Federal Republic as an indirect shareholder via KfW', parent_pct=52.6,
                chain='Deutsche Telekom AG 52.6% of T-Mobile US (itself listed; treasury shares taken into account)')],
         gov_dropped=[],
         core=ND("T-Mobile names Ericsson, Cisco and Nokia jointly as core/RAN partners for network slicing on its SA core; no single core vendor"),
         first_contract=ND("Nokia ($3.5bn, 30 Jul 2018) and Ericsson ($3.5bn, 11 Sep 2018) 5G agreements; the Nokia source in the evidence is "
                           "not a fetchable primary page, so the date is not coded"),
         vendor_operates=ND()),
    dict(region=US_REGION, country='United States', operator_name='DISH Wireless', core_operator_id='US-dish-wireless',
         name_note=("researcher decision (core panel): DISH was dismantling its own 5G network in 2026, its 600 MHz and 3.45 GHz licences "
                    "went to AT&T and AWS-4 to SpaceX, and DISH Wireless was in bankruptcy; the row describes the greenfield SA open RAN as built"),
         share=V(1.8, FLPSC, FLPSC_NOTE + "; DISH's own 10-K gives 6.995m wireless subscribers at 31 Dec 2024", 2024),
         launch=V(2022, 'https://www.prnewswire.com/news-releases/dishs-smart-5g-wireless-network-is-now-available-to-over-20-percent-of-the-us-population-301568302.html',
                  'Project Genesis commercial launch in Las Vegas, May 2022; over 20% of the US population by 14 Jun 2022; matches the discovery list (2022-05)'),
         ran5=[R('Fujitsu', 'not_disclosed', LR_US,
                 "radio units 'supplied mainly by Fujitsu of Japan and Samsung' (basis: radio units, jointly; Light Reading, 2024); a Dell'Oro "
                 "comment that DISH deployed 'mostly Fujitsu radios' (Fierce, 2022) is UNVERIFIED (403), so no category. Verified 2026-11-24 (Light Reading)"),
               R('Samsung', 'not_disclosed', 'https://news.samsung.com/global/dish-wireless-launches-virtual-open-ran-5g-network-with-samsung',
                 'O-RAN radios and vDU/vCU software; initial shipment of 24,000 radios (Feb 2023)'),
               R('Mavenir', 'not_disclosed', LR_US, "'it provides the RAN software' (Light Reading, 2024). Verified 2026-11-24")],
         ran4=[], ran4_note='greenfield 5G SA network; no DISH-operated 4G RAN (its customers used AT&T and T-Mobile networks)',
         gov=[], gov_note='no state holder: Charles Ergen ~51.3% of EchoStar (2025 annual report)',
         gov_dropped=[],
         core=V('Nokia', 'https://www.nokia.com/asset/f/214818/',
                "Nokia's document: Nokia 5G SA core deployed on public cloud for DISH's greenfield network. DISPUTED: the core panel coded "
                "Mavenir from a blog (CafeTele), which is not a citable source here; coded on Nokia's own document"),
         first_contract=ND(), vendor_operates=ND()),
    dict(region=US_REGION, country='United States', operator_name='UScellular', core_operator_id='US-uscellular',
         name_note=("researcher decision (core panel): T-Mobile acquired UScellular's wireless operations on 1 Aug 2025 and its spectrum was "
                    "being assigned to AT&T and Verizon; the row describes UScellular's own network as built"),
         share=V(1.2, FLPSC, FLPSC_NOTE + "; UScellular reported 4.433m retail connections at 31 Dec 2024", 2024),
         launch=V(2020, 'http://www.sec.gov/Archives/edgar/data/821130/000082113021000008/usm-20201231_d2.htm',
                  'commercial 5G in portions of several states incl. Iowa and Wisconsin per the 2020 10-K; a report dates it Feb 2020; the discovery list had no date'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.fierce-network.com/tech/uscellular-taps-ericsson-nokia-5g-mid-band-build',
                 'C-band and 3.45 GHz Radio System and RAN Compute (May 2022); 5G NR from late 2019; one of the two biggest vendors'),
               R('Nokia', 'not_disclosed', 'https://www.computerweekly.com/news/252486782/US-Cellular-taps-Nokia-Ericsson-to-build-out-5G-infrastructure',
                 'AirScale Cloud RAN for mmWave (Jul 2020); C-band massive MIMO (May 2022)'),
               R('Samsung', 'not_disclosed', 'https://www.fierce-network.com/wireless/uscellular-likes-samsung-will-t-mobile-still-love-it-tomorrow',
                 'mmWave and vRAN in the Mid-Atlantic region (Feb 2025)')],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.computerweekly.com/news/252486782/US-Cellular-taps-Nokia-Ericsson-to-build-out-5G-infrastructure',
                 '4G CBRS equipment and services (Jul 2020)'),
               R('Samsung', 'not_disclosed', 'https://www.fierce-network.com/tech/uscellular-taps-ericsson-nokia-5g-mid-band-build',
                 "UScellular 'also uses LTE and 5G network solutions from Samsung' (May 2022)")],
         gov=[], gov_note=("no state holder: TDS held 82.5% (30 Jun 2025) before the T-Mobile acquisition. Post-acquisition the network is "
                           "T-Mobile's, whose German state stakes are coded on T-Mobile US"),
         gov_dropped=[],
         core=V('Nokia', 'https://www.nokia.com/about-us/news/releases/2021/09/09/nokia-extends-uscellular-relationship-with-5g-standalone-core-agreement/',
                "Nokia selected for the 5G SA core (9 Sep 2021); the CTO said 'for the SA core, it's all Nokia' (Fierce, May 2024; 403 there). "
                'The 4G EPC is Nokia and Ericsson'),
         first_contract=ND('Ericsson selected for 5G NR in late 2019; exact date not stated'), vendor_operates=ND()),
    # ------------------------------------------------------------------ China
    dict(region='Asia-Pacific', country='China', operator_name='China Mobile', core_operator_id='CN-china-mobile',
         share=V(53.0, TELEGEO_CN, TELEGEO_CN_NOTE, 2025),
         launch=V(2019, REUTERS_CN, 'commercial 5G from 1 Nov 2019 (all three state operators); MIIT issued licences 6 Jun 2019'),
         ran5=[R('Huawei', 'most', CM_TENDER, "57.2%: 'Huawei will install 57.2 percent of the base stations' in the Apr 2020 tender for 232,143 5G base "
                 "stations (basis: base stations in one tender; Telecompaper, 2 Apr 2020); about 60% of the Jul 2021 700 MHz award (TelecomTV). Verified 2026-11-24"),
               R('ZTE', 'some', CM_TENDER, '28.7% of the same tender (basis: base stations; 2 Apr 2020); about 30% of the 700 MHz award. Verified 2026-11-24'),
               R('Ericsson', 'some', CM_TENDER, "11.4% of the same tender (basis: contracts; 2 Apr 2020); 11% in the 2.6 GHz round but only '2% market share' "
                 "of the 700 MHz award (TelecomTV, 19 Jul 2021). Verified 2026-11-24"),
               R('Nokia', 'small', CM_700, "Nokia Shanghai Bell 'picked up an unspecified \"small sliver\"' of the 700 MHz award, its first 5G RAN business in "
                 "China (basis: contract award; TelecomTV, 19 Jul 2021). Verified 2026-11-24")],
         ran5_note='a consortium of two unnamed Chinese firms took the remaining 2.6% of the Apr 2020 tender',
         ran4=[R('Huawei', 'not_disclosed', CM_4G, "Huawei and ZTE got 'the lion's share' of the $3.2bn 2013 LTE contracts jointly (Light Reading/Reuters, 23 Aug 2013). Verified 2026-11-24"),
               R('ZTE', 'not_disclosed', CM_4G, 'same joint wording'),
               R('Nokia', 'some', CM_4G, "about 20%: Alcatel-Lucent and Nokia Networks (both now Nokia) 'each have received about 10 percent' (basis: contract; "
                 "23 Aug 2013). Verified 2026-11-24"),
               R('Ericsson', 'some', CM_4G, "about 10%: 'about 10 percent' of the contract (basis: contract; 23 Aug 2013). Verified 2026-11-24")],
         gov=[G('China', 'China Mobile Communications Group Co., Ltd. (CMCC)', 'state_owned_company', 68.75, 'China Mobile Limited', 'direct', '2026-04',
                'https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0423/2026042301557.pdf',
                '14,890,502,494 shares at the latest practicable date (2025 annual-report materials); 68.67% direct and indirect at 30 Jun 2026',
                link_url='https://www.govinfo.gov/content/pkg/FR-2026-06-10/html/2026-11571.htm')],
         gov_note='US Federal Register (10 Jun 2026): CMCC is directly owned and controlled by SASAC',
         gov_dropped=[],
         core=ND('no China Mobile core vendor named; Huawei/ZTE are the national 5G-core vendors only in general terms'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Asia-Pacific', country='China', operator_name='China Unicom', core_operator_id='CN-china-unicom',
         share=V(20.0, TELEGEO_CN, TELEGEO_CN_NOTE, 2025),
         launch=V(2019, REUTERS_CN, 'commercial 5G from 1 Nov 2019; co-built, co-shared network with China Telecom'),
         ran5=[R('Huawei', 'not_disclosed', JOINT_TENDER, JOINT_NOTE), R('ZTE', 'not_disclosed', JOINT_TENDER, JOINT_NOTE),
               R('Ericsson', 'not_disclosed', JOINT_TENDER, JOINT_NOTE)],
         ran4=[], ran4_note='no China Unicom 4G RAN vendor named',
         gov=[G('China', 'China United Network Communications Group Company Limited (Unicom Group)', 'state_owned_company', 80.67,
                'China Unicom (Hong Kong) Limited', 'via_parent', '2026-06-30', 'https://www.chinaunicom.com.hk/en/ir/reports/ir2026/ir2026_10.pdf',
                "the filing lists it as an indirect/deemed interest in the operator itself, so it is not multiplied; recoded direct -> "
                "via_parent 2026-11-24 (researcher decision), ownership_type unchanged",
                link_url='https://www.chinaunicom.com.hk/en/ir/reports/ar2025/ar2025_20.pdf',
                chain='Unicom Group -> China United Network Communications Limited 53.52% + Unicom Group BVI 27.15% -> China Unicom (Hong Kong) Limited')],
         gov_note='the 2025 annual report calls Unicom Group a state-owned enterprise directly controlled by the PRC government',
         gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    dict(region='Asia-Pacific', country='China', operator_name='China Telecom', core_operator_id='CN-china-telecom',
         share=V(24.0, TELEGEO_CN, TELEGEO_CN_NOTE, 2025),
         launch=V(2019, REUTERS_CN, 'commercial 5G from 1 Nov 2019; co-built, co-shared network with China Unicom'),
         ran5=[R('Huawei', 'not_disclosed', JOINT_TENDER, JOINT_NOTE), R('ZTE', 'not_disclosed', JOINT_TENDER, JOINT_NOTE),
               R('Ericsson', 'not_disclosed', JOINT_TENDER, JOINT_NOTE)],
         ran4=[R('ZTE', 'some', CT_4G, "32%: 'the single biggest deal, with 32 percent of the order' (basis: first-stage 4G order, unconfirmed Chinese "
                 "media reports; Light Reading, 10 Oct 2013). Verified 2026-11-24"),
               R('Huawei', 'some', CT_4G, '28.9% of the same first-stage order (same basis and date). Verified 2026-11-24'),
               R('Nokia', 'some', CT_4G, "16.6%: Alcatel Shanghai Bell (Alcatel-Lucent, now Nokia) 'reportedly landed 16.6 percent of the deal'; NSN's share "
                 "is inside the joint <5% below (same basis and date). Verified 2026-11-24"),
               R('Ericsson', 'small', CT_4G, "<5%: 'Ericsson AB and Nokia Solutions and Networks (NSN) are believed to have been awarded less than 5 "
                 "percent of the total' jointly (same basis and date). Verified 2026-11-24")],
         gov=[G('China', 'China Telecommunications Corporation', 'state_owned_company', 63.9, 'China Telecom Corporation Limited', 'direct', '2025-12-31',
                'https://www.chinatelecom-h.com/en/ir/report/annual2025/annual2025_12.pdf', "listed as a 'state-owned legal person'; SASAC is the ultimate controller"),
              G('China', 'Guangdong Rising Holdings Group Co., Ltd.', 'state_owned_company', 5.24, 'China Telecom Corporation Limited', 'direct', '2025-12-31',
                'https://www.chinatelecom-h.com/en/ir/report/annual2025/annual2025_12.pdf', "listed as a 'state-owned legal person'")],
         gov_note='HKSCC Nominees 15.11% is a nominee holding with unknown beneficial owners',
         gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    dict(region='Asia-Pacific', country='China', operator_name='China Broadnet', core_operator_id='CN-china-broadnet',
         share=V(3.0, TELEGEO_CN, TELEGEO_CN_NOTE, 2025),
         launch=V(2022, 'https://www.bignewsnetwork.com/news/272600280/china-new-telecom-carrier-launches-5g-services',
                  'commercial 5G from 27 Jun 2022 (licence 2019); matches the discovery list'),
         ran5=[], ran5_note="no Broadnet RAN vendor named: it shares China Mobile's 700 MHz RAN and uses its 2.6 GHz network under paid access",
         ran4=[], ran4_note='no own 4G RAN (shared with China Mobile)',
         gov=[G('China', 'China Broadcasting Network Corporation', 'state_owned_company', 51.0, 'China Broadnet', 'direct', '2022-06-27',
                'https://www.telecomtv.com/content/5g/china-broadnet-the-people-s-republic-of-china-s-newest-telco-launches-5g-services-44813/amp/',
                'majority shareholder at establishment; National Radio and Television Administration named as the state authority behind the group',
                link_url='https://www.lightreading.com/asia/chinas-newest-operator-launches-into-5g-market/d/d-id/778557'),
              G('China', 'State Grid Information & Telecommunication Group', 'state_owned_company', None, 'China Broadnet', 'direct', '2022-06-27',
                'https://www.telecomtv.com/content/5g/china-broadnet-the-people-s-republic-of-china-s-newest-telco-launches-5g-services-44813/amp/',
                'named strategic shareholder; percentage not stated')],
         gov_note=('Guangdong Radio Television Network and Beijing All Media and Culture Group are government-linked shareholders with '
                   'unstated percentages; Alibaba is private'),
         gov_dropped=[],
         core=ND("multi-vendor: Huawei's converged 5G core (Huawei-sponsored Light Reading partner content, 2026) and Huawei and ZTE shortlisted "
                 "for the phase-two core (RCR Wireless, 2 Oct 2023), so no single core vendor"),
         first_contract=ND(), vendor_operates=ND()),
]
