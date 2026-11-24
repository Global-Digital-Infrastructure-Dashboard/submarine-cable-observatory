"""Core-94 migration, calibration batch (Prof. Shen, 2026-11): Germany, France and the United Kingdom (11 operators)
re-coded in the expansion's three-file format, in-session on 2026-11-24.

Inputs: the core panel (data/5g_operator_panel.csv) and its cached vendor/ownership searches (data/5g_searches.jsonl),
plus the migration searches mig|share|<id> and mig|ran|<id> (data/5g_expansion_searches.jsonl). Government stakes
re-express gov_stakes_core.py's per-holder rows. Share categories follow the user's 2026-11-23 rule: a stated
percentage maps 100% = all, >50% = most, 10-50% = some, <10% = small (the % and source in the note); otherwise the
source's own wording or not_disclosed. Every share category and computed figure was checked against the primary page
at coding time (5g_expansion/verify_2026-11-24_core1.csv).
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

register(domains={
    'company': ['telekom.com', 'telefonica.de', 'telefonica.com', 'vodafone.com', 'rakuten.com', '1und1.de', '1und1.ag',
                'static.s-sfr.fr', 'bouygues.com', 'iliad.fr', 'vodafonethree.com', 'virginmediao2.co.uk'],
    'government': ['bundesnetzagentur.de', 'arcep.fr', 'researchbriefings.files.parliament.uk'],
    'news': ['the-mobile-network.com', 'theregister.com', '5gradar.com', 'bbc.co.uk', 'techradar.com'],
})

DT_AR = 'https://report.telekom.com/annual-report-2025/_assets/downloads/sha-to-our-shareholders-dtag-ar25.pdf'
VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
TEF_CGR = 'https://www.telefonica.com/en/wp-content/uploads/sites/5/2026/02/Annual-Report-Corporate-Gobernance-2025.pdf'
ORANGE_XLSX = 'https://assets.orange.com/pm_12751_545_545865-jr7yvi3osw.xlsx'
BMI = 'https://www.bmi.bund.de/SharedDocs/pressemitteilungen/EN/2024/07/5g-en.html'
LR_DASHES = 'https://www.lightreading.com/ai-machine-learning/deutsche-telekom-dashes-vendor-hopes-for-big-mobile-uplink-spending'
LR_NOTBANNING = 'https://www.lightreading.com/5g/not-banning-huawei-just-got-hard-for-germany-to-explain'
LR_TOOTHLESS = 'https://www.lightreading.com/5g/germany-still-looks-toothless-on-huawei-as-telcos-hedge-bets'
LR_EXIT = 'https://www.lightreading.com/5g/europe-is-showing-huawei-the-exit'
LR_UNLIKELY = 'https://www.lightreading.com/5g/france-unlikely-to-ban-huawei-but-will-encourage-operators-to-steer-clear'
LR_BELLE = 'https://www.lightreading.com/5g/huawei-belle-poque-in-france-to-end-in-2028'
TT_PHASE = 'https://totaltele.com/french-operators-begin-urban-phase-out-of-huawei-tech/'
LR_DUOPOLY = 'https://www.lightreading.com/business-management/huawei-ban-risks-turning-uk-into-nordic-duopoly'
LR_AVOID = 'https://www.lightreading.com/5g/huawei-avoidance-strategy-is-paying-off-for-uk-s-o2'
UK_SHARES = 'https://researchbriefings.files.parliament.uk/documents/CDP-2023-0187/CDP-2023-0187.pdf'
UK_SHARES_NOTE = ("Ofcom Technology Tracker 2023, as cited in a House of Commons Library briefing (CDP-2023-0187): share of UK "
                  "consumers by network, including MVNOs on that network (EE 31, O2 35, Vodafone 19, Three 11). UNVERIFIED: the "
                  "briefing PDF returned 403; the figures come from the search answer (exp key mig|share|GB-vodafonethree)")
BNETZA = 'https://www.bundesnetzagentur.de/DE/Fachthemen/Telekommunikation/Marktdaten/Mobilfunkteilnehmer/start.html'
BNETZA_NOTE = ("computed from the Bundesnetzagentur's registered SIM profiles by network operator, Q3 2026 (thousands): Telekom 78,745; "
               "Vodafone 101,818; Telefónica 35,362; 1&1 14,974; total 230,899. Basis: registered SIM profiles, including second and "
               "reserve devices and M2M (the regulator says this exceeds active use; 106.4m active SIMs excl. M2M at end-2025 have no "
               "operator split). Counts verified on the regulator page 2026-11-24. Q4 2025 shares: Telekom 34.74, Vodafone 42.01, "
               "Telefónica 16.40, 1&1 6.84")
ARCEP_NOTE = 'ARCEP publishes total SIM cards only (84.9m at end-2025), not by operator'
DT_DROPPED = []
VOD_DROPPED = ['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)']


def dt_gov(chain, parent_pct=None, note=''):
    return [G('Germany', 'Federal Republic of Germany', 'government_ministry', 14.1, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
              note, parent_pct=parent_pct, chain=chain),
            G('Germany', 'KfW', 'state_holding_company', 14.2, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
              "the annual report describes the Federal Republic as an indirect shareholder via KfW. " + note, parent_pct=parent_pct, chain=chain)]


def vod_gov(chain='', parent_pct=None, note=''):
    return [G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 17.005026, 'Vodafone Group Plc',
              'via_parent', '2026-03-31', VODAFONE_AR,
              "Vodafone names e& without calling it state-owned; e&'s 2025 integrated report gives the Emirates Investment Authority 60%, "
              "ultimately controlled by the UAE Federal Government. " + note, link_url=E_AND_AR, parent_pct=parent_pct, chain=chain)]


def tef_gov(chain='', parent_pct=None):
    return [G('Spain', 'Sociedad Estatal de Participaciones Industriales (SEPI)', 'state_holding_company', 10.0, 'Telefónica, S.A.', 'via_parent',
              '2025-12-31', TEF_CGR, 'state link from data/state_holders.csv', link='reference_list', parent_pct=parent_pct, chain=chain),
            G('Saudi Arabia', 'Public Investment Fund', 'sovereign_wealth_fund', 9.97, 'Telefónica, S.A.', 'via_parent', '2025-12-31', TEF_CGR,
              'state link from data/state_holders.csv', link='reference_list', parent_pct=parent_pct, chain=chain)]


def orange_gov(basis='direct', chain='', parent_pct=None):
    kw = dict(chain=chain, parent_pct=parent_pct) if basis == 'via_parent' else {}
    return [G('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', basis, '2025-12-31', ORANGE_XLSX, '21.04% of voting rights', **kw),
            G('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', basis, '2025-12-31', ORANGE_XLSX,
              "8.00% of voting rights; Orange's file groups it with the French State as the public sector", **kw)]


OPERATORS = [
    # ------------------------------------------------------------------ Germany
    dict(region='Western Europe', country='Germany', operator_name='Telekom Deutschland', core_operator_id='DE-telekom-deutschland',
         share=V(34.10, BNETZA, BNETZA_NOTE, 2026),
         launch=V(2019, 'https://www.telekom.com/en/about-us/company-history', 'exact date not stated; matches the discovery list (2019)'),
         ran5=[R('Huawei', 'not_disclosed', LR_DASHES, "about 67%: 'Huawei has accounted for roughly two-thirds of the operator's RAN in Germany' "
                 "(basis: share of the RAN, unit not stated; Light Reading, 7 Oct 2026; not generation-specific). Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Ericsson', 'not_disclosed', LR_DASHES, "about 33%: 'Ericsson supplied the remaining one-third' (basis: share of the RAN, unit not stated; same article, 7 Oct 2026). Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Nokia', 'small', 'https://www.lightreading.com/5g/europe-s-love-of-huawei-is-crushing-ericsson-and-nokia',
                 "replacing Huawei at about 3,000 5G sites, 'roughly 8% of the RAN total' per Deutsche Telekom's capital markets day data (basis: sites; Light Reading, 29 Jul 2025); "
                 "1,000 sites live in 2025, more than 3,000 O-RAN sites targeted by 2027. DISPUTED: a Nov 2024 Light Reading report "
                 "reads the same slides as 'more than 10%' of the footprint; coded on the 8% figure. Verified 2026-11-24"),
               R('Fujitsu', 'not_disclosed', 'https://www.telekom.com/en/newsroom/latest-updates/media-information/2023/2/first-commercial-deployment-of-open-ran-with-multiple-partners',
                 'O-RAN radio units in the Neubrandenburg open RAN deployment (27 Feb 2023)')],
         ran4=[R('Huawei', 'most', LR_TOOTHLESS, "65%: Strand Consult research 'supplied 65% of Deutsche Telekom's 4G RAN' (basis: 4G RAN, unit not stated; Light Reading, 20 May 2024); the all-generation figure is about 67% (7 Oct 2026). Verified 2026-11-24"),
               R('Ericsson', 'some', LR_DASHES, "about 33%: 'Ericsson supplied the remaining one-third' of the RAN (basis: share of the RAN, all generations; Light Reading, 7 Oct 2026); LR_TOOTHLESS: 'Telekom built 4G and 5G with Huawei and Ericsson' [decision 2026-11-24: all-generation share, coded to 4G only]")],
         gov=dt_gov('Deutsche Telekom AG -> Telekom Deutschland GmbH; percentage not stated (the core panel treats it as wholly owned)'),
         gov_dropped=DT_DROPPED,
         core=ND("Huawei was phased out of the 5G core by Q2 2024 and no ZTE is used, but the replacement core vendor is not named"),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Nokia', 'Ericsson', '2018', 'not_confirmed', 'https://www.lightreading.com/5g/the-kill-huawei-mission-is-being-jeopardized-by-germany',
                     "Nokia 'lost its German RAN contract with Deutsche Telekom to Ericsson in 2018' (pre-5G era; Nokia had about a third of the RAN)"),
                   S('RAN', '5G', 'Huawei', 'Nokia', '2024-11-27', 'not_confirmed', 'https://www.lightreading.com/5g/nokia-to-finally-boot-huawei-out-of-deutsche-telekom-5g-sites',
                     'about 3,000 sites; 1,000 live in 2025, target moved to 2027'),
                   S('core', '5G', 'Huawei', 'not_disclosed', '2024', '2024-06-30', 'https://report.telekom.com/interim-report-q2-2024/management-report/risks-and-opportunities.html',
                     "Telekom reports Huawei phased out of its 5G core by Q2 2024 (the BMI contract deadline is 2026-12-31); replacement vendor not named")]),
    dict(region='Western Europe', country='Germany', operator_name='Vodafone Germany', core_operator_id='DE-vodafone', name_note='core panel name Vodafone (Vodafone GmbH)',
         share=V(44.10, BNETZA, BNETZA_NOTE, 2026),
         launch=V(2019, 'https://www.ericsson.com/en/about-us/company-facts/ericsson-worldwide/germany/5g-timeline', 'July 2019 (Reuters dates it 16 Jul 2019)'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.lightreading.com/open-ran/vodafone-spring-6-lands-with-a-whimper-for-ericsson-and-samsung',
                 "55%: Vodafone's roughly 26,000 existing German RAN sites 'divided between Huawei, with a 55% share, and Ericsson, with the "
                 "rest' (basis: existing RAN sites; Strand Consult via Light Reading, 14 Oct 2025; not generation-specific). The search's '59% of Vodafone's 5G sites' is "
                 "Strand Consult's figure for Germany's 5G sites nationally, so it is not used. Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Ericsson', 'not_disclosed', 'https://www.lightreading.com/open-ran/vodafone-spring-6-lands-with-a-whimper-for-ericsson-and-samsung',
                 "about 45%: 'Ericsson, with the rest' after Huawei's 55% (basis: existing RAN sites; 14 Oct 2025). Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Samsung', 'not_disclosed', 'https://www.vodafone.com/news/newsroom/technology/vodafone-advances-future-ready-radio-access-network',
                 "Open RAN at 'thousands of sites' in Germany (announced 14 Oct 2025); first site live in Hannover")],
         ran4=[R('Huawei', 'most', LR_TOOTHLESS, "55%: Strand Consult, Huawei 'supplied ... 55% of Vodafone's' 4G RAN (basis: 4G RAN, unit not stated; Light Reading, 20 May 2024). Verified 2026-11-24"),
               R('Ericsson', 'some', 'https://www.lightreading.com/open-ran/vodafone-spring-6-lands-with-a-whimper-for-ericsson-and-samsung', "about 45%: 'Ericsson, with the rest' of Vodafone's roughly 26,000 existing German RAN sites (basis: existing RAN sites, all generations; Strand Consult via Light Reading, 14 Oct 2025) [decision 2026-11-24: all-generation share, coded to 4G only]")],
         gov=vod_gov(chain="Vodafone Group Plc -> Vodafone GmbH; the group's percentage is not published"),
         gov_dropped=VOD_DROPPED,
         core=ND('no current 5G core vendor named; Nokia replaced Huawei in parts of the core (reported 2019)'),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('core', '4G', 'Huawei', 'Nokia', '2019-02-07', 'not_confirmed', 'https://www.lightreading.com/5g/nokia-replacing-huawei-in-vodafone-s-german-core',
                     'Nokia won a tender about two years earlier to replace Huawei in parts of the German core; some Huawei components remained')]),
    dict(region='Western Europe', country='Germany', operator_name='Telefónica Germany', core_operator_id='DE-telefonica-germany', name_note='brand O2',
         share=V(15.31, BNETZA, BNETZA_NOTE + '; the 33.1% in its annual report is mobile service revenue, not customers', 2026),
         launch=V(2020, 'https://www.telefonica.de/news/press-releases-telefonica-germany/2020/10/o2-switches-on-5g-network-not-later-than-2025-5g-will-be-supplied-all-over-germany.html',
                  'commercial 5G from 6 Oct 2020 (Munich, Berlin, Hamburg, Cologne, Frankfurt); matches the discovery list (2020-10)'),
         ran5=[R('Huawei', 'not_disclosed', LR_NOTBANNING, "about 50%: 'Its network is divided quite evenly between Huawei and Nokia' (basis: network, unit not stated; "
                 "Light Reading, 2 Oct 2026; not generation-specific). Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Nokia', 'not_disclosed', LR_NOTBANNING, "about 50%: same wording (basis: network, unit not stated; 2 Oct 2026); Nokia also signed a five-year RAN deal (DCD, Jul 2026). Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Ericsson', 'not_disclosed', 'https://www.telefonica.de/news/press-releases-telefonica-germany/2025/03/new-network-architecture-with-a-world-premiere-in-offenbach-germany-o2-telefonica-deploys-first-ericsson-cloud-ran-in-a-5g-standalone-network.html',
                 'Ericsson Cloud RAN in the 5G SA network in Offenbach (Mar 2025)')],
         ran4=[R('Huawei', 'some', LR_TOOTHLESS, "50%: Strand Consult, Huawei 'supplied ... 50% of Telefónica's' 4G RAN (basis: 4G RAN, unit not stated; Light Reading, 20 May 2024). Verified 2026-11-24"),
               R('Nokia', 'some', LR_NOTBANNING, "about 50%: 'Its network is divided quite evenly between Huawei and Nokia' (basis: network, all generations; Light Reading, 2 Oct 2026) [decision 2026-11-24: all-generation share, coded to 4G only]")],
         gov=tef_gov(chain='Telefónica, S.A. ~96.84% of Telefónica Deutschland', parent_pct=96.84),
         gov_dropped=[],
         core=V('Ericsson', 'https://www.telefonica.de/file/public/826/ANNUAL-REPORT-2025-EN-Telefonica-Deutschland-Holding-AG.pdf?attachment=1',
                "annual report 2025: 5G core 'almost exclusively' Ericsson; a Nokia 5G cloud core on AWS Outposts followed in Mar 2026"),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('core', '5G', 'Ericsson', 'Nokia', '2026-03', 'not_confirmed',
                     'https://www.telefonica.de/news/press-releases-telefonica-germany/2026/03/o2-telefonica-brings-5g-cloud-core-to-own-data-center-with-nokia-and-aws-outposts.html',
                     "Nokia 5G cloud core in Telefónica's own data centre on AWS Outposts; a Nokia document says Telefónica 'replaced Ericsson with "
                     "Nokia' (date not stated); extent of the replacement not stated")]),
    dict(region='Western Europe', country='Germany', operator_name='1&1', core_operator_id='DE-1-1-mobilfunk', name_note='core panel name 1&1 Mobilfunk',
         share=V(6.49, BNETZA, BNETZA_NOTE, 2026),
         launch=V(2023, 'https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/EN/2024/20240314_MoFu.html',
                  "own public mobile network since 8 Dec 2023 (Bundesnetzagentur). The regulator also says 1&1 put a 5G network into "
                  "operation for end-users in Dec 2022; the discovery list has no date"),
         ran5=[R('NEC', 'all', 'https://unternehmen.1und1.de/o-ran-mobilfunknetz/2024',
                 "basis: radio units (antennas) at every antenna site: 'An allen Antennenstandorten verbaut 1&1 Gigabitantennen von seinem Partner NEC' (1&1, 29 Mar 2024). Verified 2026-11-24"),
               R('Rakuten Symphony', 'not_disclosed', 'https://global.rakuten.com/corp/news/press/2023/1208_01.html',
                 'RAN software and network platform; Light Reading (Nov 2023) says 1&1 appears to have only one RAN software provider (Rakuten)')],
         ran5_note='CCI antennas and Mavenir/Altiostar software were also named at the Jan 2023 launch; not coded separately',
         ran4=[], ran4_note='no own 4G RAN found; 4G via Telefónica and Vodafone roaming',
         gov=[], gov_note='no state holder found (United Internet AG, private/listed)', gov_dropped=[],
         core=V('Mavenir', 'https://global.rakuten.com/corp/news/press/2023/1208_01.html', "Mavenir supplies 'all components in the core network' (8 Dec 2023)"),
         first_contract=ND(), vendor_operates=ND('Rakuten Symphony is general contractor and runs the orchestration platform; not stated as operating the network')),
    # ------------------------------------------------------------------ France
    dict(region='Western Europe', country='France', operator_name='Orange France', core_operator_id='FR-orange-france',
         share=V(30.3, 'https://assets.orange.com/medias/domain12751/media101746/523989-ffp7njes6v.pdf',
                 "Orange's own estimate, Q3 2025: share by mobile-customer volume, excluding SIM cards dedicated to connected "
                 "devices/M2M (exp key mig|mktshare|France); " + ARCEP_NOTE + ', so no regulator figure', 2025),
         launch=V(2020, 'https://en.arcep.fr/news/press-releases/view/n/5g-eng-161220.html',
                  "ARCEP: commercial 5G opened between late Nov and mid-Dec 2020, Orange among them; discovery list gives 2020-12-03"),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.lightreading.com/5g/eurobites-orange-france-goes-with-nokia-and-ericsson-for-5g-rollout',
                 'west and south-east regions of mainland France (31 Jan 2020); no percentage'),
               R('Ericsson', 'not_disclosed', 'https://www.lightreading.com/5g/eurobites-orange-france-goes-with-nokia-and-ericsson-for-5g-rollout',
                 'Île-de-France, north-east and south-west (31 Jan 2020); no percentage')],
         ran4=[R('Nokia', 'not_disclosed', LR_EXIT, "Orange 'already rel[ies] entirely on' Ericsson and Nokia (2020); Nokia's regions as for 5G"),
               R('Ericsson', 'not_disclosed', LR_EXIT, "same; Ericsson's regions as for 5G")],
         gov=orange_gov('direct'),
         gov_dropped=[],
         core=ND(), first_contract=ND('Nokia and Ericsson selected 31 Jan 2020 (announcement); signing date not stated'), vendor_operates=ND()),
    dict(region='Western Europe', country='France', operator_name='SFR', core_operator_id='FR-sfr',
         share=ND(ARCEP_NOTE),
         launch=V(2020, 'https://www.samenacouncil.org/samena_daily_news?news=88757', 'Nice, November 2020; matches the discovery list (2020-11)'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.datacenterdynamics.com/en/news/bouygues-telecom-and-sfr-to-take-legal-action-after-forced-huawei-removal/',
                 'Huawei involved in its 5G plans; being removed since 2021 (Nov 2026)'),
               R('Nokia', 'not_disclosed', 'https://www.lightreading.com/5g/huawei-belle-poque-in-france-to-end-in-2028', 'the non-Huawei RAN vendor; 5G share not stated')],
         ran4=[R('Huawei', 'most', LR_EXIT, "55%: SFR-Numericable 'uses Huawei across 55% of RAN sites, according to Strand Consult' (basis: RAN sites; Light Reading, 10 Sep 2020); AFP (via "
                 "Light Reading) says 'around 52%' of the network. Verified 2026-11-24"),
               R('Nokia', 'some', LR_BELLE, "about 45%: 'appears to have used Nokia in areas where Huawei is not its supplier' (basis: areas/sites not served by Huawei; Light Reading, 23 Jul 2020). Verified 2026-11-24")],
         gov=[], gov_note='no state holder found (Altice France / Next Alt, private)', gov_dropped=[],
         core=V('Nokia', 'https://static.s-sfr.fr/AlticeFrance/publications/Investors/Esg/2025/sfr-alticefrance-dpef-2024-en-250429.pdf',
                'Nokia supports the rollout of its latest-generation core including 5G SA (Altice France sustainability disclosure, Apr 2025)'),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Huawei', 'Nokia', '2021-03', 'not_confirmed', TT_PHASE,
                     "removal of Huawei 4G from dense areas, switching to Nokia (Mar 2021). UNVERIFIED: the article body could not be "
                     "retrieved. France does not renew Huawei authorisations, leaving operators until 2028 (Light Reading, 2020)")]),
    dict(region='Western Europe', country='France', operator_name='Bouygues Telecom', core_operator_id='FR-bouygues-telecom',
         share=V(22.7, 'https://www.bouygues.com/app/uploads/2025/11/bouygues_deu_2025_uk_web.pdf',
                 "Bouygues 2025 URD citing ARCEP data (5 Feb 2026): 18.6m mobile-plan customers of 82.3m SIMs excl. M2M; the share is "
                 "the company's own figure", 2025),
         launch=V(2020, 'https://www.bouygues.com/app/uploads/2020/11/press-release-bouygues-telecom-launches-its-5g-network-in-20-major-towns-and-cities.pdf',
                  '1 Dec 2020 in 20 towns and cities; matches the discovery list'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.bouygues.com/app/uploads/2025/11/bouygues_deu_2025_uk_web.pdf',
                 "standalone 5G network 'developed with Ericsson' (URD 2025); no share wording"),
               R('Huawei', 'not_disclosed', LR_EXIT, 'legacy Huawei; 3,000 Huawei antennas in dense areas to go by 2028')],
         ran4=[R('Huawei', 'some', LR_UNLIKELY, "about 50%: Huawei 'provides almost 50% of Bouygues Telecom's 4G RAN, with the remainder from "
                 "Ericsson' (basis: 4G RAN, unit not stated; AFP via Light Reading, 6 Jul 2020); Strand Consult gives 50% of RAN sites (10 Sep 2020). Verified 2026-11-24"),
               R('Ericsson', 'some', LR_UNLIKELY, "about 50%: 'the remainder from Ericsson' (basis: 4G RAN, unit not stated; 6 Jul 2020). Verified 2026-11-24")],
         gov=[], gov_note='no state holder found (Bouygues SA, listed; family-controlled)', gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/news/2022/6/end-to-end-ericsson-sa-5g-for-bouygues-telecom', 'end-to-end Ericsson SA 5G incl. dual-mode core (Jun 2022)'),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Huawei', 'Ericsson', '2021-03', 'deadline 2028', TT_PHASE,
                     "Huawei 4G removed from dense areas and replaced with Ericsson (Mar 2021). UNVERIFIED: article body not retrievable. "
                     "Light Reading (2020, verified) says Bouygues will dismantle 3,000 Huawei antennas in dense areas by 2028")]),
    dict(region='Western Europe', country='France', operator_name='Free Mobile', core_operator_id='FR-free-mobile',
         share=ND(ARCEP_NOTE + '; Free reports 15.7m French mobile-plan subscribers at end-2025, no share'),
         launch=V(2020, 'https://www.iliad.fr/media/CP_151220_Eng_5d4b2b84a5.pdf', '15 Dec 2020; matches the discovery list'),
         ran5=[R('Nokia', 'not_disclosed', LR_UNLIKELY, "'Iliad's Free has picked Nokia for its 5G networks in France and Italy' (Jul 2020). Verified 2026-11-24")],
         ran4=[], ran4_note="Light Reading (2020) says Iliad relies 'entirely on' Ericsson and Nokia, without a 4G split; Iliad's filings name neither as its 4G supplier",
         gov=[], gov_note='no state holder found (iliad, Niel family)', gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ United Kingdom
    dict(region='Western Europe', country='United Kingdom', operator_name='EE', core_operator_id='GB-ee', name_note='BT Group',
         share=V(31.0, UK_SHARES, UK_SHARES_NOTE, 2023),
         launch=V(2019, 'https://www.telecompaper.com/news/ee-confirms-uk-5g-network-launch-on-30-may--1293813', '30 May 2019; matches the discovery list'),
         ran5=[R('Ericsson', 'some', 'https://www.5gradar.com/news/ericsson-joins-nokia-as-one-of-bts-two-main-5g-providers',
                 "about 50%: Ericsson will be 'managing around 50 percent of the company's 5G traffic' (basis: expected share of BT's 5G traffic, not sites; 5G Radar, 2020). Verified 2026-11-24"),
               R('Nokia', 'not_disclosed', 'https://www.theregister.com/2020/10/28/ee_ericsson_5g_ran',
                 "selected 29 Sep 2020; The Register quotes Nokia as 'the leading RAN vendor in EE's network, [with a] 63 per cent share of the "
                 "RAN' (Oct 2020), which conflicts with Light Reading's Huawei two-thirds; not coded as a 5G share. Verified 2026-11-24")],
         ran4=[R('Huawei', 'most', LR_DUOPOLY, "about 67%: 'about two-thirds of its radio access network (RAN), or roughly 12,500 sites, with Nokia "
                 "supplying the remainder' (basis: RAN sites; Light Reading, Jul 2020). DISPUTED with The Register's Nokia 63% (Oct 2020). Verified 2026-11-24"),
               R('Nokia', 'some', LR_DUOPOLY, "about 33%: 'Nokia supplying the remainder' (basis: RAN sites; Jul 2020). Verified 2026-11-24")],
         gov=[], gov_note='no state holder of 5% or more found (BT Group plc, listed)', gov_dropped=[],
         core=V('Ericsson', 'https://www.lightreading.com/5g/bt-aims-to-resuscitate-5g-with-major-standalone-rollout',
                'converged Ericsson core for 4G, 5G NSA and SA; Ericsson 5G core selected Apr 2020'),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '5G', 'Huawei', 'Nokia', '2020-09-29', 'deadline 2027-12-31', 'https://www.theregister.com/2020/09/29/ee_picks_nokia_for_5g_ran/',
                     'UK requires Huawei out of 5G networks by end-2027'),
                   S('RAN', '5G', 'Huawei', 'Ericsson', '2020-10-28', 'deadline 2027-12-31', 'https://www.theregister.com/2020/10/28/ee_ericsson_5g_ran',
                     "'multi-year exercise'"),
                   S('core', '4G', 'Huawei', 'Ericsson', '2020', 'not_confirmed', LR_DUOPOLY,
                     "'a full transition to Ericsson will happen by 2023, says the operator' (2020); the vendor search reports the converged core replacing it in 2024")]),
    dict(region='Western Europe', country='United Kingdom', operator_name='Virgin Media O2', core_operator_id='GB-telefonica-uk',
         name_note='core panel name Telefónica UK; brand O2; VMED O2 UK joint venture with Liberty Global',
         share=V(35.0, UK_SHARES, UK_SHARES_NOTE + '; the O2 figure', 2023),
         launch=V(2019, 'https://www.bbc.co.uk/news/technology-50068422', '17 Oct 2019 (Belfast, Cardiff, Edinburgh, Leeds, London, Slough); matches the discovery list (2019-10)'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.lightreading.com/5g/ericsson-eats-into-nokia-s-share-of-vmo2-network-in-new-5g-deals',
                 "Ericsson will 'power the majority of Virgin Media O2's radio network' under the 2026 deal (basis: radio network, unit not stated; Light Reading, 31 Mar 2026; wording, no %). Verified 2026-11-24 [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Nokia', 'not_disclosed', 'https://news.virginmediao2.co.uk/virgin-media-o2-accelerates-its-mobile-transformation-plan-with-major-network-modernisation-deals/',
                 "the other 'primary' 5G RAN partner since 2019; share not stated"),
               R('Huawei', 'small', 'https://the-mobile-network.com/2019/10/o2s-hidden-5g-launch-vendor-huawei/',
                 "O2: 'a very small number of Huawei sites from that trial, which will be replaced with Nokia kit' (basis: sites, a few London trial sites; The Mobile Network, 30 Oct 2019). Verified 2026-11-24")],
         ran4=[R('Ericsson', 'most', 'https://www.lightreading.com/5g/ericsson-eats-into-nokia-s-share-of-vmo2-network-in-new-5g-deals', "Ericsson will 'power the majority of Virgin Media O2's radio network' under the 2026 deal (basis: radio network, all generations; Light Reading, 31 Mar 2026; wording, no %); in 2020 it had two of four UK regions (LR_AVOID) [decision 2026-11-24: all-generation share, coded to 4G only]"),
               R('Nokia', 'not_disclosed', LR_AVOID, 'two of four UK regions (same)')],
         gov=tef_gov(chain='Telefónica, S.A. 50% of the VMED O2 UK joint venture with Liberty Global', parent_pct=50.0),
         gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '5G', 'Huawei', 'Nokia', '2019-10-30', 'not_confirmed', 'https://the-mobile-network.com/2019/10/o2s-hidden-5g-launch-vendor-huawei/',
                     'London Huawei trial sites to be replaced with Nokia; no swap-out date')]),
    dict(region='Western Europe', country='United Kingdom', operator_name='VodafoneThree', core_operator_id='GB-vodafonethree',
         name_note='Vodafone UK and Three UK merged May 2025',
         share=ND(UK_SHARES_NOTE + '; no combined VodafoneThree figure (Vodafone 19, Three 11 separately) and summing brands is not coded'),
         launch=V(2019, 'https://www.techradar.com/news/5g-uk', 'predecessor Vodafone UK launched 3 Jul 2019 (Three UK Feb 2020); matches the discovery list'),
         ran5=[R('Ericsson', 'most', 'https://www.telecomtv.com/content/5g/samsung-squeezed-out-of-vodafonethree-s-2bn-uk-network-refresh-53887/',
                 "about 59%: 'supplying most of the radio access network (RAN) gear', radio units for 10,000 of the 17,000 refresh sites "
                 "(basis: refresh sites; TelecomTV, 22 Sep 2025). Verified 2026-11-24"),
               R('Nokia', 'some', 'https://www.lightreading.com/5g/nokia-is-the-big-winner-in-vodafonethree-5g-refresh',
                 "about 41% (computed: 7,000 of the 17,000 refresh sites; basis: refresh sites; Light Reading, 23 Sep 2025); replaces Huawei at about 3,700 sites. Verified 2026-11-24"),
               R('Huawei', 'not_disclosed', 'https://www.lightreading.com/5g/nokia-is-the-big-winner-in-vodafonethree-5g-refresh', 'being removed by the 2027 deadline')],
         ran5_note='Samsung has no role in the refresh (active at about 70 sites)',
         ran4=[R('Ericsson', 'most', LR_AVOID, "56%: legacy Vodafone UK 'said 56% of sites were Ericsson, 32% Huawei and 12% Nokia' (basis: sites; 2019 figures, "
                 "pre-merger; Light Reading, 11 Jun 2020). Verified 2026-11-24"),
               R('Huawei', 'some', LR_AVOID, '32% of legacy Vodafone UK sites (basis: sites; 2019). Verified 2026-11-24'),
               R('Nokia', 'some', LR_AVOID, '12% of legacy Vodafone UK sites (basis: sites; 2019), being phased out by Ericsson. Verified 2026-11-24'),
               R('Samsung', 'not_disclosed', LR_AVOID, 'legacy Three UK 4G vendor')],
         gov=vod_gov(parent_pct=100.0, note="Vodafone completed its buyout of CKHGT's 49% on 30 Jul 2026"),
         gov_dropped=VOD_DROPPED,
         core=V('Ericsson', 'https://www.vodafonethree.com/ericsson-rollout-begins-5g-core-network/', 'national 5G core rollout began 17 Sep 2026'),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '5G', 'Huawei', 'Nokia', '2025-09', 'deadline 2027-12-31', 'https://www.lightreading.com/5g/nokia-is-the-big-winner-in-vodafonethree-5g-refresh',
                     'Nokia replaces Huawei at about 3,700 sites, and Samsung at former Three/Vodafone sites, in the refresh'),
                   S('RAN', '5G', 'Huawei', 'Ericsson', '2020', 'not_confirmed', 'https://www.lightreading.com/5g/ericsson-swings-into-5g-ran-action-at-three-uk',
                     "Three UK: Ericsson took over the next stage of 5G after the UK restrictions; still under way in 2024")]),
]
