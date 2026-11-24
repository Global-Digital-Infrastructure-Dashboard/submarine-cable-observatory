"""Core-94 migration, batch core6 (Prof. Shen, 2026-11): Poland, Czechia and Slovakia (11 operators) re-coded in the
expansion's three-file format, in-session on 2026-11-24, following the calibration batch (coded_batch_core1.py).

Inputs: the core panel (data/5g_operator_panel.csv) and its cached vendor/ownership searches (data/5g_searches.jsonl),
plus the migration searches mig|mktshare|<market>, mig|share|<id> and mig|ran|<id> (data/5g_expansion_searches.jsonl).
Government stakes re-express gov_stakes_core.py's per-holder rows. Share categories follow the user's rules
(2026-11-23/24): a stated percentage maps 100% = all, >50% = most, 10-50% = some, <10% = small; stated traffic/site/unit
shares map by the same rule; 'sole' -> all; the note states the basis and date. Every share category and checked
figure: 5g_expansion/verify_2026-11-24_core6.csv.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

register(domains={
    'company': ['orange-ir.pl', 'play.pl', 't-mobile.pl', 'grupapolsatplus.pl', 't-press.cz', 't-mobile.cz', 'o2.cz',
                'o2.sk', 'orange.sk', 'telekom.sk', 'mavenir.com', 'report.telekom.com', 'zte.com.cn', 'ericsson.com',
                'nokia.com', 'orange.com', 'assets.orange.com', 'reports.investors.vodafone.com', 'eand.com'],
    'government': ['uke.gov.pl', 'ctu.gov.cz', 'teleoff.gov.sk', 'digital-strategy.ec.europa.eu'],
    'research_industry_group': ['gsma.com', 'samenacouncil.org', 'amcham.sk'],
    'news': ['lightreading.com', 'broadbandtvnews.com', 'reuters.com', 'verdict.co.uk', 'new-techeurope.com',
             'mobileeurope.co.uk', 'telecompaper.com', 'telecomtv.com'],
}, overrides={
    # Nokia's own release on a press-release distribution site
    'https://www.einpresswire.com/article/509334272/nokia-to-prepare-orange-slovensko-ran-for-5g': 'company',
    # e& PPF Telecom Group's own annual accounts on a CDN host
    'https://www.datocms-assets.com/56100/1771365178-fr39_20260217_eand_ppf_telecom_group_fy2025_annual_accounts_public.pdf': 'company',
})

# ------------------------------------------------------------------ shared sources
UKE_2024 = 'https://www.uke.gov.pl/download/gfx/uke/en/defaultaktualnosci/36/413/3/2026_06_24_rost_mzdo.pdf'
UKE_2022 = 'https://www.uke.gov.pl/download/gfx/uke/en/defaultaktualnosci/36/382/4/report_tele_en_akcept_2_15.11.2023_final.pdf'
UKE_NOTE = ("UKE, Report on the state of the telecommunications market: share of mobile telephony users (SIM card holders; "
            "active SIMs exclude M2M). 2024 report (p.58, text): P4 29.8, Orange 26.5; the other two operators' 2024 values are "
            "only in an image chart (Figure 53) and are not extractable. 2022 report (p.20): P4 30.2, Orange 26.6, Polkomtel 20.4, "
            "T-Mobile 19.2. Both verified 2026-11-24. The latest stated figure is coded for each operator, so the year differs "
            "within Poland")
GSMA_PL = 'https://www.gsma.com/get-involved/gsma-membership/gsma_resources/poland-races-to-regain-5g-competitiveness-in-europe-with-mid-band-rollout/'
PL_LAUNCH_NOTE = ("the discovery search (UKE, GSMA, EU sources) describes all four Polish operators as commercially launched in 2020 "
                  "on 2100 MHz, with C-band services from Jan 2024; exact date not found (an aggregator's 'July 2020' is not cited)")
LR_EXIT = 'https://www.lightreading.com/5g/europe-is-showing-huawei-the-exit'
LR_EXIT_NOTE = "Strand Consult via Light Reading (10 Sep 2020): '{x}% of RAN is Huawei-supplied'; basis: RAN, all generations, 2020. Verified 2026-11-24"
LR_2012 = 'https://www.lightreading.com/mobile-core/ericsson-ousted-from-shared-network'
LR_2012_NOTE = ("Light Reading (26 Jan 2012): Orange and T-Mobile chose Huawei and NSN for their NetWorks! shared RAN; Orange "
                "confirmed 'Ericsson's equipment will be replaced by equipment from Huawei and NSN'. Generation not stated "
                "(pre-LTE shared network). Verified 2026-11-24")
CTU_2025 = 'https://ctu.gov.cz/sites/default/files/obsah/stranky/570300/soubory/annual-report-2025.pdf'
CTU_NOTE = ("ČTÚ Annual Report 2025, Chart 1 (p.10): shares of active retail mobile SIM cards, mid-2025 (30 Jun 2025). T-Mobile "
            "38.48%. The chart labels BOTH O2 and Vodafone 33.18%, which with T-Mobile and MVNOs (3.24%) sums to 108%; the text "
            "gives the three MNOs 96.76% together, so O2 and Vodafone hold 33.18% and 25.10% between them, but the chart does not "
            "say which is which (one search reports Vodafone 25.15%). Verified 2026-11-24")
LR_CZ = 'https://www.lightreading.com/5g/odds-shorten-on-huawei-5g-ban-in-czech-republic'
LR_CZ_NOTE = ("Light Reading (8 Feb 2022): CETIN 'is providing infrastructure for both O2 and T-Mobile, which share active mobile "
              "network equipment' and is 'ditching Huawei as it deploys a 5G network built solely by Ericsson'; CETIN: 'we are "
              "replacing Huawei AND Nokia', its 4G network having been 'built with both companies' technologies'. Verified 2026-11-24")
LR_VOD = 'https://www.lightreading.com/5g/as-eu-dithers-vodafone-prepares-for-huawei-removal'
SK_SHARE_NOTE = ("no regulator table by operator found. The 2025 market search's figures come from a Frontier Economics deck in "
                 "Slovak Telekom's spectrum filing on the regulator's site (TeleGeography data, Dec 2021); its chart labels "
                 "('28% 34% 29% 9% TM OSK O2 SWAN ST') cannot be matched to operators reliably, and the two searches assign 34% "
                 "and 28% to different operators. Checked 2026-11-24; not coded")
DT_AR = 'https://report.telekom.com/annual-report-2025/_assets/downloads/sha-to-our-shareholders-dtag-ar25.pdf'
DT_Q3 = 'https://report.telekom.com/interim-report-q3-2026/to-our-shareholders/the-t-share.html'
ORANGE_URD = 'https://assets.orange.com/medias/domain12751/media101922/576636-wexkleg98s-75.pdf'
ORANGE_SA = 'https://www.orange.com/en/press-release/orange-selects-suppliers-for-its-5g-stand-alone-5g-sa-networks-in-europe-234893'
VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
EPPF = 'https://www.datocms-assets.com/56100/1771365178-fr39_20260217_eand_ppf_telecom_group_fy2025_annual_accounts_public.pdf'


def dt_gov(chain, bund=14.1, kfw=14.2, as_of='2025-12-31', url=DT_AR):
    return [G('Germany', 'Federal Republic of Germany', 'government_ministry', bund, 'Deutsche Telekom AG', 'via_parent', as_of, url,
              '', chain=chain),
            G('Germany', 'KfW', 'state_holding_company', kfw, 'Deutsche Telekom AG', 'via_parent', as_of, url,
              'holds part of the federal stake', chain=chain)]


def orange_gov(chain, parent_pct=None):
    return [G('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_URD,
              '21.04% of voting rights (Orange 2025 Universal Registration Document)', parent_pct=parent_pct, chain=chain),
            G('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_URD,
              "8.00% of voting rights; included in the public-sector holding with the French State", parent_pct=parent_pct, chain=chain)]


def e_and_vodafone(chain):
    return [G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 17.005026,
              'Vodafone Group Plc', 'via_parent', '2026-03-31', VODAFONE_AR,
              "the Vodafone filing names e& without calling it state-owned; e&'s 2025 integrated annual report gives the Emirates "
              "Investment Authority 60%, ultimately controlled by the UAE Federal Government",
              link_url=E_AND_AR, chain=chain)]


VOD_DROPPED = ['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)']

OPERATORS = [
    # ------------------------------------------------------------------ Poland
    dict(region='Central Asia & Eastern Europe', country='Poland', operator_name='Orange Polska', core_operator_id='PL-orange-polska',
         share=V(26.5, UKE_2024, UKE_NOTE, 2024),
         launch=V(2020, GSMA_PL, PL_LAUNCH_NOTE),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-wins-ten-year-network-expansion-deal-with-orange-polska/',
                 "Nokia (7 Jun 2022): ten-year extension that 'will cover 50 percent of Orange's network in northern Poland', modernising "
                 "the existing radio network and adding 5G; basis: share of Orange's network (unit not stated), 2022. Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]")],
         ran5_note='no other 5G RAN supplier named in the evidence; Ericsson is the 5G SA core vendor, not RAN',
         ran4=[R('Huawei', 'most', 'https://www.lightreading.com/5g/orange-europe-boss-we-ll-stick-with-huawei-unless-it-is-banned',
                 "Light Reading (5 Oct 2021), citing Strand Consult: 'In Poland ... Huawei provided 70% of the 4G RAN in 2020'; basis: "
                 "4G RAN, 2020. Verified 2026-11-24. The 2020 Light Reading table gives the same 70% for Orange's RAN"),
               R('Nokia', 'some', 'https://www.nokia.com/newsroom/nokia-wins-ten-year-network-expansion-deal-with-orange-polska/',
                 "Nokia (7 Jun 2022): the ten-year extension 'will cover 50 percent of Orange's network in northern Poland' (basis: share of the network, all generations; 2022). DATED: Huawei's 70% is 2020 [decision 2026-11-24: all-generation share, coded to 4G only]; the 2022 Nokia extension modernises the existing radio network in its half of the network; prior Nokia (NSN) supply in the "
                 "2012 NetWorks! shared RAN")],
         gov=orange_gov('Orange S.A. 50.67% of Orange Polska (listed in Warsaw), 31 Dec 2025', parent_pct=50.67),
         gov_dropped=[], gov_note=("Allianz Polska OFE/DFE (8.12%) and Nationale-Nederlanden OFE/DFE (6.40%) are private pension funds; "
                                   "Orange S.A.'s 50.67% is from the Orange Polska 2025 financial report "
                                   "(https://www.orange-ir.pl/wp-content/uploads/2026/03/financial-report-OPL-Group-2025.pdf)"),
         core=V('Ericsson', ORANGE_SA, "Orange (21 Feb 2022): Ericsson for the 5G SA core in Poland; Oracle supplies signalling/routing "
                "group-wide (not coded as the core)"),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '2G/3G (not stated)', 'Ericsson', 'Huawei', '2012-01-26', 'not_confirmed', LR_2012, LR_2012_NOTE),
                   S('RAN', '2G/3G (not stated)', 'Ericsson', 'Nokia', '2012-01-26', 'not_confirmed', LR_2012,
                     LR_2012_NOTE + '; NSN is now Nokia')]),
    dict(region='Central Asia & Eastern Europe', country='Poland', operator_name='Play', core_operator_id='PL-p4',
         name_note='core panel name P4 (legal entity P4 sp. z o.o.); brand Play',
         share=V(29.8, UKE_2024, UKE_NOTE, 2024),
         launch=V(2020, GSMA_PL, PL_LAUNCH_NOTE),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.mobileeurope.co.uk/ericsson-to-build-new-5g-ran-for-polish-mobile-operator-play-with-kit-they-joints-developed/',
                 "Mobile Europe (22 Oct 2021): Ericsson 'contracted to modernise the Play's RAN throughout Poland with Ericsson Radio "
                 "System 5G kit'; no share wording; Ericsson was an 'additional partner' from Jul 2018. Verified 2026-11-24")],
         ran5_note=("Huawei's 5G role not stated: Play's 2025 report names Huawei and Ericsson as Poland's two main mobile equipment "
                    "suppliers without Play's split; Strand's 90% (below) covers the whole RAN in 2020 and is coded as 4G only"),
         ran4=[R('Huawei', 'most', LR_EXIT, LR_EXIT_NOTE.format(x=90) + "; coded to 4G only because Play's 5G was then nascent and "
                 "Ericsson has modernised the RAN since 2021")],
         gov=[], gov_dropped=[], gov_note='controlled by iliad (NJJ/Xavier Niel, private); no state holder in the evidence',
         core=ND("Play's 2025 management report says it began implementing an independent 5G core for supplier diversification; vendor not named"),
         first_contract=ND('Ericsson selected Jul 2018 for RAN expansion with 5G-ready products; not stated to be a 5G contract'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Poland', operator_name='T-Mobile Polska', core_operator_id='PL-t-mobile-polska',
         share=V(19.2, UKE_2022, UKE_NOTE, 2022),
         launch=V(2020, 'https://www.broadbandtvnews.com/2020/06/08/t-mobile-enters-polish-5g-market/',
                  'commercial 5G from 9 Jun 2020 (announced 8 Jun); a Dec 2018 Warsaw network was pre-commercial'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/about-us/news/releases/2022/03/22/nokia-extends-partnership-with-t-mobile-polska-in-ten-year-deal/',
                 "Nokia (22 Mar 2022): 'Nokia will increase its share in T-Mobile's network to 50 percent', covering radio modernisation "
                 "and 5G rollout; basis: share of the network (unit not stated), target under the ten-year deal. Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]")],
         ran5_note=("WRONG claim not coded: the search's 'Huawei sole 5G vendor (2020)' is SDxCentral of 10 Dec 2018 and describes the "
                    "pre-commercial Warsaw network. Huawei's share of the commercial 5G RAN is not stated"),
         ran4=[R('Huawei', 'most', LR_EXIT, LR_EXIT_NOTE.format(x=70)),
               R('Nokia', 'some', 'https://www.nokia.com/about-us/news/releases/2022/03/22/nokia-extends-partnership-with-t-mobile-polska-in-ten-year-deal/',
                 "'Nokia will increase its share in T-Mobile's network to 50 percent' (basis: share of the network, all generations; target under the Mar 2022 ten-year deal). DATED: Huawei's 70% is 2020 [decision 2026-11-24: all-generation share, coded to 4G only]; " 'Nokia has supplied 2G/3G/4G and 5G DSS radio technology; part of the 2012 NetWorks! shared RAN')],
         gov=dt_gov('Deutsche Telekom AG -> T-Mobile Polska; percentage not stated (treated as wholly owned in gov_stakes_core)'),
         gov_dropped=[], gov_note='',
         core=ND(), first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '2G/3G (not stated)', 'Ericsson', 'Huawei', '2012-01-26', 'not_confirmed', LR_2012, LR_2012_NOTE),
                   S('RAN', '2G/3G (not stated)', 'Ericsson', 'Nokia', '2012-01-26', 'not_confirmed', LR_2012,
                     LR_2012_NOTE + '; T-Mobile\'s own network had been built on Ericsson and NSN equipment')]),
    dict(region='Central Asia & Eastern Europe', country='Poland', operator_name='Plus', core_operator_id='PL-polkomtel',
         name_note='core panel name Polkomtel (legal entity Polkomtel sp. z o.o.); brand Plus',
         share=V(20.4, UKE_2022, UKE_NOTE, 2022),
         launch=V(2020, 'https://www.reuters.com/article/technology/polands-cyfrowy-polsat-to-launch-5g-network-on-monday-idUSL8N2CQ5H8/',
                  'May 2020 (Reuters: launch on Monday, using Nokia and Ericsson)'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/news/2020/1/polkomtel-plus-5g-in-poland-with-ericsson',
                 'initial 5G RAN in five cities (Gdańsk, Łódź, Poznań, Szczecin, Wrocław; Jan 2020); regional split only'),
               R('Nokia', 'not_disclosed', 'https://www.nokia.com/about-us/news/releases/2020/12/18/nokia-and-polkomtel-turn-on-5g-services-in-poland/',
                 '5G AirScale radio on the existing Nokia AirScale LTE infrastructure (18 Dec 2020)')],
         ran5_note=("Plus (11 Sep 2026): 'One hundred percent of the radio equipment ... will come exclusively from Nokia and Ericsson' "
                    "in its modernisation programme, with no split (verified 2026-11-24)"),
         ran4=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/about-us/news/releases/2020/12/18/nokia-and-polkomtel-turn-on-5g-services-in-poland/',
                 'existing Nokia AirScale LTE infrastructure'),
               R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/news/2020/1/polkomtel-plus-5g-in-poland-with-ericsson',
                 "the 5G deal builds on an existing Ericsson-Plus RAN and core partnership")],
         gov=[], gov_dropped=[], gov_note='controlled by the TiVi Foundation (Zygmunt Solorz, private); no state holder in the evidence',
         core=V('Ericsson', 'https://www.ericsson.com/en/news/2020/1/polkomtel-plus-5g-in-poland-with-ericsson', '5G core incl. 5G EPC products (Jan 2020)'),
         first_contract=ND('Ericsson 5G RAN/core deployment announced Jan 2020; contract date not stated'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Czechia
    dict(region='Central Asia & Eastern Europe', country='Czechia', operator_name='O2 Czech Republic', core_operator_id='CZ-o2-czech-republic',
         share=ND(CTU_NOTE + '; O2 is one of the two 33.18/25.10 holders'),
         launch=V(2020, 'http://ctu.gov.cz/sites/default/files/obsah/ctu/monitorovaci-zprava-c.7/2020/obrazky/mz_2020-07_en.pdf',
                  'ČTÚ monitoring report 7/2020: O2 announced commercial 5G from 1 Jul 2020 (Prague centre, Kolín)'),
         ran5=[R('Ericsson', 'all', LR_CZ, "CETIN's 5G network (O2's network company) 'built solely by Ericsson'; basis: CETIN's 5G network, "
                 "Feb 2022. " + LR_CZ_NOTE)],
         ran4=[R('Huawei', 'not_disclosed', LR_CZ, "CETIN's 4G network built with Huawei and Nokia technologies, no split"),
               R('Nokia', 'not_disclosed', LR_CZ, "CETIN's 4G network built with Huawei and Nokia technologies, no split")],
         gov=[], gov_dropped=[], gov_note='PPF Group (Kellner family, private); no state holder',
         core=V('Nokia', 'https://digital-strategy.ec.europa.eu/en/miscellaneous/o2-czech-republic-deploys-nokia-5g-standalone-core',
                'Nokia 5G Standalone core (Jun 2025); the earlier NSA EPC vendor is not named'),
         first_contract=ND('CETIN selected Ericsson in Oct 2020 (Reuters); O2-specific 5G contract date not stated'),
         vendor_operates=ND('CETIN (a PPF sister company) runs the network; no equipment vendor operates it'),
         switches=[S('RAN', '4G and legacy', 'Huawei', 'Ericsson', '2020-10-19', 'not_confirmed', LR_CZ,
                     "CETIN replacing previous-generation technology with Ericsson across the country while switching on 5G; selection "
                     "reported 19 Oct 2020 (Reuters), contract 18 Nov 2020 (Ericsson). " + LR_CZ_NOTE),
                   S('RAN', '4G and legacy', 'Nokia', 'Ericsson', '2020-10-19', 'not_confirmed', LR_CZ, 'same programme. ' + LR_CZ_NOTE)]),
    dict(region='Central Asia & Eastern Europe', country='Czechia', operator_name='T-Mobile Czech Republic', core_operator_id='CZ-t-mobile-czech-republic',
         share=V(38.48, CTU_2025, CTU_NOTE, 2025),
         launch=V(2020, 'https://www.t-press.cz/en/tiskove-zpravy/-/releases/t-mobile-spousti-5g-sit-a-do-konce-roku-pokryje-ctvrtinu-populace-prahy-a-brna/7435264',
                  'commercial 5G from 1 Nov 2020 in Prague and Brno (announced 21 Oct 2020); verified 2026-11-24'),
         ran5=[R('Ericsson', 'not_disclosed', LR_CZ, "via the CETIN network that O2 and T-Mobile share ('share active mobile network "
                 "equipment'), built solely by Ericsson; T-Mobile's own unshared sites and their vendor are not stated, so no share "
                 "category. " + LR_CZ_NOTE)],
         ran4=[R('Huawei', 'not_disclosed', LR_CZ, "Strand Consult (2020) via Light Reading (Feb 2022): all three Czech operators 'relied "
                 "heavily on Huawei' for 4G and only O2 bought non-Chinese 4G RAN; no T-Mobile percentage")],
         gov=dt_gov('Deutsche Telekom AG -> T-Mobile Czech Republic; percentage not stated (treated as wholly owned in gov_stakes_core)',
                    bund=14.22, kfw=14.37, as_of='2026-09-30', url=DT_Q3),
         gov_dropped=[], gov_note="Deutsche Telekom's 30 Sep 2026 figures, as in gov_stakes_core (other DT rows use 31 Dec 2025)",
         core=V('Mavenir', 'https://www.nokia.com/asset/f/214972/', "converged packet core for 2G-5G NSA, preparing for SA (Feb 2024 award), "
                "as reported in a Nokia market document"),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Czechia', operator_name='Vodafone Czech Republic', core_operator_id='CZ-vodafone-czech-republic',
         share=ND(CTU_NOTE + '; Vodafone is one of the two 33.18/25.10 holders'),
         launch=V(2020, 'https://ctu.gov.cz/sites/default/files/obsah/ctu/monthly-monitoring-report-no.11/2020/obrazky/monitoringreport202011fin.pdf',
                  "ČTÚ monthly monitoring report 11/2020: 'Vodafone launched 5G in October' (Prague and Brno centres); verified 2026-11-24"),
         ran5=[R('Huawei', 'not_disclosed', LR_VOD, "Strand Consult via Light Reading (27 Jul 2020): 'In six countries, including the Czech Republic ... "
                 "Huawei accounts for the entirety of Vodafone's RAN'; basis: RAN, all generations, 2020. Light Reading "
                 "(Feb 2022) adds that Vodafone 'would continue to build a 5G RAN with Huawei technologies \"at pace\"' (group CEO) and "
                 "had not publicised a Czech switch, which confirms Huawei in 5G but not its share. Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]")],
         ran4=[R('Huawei', 'all', LR_VOD, "the same 2020 'entirety of Vodafone's RAN' statement (all generations). Verified 2026-11-24")],
         gov=e_and_vodafone('Vodafone Group Plc -> Vodafone Czech Republic; percentage not stated (treated as wholly owned in gov_stakes_core)'),
         gov_dropped=VOD_DROPPED, gov_note="Vega's Jul 2026 agreement to buy e&'s stake is not shown as completed",
         core=ND("Vodafone removed Huawei from European cores (group decision, 2020); the Czech 5G core vendor is not named"),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Slovakia
    dict(region='Central Asia & Eastern Europe', country='Slovakia', operator_name='Orange Slovensko', core_operator_id='SK-orange-slovensko',
         share=ND(SK_SHARE_NOTE + "; Orange's own reports give only its customer count (2.392m active, end-2024)"),
         launch=V(2021, 'https://www.verdict.co.uk/orange-slovakia-5g-network/', 'commercial 5G 12 May 2021 (parts of Bratislava and Banská Bystrica); matches the discovery list'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.mobileeurope.co.uk/orange-slovensko-taps-nokia-for-5g-ran/',
                 'selected (Feb 2020) to prepare the RAN for 5G with AirScale hardware/software; no share wording')],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.mobileeurope.co.uk/orange-slovensko-taps-nokia-for-5g-ran/',
                 "'recently modernised AirScale-based 4G network'; Orange's 2017 report books a gradual swap of Alcatel RAN technology from "
                 "2018 (Alcatel-Lucent is now part of Nokia, so no switch row)")],
         gov=orange_gov('Orange S.A. -> Atlas Services Belgium -> 100% of Orange Slovensko'),
         gov_dropped=[], gov_note='',
         core=V('Nokia', ORANGE_SA, 'Orange (21 Feb 2022): Nokia for the 5G SA core in Slovakia'),
         first_contract=V('2020-02-10', 'https://www.einpresswire.com/article/509334272/nokia-to-prepare-orange-slovensko-ran-for-5g',
                          "Nokia's announcement of the 5G RAN selection (announcement date; signing date not stated)"),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Slovakia', operator_name='Slovak Telekom', core_operator_id='SK-slovak-telekom',
         share=ND(SK_SHARE_NOTE),
         launch=V(2020, 'https://www.ericsson.com/en/press-releases/3/2020/slovak-telekom-to-launch-commercial-5g-with-ericsson',
                  'commercial 5G from 10 Dec 2020 (large areas of Bratislava); matches the discovery list (2020-12)'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/3/2020/slovak-telekom-to-launch-commercial-5g-with-ericsson',
                 "selected to deliver the 5G RAN with Ericsson Spectrum Sharing (Dec 2020); no share wording. In Oct 2020 Slovak Telekom "
                 "said it was negotiating with ZTE, Nokia, Huawei and Ericsson; no other award is evidenced")],
         ran4=[R('Ericsson', 'all', 'https://www.lightreading.com/mobile-core/slovak-telekom-launches-4g-with-ericsson',
                 "Ericsson 'is the sole vendor for the LTE radio network' (Light Reading, 16 Dec 2013); basis: LTE radio network, 2013. "
                 "Verified 2026-11-24")],
         gov=dt_gov('Deutsche Telekom AG -> Slovak Telekom; percentage not stated (treated as wholly owned in gov_stakes_core)'),
         gov_dropped=[], gov_note='',
         core=V('Mavenir', 'https://www.mavenir.com/press-releases/slovak-telekom-chooses-mavenirs-converged-packet-core-in-core-supply-partnership/',
                "converged packet core across 'all Gs' incl. 5G SA capabilities (Feb/Mar 2024)"),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Slovakia', operator_name='O2 Slovakia', core_operator_id='SK-o2-slovakia',
         share=ND(SK_SHARE_NOTE + '; O2 reports 2.37m active SIMs (2023) without a market share'),
         launch=V(2021, 'https://www.samenacouncil.org/samena_daily_news?news=86188',
                  'commercial 5G in 15 western Slovak towns, Sep 2021; DISPUTED: the discovery list has a 6 Oct 2020 soft launch/pilot in '
                  'Bratislava; coded the commercial switch-on'),
         ran5=[R('Ericsson', 'all', 'https://www.new-techeurope.com/2021/04/27/o2-slovakia-selects-ericsson-as-commercial-5g-partner/amp/',
                 "'Ericsson has been selected by O2 Slovakia as its sole 5G radio access network (RAN) technology solutions vendor' "
                 "(27 Apr 2021), after a multi-vendor trial; basis: 5G RAN supplier selection, 2021. Verified 2026-11-24")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.new-techeurope.com/2021/04/27/o2-slovakia-selects-ericsson-as-commercial-5g-partner/amp/',
                 'the contract also modernises the 2G, 3G and 4G RAN with Ericsson Radio System; the incumbent vendor is not named')],
         gov=[G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 50.0,
                'e& PPF Telecom Group B.V.', 'via_parent', '2025-12-31', EPPF,
                '50% plus one share; the accounts name the UAE Federal Government as e&\'s ultimate controlling party',
                chain='e& PPF Telecom Group B.V. -> PPF TMT Bidco 1 N.V. 100% -> O2 Slovakia (holding company for O2 Slovakia, '
                      'Yettel Hungary, Yettel Bulgaria, Yettel Serbia)')],
         gov_dropped=[], gov_note="O2 Slovakia's own ownership search gives an outdated chain (O2 Czech Republic 100% at 2015); the e& PPF accounts supersede it",
         core=ND('5G SA planned for Q4 2026; core vendor not named'),
         first_contract=V('2021-02-16', 'https://telecompaper.com/news/o2-slovakia-picks-ericsson-as-partner-for-5g-deployment--1372649',
                          'Ericsson announced as 5G deployment partner (announcement date)'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Slovakia', operator_name='4ka', core_operator_id='SK-swan',
         name_note='core panel name SWAN (legal entity SWAN, a.s.); brand 4ka',
         share=ND(SK_SHARE_NOTE + '; SWAN reports 670,000+ mobile clients (2024) without a share'),
         launch=V(2019, 'https://amcham.sk/publications/issues/2022-3-regional-development/article/273751/united-to-become-greater',
                  "AmCham interview: 4ka launched 'the first commercial 5G mobile-network operations in Slovakia' in 2019. DISPUTED: the "
                  "discovery list calls the late-2019 Banská Bystrica service a limited launch/technical pilot; coded the stated 2019"),
         ran5=[R('ZTE', 'not_disclosed', 'https://www.zte.com.cn/global/about/news/20190712e1.html',
                 "ZTE 5G end-to-end solution (wireless access and core) used for Slovakia's first 5G video call (12 Jul 2019); 5G commercial "
                 "contract signed 31 May 2019; no share wording")],
         ran4=[R('ZTE', 'all', 'https://www.lightreading.com/5g/amid-the-rubble-of-l-aquila-zte-tries-to-rebuild',
                 "SWAN 'relies solely on ZTE for its core and 1800MHz-based radio access networks' (Light Reading, 16 Nov 2018); basis: "
                 "1800 MHz RAN, 2018. Verified 2026-11-24")],
         gov=[], gov_dropped=[], gov_note='privately owned (SWAN Group); no state holder in the evidence',
         core=V('ZTE', 'https://www.lightreading.com/5g/amid-the-rubble-of-l-aquila-zte-tries-to-rebuild',
                "solely ZTE for the core (2018, 4G); ZTE's 2019 5G end-to-end solution included the core network"),
         first_contract=V('2019-05-31', 'https://www.zte.com.cn/global/about/news/20190712e1.html', 'SWAN Mobile and ZTE 5G commercial contract'),
         vendor_operates=ND()),
]
