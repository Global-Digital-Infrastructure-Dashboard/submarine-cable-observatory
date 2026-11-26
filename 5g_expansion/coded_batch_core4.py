"""Core-94 migration, batch core4 (Prof. Shen, 2026-11): Finland, Belgium and Austria (10 operators) re-coded in the
expansion's three-file format, in-session on 2026-11-24, following the calibration batch (coded_batch_core1.py).

Inputs: the core panel (data/5g_operator_panel.csv) and its cached vendor/ownership searches (data/5g_searches.jsonl),
plus the migration searches mig|mktshare|<market>, mig|share|<id> and mig|ran|<id> (data/5g_expansion_searches.jsonl).
Government stakes re-express gov_stakes_core.py's per-holder rows (one addition, Telia Finland, is flagged below).
Share categories follow the user's rules (2026-11-23/24): a stated percentage maps 100% = all, >50% = most, 10-50% =
some, <10% = small; stated traffic/site/unit shares map by the same rule; 'majority' -> most, 'roughly evenly' -> some;
the note states the basis and date. Every share category and checked figure: 5g_expansion/verify_2026-11-24_core4.csv.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

register(domains={
    'company': ['elisa.com', 'elisa.fi', 'dna.fi', 'telenor.com', 'teliacompany.com', 'telia.fi', 'proximus.com',
                'corporate.orange.be', 'libertyglobal.com', 'telenet.be', 'citymesh.com', 'a1.com', 'magenta.at',
                'drei.at', 'ckh.com.hk', 'sttinfo.fi'],
    'government': ['traficom.fi', 'bipt.be', 'rtr.at'],
    'news': ['mobileeurope.co.uk', 'vindobona.org', 'convergedigest.com', 'telecomlead.com', 'sdxcentral.com'],
    'other': ['stocksummer.com', 'financialfilings.com'],
}, overrides={
    # Telia's own presentation hosted on the regulator's site
    'https://www.traficom.fi/files/media/file/Tomi%20Sarajisto_Traficom%20Event%205G%20and%20Sustainability_shared.pdf': 'company',
    # Orange Belgium's annual report on a filings aggregator
    'https://financialfilings.com/filings/orange-belgium-sa/annual-report/2026/33251653/': 'company',
}, vendors=['Affirmed Networks'])

# ------------------------------------------------------------------ shared sources
TRAFICOM_5G = 'https://www.traficom.fi/files/media/file/5G%20in%20Finland_20201229.pdf'
TRAFICOM_NOTE = ("Traficom, '5G in Finland' (29 Dec 2020), p.7: market shares of mobile subscriptions, December 2019, all "
                 "subscriptions: DNA 29, Elisa 39, Telia Finland 31, other 1 (verified 2026-11-24). The latest regulator figure "
                 "covering every operator; Traficom's later Nordic-Baltic reports give only the leading operator's share (38%, 2024)")
SYV_URL = 'https://www.telecompaper.com/news/nokia-supplies-dna-telia-venture-syv-with-5g-ran-and-managed-services-in-modernisation-contract--1359205'
SYV_NOTE = ("Telecompaper (26 Oct 2020): DNA and Telia Finland selected Nokia for RAN equipment and managed services in their SYV "
            "shared network (northern and eastern Finland, 'over 50 percent of the country area'): 5G RAN, modernisation of "
            "2G/3G/4G sites, rollout early 2021 to end-2023. Verified 2026-11-24")
BIPT_NOTE = ("BIPT publishes mobile market shares only as turnover ranges (2025: Proximus incl. Scarlet & Mobile Vikings 40-50%, "
             "Orange/VOO 30-40%, Telenet 20-30%) and no operator SIM or subscription counts")
RTR = 'https://www.rtr.at/rtr/publikationen/Kommunikationsbericht/RTR_Kommunikationsbericht-25-Engl-BF.pdf'
RTR_NOTE = ("RTR Communications Report 2025, Figure 63 (p.255): mobile market shares by SIM card excluding M2M, Q4 2025: A1 36.16, "
            "Magenta 24.93, Drei 20.10, HoT 9.94, spusu 5.49, others 3.38. Verified 2026-11-24 against the figure's text layer "
            "(series order read from the labels; matches the migration search's end-2025 figures)")
LR_PROXIMUS = 'https://www.lightreading.com/5g/proximus-dumps-huawei-in-luxembourg-too'
LR_TELENET = 'https://www.lightreading.com/5g/telenet-gives-ericsson-a-bigger-5g-role'
TP_PROXIMUS = 'https://www.telecompaper.com/news/proximus-picks-nokia-for-new-ran-ericsson-to-upgrade-core-for-5g--1357155'
ME_BELGIUM = 'https://www.mobileeurope.co.uk/belgium-s-big-two-remove-huawei-from-the-ran/'
DT_AR = 'https://report.telekom.com/annual-report-2025/_assets/downloads/sha-to-our-shareholders-dtag-ar25.pdf'
ORANGE_URD = 'https://assets.orange.com/medias/domain12751/media101922/576636-wexkleg98s-75.pdf'
A1_AR = 'https://a1.com/wp-content/uploads/sites/6/2026/03/A1-Telekom-Austria-Group-Annual-financial-report-2025.pdf'
VINDOBONA = 'https://www.vindobona.org/article/huaweis-5g-network-technology-in-austria-systemic-rival-at-the-gate-to-europe'


def dt_gov(chain, note=''):
    return [G('Germany', 'Federal Republic of Germany', 'government_ministry', 14.1, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
              note, chain=chain),
            G('Germany', 'KfW', 'state_holding_company', 14.2, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
              "the annual report describes the Federal Republic as an indirect shareholder via KfW. " + note, chain=chain)]


def orange_gov(chain):
    return [G('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_URD,
              '21.04% of voting rights (Orange 2025 Universal Registration Document)', chain=chain),
            G('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_URD,
              "8.00% of voting rights; the filing identifies it as the French state-owned investment company", chain=chain)]


def obag_gov(chain):
    return [G('Austria', 'Österreichische Beteiligungs AG (ÖBAG)', 'state_holding_company', 28.42, 'Telekom Austria AG', 'via_parent',
              '2025-12-31', A1_AR, 'held for the Republic of Austria; América Móvil B.V. holds 60.94%', chain=chain)]


OPERATORS = [
    # ------------------------------------------------------------------ Finland
    dict(region='Western Europe', country='Finland', operator_name='Elisa', core_operator_id='FI-elisa',
         share=V(39.0, TRAFICOM_5G, TRAFICOM_NOTE + "; S&P (Apr 2025), citing Traficom, gives Elisa 38% in June 2024", 2019),
         launch=V(2018, 'https://elisa.com/corporate/about-elisa/history/', "27 Jun 2018, Tampere (and Tallinn); the discovery list has no date"),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/about-us/news/releases/2020/09/30/nokia-selected-as-nationwide-supplier-of-5g-ran-by-elisa-finland/',
                 "selected as 'nationwide supplier of 5G RAN' (30 Sep 2020); no share wording; four-year modernisation deal for Finland and Estonia (Jun 2025)"),
               R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2020/9/elisa-finland-adds-5g-ran-to-ericsson-5g-core-partnership',
                 'Ericsson 5G Radio System products introduced into the network from 2021 (29 Sep 2020)')],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.lightreading.com/2g-3g-4g/elisa-upgrades-to-lte-with-nsn',
                 'supplier named as Nokia Siemens Networks: first LTE phase and Single RAN modernisation of GSM/3G (15 Dec 2010)')],
         gov=[G('Finland', 'Solidium Oy', 'state_holding_company', 10.04, 'Elisa Oyj', 'direct', '2026-08-14', 'https://app.stocksummer.com/stocks/detail/EIA.F',
                "major-shareholder listing; Solidium described as the Finnish state investment company. S&P (24 Mar 2026) puts the Finnish "
                "government at 10.5%",
                link_url='https://static.elisa.com/v2/image/2tqybbhjs47b/2yRSJFxrClU1u5UYgaNoPL/RatingsDirect_TearSheet_ElisaOyj_3543894_Apr-10-2026.pdf')],
         gov_dropped=[], gov_note=('Ilmarinen (3.134%) does not meet the pension rule (2026-11-26): a mutual pension insurer owned by its policyholders '
                                   'and insured, whose board is elected by its supervisory board, not appointed by government (ilmarinen.fi)'),
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/2020/9/elisa-finland-adds-5g-ran-to-ericsson-5g-core-partnership',
                'Ericsson Cloud Packet Core live in the 5G network; dual-mode 5G Core being deployed for SA (29 Sep 2020)'),
         first_contract=ND('Nokia and Ericsson 5G RAN agreements announced 29-30 Sep 2020, after the 2018 launch; first 5G contract date not found'),
         vendor_operates=ND()),
    dict(region='Western Europe', country='Finland', operator_name='DNA', core_operator_id='FI-dna',
         share=V(29.0, TRAFICOM_5G, TRAFICOM_NOTE, 2019),
         launch=V(2020, 'https://www.sttinfo.fi/tiedote/69873545/dna-begins-selling-5g-subscriptions?publisherId=1881',
                  'year per the discovery list and the migration search (Traficom); exact date not stated'),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.sttinfo.fi/tiedote/69871562/dna-home-5g-service-launched?publisherId=1881',
                 "DNA 'selected Huawei as a new supplier for the 5G radio network' while continuing with incumbent 4G supplier Ericsson"),
               R('Nokia', 'not_disclosed', SYV_URL, 'SYV shared network only (northern and eastern Finland). ' + SYV_NOTE)],
         ran4=[R('Ericsson', 'not_disclosed', 'https://convergedigest.com/finland-dna-signs-ericsson-for-4glte/',
                 "three-year contract covering 'GSM/HSPA/LTE radio access', extending an existing partnership; incumbent 4G supplier"),
               R('Huawei', 'not_disclosed', SYV_URL, "SYV shared network before Nokia's replacement: the same page reports SYV deploying Huawei "
                 "Active Antenna Units (Mar 2016); being replaced")],
         gov=[G('Norway', 'Government of Norway', 'government_ministry', 53.97, 'Telenor ASA', 'via_parent', '2026-02-27',
                'https://www.telenor.com/investors/shareholder-centre/major-shareholders/shareholders-as-of-27-february-2026/', '',
                chain="Telenor ASA -> Telenor Finland Holding Oy (sole shareholder of DNA Plc; Telenor's percentage of it not stated)")],
         gov_dropped=['Folketrygdfondet (Government Pension Fund Norway) 4.55% of Telenor ASA (meets the pension rule, 2026-11-26; board seat not checked)'],
         gov_note='Folketrygdfondet meets the pension rule (state-owned by statute, board appointed by the Ministry of Finance) but is below 5%',
         core=V('Affirmed Networks', 'https://www.sttinfo.fi/tiedote/69871562/dna-home-5g-service-launched?publisherId=1881',
                'virtualised 5G core from Affirmed Networks on a Nokia virtualisation platform; SA core for all 5G base stations by end-2021'),
         first_contract=ND(),
         vendor_operates=V(True, SYV_URL, 'for the SYV shared network only: Nokia responsible for infrastructure upgrade, field maintenance, '
                           'network monitoring and implementation; DNA runs its own RAN in dense areas. ' + SYV_NOTE),
         switches=[S('RAN', '4G', 'Huawei', 'Nokia', '2020-10-26', 'not_confirmed (due end-2023)', SYV_URL,
                     "SYV shared network: Nokia 'will replace SYV's current RAN equipment' (2G/3G/4G sites, plus 5G); Huawei as the old vendor rests "
                     "on Telecompaper's 2016 report of Huawei AAUs in SYV and a Dec 2023 telecoms.com report (403, not fetched); the core panel "
                     "says Huawei was replaced by end-2023")]),
    dict(region='Western Europe', country='Finland', operator_name='Telia Finland', core_operator_id='FI-telia-finland',
         share=V(31.0, TRAFICOM_5G, TRAFICOM_NOTE, 2019),
         launch=V(2019, 'https://www.traficom.fi/files/media/file/Tomi%20Sarajisto_Traficom%20Event%205G%20and%20Sustainability_shared.pdf',
                  "Telia presentation at a Traficom event: first 5G coverage in Finland's seven largest cities before Christmas 2019"),
         ran5=[R('Nokia', 'all', 'https://www.mobileeurope.co.uk/telia-company-picks-nokia-for-5g-in-finland-standalone-core-across-all-markets/',
                 "Mobile Europe (21 Oct 2020): Telia signed 'an exclusive 5G alliance' for the Nordics and Baltics with Nokia, 'except Ericsson "
                 "is supplying 5G infra in Sweden and Estonia, as well as Norway'; Nokia is 'the incumbent radio provider' in Finland. The "
                 "search's 'sole supplier' is not the page's wording; 'exclusive' coded as all. Verified 2026-11-24")],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.mobileeurope.co.uk/telia-company-picks-nokia-for-5g-in-finland-standalone-core-across-all-markets/',
                 "incumbent radio provider; the five-year deal modernises existing radio networks (7,500 sites across markets)")],
         gov=[G('Sweden', 'Swedish State', 'government_ministry', 41.1, 'Telia Company AB', 'via_parent', '2025-12-31',
                'https://www.teliacompany.com/downloads/u5c1v3pt22v8/5rdR72LuLgRQ5Ge4bOprhJ/1d446df8ad766c19090613b162b24952/Telia_Annual_report_2025.pdf',
                "ADDED in the migration; researcher decision 2026-11-24: treated as wholly owned by Telia Company, like Telia Norge "
                "and Telia Eesti (Telia Company's percentage of Telia Finland is not stated), and now also in gov_stakes_core.py",
                chain="Telia Company AB -> Telia Finland; Telia Company's percentage not stated (treated as wholly owned)")],
         gov_dropped=['Norges Bank 1.7% of Telia Company AB (2026-06-30; board seat not checked)'],
         core=V('Nokia', 'https://www.nokia.com/about-us/news/releases/2021/11/10/nokia-deploys-its-5g-standalone-core-for-telia-in-finland/',
                'cloud-native 5G SA core (10 Nov 2021); 4G EPC vendor not named'),
         first_contract=V('2020-10-21', 'https://www.mobileeurope.co.uk/telia-company-picks-nokia-for-5g-in-finland-standalone-core-across-all-markets/',
                          'five-year Nokia 5G RAN and SA-core agreement announced; earlier 5G vendor arrangements for the 2019 launch not found'),
         vendor_operates=V(True, SYV_URL, 'for the SYV shared network only (with DNA): Nokia managed services; Telia runs its own RAN in dense '
                           'areas. ' + SYV_NOTE),
         switches=[S('RAN', '4G', 'Huawei', 'Nokia', '2020-10-26', 'not_confirmed (due end-2023)', SYV_URL,
                     'SYV shared network (with DNA): Nokia replaces the current RAN equipment; old vendor as in the DNA row')]),
    # ------------------------------------------------------------------ Belgium
    dict(region='Western Europe', country='Belgium', operator_name='Proximus', core_operator_id='BE-proximus',
         share=ND(BIPT_NOTE + "; a 2018 BIPT impact study gave Proximus 41% of active clients (historical)"),
         launch=V(2020, 'https://www.reuters.com/article/belgium-proximus-5g-idUSL4N2BO2M6', '1 Apr 2020, 30 cities and Brussels Airport; matches the discovery list'),
         ran5=[R('Nokia', 'not_disclosed', TP_PROXIMUS, "selected 'to upgrade its radio access network' and build on the initial 5G network (9 Oct 2020); "
                 "no share wording. Verified 2026-11-24"),
               R('Ericsson', 'not_disclosed', TP_PROXIMUS, "indoor Radio Dot small cells for 4G and 5G only, per the migration search (not checked); "
                 "the core panel lists Ericsson as a RAN vendor")],
         ran4=[R('Huawei', 'all', LR_PROXIMUS, "100%: 'Proximus was previously 100% reliant on equipment from Huawei for its 4G radio access "
                 "networks (RAN) in Belgium and Luxembourg' (Strand Consult via Light Reading, Dec 2020; before the Nokia replacement). Verified 2026-11-24"),
               R('Nokia', 'not_disclosed', TP_PROXIMUS, "replacement supplier: 'largely replacing the existing radio network provided by Huawei' through 2023")],
         gov=[G('Belgium', 'Federal Holding and Investment Company (SFPIM)', 'state_holding_company', 53.51, 'Proximus PLC', 'direct', '2026-01',
                'https://www.proximus-cdn.com/dam/jcr:44041fd1-b790-497d-b397-cb03869fab27/proximus-integrated-annual-report-2026-v1.1_en.pdf',
                'shareholder analysis Jan 2026; the Belgian State transferred its shares to SFPIM on 24 May 2024',
                link_url='https://www.proximus-cdn.com/dam/jcr:95a3de33-0f87-46c7-a378-f11d184fde2e/08_management-report-2025-proximus-plc_en.pdf')],
         gov_dropped=[],
         core=V('Ericsson', TP_PROXIMUS, "selected for 'a new mobile data core network' (9 Oct 2020). Proximus launched a cloud-native 5G SA core "
                "(5G+) in Apr 2026 without naming its vendor. Verified 2026-11-24"),
         first_contract=V('2020-10-09', TP_PROXIMUS, 'Nokia RAN and Ericsson core selection announced; the Apr 2020 DSS launch used the existing network'),
         vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Huawei', 'Nokia', '2020-10-09', 'not_confirmed (planned 2023)', TP_PROXIMUS,
                     "2G/3G/4G RAN upgrade by Nokia 'over the period to 2023', largely replacing Huawei; RAN shared with Orange Belgium. "
                     "Later Proximus reports still describe the upgrade as ongoing")]),
    dict(region='Western Europe', country='Belgium', operator_name='Orange Belgium', core_operator_id='BE-orange-belgium',
         share=ND(BIPT_NOTE),
         launch=V(2020, 'https://www.bipt.be/users/faq/what-is-the-5g-offer',
                  "BIPT: 5G operational in Belgium since the end of 2020, with Orange among the operators offering it; exact date not found"),
         ran5=[R('Nokia', 'not_disclosed', ME_BELGIUM, "chosen to update 2G/3G/4G RANs and deploy 5G (9 Oct 2020). UNVERIFIED: the 'sole radio "
                 "supplier for this 5G network' quote (telecoms.com) returned 403, so no share category is coded")],
         ran4=[R('Huawei', 'all', LR_TELENET, "100%: 'Orange Belgium and Proximus were 100% reliant on Huawei' for 4G RAN (Strand Consult 2020 via "
                 "Light Reading, Oct 2021; before the Nokia replacement). Verified 2026-11-24"),
               R('Nokia', 'not_disclosed', ME_BELGIUM, "replacement supplier; Orange expected its 2G/3G/4G radio networks upgraded by 2023. Verified 2026-11-24")],
         gov=orange_gov('Orange S.A. -> Atlas Services Belgium SA (wholly owned) 76.29% of Orange Belgium (voting rights, 6 Oct 2025)'),
         gov_dropped=[],
         gov_note='Nethys (4.43%) is described only as public-sector-linked, so it is not a state holder here',
         core=V('Ericsson', ME_BELGIUM, "the Nokia 5G RAN runs on 'Orange Belgium's current Ericsson core network' in NSA mode, with Ericsson 5G SA "
                "to follow (9 Oct 2020); the annual reports describe the SA core as Ericsson packet core, Oracle signalling/routing and Nokia "
                "subscriber data management. Verified 2026-11-24"),
         first_contract=V('2020-10-09', ME_BELGIUM, 'Nokia RAN selection announced'),
         vendor_operates=ND('Nokia deploys and modernises the shared RAN; no managed operations stated'),
         switches=[S('RAN', '4G', 'Huawei', 'Nokia', '2020-10-09', 'not_confirmed (planned 2023)', ME_BELGIUM,
                     "2G/3G/4G radio networks upgraded with Nokia by 2023 (shared with Proximus); Orange Belgium's 2022 report planned 1,536 sites "
                     "dismantled by end-2025 and its 2024 report records EUR 7.5m accelerated depreciation for replacing all Huawei RAN material")]),
    dict(region='Western Europe', country='Belgium', operator_name='Telenet', core_operator_id='BE-telenet', name_note='also brand BASE',
         share=ND(BIPT_NOTE),
         launch=V(2021, 'https://www.bipt.be/consumers/faq/do-we-already-use-5g-in-belgium',
                  'gradual launch from Dec 2021; Telenet Business and BASE from spring 2022; matches the discovery list (2021-12)'),
         ran5=[R('Ericsson', 'not_disclosed', LR_TELENET, '5G RAN supplier (Mar 2021); Oct 2021 managed-services deal includes deployment of 5G hardware. Verified 2026-11-24')],
         ran4=[R('ZTE', 'all', LR_TELENET, "100%: 'Telenet was previously 100% reliant on equipment from ZTE for its 4G RAN' (Strand Consult 2020 "
                 "via Light Reading, Oct 2021; before the Ericsson modernisation). Verified 2026-11-24"),
               R('Ericsson', 'not_disclosed', 'https://telecomlead.com/5g/telenet-selects-ericsson-nokia-google-cloud-for-5g-network-99186',
                 'modernisation of the existing 2G/3G/4G RAN under the Mar 2021 agreement')],
         gov=[], gov_dropped=[],
         gov_note='wholly owned by Liberty Global Ltd. since Oct 2023; no state holder found among its shareholders',
         core=V('Nokia', 'https://www.libertyglobal.com/telenet-introduces-ericsson-nokia-google-cloud-as-partners-for-the-rollout-of-its-5g-network/',
                'cloud-native 5G core on Google Cloud Anthos (15 Mar 2021); BIPT (Jan 2026) still describes Telenet 5G as NSA; EPC vendor not named'),
         first_contract=V('2021-03-15', 'https://www.libertyglobal.com/telenet-introduces-ericsson-nokia-google-cloud-as-partners-for-the-rollout-of-its-5g-network/',
                          'Ericsson (RAN), Nokia (core) and Google Cloud announced as 5G partners'),
         vendor_operates=V(True, LR_TELENET, "five-year managed services deal (Oct 2021): Ericsson takes 'responsibility for planning, design, "
                           "operations and optimization' and employs 15 Telenet mobile engineers. Verified 2026-11-24"),
         switches=[S('RAN', '4G', 'ZTE', 'Ericsson', '2021-03-15', 'not_confirmed', LR_TELENET,
                     "Light Reading (Oct 2021): Telenet 'appears to have fully pivoted away from Chinese supplier ZTE'; completion not stated")]),
    dict(region='Western Europe', country='Belgium', operator_name='Citymesh Mobile', core_operator_id='BE-citymesh-mobile',
         name_note='network marketed with DIGI Belgium (Digi Communications Belgium: Digi Romania 51%, Citymesh 49%, Jul 2025)',
         share=ND('BIPT gives no Citymesh/DIGI share; it says DIGI held 0-5% of active SIMs at end-2025'),
         launch=ND('the discovery list gives 2024-12 (the DIGI network launch); no source in the migration search states a commercial 5G launch'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.citymesh.com/partners/nokia', "Nokia partnership page names AirScale radios; DIGI's 2025 annual "
                 "report names Nokia and Ericsson as group mobile-equipment suppliers without tying them to Belgium")],
         ran4=[], ran4_note='4G RAN vendor not named; Citymesh relies on Proximus for nationwide coverage (roaming)',
         gov=[], gov_dropped=[], gov_note='Digi Communications N.V. and Citymesh (Cegeka-controlled) are private; no state holder found',
         core=V('Nokia', 'https://www.nokia.com/newsroom/citymesh-goes-live-with-worlds-first-commercial-mobile-service-on-5g-core-saas-powered-by-nokia-and-aws/',
                'Nokia Core SaaS on AWS for 4G and 5G core, commercial service live 19 Feb 2026'),
         first_contract=V('2024-02-28', 'https://www.nokia.com/newsroom/citymesh-selects-nokia-core-saas-to-support-rollout-of-nationwide-b2b-mobile-services-in-belgium/',
                          'Citymesh selects Nokia Core SaaS (announcement date)'),
         vendor_operates=ND('Nokia Core SaaS includes lifecycle management of the core; no vendor-operated network stated')),
    # ------------------------------------------------------------------ Austria
    dict(region='Western Europe', country='Austria', operator_name='A1 Telekom Austria', core_operator_id='AT-a1-telekom-austria',
         share=V(36.16, RTR, RTR_NOTE, 2025),
         launch=V(2020, 'https://newsroom.a1.com/news-a1-telekom-austria-group-announces-that-its-austrian-subsidiary-a1-starts-largest-5g-network-in-austria?id=100423&menueid=14594&l=english',
                  '25 Jan 2020: 350 5G locations in 129 municipalities; the discovery list has no date'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.reuters.com/article/us-telekom-austria-5g-nokia-idUSKCN1R61SX',
                 "A1 selected Nokia to build Austria's 5G network (25 Mar 2019); the only named Austrian 5G RAN supplier, no share wording")],
         ran4=[], ran4_note="Reuters says only that A1 uses 'equipment from European vendors like Ericsson and Nokia in countries such as Austria'",
         gov=obag_gov('Telekom Austria AG (listed) -> A1 Telekom Austria AG; percentage not stated (the core panel treats it as wholly owned)'),
         gov_dropped=[],
         core=V('Nokia', 'https://www.reuters.com/article/us-telekom-austria-5g-nokia-idUSKCN1R61SX',
                "Nokia to provide '5G wireless technology and cloud-based core network technology' (Reuters, 25 Mar 2019); SDxCentral says the "
                "contract covered RAN and cloud-native 5G core. The core panel left the core vendor not_disclosed"),
         first_contract=V('2019-03-25', 'https://www.reuters.com/article/us-telekom-austria-5g-nokia-idUSKCN1R61SX', 'Nokia selected for the Austrian 5G network'),
         vendor_operates=ND()),
    dict(region='Western Europe', country='Austria', operator_name='Magenta Telekom', core_operator_id='AT-t-mobile-austria',
         name_note='core panel name T-Mobile Austria; renamed Magenta Telekom',
         share=V(24.93, RTR, RTR_NOTE, 2025),
         launch=V(2019, 'https://newsroom.magenta.at/2019/03/26/5g-austria/', "26 Mar 2019, first 5G base stations activated; Deutsche Telekom's Q1 2019 "
                  'report confirms; the discovery list has no date'),
         ran5=[R('Huawei', 'not_disclosed', VINDOBONA, "the initial 5G network (58 sites in 33 municipalities) 'was built by Huawei'; Magenta said in "
                 "Jul 2020 it would stay with Huawei for the rollout. A Mar 2019 report says its first 25 base stations were 'all from Huawei' "
                 "(initial sites only, so not coded as all)")],
         ran4=[R('Huawei', 'not_disclosed', VINDOBONA, "upgrading the existing Huawei LTE equipment to 5G was 'comparatively easy' (Jul 2020); Ericsson "
                 "and Nokia equipment is also used somewhere in the network")],
         gov=dt_gov("Deutsche Telekom AG -> T-Mobile Austria Holding GmbH -> Magenta Telekom; wholly owned within the DT Group per the ownership "
                    "search, percentage not stated in a filing"),
         gov_dropped=[],
         core=ND('Huawei is reported as not used in the core network; the core vendor is not named'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Western Europe', country='Austria', operator_name='Drei', core_operator_id='AT-hutchison-drei-austria',
         name_note='core panel name Hutchison Drei Austria',
         share=V(20.10, RTR, RTR_NOTE, 2025),
         launch=V(2019, 'https://www.zte.com.cn/global/carrier/operator_success_solutions/202111191624.html',
                  "first commercial 5G tariffs in Sep 2019 (ZTE case study); an industry directory gives Linz, 20 Jun 2019; the discovery list has no date"),
         ran5=[R('ZTE', 'not_disclosed', 'https://www.sdxcentral.com/news/hutchison-drei-austria-taunts-rivals-with-real-5g/',
                 "ZTE supplied the first phase of 5G (20 base stations by the 2019 launch); a later phase was to be tendered; no share wording")],
         ran4=[], ran4_note='ZTE and Huawei appear only in personal LinkedIn profiles (not cited)',
         gov=[], gov_dropped=[],
         gov_note='100% owned by CK Hutchison Holdings (largest holder the Li Ka-shing Unity Trust, 26.26%); no state holder found',
         core=V('Ericsson', 'https://www.ericsson.com/en/news/3/2025/ericsson-drei-austria-modernize-core-network',
                'cloud-native dual-mode 5G core, multi-year modernisation announced 3 Sep 2025; the earlier EPC vendor is not named'),
         first_contract=ND(), vendor_operates=ND()),
]
