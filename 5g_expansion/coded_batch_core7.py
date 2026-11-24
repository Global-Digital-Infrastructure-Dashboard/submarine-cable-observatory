"""Core-94 migration, batch core7 (Prof. Shen, 2026-11): Hungary, Croatia and Romania (9 operators) re-coded in the
expansion's three-file format, in-session on 2026-11-24, following the calibration batch (coded_batch_core1.py).

Inputs: the core panel (data/5g_operator_panel.csv) and its cached vendor/ownership searches (data/5g_searches.jsonl),
plus the migration searches mig|mktshare|<market>, mig|share|<id> and mig|ran|<id> (data/5g_expansion_searches.jsonl).
Government stakes re-express gov_stakes_core.py's per-holder rows. Hrvatski Telekom: only the German state via Deutsche
Telekom; the Croatian War Veterans' Fund is not a state holder (researcher decision 2026-11-23 after reading HT's 2025
annual report, pp. 8/19/29) and CERP's 1.9% is below 5%.
Share categories follow the user's rules (2026-11-23/24): a stated percentage maps 100% = all, >50% = most, 10-50% =
some, <10% = small; stated traffic/site/unit shares map by the same rule; 'sole'/'exclusive' -> all; the note states the
basis and date. Every share category and checked figure: 5g_expansion/verify_2026-11-24_core7.csv.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

register(domains={
    'company': ['telekom.hu', 'yettel.hu', 'one.hu', '4ig.hu', 't.ht.hr', 'hrvatskitelekom.hr', 'ericssonnikolatesla.com',
                'datocms-assets.com', 'report.telekom.com', 'a1.com', 'eand.com'],
    'government': ['nmhh.hu', 'trade.gov', 'ancom.ro'],
    'research_industry_group': ['eizg.hr'],
    'news': ['rcrwireless.com', 'seenews.com', 'romania-insider.com', 'telecomlead.com'],
}, overrides={
    # Digi's own annual report hosted on the Bucharest Stock Exchange
    'https://www.bvb.ro/infocont/infocont26/DIGI_20260430222641_Digi-Communications-N-V---2025-Annual-Report.pdf': 'company',
})

# ------------------------------------------------------------------ shared sources
NMHH = 'https://nmhh.hu/cikk/261749/Mobilpiaci_jelentes__2026_I_felev'
NMHH_NOTE = ("NMHH, Mobilpiaci jelentés 2026 I. félév (13 Nov 2026), Table 15: market shares by number of subscriptions "
             "carrying voice calls, 2026 Q2: Magyar Telekom 45.4, One 28.4, Yettel 24.8, others 1.5 (verified 2026-11-24; the "
             "market-level search's 46/28/25 is the year-end-2025 Telecompaper rounding)")
EIZG = 'https://www.eizg.hr/userdocsimages/publikacije/serijske-publikacije/sector-analyses/sa_telecommunications_2025.pdf'
EIZG_NOTE = ("Economic Institute Zagreb, 'Telecommunications 2025' (23 Jan 2026), citing HAKOM data: shares of users of mobile "
             "telephone services, Q4 2024: HT 44.4, A1 34.1, Telemach 21.5 (total 4,717,531 users; M2M treatment not stated). "
             "UNVERIFIED: the PDF failed the TLS handshake on 2026-11-24, so the period label is the search's; HAKOM's own reports "
             "give only revenue shares (2024: HT 46, A1 33, Telemach 21)")
ANCOM = 'https://www.ancom.ro/en/about-us/media-en/press-releases/over-7-million-fixed-internet-connections-by-the-end-of-2025/'
ANCOM_NOTE = ("ANCOM press release on end-2025 statistics: shares of active mobile SIM cards, approximately Orange 34, Digi 34, "
              "Vodafone 24 (22.8 million SIM cards; M2M treatment not stated). UNVERIFIED: ancom.ro failed the TLS handshake on "
              "2026-11-24, so the figures and period are the search's. ANCOM's end-2024 release gives Orange 35, Digi 28, Vodafone 25; "
              "by subscribers (contracts) Digi leads with 75%")
DT_AR = 'https://report.telekom.com/annual-report-2025/_assets/downloads/sha-to-our-shareholders-dtag-ar25.pdf'
ORANGE_URD = 'https://assets.orange.com/medias/domain12751/media101922/576636-wexkleg98s-75.pdf'
A1_AR = 'https://a1.com/wp-content/uploads/sites/6/2026/03/A1-Telekom-Austria-Group-Annual-financial-report-2025.pdf'
VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
EAND_PPF = 'https://www.datocms-assets.com/56100/1771365178-fr39_20260217_eand_ppf_telecom_group_fy2025_annual_accounts_public.pdf'
TRADE_HU = 'https://www.trade.gov/market-intelligence/hungary-ict-5g-development'
TRADE_HU_CCG = 'https://www.trade.gov/country-commercial-guides/hungary-information-and-communication-technology'
LR_HUAWEI_2020 = 'https://www.lightreading.com/5g/europe-s-dependence-on-huawei-laid-bare-in-new-study'
LR_RO_BAN = 'https://www.lightreading.com/5g/vodafone-orange-face-5g-rip-and-replace-as-romania-bans-huawei'
LR_RO_SHARING = 'https://www.lightreading.com/open-ran/open-ran-sharing-is-the-next-possible-blow-to-kit-vendors'
LR_SPRING6 = 'https://www.lightreading.com/open-ran/vodafone-spring-6-lands-with-a-whimper-for-ericsson-and-samsung'
LR_ORANGE_BOSS = 'https://www.lightreading.com/5g/orange-europe-boss-well-stick-with-huawei-unless-it-is-banned/d/d-id/772568?_mc=RSS_LR_EDT'
LR_ORANGE_ORAN = 'https://www.lightreading.com/open-ran/huawei-likely-loser-in-orange-open-ran-plan/d/d-id/769012'
HT_RAN_2024 = 'https://www.t.ht.hr/en/investor-relations/investor-news/7204/Hrvatski-Telekom-and-Ericsson-Nikola-Tesla-continue-to-cooperate-in-the-5G-radio-network-segment.html'
ENT_A1_2026 = 'https://ericssonnikolatesla.com/en/news/a1-hrvatska-and-ericsson-nikola-tesla-continue-to-cooperate-in-the-radio-network-segment/'
ENT_A1_2021 = 'https://ericssonnikolatesla.com/en/news/20210331-agreement/'
RO_DEADLINE = 'deadline 2028 (RAN, seven years under Law 163/2021 as read by Strand Consult; core 2026)'


def dt_gov(chain, factor_note):
    return [G('Germany', 'Federal Republic of Germany', 'government_ministry', 14.1, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
              factor_note, chain=chain),
            G('Germany', 'KfW', 'state_holding_company', 14.2, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
              "the annual report describes the Federal Republic as an indirect shareholder via KfW. " + factor_note, chain=chain)]


def orange_gov(chain, parent_pct):
    return [G('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_URD,
              '21.04% of voting rights (Orange 2025 Universal Registration Document)', parent_pct=parent_pct, chain=chain),
            G('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_URD,
              '8.00% of voting rights; the filing groups it with the French State (22.95% in concert)', parent_pct=parent_pct, chain=chain)]


def obag_gov(chain, parent_pct=None):
    return [G('Austria', 'Österreichische Beteiligungs AG (ÖBAG)', 'state_holding_company', 28.42, 'Telekom Austria AG', 'via_parent',
              '2025-12-31', A1_AR, 'held for the Republic of Austria; América Móvil B.V. holds 60.94%', parent_pct=parent_pct, chain=chain)]


def eand_ppf_gov():
    return [G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 50.0,
              'e& PPF Telecom Group B.V.', 'via_parent', '2025-12-31', EAND_PPF,
              '50% plus one share; the accounts name the UAE Federal Government as ultimate controlling party',
              chain='e& PPF Telecom Group B.V. -> PPF TMT Bidco 1 N.V. 100% -> Yettel Magyarország (Bidco\'s percentage not stated)')]


OPERATORS = [
    # ------------------------------------------------------------------ Hungary
    dict(region='Central Asia & Eastern Europe', country='Hungary', operator_name='Magyar Telekom', core_operator_id='HU-magyar-telekom',
         share=V(45.4, NMHH, NMHH_NOTE, 2026),
         launch=V(2020, 'https://www.telekom.hu/about_us/press_room/press_releases/2020/april_9',
                  "commercial 5G from 9 Apr 2020 with Ericsson base stations (matches the discovery date); NMHH calls it the second Hungarian "
                  "operator after Vodafone"),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.telekom.hu/about_us/press_room/press_releases/2020/april_9',
                 "Ericsson supplied the 5G base stations at launch (9 Apr 2020) and Ericsson Radio System with spectrum sharing in Budapest "
                 "(20 Nov 2020); no sole-supplier wording. Magyar Telekom says its full supplier list is confidential")],
         ran4=[R('Ericsson', 'not_disclosed', TRADE_HU, "US ITA: Magyar Telekom 'worked with Ericsson on the construction of its 4G network'")],
         ran4_note='Huawei appears only for the optical (transport) network and 5G tests, not as a RAN supplier',
         gov=dt_gov('Deutsche Telekom AG ~65.78% indirect of Magyar Telekom (itself listed on the Budapest Stock Exchange)', ''),
         gov_dropped=[],
         core=V('Mavenir', 'https://www.rcrwireless.com/20221117/featured/magyar-telekom-picks-mavenirs-5g-packet-core',
                'converged 2G-5G packet core (NSA and SA), selected Nov 2022'),
         first_contract=ND('Ericsson 5G deployment by Apr 2020; contract date not found'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Hungary', operator_name='Yettel Magyarország', core_operator_id='HU-yettel-magyarorszag',
         name_note='formerly Telenor Hungary',
         share=V(24.8, NMHH, NMHH_NOTE, 2026),
         launch=V(2020, 'https://en.yettel.hu/press/press-release/30-years-after-the-launch-of-the-first-gsm-service-you-can-use-mobile-internet-to-surf-the-web-at-home',
                  "Yettel's own release says commercial 5G launched in 2020 (no date); DISAGREES with the discovery list's 2021, which cited "
                  "a Telenor 200-base-station release; 5G SA followed in Nov 2023"),
         ran5=[R('Nokia', 'not_disclosed', TRADE_HU_CCG, "US ITA: Nokia and Ericsson are the 'main equipment providers for Yettel's network "
                 "modernization in Hungary' (with CETIN Hungary); no split by vendor or generation"),
               R('Ericsson', 'not_disclosed', TRADE_HU_CCG, 'same source; no split by vendor or generation')],
         ran5_note="ZTE technology appears only in Telenor's May 2019 Győr 5G pilot (not coded)",
         ran4=[], ran4_note='the ITA guide does not split the Nokia/Ericsson modernisation by generation, so no 4G vendor is coded',
         gov=eand_ppf_gov(), gov_dropped=[],
         gov_note="PPF's side of the partnership is privately held (Kellner family)",
         core=ND('5G SA uses a 5G core; vendor not named'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Hungary', operator_name='One Magyarország', core_operator_id='HU-one-magyarorszag',
         name_note='formerly Vodafone Hungary (4iG acquisition 2023)',
         share=V(28.4, NMHH, NMHH_NOTE, 2026),
         launch=V(2019, TRADE_HU, "Vodafone Hungary launched commercial 5G in Oct 2019 'in partnership with Huawei' (discovery list: 7 Oct 2019)"),
         ran5=[R('Huawei', 'not_disclosed', TRADE_HU, "Vodafone Hungary's Oct 2019 commercial 5G launch was 'in partnership with Huawei'; "
                 "no share wording")],
         ran4=[R('Huawei', 'all', LR_HUAWEI_2020, "basis: RAN equipment, Strand Consult via Light Reading (30 Jun 2020): 'Vodafone is "
                 "100% reliant on Huawei' in six markets including Hungary (the study concerns 4G RAN). Verified 2026-11-24")],
         gov=[G('Hungary', 'Corvinus Nemzetközi Befektetési Zrt.', 'state_holding_company', 37.9, '4iG Távközlési Holding Zrt.', 'via_parent',
                '2026-03-31', 'https://www.4ig.hu/sw/static/file/4iG_consolidated_report_2026_Q1_EN.pdf',
                "the report names Corvinus as the vehicle through which the Hungarian state holds the stake; 4iG Plc holds 62.1%",
                parent_pct=100.0)],
         gov_dropped=[], gov_note='no state holder of 4iG Plc itself (Jászai-controlled; Rheinmetall 25.12%)',
         core=ND("DISAGREES with the core panel (Ericsson; Huawei), which rests only on an engineer's LinkedIn profile, not cited here"),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Croatia
    dict(region='Central Asia & Eastern Europe', country='Croatia', operator_name='Hrvatski Telekom', core_operator_id='HR-hrvatski-telekom',
         name_note='brands Hrvatski Telekom, bonbon',
         share=V(44.4, EIZG, EIZG_NOTE, 2024),
         launch=V(2020, 'https://www.t.ht.hr/en/Press/press-releases/5339/Hrvatski-Telekom-the-first-to-launch-commercial-5G-network.html',
                  'commercial 5G from 29 Oct 2020 (the discovery list has no date)'),
         ran5=[R('Ericsson', 'all', HT_RAN_2024, "basis: RAN contract, HT investor news (23 Jan 2024): Ericsson Nikola Tesla 'will be the "
                 "exclusive supplier of the radio part of Hrvatski Telekom's mobile network (RAN) until the end of 2027'; earlier selected as "
                 "'sole supplier of 5G RAN' to 2024 (Jun 2020). Verified 2026-11-24")],
         ran4=[R('Ericsson', 'all', HT_RAN_2024, "same agreement covers the radio part of the whole mobile network, not only 5G; Ericsson "
                 "modernised HT's radio network from 2018. Verified 2026-11-24")],
         gov=dt_gov("Deutsche Telekom AG -> DT Europe Holding GmbH -> DT Europe Holding B.V. -> DT Europe B.V. (each 100%, HT 2025 annual "
                    "report p.8) -> 54.6% of HT", ''),
         gov_dropped=['CERP (Restructuring and Sale Center) / Republic of Croatia 1.9% of Hrvatski Telekom (2025-12-31; board seat not checked)'],
         gov_note=("Croatian War Veterans' Fund 7.1% NOT a state holder (researcher decision 2026-11-23): HT's 2025 annual report "
                   "(pp. 8, 19, 29) names it without any state link while attributing CERP's 1.9% to the Republic of Croatia"),
         core=V('Ericsson', 'https://www.t.ht.hr/en/Press/press-releases/7129/Hrvatski-Telekom-and-Crnogorski-Telekom-contract-Ericsson-Nikola-Tesla-for-the-deployment-of-Ericsson-s-dual-mode-5G-Core-for-it.html',
                'Ericsson cloud-native dual-mode 4G/5G core, contracted with Ericsson Nikola Tesla (Dec 2023)'),
         first_contract=V('2020-06-24', 'https://telecomlead.com/telecom-equipment/hrvatski-telekom-selects-ericsson-for-5g-ran-products-95677',
                          'Ericsson Nikola Tesla selected as sole 5G RAN supplier to 2024 (announcement date)'),
         vendor_operates=ND('network construction and maintenance moved from Ericsson Nikola Tesla Servisi to HT Services on 1 Jan 2024 '
                            '(an organisational transfer, not vendor-managed operations)')),
    dict(region='Central Asia & Eastern Europe', country='Croatia', operator_name='A1 Hrvatska', core_operator_id='HR-a1-hrvatska',
         share=V(34.1, EIZG, EIZG_NOTE, 2024),
         launch=ND("August 2021 per the migration search, from an industry directory only (Powertec, not cited); the discovery "
                   "list has no date"),
         ran5=[R('Ericsson', 'not_disclosed', ENT_A1_2026, "basis: RAN contract, Ericsson Nikola Tesla (27 May 2026): ENT 'will remain the exclusive "
                 "supplier of the radio part of A1 Hrvatska's mobile network' for five years; the 2021 agreement had no exclusivity wording. "
                 "Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]")],
         ran4=[R('Ericsson', 'all', ENT_A1_2026, "same agreement (radio part of the whole mobile network); ENT has supplied A1's radio network "
                 "since the operator entered the market (31 Mar 2021 release). Verified 2026-11-24")],
         gov=obag_gov('A1 Hrvatska d.o.o. wholly owned by A1 Telekom Austria AG (100.0%, 31 Dec 2025)', parent_pct=100.0),
         gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/news/2021/9/a1-opts-for-ericsson-5g-core-in-croatia-and-bulgaria',
                'cloud-native dual-mode 5G Core for Croatia (1 Sep 2021)'),
         first_contract=V('2021-03-31', ENT_A1_2021, "five-year frame agreement with Ericsson Nikola Tesla, 'continuation of strategic "
                          "cooperation in the 5G area'; signing date as announced"),
         vendor_operates=ND('Ericsson Nikola Tesla also provides maintenance services (2026 agreement); not network operation')),
    dict(region='Central Asia & Eastern Europe', country='Croatia', operator_name='Telemach Hrvatska', core_operator_id='HR-telemach-hrvatska',
         share=V(21.5, EIZG, EIZG_NOTE, 2024),
         launch=ND('June 2022 per an industry directory (Powertec, not cited); in Aug 2021 Telemach said 5G would start in Osijek'),
         ran5=[], ran5_note='5G RAN vendor not named in any source; Ericsson Nikola Tesla worked on its core and transport (Q1 2021), not RAN',
         ran4=[], ran4_note='4G RAN vendor not named',
         gov=[], gov_dropped=[], gov_note='United Group (BC Partners ~56%, management 42%); EBRD 2% is a multilateral bank, not a state holder',
         core=V('Nokia', 'https://seenews.com/news/united-group-picks-nokia-to-upgrade-core-networks-in-bulgaria-croatia-slovenia-750552',
                'United Group selected Nokia as core-network supplier for Bulgaria, Croatia and Slovenia (11 Aug 2021): 3G/4G first, then 5G NSA and SA'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Romania
    dict(region='Central Asia & Eastern Europe', country='Romania', operator_name='Orange Romania', core_operator_id='RO-orange-romania',
         share=V(34.0, ANCOM, ANCOM_NOTE, 2025),
         launch=V(2019, 'https://www.romania-insider.com/business/orange-romania-5g-services-november-2019',
                  "commercial 5G from 5 Nov 2019 in Bucharest, Cluj-Napoca and Iași; DISAGREES with the discovery list's May 2019"),
         ran5=[R('Ericsson', 'not_disclosed', LR_ORANGE_ORAN, "Light Reading (2020): in Romania Orange 'has flagged a 5G deal with Ericsson' "
                 "(table: legacy Huawei, 5G deal Ericsson). Verified 2026-11-24"),
               R('Huawei', 'not_disclosed', LR_RO_BAN, "Orange Romania (Mar 2024): its network 'uses equipment produced by several suppliers, "
                 "including Huawei', to be replaced within the legal terms. Verified 2026-11-24"),
               R('Samsung', 'not_disclosed', LR_RO_SHARING, "basis: sites, Light Reading (28 May 2024): Samsung is 'the sole RAN vendor at "
                 "multiple Romanian sites shared by Orange and Vodafone' (2G/4G/5G), an open RAN 'cluster' of sites; no share of the network")],
         ran4=[R('Huawei', 'all', LR_ORANGE_BOSS, "basis: 4G RAN, Strand Consult data via Light Reading (2021): in Romania Huawei 'was Orange's "
                 "sole 4G RAN vendor'. Verified 2026-11-24")],
         gov=[G('Romania', 'Romanian Ministry of Research, Innovation and Digitalization', 'government_ministry', 20.0, 'Orange Romania', 'direct',
                '2025-12-31', 'https://www.orange.com/en/press-release/orange-announces-the-completion-of-the-merger-between-orange-romania-sa-and-orange-romania-communications-sa-as-of-june-1-2024-233906',
                "80/20 split after the 1 Jun 2024 merger with Orange Romania Communications; recoded 2026-11-23 under Prof. Shen's rule "
                "(Orange Romania was the lead example for summing across states)"),
              *orange_gov('Orange S.A. 80% of Orange Romania', 80.0)],
         gov_dropped=[],
         core=ND('commercial core vendor not named; Ericsson vEPC and Nokia 5G core appear only in the Bucharest 5G Labs testbed'),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Huawei', 'Samsung', '2024-05-28', 'not_confirmed; ' + RO_DEADLINE, LR_RO_SHARING,
                     "at sites shared with Vodafone only: Samsung 'is replacing the out-of-favor Huawei, which previously supplied all the 4G kit "
                     "for Orange and Vodafone' (open RAN cluster, also 2G/5G). Verified 2026-11-24")]),
    dict(region='Central Asia & Eastern Europe', country='Romania', operator_name='Vodafone Romania', core_operator_id='RO-vodafone-romania',
         share=V(24.0, ANCOM, ANCOM_NOTE, 2025),
         launch=V(2019, LR_RO_BAN, "Light Reading (4 Mar 2024): 'Vodafone reportedly launched its first 5G services in 2019'; the discovery "
                  "list gives May 2019. Verified 2026-11-24"),
         ran5=[R('Ericsson', 'most', LR_RO_BAN, "basis: urban sites, Light Reading (4 Mar 2024): 'Ericsson will equip 80% of urban sites' "
                 "(six-year 5G RAN deal, Feb 2024). Verified 2026-11-24"),
               R('Samsung', 'some', LR_RO_BAN, "basis: urban sites, same article: 'Samsung addressing the other 20%' (open RAN, 90+ sites in 20 "
                 "cities). Verified 2026-11-24")],
         ran5_note="the 2019 launch network's vendor is not stated; Huawei was the incumbent but no source names it for 5G",
         ran4=[R('Huawei', 'all', LR_SPRING6, "basis: RAN, Light Reading (14 Oct 2025): 'In Romania, Vodafone had been totally reliant on "
                 "Huawei'; Strand Consult (Jun 2020) also gives 100%. Being replaced. Verified 2026-11-24")],
         gov=[G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 17.005026, 'Vodafone Group Plc',
                'via_parent', '2026-03-31', VODAFONE_AR,
                "the Vodafone filing names e& but does not call it state-owned; e&'s 2025 integrated annual report gives the Emirates "
                "Investment Authority 60%, ultimately controlled by the UAE Federal Government",
                link_url=E_AND_AR, chain='Vodafone Group Plc -> Vodafone România S.A.; percentage not stated (group subsidiaries 100% unless indicated)')],
         gov_dropped=['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)'],
         core=ND('core vendor not named; Huawei core replacement deadline 2026 under the Romanian law (Strand Consult)'),
         first_contract=ND('Ericsson 5G RAN partnership announced 12 Feb 2024, after the 2019 launch; first 5G contract not found'),
         vendor_operates=ND(),
         switches=[S('RAN', '4G/5G', 'Huawei', 'Ericsson', '2024-02-12', 'not_confirmed; ' + RO_DEADLINE, LR_SPRING6,
                     "'Ericsson has also been replacing Huawei across 80% of Vodafone Romania's urban footprint' (Oct 2025); partnership "
                     "announced 12 Feb 2024. Verified 2026-11-24"),
                   S('RAN', '4G/5G', 'Huawei', 'Samsung', '2024-02', 'not_confirmed; ' + RO_DEADLINE, LR_RO_BAN,
                     "Samsung takes the other 20% of urban sites and 'will provide not just 5G but other mobile generations, implying Huawei "
                     "will be completely removed from these sites'. Verified 2026-11-24")]),
    dict(region='Central Asia & Eastern Europe', country='Romania', operator_name='Digi Romania', core_operator_id='RO-rcs-rds',
         name_note='core panel name RCS & RDS (legal entity RCS & RDS S.A.; brand Digi)',
         share=V(34.0, ANCOM, ANCOM_NOTE, 2025),
         launch=ND('ANCOM confirms 5G connections but no Digi launch date; the discovery list has none'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.bvb.ro/infocont/infocont26/DIGI_20260430222641_Digi-Communications-N-V---2025-Annual-Report.pdf',
                 "Digi 2025 annual report: the Romanian mobile network is based on Nokia and Ericsson equipment; no split by vendor, element or generation"),
               R('Ericsson', 'not_disclosed', 'https://www.bvb.ro/infocont/infocont26/DIGI_20260430222641_Digi-Communications-N-V---2025-Annual-Report.pdf',
                 'same source')],
         ran5_note="Huawei was in Digi's 2021 supplier list only; no removal is stated",
         ran4=[], ran4_note='the annual report does not split mobile suppliers by generation',
         gov=[], gov_dropped=[], gov_note='controlled by Zoltán Teszári (60.1% of Digi Communications N.V.); no state holder',
         core=ND(), first_contract=ND(), vendor_operates=ND()),
]
