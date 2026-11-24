"""Core-94 migration, batch core8 (Prof. Shen, 2026-11): Bulgaria, Greece, Estonia and Lithuania (12 operators) re-coded
in the expansion's three-file format, in-session on 2026-11-24, following the calibration batch (coded_batch_core1.py).

Inputs: the core panel (data/5g_operator_panel.csv) and its cached vendor/ownership searches (data/5g_searches.jsonl),
plus the migration searches mig|mktshare|<market>, mig|share|<id> and mig|ran|<id> (data/5g_expansion_searches.jsonl).
Government stakes re-express gov_stakes_core.py's per-holder rows. Share categories follow the user's rules
(2026-11-23/24): a stated percentage maps 100% = all, >50% = most, 10-50% = some, <10% = small; stated traffic/site/
unit shares map by the same rule; 'majority' -> most, 'roughly evenly' -> some; the note states the basis and date.
Every share category and checked figure: 5g_expansion/verify_2026-11-24_core8.csv.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

S_AND_P_ELISA = 'https://static.elisa.com/v2/image/2tqybbhjs47b/2yRSJFxrClU1u5UYgaNoPL/RatingsDirect_TearSheet_ElisaOyj_3543894_Apr-10-2026.pdf'
S_AND_P_ELISA_2024 = 'https://static.elisa.com/v2/image/2tqybbhjs47b/2vyQ5SodPQm9m4QE980goRr/RatingsDirect_ElisaOyj_57891312_May-02-2024.PDF'

register(domains={
    'company': ['a1.com', 'a1.bg', 'vivacom.bg', 'yettel.bg', 'telekom.com', 'telekom.gr', 'cosmote.gr', 'vodafone.com',
                'teliacompany.com', 'telia.lt', 'telia.ee', 'tele2.com', 'elisa.com', 'nasdaqbaltic.com', 'bitegroup.net'],
    'government': ['crc.bg', 'eett.gr', 'rrt.lt', 'curia.europa.eu'],
    'research_industry_group': ['robert-schuman.eu', 'strandconsult.dk'],
    'news': ['broadbandtvnews.com', 'krib.bg', 'mobileeurope.co.uk', 'news.err.ee', 'madeinvilnius.lt', 'insidetelecom.com'],
    'other': ['brand.com'],
}, overrides={
    # e& PPF Telecom Group's own annual accounts on a CDN
    'https://www.datocms-assets.com/56100/1771365178-fr39_20260217_eand_ppf_telecom_group_fy2025_annual_accounts_public.pdf': 'company',
    # Nokia's press release reposted by TCCA
    'https://tcca.info/news/962/nokia_wins_fiveyear_5g_deal_with_elisa_estonia_as_sole_ran_vendor/': 'company',
    # S&P rating reports hosted by Elisa
    S_AND_P_ELISA: 'research_industry_group',
    S_AND_P_ELISA_2024: 'research_industry_group',
})

# ------------------------------------------------------------------ shared sources
CRC25 = 'https://crc.bg/files/Annual%20Report-%D0%95%D0%A1%D0%90_2025_CRC_eng.pdf'
CRC_NOTE = ("CRC Annual Report 2025, Table 5 (p.29): shares of retail mobile voice service by number of subscribers at 31 Dec 2025: "
            "A1 35.9, Vivacom 33.1, Yettel 31.0 (2024: 36.5 / 32.8 / 30.7). Verified 2026-11-24. The same report's 'mobile access "
            "subscribers' measure ranks Vivacom first (36.3 / A1 33.9 / Yettel 29.8 per the search); voice subscribers coded")
EETT24 = 'https://www.eett.gr/wp-content/uploads/2026/02/EETT_MARKET_REVIEW_2024.pdf'
EETT_NOTE = ("EETT Market Review 2024 (p.5): shares of total mobile connections (mobile telephony, datacards, M2M, etc.; registered, "
             "not only active) in 2024: OTE 44.4, Vodafone 34.1, Nova 21.5. Verified 2026-11-24. Active-connection shares are "
             "given only as ranges (OTE 45-55%, Vodafone 25-35%)")
A1_AR = 'https://a1.com/wp-content/uploads/sites/6/2026/03/A1-Telekom-Austria-Group-Annual-financial-report-2025.pdf'
EPPF = 'https://www.datocms-assets.com/56100/1771365178-fr39_20260217_eand_ppf_telecom_group_fy2025_annual_accounts_public.pdf'
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
DT_AR = 'https://report.telekom.com/annual-report-2025/_assets/downloads/sha-to-our-shareholders-dtag-ar25.pdf'
VOD_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
VOD_HOLDING = 'https://www.vodafone.com/~/media/Files/V/vodafone/corp/results-and-presentations/vodafone-group-holding-structure-12-05-2026.pdf'
LR_HUAWEI_2020 = 'https://www.lightreading.com/5g/europes-dependence-on-huawei-laid-bare-in-new-study/d/d-id/762040'
STRAND_2026 = 'https://strandconsult.dk/fact-check-gsma-intelligences-report-the-cost-of-removing-designated-third-country-vendors-from-eu-telecoms-networks/'
SCHUMAN = 'https://www.robert-schuman.eu/en/european-issues/817-the-european-strategic-approach-to-technological-security-the-challenges-posed-by-china'
TELIA_SHAREHOLDINGS = 'https://www.teliacompany.com/en/articles/shareholdings'
TELIA_AR25 = 'https://www.teliacompany.com/downloads/u5c1v3pt22v8/5rdR72LuLgRQ5Ge4bOprhJ/1d446df8ad766c19090613b162b24952/Telia_Annual_report_2025.pdf'
LR_TELIA_CORE = 'https://www.lightreading.com/5g/telia-picks-nokia-for-standalone-5g-core-in-six-markets'
TELIA_CORE_NOTE = ("Light Reading (21 Oct 2020), verified 2026-11-24: Telia's CEO says Nokia 'is our sole supplier of 5G standalone core "
                   "in all markets'; the six markets include Estonia and Lithuania")
NOKIA_TELE2_BALTICS = 'https://www.nokia.com/newsroom/nokia-and-tele2-expand-5g-partnership-in-the-baltics/'
TELE2_BALTICS_NOTE = ("Nokia release (Jan 2022): 'Nokia is the incumbent and sole supplier in the deal' to modernize Tele2's nationwide "
                      "radio network in Estonia, Latvia and Lithuania (basis: Baltic 5G RAN deal; verified 2026-11-23 in batch 3 for Latvia)")
LR_NSN_TELE2 = 'https://www.lightreading.com/2g-3g-4g/tele2-picks-nsn-for-lte-in-the-baltics'
NSN_NOTE = ("named as Nokia Siemens Networks: 'selected as the sole supplier of the operator's 4G, LTE radio and core network' in "
            "Estonia, Latvia and Lithuania (basis: LTE radio and core contract, 25 Apr 2012; verified 2026-11-24)")
TELE2_CORE = 'https://www.tele2.com/media/news/2021/tele2-partners-with-nokia-for-5g-core-deployment-in-sweden-and-the-baltics/'
LR_TELIA_LT = 'https://www.lightreading.com/5g/telia-lithuania-adds-to-huawei-s-european-pain'
TELIA_LT_AR23 = 'https://nasdaqbaltic.com/market/upload/reports/tel1/2023_ar_en_eur_solo_ias.pdf'
DT_BITE = 'https://developingtelecoms.com/telecom-business/operator-news/13506-ericsson-takes-a-bite-of-baltics-5g-networks.html'
BLOOMBERG_BG = ("Bloomberg TV Bulgaria (29 Jun 2021), read 2026-11-24 via the China Index citation but not in the cached evidence, "
                "so not cited: an expert says A1 uses Nokia, Vivacom 'several, but mainly Huawei', Telenor (now Yettel) 'entirely Huawei' for 5G")
EE_SHARE_NOTE = ("no regulator publishes Estonian shares by operator: Traficom's Nordic-Baltic report gives only the leading operator "
                 "(43%, 2023, mobile subscriptions excl. M2M). A secondary PDF (ozi-ru.net) attributes Telia 44 / Elisa 32 / Tele2 24 "
                 "(end-2023, by subscribers) to the regulator; not a citable source and not coded")
LT_SHARE_NOTE = ("no current regulator share by operator: RRT's last operator table in the evidence is Q4 2017 (active SIMs: Tele2 42.6, "
                 "Telia 30.1, Bite 25.3) and the PDF now returns 404 (UNVERIFIED, and stale); Telia Lietuva's reports give revenue "
                 "shares only (Q3 2025: Telia 38.8, Tele2 28.4, Bite 21.0)")


def dt_gov(chain, parent_pct=None):
    note = "the annual report describes the Federal Republic as an indirect shareholder via KfW"
    return [G('Germany', 'Federal Republic of Germany', 'government_ministry', 14.1, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
              '', chain=chain, parent_pct=parent_pct),
            G('Germany', 'KfW', 'state_holding_company', 14.2, 'Deutsche Telekom AG', 'via_parent', '2025-12-31', DT_AR,
              note, chain=chain, parent_pct=parent_pct)]


def eand_vod(chain='', parent_pct=None):
    return [G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 17.005026,
              'Vodafone Group Plc', 'via_parent', '2026-03-31', VOD_AR,
              "e&'s 2025 integrated annual report: Emirates Investment Authority 60%, ultimately controlled by the UAE Federal Government",
              link_url=E_AND_AR, chain=chain, parent_pct=parent_pct)]


def telia_gov(url, as_of, chain='', parent_pct=None):
    return [G('Sweden', 'Swedish State', 'government_ministry', 41.1, 'Telia Company AB', 'via_parent', as_of, url,
              '', chain=chain, parent_pct=parent_pct)]


OPERATORS = [
    # ------------------------------------------------------------------ Bulgaria
    dict(region='Central Asia & Eastern Europe', country='Bulgaria', operator_name='A1 Bulgaria', core_operator_id='BG-a1-bulgaria',
         share=V(35.9, CRC25, CRC_NOTE, 2025),
         launch=V(2020, 'https://www.broadbandtvnews.com/2020/11/23/a1-introduces-5g-to-bulgaria/',
                  "23 Nov 2020 report: 5G launched in central, residential and business areas of Sofia; discovery gives 2020-11"),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-expands-5g-radio-and-core-contract-with-a1-telekom-austria-group-into-new-markets',
                 "AirScale 5G RAN for Bulgaria (Aug 2021, deployment already under way); Inside Telecom: 'Nokia will deploy the radio "
                 "network' in Bulgaria, Ericsson the core; no share wording. " + BLOOMBERG_BG)],
         ran4=[], ran4_note='4G RAN vendor not named in the sources',
         gov=[G('Austria', 'Österreichische Beteiligungs AG (ÖBAG)', 'state_holding_company', 28.42, 'Telekom Austria AG', 'via_parent',
                '2025-12-31', A1_AR, 'held for the Republic of Austria; América Móvil B.V. holds 60.94%',
                chain='Telekom Austria AG (listed) -> A1 Bulgaria EAD, listed at 100.00% in the A1 Group structure')],
         gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/news/2021/9/a1-opts-for-ericsson-5g-core-in-croatia-and-bulgaria',
                'cloud-native dual-mode 5G Core for Bulgaria (Sep 2021)'),
         first_contract=ND('the Nokia RAN (Aug 2021) and Ericsson core (Sep 2021) selections came after the Nov 2020 launch; no earlier dated 5G contract found'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Bulgaria', operator_name='Vivacom', core_operator_id='BG-bulgarian-telecommunications-company',
         name_note='Bulgarian Telecommunications Company EAD (core panel name), brand Vivacom',
         share=V(33.1, CRC25, CRC_NOTE, 2025),
         launch=V(2020, 'https://krib.bg/en/vivacom-ima-nay-barzata-5g-mrezha-v-balgariya-spored-prouchvane-na-ookla/',
                  "Sep 2020 per the migration search (a secondary source gives 1 Sep 2020); not confirmed by an operator or CRC document; "
                  "discovery gives 2020-09"),
         ran5=[], ran5_note=("5G RAN vendor not named in the cached evidence; Vivacom's 2023 report confirms commercial 5G without a vendor. "
                             + BLOOMBERG_BG + ". Parallel Wireless Open RAN 2G/4G/5G trial (Jun 2023) is a trial, not coded"),
         ran4=[R('Huawei', 'all', 'https://www.vivacom.bg/bg/files/6359-sustainability-report-2015.pdf',
                 "2015 sustainability report p.17: Vivacom's largest-ever tender 'for SRAN equipment and maintenance supplier including for "
                 "future 4G integration. Today, Huawei is the winning bidder and an exclusive VIVACOM partner' (basis: SRAN/4G tender, 2015; verified 2026-11-24)")],
         gov=[], gov_note=("no current state holder: United Group B.V. (BC Partners majority) owns Vivacom; VTB's stake via V Telecom Investment "
                           "and Bulgaria's golden share are 2013 history"),
         gov_dropped=[],
         core=ND('no 5G core or EPC vendor named; Nokia is named only for cloud-native core products and GPON fixed access'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Bulgaria', operator_name='Yettel Bulgaria', core_operator_id='BG-yettel-bulgaria',
         name_note='formerly Telenor Bulgaria',
         share=V(31.0, CRC25, CRC_NOTE, 2025),
         launch=V(2021, 'https://brand.com/brand-wiki/yettel-bulgaria',
                  "nationwide 5G from 10 Jun 2021 (weak source: brand wiki); discovery gives 2021-06-10; the migration search gives June 2021"),
         ran5=[R('Huawei', 'not_disclosed', 'https://china-index.io/indicator/question57',
                 "China Index (Bulgaria entry, verified 2026-11-24): Yettel 'has built its 5G networks with Huawei technolog[y]', citing "
                 "Bloomberg TV Bulgaria. " + BLOOMBERG_BG + "; 'entirely' would map to all, but that source is not in the cached evidence")],
         ran4=[], ran4_note="Huawei rebuilt Telenor Bulgaria's 2G/3G network 'to support later LTE development' (brand wiki only); not coded",
         gov=[G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 50.0,
                'e& PPF Telecom Group B.V.', 'via_parent', '2025-12-31', EPPF,
                "50% plus one share since 24 Oct 2024; the accounts name the UAE Federal Government as ultimate controlling party; "
                "e&'s 2025 report: Emirates Investment Authority 60%", link_url=E_AND_AR,
                chain='e& PPF Telecom Group B.V. -> PPF TMT Bidco 1 N.V. 100% -> Yettel Bulgaria EAD (wholly owned per Yettel ESG Report 2025)')],
         gov_dropped=[],
         core=ND('no core vendor named; a "Telco Core Swap" appears only in a personal profile'),
         first_contract=ND(),
         vendor_operates=ND('the network is operated with CETIN Bulgaria (a PPF-group infrastructure company, not an equipment vendor)')),
    # ------------------------------------------------------------------ Greece
    dict(region='Western Europe', country='Greece', operator_name='OTE (COSMOTE Telekom)', core_operator_id='GR-ote-cosmote-telekom-telekom',
         name_note='core panel name OTE (COSMOTE Telekom / Telekom); COSMOTE rebranded Telekom in Greece',
         share=V(44.4, EETT24, EETT_NOTE, 2024),
         launch=V(2020, 'https://www.telekom.com/en/newsroom/latest-updates/media-information/2020/12/cosmote-launches-5g-and-hits-another-network-first-in-greece',
                  '17 Dec 2020, Athens, Thessaloniki and other cities; discovery gives 2020-12'),
         ran5=[R('Ericsson', 'all', 'https://www.mobileeurope.co.uk/cosmote-greece-selects-ericsson-for-5g-ran/',
                 "Mobile Europe (25 Mar 2020), verified 2026-11-24: COSMOTE 'has chosen Ericsson as its sole 5G radio access network (RAN) "
                 "vendor' (basis: 5G RAN vendor selection, Mar 2020). DISPUTED between this and Strand Consult (2026), which puts Deutsche "
                 "Telekom's Greek high-risk-supplier exposure at 100% (unit not stated, probably the legacy 4G footprint); coded the operator/vendor statement")],
         ran4=[], ran4_note=("the Ericsson 5G deal also 'strengthens existing networks nationwide' (no 4G share); Strand Consult (2026) gives "
                             "DT Greece 100% high-risk-supplier exposure, not attributed to a generation or vendor; not coded"),
         gov=dt_gov('Deutsche Telekom AG 54.38% of OTE (itself listed in Athens)', parent_pct=54.38),
         gov_dropped=[], gov_note='no Greek state holder of 5% or more in the evidence',
         core=V('Ericsson', 'https://www.ericsson.com/en/cases/2026/cosmote-telekom', 'Ericsson case study (Mar 2026): 5G SA radio and core capabilities'),
         first_contract=V('2020-03', 'https://www.mobileeurope.co.uk/cosmote-greece-selects-ericsson-for-5g-ran/',
                          'Ericsson selected as sole 5G RAN vendor (announced 25 Mar 2020); signing date not stated'),
         vendor_operates=ND()),
    dict(region='Western Europe', country='Greece', operator_name='Vodafone Greece', core_operator_id='GR-vodafone-greece',
         share=V(34.1, EETT24, EETT_NOTE, 2024),
         launch=ND("2021 per the migration search and the discovery row (2021-01), without a dated source; 5G SA launched 17 Jun 2026 (Patras)"),
         ran5=[R('Huawei', 'all', STRAND_2026,
                 "Strand Consult (2026), verified 2026-11-24: 'Vodafone is also heavily exposed ... including 100% reliance on Huawei in the "
                 "Czech Republic, Greece, Hungary, and Romania' (basis: high-risk-supplier exposure of the RAN upgraded from 4G to 5G, unit not stated, 2026)")],
         ran4=[R('Huawei', 'all', LR_HUAWEI_2020,
                 "Light Reading citing Strand Consult (30 Jun 2020), verified 2026-11-24: 'Vodafone is 100% reliant on Huawei in the six markets "
                 "of the Czech Republic, Greece, ...' (basis: 4G RAN equipment, Jun 2020)")],
         gov=eand_vod(chain='Vodafone Group Plc 99.9% of Vodafone Greece (holding structure, 12 May 2026)', parent_pct=99.9),
         gov_dropped=['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)'],
         core=ND('a dedicated 5G core runs the 2026 SA service, vendor not named; Huawei core replacement (EUR 200m) is a Vodafone Europe-wide programme'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Western Europe', country='Greece', operator_name='Nova', core_operator_id='GR-nova',
         name_note='continues WIND Hellas mobile operations after the Jan 2023 merger (core-panel researcher decision 2026-11-13)',
         share=V(21.5, EETT24, EETT_NOTE, 2024),
         launch=ND('no Nova or WIND Hellas commercial 5G launch date in the evidence (2024 sustainability report: 90% 5G population coverage)'),
         ran5=[], ran5_note=("no 5G RAN vendor named for Nova; Robert Schuman Foundation's Huawei statement (see 4G) is in present tense "
                             "but in the 4G context, so not coded for 5G. VICTUS Networks (Vodafone-Nova 50:50 JV) runs shared RAN, "
                             "vendors not attributed"),
         ran4=[R('Huawei', 'most', SCHUMAN,
                 "Robert Schuman Foundation (policy paper, 2026), verified 2026-11-24: 'Wind Hellas' radio access network is almost "
                 "exclusively provided by Huawei', after Huawei upgraded its 4G networks ('almost exclusively' read as most; basis: RAN, "
                 "generation not stated, 4G context)")],
         gov=[], gov_note='privately held (United Group B.V.: BC Partners ~56%, management 42%); EBRD 2% is a multilateral bank, not a state holder',
         gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND('VICTUS Networks (Vodafone/Nova JV) operates and maintains the shared RAN and transport; not a vendor')),
    # ------------------------------------------------------------------ Estonia
    dict(region='Central Asia & Eastern Europe', country='Estonia', operator_name='Telia Eesti', core_operator_id='EE-telia-eesti',
         share=ND(EE_SHARE_NOTE + "; the migration search's Telia 41.8% is Oct 2018"),
         launch=V(2020, 'https://news.err.ee/1157319/telia-rolling-out-5g-services-in-select-regions-of-estonia', '10 Nov 2020, Tallinn, Tartu and Pärnu; discovery gives 2020-11'),
         ran5=[R('Ericsson', 'not_disclosed', LR_TELIA_CORE,
                 "Light Reading (21 Oct 2020), verified 2026-11-24: 'Ericsson ... scooped up 5G RAN contracts in Sweden and Estonia'; "
                 "renewed for four years on 6 Nov 2025; no share wording")],
         ran4=[], ran4_note="Telia's 2021 report: existing Estonian RAN assets replaced in 2021-2025 with Ericsson/Nokia; old vendor and split not stated",
         gov=telia_gov(TELIA_SHAREHOLDINGS, '2026-06-30', chain='Telia Company AB -> Telia Eesti AS (wholly owned per the Estonian register)'),
         gov_dropped=[],
         core=V('Nokia', LR_TELIA_CORE, TELIA_CORE_NOTE),
         first_contract=V('2020-10', LR_TELIA_CORE, 'Ericsson 5G RAN and Nokia SA core deals announced Oct 2020, before the Nov 2020 launch'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Estonia', operator_name='Elisa Eesti', core_operator_id='EE-elisa-eesti',
         share=V(35.0, S_AND_P_ELISA_2024,
                 "S&P rating report on Elisa Oyj (May 2024): Elisa is Estonia's second operator with a 35% mobile share by subscriptions, 2023 "
                 "(not a regulator figure). " + EE_SHARE_NOTE, 2023),
         launch=V(2018, 'https://www.telecompaper.com/news/elisa-claims-worlds-first-commercial-5g-network-launch--1250503',
                  "27 Jun 2018, Tallinn (and Tampere); Elisa Eesti announced a separate launch on a 'true 5G frequency' on 27 Jun 2022 after the auction"),
         ran5=[R('Nokia', 'all', 'https://tcca.info/news/962/nokia_wins_fiveyear_5g_deal_with_elisa_estonia_as_sole_ran_vendor/',
                 "Nokia release (20 Dec 2021, via TCCA; nokia.com returned 403), verified 2026-11-24: nationwide 5G RAN, 'Nokia will be the sole "
                 "provider, replacing the incumbent vendor' (basis: 5G RAN contract, Dec 2021); four-year modernisation extension Jun 2025")],
         ran4=[R('Nokia', 'not_disclosed', 'https://tcca.info/news/962/nokia_wins_fiveyear_5g_deal_with_elisa_estonia_as_sole_ran_vendor/',
                 'the Dec 2021 deal also replaces the existing 4G infrastructure; completion not stated'),
               R('Huawei', 'not_disclosed', 'https://infocuria.curia.europa.eu/tabs/document/C/2024/C-0354-24-00000000RP-01-P-01/CONCL/317929-EN-1-html',
                 "CJEU Advocate General opinion in C-354/24 (19 Mar 2026), per the search: Elisa Eesti's mobile radio network is Huawei hardware "
                 "and software (UNVERIFIED: the page renders client-side); share after the Nokia replacement not stated")],
         gov=[G('Finland', 'Finnish government (incl. Solidium Oy)', 'government_ministry', 10.5, 'Elisa Oyj', 'via_parent', '2026-03-24', S_AND_P_ELISA,
                "FLAG (threshold): S&P gives the Finnish government 10.5% (24 Mar 2026); a second source gives Solidium Oy 10.0% (Oct 2026), "
                "which would not cross 'above 10%'; the two may be the same holding on different bases, so they are not added",
                chain='Elisa Oyj -> Elisa Eesti AS (sole shareholder per the Estonian register)')],
         gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/3/2022/elisa-selects-ericsson-5g-core-to-empower-standalone-network-in-estonia',
                'dual-mode 5G Core for the Estonian SA network (Nov 2022)'),
         first_contract=ND('the Nokia RAN deal (Dec 2021) followed the 2018 launch; no dated earlier 5G contract found'),
         vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Huawei', 'Nokia', '2021-12-20', 'deadline 2025-12-31',
                     'https://infocuria.curia.europa.eu/tabs/document/C/2024/C-0354-24-00000000RP-01-P-01/CONCL/317929-EN-1-html',
                     "Nokia's release names only 'the incumbent vendor'; the CJEU AG opinion (UNVERIFIED, see 4G) names Huawei and the "
                     "Estonian authorisation's 31 Dec 2025 replacement deadline (core-panel rip_and_replace_deadline)")]),
    dict(region='Central Asia & Eastern Europe', country='Estonia', operator_name='Tele2 Eesti', core_operator_id='EE-tele2-eesti',
         share=ND(EE_SHARE_NOTE + "; Tele2 reports 455,000 Estonian mobile customers at end-2023 without a market total"),
         launch=V(2022, 'https://www.samenacouncil.org/samena_daily_news?news=90948', '20 Jul 2022, parts of Tallinn and Kiisa'),
         ran5=[R('Nokia', 'all', NOKIA_TELE2_BALTICS, TELE2_BALTICS_NOTE)],
         ran4=[R('Nokia', 'all', LR_NSN_TELE2, NSN_NOTE)],
         gov=[], gov_note='Tele2 Sverige AB is the sole shareholder; no state holder of 5% or more in Tele2 AB', gov_dropped=[],
         core=V('Nokia', TELE2_CORE, '5G core for Sweden and the Baltics (Jan 2021)'),
         first_contract=V('2021-01', TELE2_CORE, 'Nokia 5G core partnership for Sweden and the Baltics announced Jan 2021'),
         vendor_operates=ND()),
    # ------------------------------------------------------------------ Lithuania
    dict(region='Central Asia & Eastern Europe', country='Lithuania', operator_name='Telia Lietuva', core_operator_id='LT-telia-lietuva',
         share=ND(LT_SHARE_NOTE),
         launch=V(2022, 'https://ml-eu.globenewswire.com/Resource/Download/d38adeb1-3983-41c7-81ad-9fc19784375e',
                  '26 Sep 2022, on receiving RRT permission for commercial 5G'),
         ran5=[R('Ericsson', 'not_disclosed', LR_TELIA_LT,
                 "Light Reading (Nov 2020), verified 2026-11-24: 'The operator has said that Ericsson will be its sole partner for RAN technology "
                 "in Lithuania' (basis: RAN technology partner, Nov 2020); Telia's 2023 report: 'completed the upgrade of its entire mobile "
                 "network using Ericsson equipment' [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]")],
         ran4=[R('Ericsson', 'all', TELIA_LT_AR23,
                 "Telia Lietuva 2023 report (p.9, p.25), verified 2026-11-24: 'completed the upgrade of its entire mobile network using Ericsson "
                 "equipment'; the RAN upgrade begun in 2021 covered nearly 1,650 base stations (basis: whole mobile network, 2023)")],
         gov=telia_gov(TELIA_AR25, '2025-12-31', chain='Telia Company AB 88.15% of Telia Lietuva (itself listed on Nasdaq Vilnius)', parent_pct=88.15),
         gov_dropped=[],
         core=V('Nokia', LR_TELIA_CORE, TELIA_CORE_NOTE),
         first_contract=V('2020-10', LR_TELIA_CORE, 'Nokia SA core deal covering Lithuania announced Oct 2020 (Ericsson RAN partnership 3 Nov 2020)'),
         vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Huawei', 'Ericsson', '2020-11-03', '2023', LR_TELIA_LT,
                     "Light Reading (Nov 2020), verified: Telia confirmed a 'large part' of its 4G RAN was Huawei (Strand Consult: 100%) and picked "
                     "Ericsson for about 2,000 sites; completion: Telia Lietuva 2023 report (upgrade completed 2023)")]),
    dict(region='Central Asia & Eastern Europe', country='Lithuania', operator_name='Bitė Lietuva', core_operator_id='LT-bite-lietuva',
         share=ND(LT_SHARE_NOTE),
         launch=V(2022, 'https://madeinvilnius.lt/en/business/Vilnius-market/bite-starts-providing-5g-connection-services/',
                  "25 Oct 2022: Bitė started providing 5G service with Ericsson equipment; discovery status 'unclear'"),
         ran5=[R('Ericsson', 'all', DT_BITE,
                 "Developing Telecoms (May 2022), verified 2026-11-23 in batch 3: Ericsson 'will be the sole provider of nationwide RAN for Bite' "
                 "in Lithuania and Latvia, 2022-2028 (basis: nationwide RAN contract, May 2022)")],
         ran4=[], ran4_note="4G vendor (Ericsson in Lithuania, Huawei in Latvia) appears only in a personal profile; not coded",
         gov=[], gov_note='privately held (Bitė Group; Providence Equity-era owners); no state holder in the evidence', gov_dropped=[],
         core=V('Nokia', 'https://www.nokia.com/newsroom/bite-group-selects-nokias-packet-core-to-drive-5g-evolution-and-to-simplify-and-enhance-network-capacity/',
                "Nokia release (28 Aug 2024), read 2026-11-24: Bitė Group selected Nokia's Packet Core (2G-5G) for Lithuania and Latvia. "
                "DISPUTED between this and the core panel's Ericsson (Ericsson news, 17 May 2022, 'sole network supplier'); the Nokia "
                "release does not say it replaces Ericsson; coded the later selection"),
         first_contract=V('2022-05', DT_BITE, 'Ericsson sole nationwide RAN deal (2022-2028) announced May 2022'),
         vendor_operates=ND()),
    dict(region='Central Asia & Eastern Europe', country='Lithuania', operator_name='Tele2 Lithuania', core_operator_id='LT-tele2',
         name_note='core panel name Tele2',
         share=ND(LT_SHARE_NOTE),
         launch=ND("no Tele2 Lithuania commercial 5G launch date in the evidence; RRT required auction winners to start 5G in 2023; discovery status 'unclear'"),
         ran5=[R('Nokia', 'all', NOKIA_TELE2_BALTICS, TELE2_BALTICS_NOTE)],
         ran4=[R('Nokia', 'all', LR_NSN_TELE2, NSN_NOTE)],
         gov=[], gov_note='no state holder of 5% or more in Tele2 AB',
         gov_dropped=['Norges Bank Investment Management 1.69% of Tele2 AB (Nov 2026; board seat not checked)'],
         core=V('Nokia', TELE2_CORE, '5G core for Sweden and the Baltics (Jan 2021)'),
         first_contract=V('2021-01', TELE2_CORE, 'Nokia 5G core partnership for Sweden and the Baltics announced Jan 2021'),
         vendor_operates=ND()),
]
