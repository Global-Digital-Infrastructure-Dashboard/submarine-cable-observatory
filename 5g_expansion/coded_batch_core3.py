"""Core-94 migration, batch core3 (Prof. Shen, 2026-11): Sweden, Norway and Denmark (10 operators) re-coded in the
expansion's three-file format, in-session on 2026-11-24, following the calibration batch (coded_batch_core1.py).

Inputs: the core panel (data/5g_operator_panel.csv) and its cached vendor/ownership searches (data/5g_searches.jsonl),
plus mig|mktshare|<market>, mig|share|<id> and mig|ran|<id> (data/5g_expansion_searches.jsonl). Government stakes
re-express gov_stakes_core.py's per-holder rows. Share categories follow the user's 2026-11-23/24 rules (stated % ->
all/most/some/small; 'sole'/'exclusively' -> all; basis and date in the note). Every share category and computed
figure was checked against the primary page at coding time (5g_expansion/verify_2026-11-24_core3.csv).

Shared networks: Tele2 Sweden and Telenor Sweden run one RAN through Net4Mobility (50/50), coded on both rows;
TT-Network is the single row for the Danish joint network of Telenor Denmark and Norlys (ex-Telia Denmark), per the
core panel's researcher decision.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

register(domains={
    'company': ['telenor.com', 'telenor.no', 'tele2.com', 'tele2iot.com', 'teliacompany.com', 'telia.se', 'telia.dk', '3.dk',
                'tdcnet.dk', 'tdcnet.com', 'mavenir.com', 'live.euronext.com', 'kommunikasjon.ntb.no', 'regnskaber.cvrapi.dk'],
    'government': ['nkom.no', 'pts.se', 'digst.dk', 'ens.dk'],
    'news': ['mobileeurope.co.uk', 'fierce-network.com', 'sdxcentral.com', 'computerweekly.com', 'cphpost.dk', 'thelocal.dk'],
})

TELIA_SHAREHOLDINGS = 'https://www.teliacompany.com/en/articles/shareholdings'
TELIA_AR25 = 'https://www.teliacompany.com/downloads/u5c1v3pt22v8/5rdR72LuLgRQ5Ge4bOprhJ/1d446df8ad766c19090613b162b24952/Telia_Annual_report_2025.pdf'
TELENOR_SHARE = 'https://www.telenor.com/who-we-are/corporate-governance/telenors-share-and-shareholders/'
TELENOR_AR25 = 'https://live.euronext.com/sites/default/files/company_press_releases/attachments_oslo/2026/03/26/669362_Annual%20Report%202025%20-%20English.pdf'
LR_TELIA_CORE = 'https://www.lightreading.com/5g/telia-picks-nokia-for-standalone-5g-core-in-six-markets'
LR_SE_SWAP = 'https://www.lightreading.com/5g/huawei-swap-out-starts-after-sweden-s-5g-auction'
LR_N4M = 'https://www.lightreading.com/5g/nokia-highlights-new-4g-and-5g-role-at-sweden-s-net4mobility'
TP_SE_LAUNCH = 'https://www.telecompaper.com/news/tele2-telia-and-3-sweden-announce-5g-networks-launches--1339788'
TELE2_5G_VENDORS = 'https://www.tele2.com/media/news/2021/tele2-and-telenor-win-swedish-5g-frequencies-and-choose-ericsson-and-nokia-as-vendors-for-their-nationwide-5g-rollout/'
NKOM_2025 = ('https://nkom.no/statistikk/statiske-rapporter-og-analyser/_/attachment/inline/043adde1-4792-47a1-821d-66c645086e35:'
             'b7fc0f6620b59e582343a7589cd4205753a4aa2b/Ekomstatistikken%202025%20(2).pdf')
NKOM_NOTE = ('Nkom, Ekomstatistikken 2025 (p.13, figure 9): share of mobile telephony subscriptions at end-2025 (private and business '
             'combined); Telenor Norge 40.4, Telia Norge 32.8, Lyse 17.1; the three together 90.4. Verified 2026-11-24')
LR_EUROBITES = 'https://www.lightreading.com/5g/eurobites-huawei-loses-telenor-to-ericsson'
TELENOR_SELECTION = 'https://www.telenor.com/media/newsroom/archive/telenor-completes-5g-vendor-selection-for-norway/'
LR_TELIA_NO = 'https://www.lightreading.com/5g/telia-norway-goes-all-ericsson-on-5g-and-dumps-huawei'
LR_DK_SWAP = 'https://www.lightreading.com/5g/goodbye-huawei-hello-ericsson-swap-out-gathers-pace'
PTS_NOTE = ("PTS publishes operator market shares (The Swedish Telecommunications Market 2023, figure 8; online tables), but the "
            "searches did not return the operator figures and both PTS files were blocked to automated download on 2026-11-24 "
            "(UNVERIFIED); the four network operators together held 96% of mobile subscriptions at 31 Dec 2023")
N4M_NOTE = 'Net4Mobility, the 50/50 Tele2-Telenor joint venture, builds and runs the shared 2G/4G/5G RAN for both operators'


def n4m_ran5():
    return [R('Ericsson', 'not_disclosed', TELE2_5G_VENDORS,
              "Net4Mobility chose Ericsson and Nokia for the joint nationwide 5G RAN (20 Jan 2021); no split stated. " + N4M_NOTE),
            R('Nokia', 'not_disclosed', LR_N4M,
              "five-year deal to roll out 5G across 'significant areas of Sweden' (May 2021); no share stated. Verified 2026-11-24")]


def n4m_ran4():
    return [R('Huawei', 'all', LR_SE_SWAP,
              "before the 2021 replacement: 'the joint venture has relied exclusively on Huawei in the RAN' (Light Reading, Jan 2021; "
              "RAN basis, not a percentage). Historical. Verified 2026-11-24"),
            R('Nokia', 'not_disclosed', LR_N4M,
              "Nokia 'will replace the incumbent vendor's 4G network' (May 2021); its 4G share after the swap is not stated. Verified 2026-11-24")]


def n4m_switch():
    return [S('RAN', '4G', 'Huawei', 'Nokia', '2021-05', 'deadline 2025-01-01', LR_N4M,
              "Nokia replaces Huawei's 4G network at Net4Mobility; PTS licence conditions required Huawei/ZTE equipment out by "
              "1 Jan 2025; completion not confirmed in the evidence. Verified 2026-11-24")]


def telenor_gov(chain, parent_pct=None, pct=53.97, as_of='2026-02-27', url=TELENOR_SHARE, note=''):
    return [G('Norway', 'Government of Norway', 'government_ministry', pct, 'Telenor ASA', 'via_parent', as_of, url,
              "the Norwegian state's holding is managed by the Ministry of Trade, Industry and Fisheries. " + note,
              parent_pct=parent_pct, chain=chain)]


def telia_gov(basis='via_parent', chain='', url=TELIA_AR25, as_of='2025-12-31'):
    kw = dict(chain=chain) if basis == 'via_parent' else {}
    return [G('Sweden', 'Swedish State', 'government_ministry', 41.1, 'Telia Company AB', basis, as_of, url,
              'largest shareholder of the listed parent', **kw)]


FOLKETRYGD_NOTE = ("Folketrygdfondet meets Prof. Shen's pension rule (2026-11-26: owned by the state alone, board appointed by the "
                   "Ministry of Finance, Lov om Folketrygdfondet) but holds under 5% of Telenor ASA, so it is listed below the threshold")
FOLKETRYGD_DROP = 'Folketrygdfondet (Government Pension Fund Norway) 4.35-4.76% of Telenor ASA (2025-26; meets the pension rule; board seat not checked)'

LYSE_AR = ('https://live.euronext.com/sites/default/files/company_press_releases/attachments_oslo/2026/03/25/'
           '669268_Lyse%20%C3%85rsrapport%202025.pdf')
LYSE_NOTE = "municipal shareholder of Lyse AS at 31 Dec 2025 (Lyse annual report 2025, p.216 and p.251 shareholder table)"
LYSE_CHAIN = "Lyse AS 100% of Ice Communication Norge AS and of Ice Norge AS (annual report 2025, p.247 subsidiary list)"

OPERATORS = [
    # ------------------------------------------------------------------ Sweden
    dict(region='Western Europe', country='Sweden', operator_name='Telia', core_operator_id='SE-telia', name_note='Telia Sverige (Telia Company AB)',
         share=ND(PTS_NOTE),
         launch=V(2020, TP_SE_LAUNCH, "first major commercial 5G network inaugurated in Stockholm on 25 May 2020 (Ericsson-powered); "
                  "matches the discovery list (2020-05). Verified 2026-11-24"),
         ran5=[R('Ericsson', 'not_disclosed', LR_TELIA_CORE,
                 "five-year 'multi-billion' krona 5G RAN deal for Sweden and Estonia covering 10,000 sites (Oct 2020). UNVERIFIED: the "
                 "search calls Ericsson the 'sole supplier', but the two pages checked (Light Reading Oct 2020 and Jan 2021) say only "
                 "that Ericsson won the Swedish 5G RAN / is 'a domestic supplier of 5G RAN'")],
         ran4=[R('Ericsson', 'not_disclosed', LR_TELIA_CORE, "the same deal 'involves modernizing the existing 4G networks'; 4G share not stated")],
         gov=telia_gov(basis='direct', url=TELIA_SHAREHOLDINGS, as_of='2026-06-30'),
         gov_dropped=['Norges Bank 1.7% of Telia Company AB (2026-06-30; board seat not checked)'],
         core=V('Nokia', LR_TELIA_CORE, "Telia's CEO: Nokia 'is our sole supplier of 5G standalone core in all markets' (Oct 2020). Verified 2026-11-24"),
         first_contract=ND('Ericsson and Nokia deals announced Oct 2020, after the May 2020 launch'),
         vendor_operates=ND()),
    dict(region='Western Europe', country='Sweden', operator_name='Tele2', core_operator_id='SE-tele2', name_note='Tele2 Sverige AB',
         share=ND(PTS_NOTE),
         launch=V(2020, TP_SE_LAUNCH, 'own 5G network switched on 24 May 2020, available to customers from 24 Jun 2020 (Stockholm, '
                  'Gothenburg, Malmo); matches the discovery list (2020-05). Verified 2026-11-24'),
         ran5=n4m_ran5(), ran4=n4m_ran4(),
         gov=[], gov_note='no state holder at 5% or more (largest holder Freya Investissement, 19.8% of capital; Tele2 annual report 2025)',
         gov_dropped=['Norges Bank Investment Management 1.6% of Tele2 AB (2025-12-31; board seat not checked)'],
         core=V('Nokia', 'https://www.tele2.com/media/news/2021/tele2-partners-with-nokia-for-5g-core-deployment-in-sweden-and-the-baltics/',
                '5G core for Sweden and the Baltics (2021); Nokia cloud also supports the 4G core functions'),
         first_contract=ND('Ericsson/Nokia 5G RAN selection announced 20 Jan 2021, after the 2020 launch'),
         vendor_operates=ND('Tele2 says it operates and monitors its Swedish 5G network from Sweden; no vendor-run operations stated'),
         switches=n4m_switch()),
    dict(region='Western Europe', country='Sweden', operator_name='Telenor Sweden', core_operator_id='SE-telenor', name_note='core panel name Telenor; brand Vimla',
         share=ND(PTS_NOTE + '; Telenor reports 3.0m Swedish mobile subscribers at 31 Dec 2024 without a share'),
         launch=V(2020, TP_SE_LAUNCH, "Telenor Sweden activated 5G in central Stockholm on 29 Oct 2020 (Telecompaper item on the same page). "
                  "The search's '24 May 2020' is Tele2's switch-on, not Telenor's. Verified 2026-11-24"),
         ran5=n4m_ran5(), ran4=n4m_ran4(),
         gov=telenor_gov('Telenor ASA -> Telenor Sverige; percentage not stated (the core panel treats it as wholly owned)'),
         gov_note=FOLKETRYGD_NOTE, gov_dropped=[FOLKETRYGD_DROP],
         core=ND('no Telenor Sweden or Net4Mobility core vendor named'),
         first_contract=ND(), vendor_operates=ND(),
         switches=n4m_switch()),
    dict(region='Western Europe', country='Sweden', operator_name='Tre', core_operator_id='SE-tre', name_note='Hi3G Access AB; brands Tre, 3, Hallon',
         share=ND(PTS_NOTE),
         launch=V(2020, TP_SE_LAUNCH, "5G brought on stream in the centres of Malmo, Lund, Helsingborg, Vasteras, Uppsala and western Stockholm "
                  "in June 2020. DISPUTED: the same item says this expands 'the public 5G network it launched in Arsta/Enskede ... in "
                  "December 2019, when it announced testing'; coded 2020 as the first launch not described as testing. 5G SA followed in "
                  "Dec 2025 (Ericsson). Verified 2026-11-24"),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2026/1/three-sweden-launches-ericsson-powered-commercial-5g-sa',
                 'Ericsson RAN in the 5G SA network launched Dec 2025 (announced 19 Jan 2026); Tre earlier said it had several suppliers; no share stated')],
         ran5_note='Nokia as a 5G RAN supplier appears only on Wikipedia, which is not cited',
         ran4=[R('Huawei', 'not_disclosed', LR_SE_SWAP, "Hi3G Access 'reportedly uses a mixture of Huawei and ZTE equipment in its RAN' (Jan 2021). Verified 2026-11-24"),
               R('ZTE', 'not_disclosed', LR_SE_SWAP, 'same report; no split stated. Verified 2026-11-24')],
         ran4_note='the LTE launch with ZTE (2012) and later switch to Huawei and Ericsson appear only on Wikipedia, so no switch row is coded',
         gov=[], gov_note='CK Hutchison (ultimate parent, Cayman Islands, Hong Kong-listed) has no state holder in the evidence', gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/2026/1/three-sweden-launches-ericsson-powered-commercial-5g-sa',
                'cloud-native 5G Core in the end-to-end Ericsson 5G SA network (Dec 2025)'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Norway
    dict(region='Western Europe', country='Norway', operator_name='Telenor Norge', core_operator_id='NO-telenor-norge',
         share=V(40.4, NKOM_2025, NKOM_NOTE, 2025),
         launch=V(2020, TELENOR_SELECTION, "Telenor said (13 Dec 2019) it would 'ramp up the roll out of 5G to our customers in Norway in 2020'; "
                  'exact commercial launch date not found; the discovery list gives 2020-03'),
         ran5=[R('Ericsson', 'not_disclosed', TELENOR_SELECTION,
                 "'Ericsson will modernise and build the Telenor's 5G radio access network' (13 Dec 2019); modernisation over 4-5 years. "
                 "The search's 'sole vendor' wording is not used: Telenor's own release keeps Huawei for 5G in selected areas (verified 2026-11-24)"),
               R('Huawei', 'not_disclosed', TELENOR_SELECTION,
                 "Telenor 'will use equipment from existing RAN vendor Huawei to maintain the 4G network and also upgrade to 5G coverage in "
                 "selected areas of Norway' during the modernisation (13 Dec 2019); no completion of the phase-out confirmed")],
         ran4=[R('Huawei', 'all', LR_EUROBITES, "Huawei 'came in as Telenor's sole RAN vendor during the 4G era' (Light Reading, 13 Dec 2019; "
                 "RAN basis). Verified 2026-11-24")],
         gov=telenor_gov('Telenor ASA -> Telenor Norge; percentage not stated (the core panel treats it as wholly owned)'),
         gov_note=FOLKETRYGD_NOTE,
         gov_dropped=[FOLKETRYGD_DROP, 'Kuwait Investment Authority 0.53% of Telenor ASA (2026-02-27; board seat not checked)'],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/2018/11/telenor-selects-ericsson-for-5g-core-network-transformation',
                "Ericsson selected for the 5G core transformation (Nov 2018); Telenor's Dec 2019 release says the core is upgraded through "
                'agreements with Nokia and Ericsson'),
         first_contract=V('2018-11', 'https://www.ericsson.com/en/press-releases/2018/11/telenor-selects-ericsson-for-5g-core-network-transformation',
                          'Ericsson 5G core agreement announced Nov 2018 (Norway, Sweden, Denmark); signing date not stated'),
         vendor_operates=V(False, TELENOR_SELECTION, "'The full mobile network, including core, is planned, operated and managed by Telenor "
                           "Norway' (13 Dec 2019). Verified 2026-11-24"),
         switches=[S('RAN', '5G', 'Huawei', 'Ericsson', '2019-12-13', 'not_confirmed', TELENOR_SELECTION,
                     'Ericsson to modernise and build the RAN over 4-5 years, Huawei kept for 4G and selected 5G areas meanwhile; Huawei '
                     'had been the sole 4G RAN vendor. Completion not confirmed in the evidence')]),
    dict(region='Western Europe', country='Norway', operator_name='Telia Norge', core_operator_id='NO-telia-norge',
         share=V(32.8, NKOM_2025, NKOM_NOTE, 2025),
         launch=V(2020, 'https://www.ericsson.com/en/news/3/2020/telia-norway-launches-commercial-5g-powered-by-ericsson',
                  'commercial 5G from 12 May 2020 in Lillestrom and parts of Groruddalen (Oslo region); matches the discovery list (2020-05)'),
         ran5=[R('Ericsson', 'all', LR_TELIA_NO, "Telia Norway 'will build a 5G radio network using Sweden's Ericsson as its sole supplier' "
                 "(Light Reading, Oct 2019; RAN basis). Verified 2026-11-24")],
         ran4=[R('Huawei', 'not_disclosed', LR_TELIA_NO, "Huawei 'currently supplies 4G products' (Oct 2019) and is to be phased out; share not stated")],
         gov=telia_gov(chain='Telia Company AB -> Telia Norge AS; percentage not stated (the core panel treats it as wholly owned)'),
         gov_dropped=[],
         core=V('Nokia', LR_TELIA_CORE, "Nokia is Telia's 'sole supplier of 5G standalone core in all markets' (Oct 2020); Nokia also "
                "supplied the cloud packet core (2018). Verified 2026-11-24"),
         first_contract=V('2019-10', 'https://www.ericsson.com/en/press-releases/2019/10/telia-norway-selects-ericsson-as-sole-5g-ran-provider',
                          'Ericsson selected as sole 5G RAN provider (press release, Oct 2019); signing date not stated'),
         vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Huawei', 'Ericsson', '2019-10', 'not_confirmed', LR_TELIA_NO,
                     "Ericsson to phase out other vendors' equipment: 'Up until 2023 [that] will be changed out so there is a full Ericsson "
                     "network on the radio side'; completion not confirmed. Verified 2026-11-24")]),
    dict(region='Western Europe', country='Norway', operator_name='Ice', core_operator_id='NO-ice-communication-norge',
         name_note='core panel name Ice Communication Norge; Nkom reports it in the Lyse group',
         share=V(17.1, NKOM_2025, NKOM_NOTE + '; the 17.1% is the Lyse group, which owns Ice', 2025),
         launch=ND('no commercial 5G launch date found in the evidence'),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.mobileeurope.co.uk/nokia-wins-5-year-5g-ice-norway-deal/',
                 "five-year contract (Jul 2022) for the 4G and 5G radio network: AirScale Single RAN, base stations and Massive MIMO. The "
                 "search's 'exclusively Nokia' for 5G is not used: the annual-report sentence covers 2G, 3G and 4G only (verified 2026-11-24)")],
         ran4=[R('Nokia', 'all', 'https://kommunikasjon.ntb.no/ir-files/17847219/1327/1778/Annual%20Report%202021.pdf',
                 "'for 2G, 3G and 4G networks, Ice has on its own initiative chosen to exclusively use Nokia' (Ice Group annual report 2021, "
                 "p.38). Verified 2026-11-24")],
         ran4_note='the 2014 Alcatel-Lucent LTE contract is not coded as a switch (Alcatel-Lucent became part of Nokia in 2016)',
         gov=[G('Norway', f'{m} kommune', 'government_ministry', pct, 'Lyse AS', 'via_parent', '2025-12-31', LYSE_AR,
                LYSE_NOTE, parent_pct=100.0, chain=LYSE_CHAIN, level='local')
              for m, pct in (('Stavanger', 45.74), ('Sandnes', 19.53), ('Sola', 8.74), ('Time', 5.83))],
         gov_note=("local government (Prof. Shen, 2026-11-26): Lyse AS is owned by 15 municipalities in Rogaland and Agder; its "
                   "articles allow only municipalities as shareholders, and the municipalities are represented on the group board "
                   "(Lyse annual report 2025, pp. 98, 216, 251; read directly 2026-11-26). This replaces the earlier 'not coded': the "
                   "ownership search's A1/America Movil chain is wrong for Ice since Lyse's takeover"),
         gov_dropped=[f'{m} kommune {pct}% of Lyse AS (2025-12-31; local government; board seat not checked)'
                      for m, pct in (('Klepp', 4.23), ('Hå', 3.78), ('Randaberg', 3.28), ('Eigersund', 2.95), ('Strand', 2.53),
                                     ('Hjelmeland', 0.99), ('Gjesdal', 0.93), ('Lund', 0.71), ('Bjerkreim', 0.51), ('Suldal', 0.12),
                                     ('Sirdal', 0.12))],
         core=V('Mavenir', 'https://www.mavenir.com/press-releases/mavenirs-converged-packet-core-powering-ice-norways-4g-and-5g-network/',
                "converged packet core for 4G, 5G NSA and 5G SA (9 Feb 2023); an earlier Nokia AirFrame core agreement existed, and whether "
                'Mavenir replaced it is not stated'),
         first_contract=ND(), vendor_operates=ND('Nokia NetAct supports network management; operations by Nokia not stated')),
    # ------------------------------------------------------------------ Denmark
    dict(region='Western Europe', country='Denmark', operator_name='TDC NET', core_operator_id='DK-tdc-net',
         name_note='TDC NET A/S, the network company of the former TDC (retail brands sit with Nuuday)',
         share=ND("no regulator figure by operator in the evidence (the Danish Agency for Digital Government's background tables were "
                  "not returned); TDC NET is a wholesale network company"),
         launch=V(2020, 'https://www.ericsson.com/en/news/2020/9/tdc-denmark-goes-live-with-ericsson-5g',
                  'TDC went live with Ericsson 5G in Sep 2020 (7 Sep per Ericsson case material); nationwide by Dec 2020'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.sdxcentral.com/news/ericsson-ousts-huawei-as-tdcs-5g-vendor-in-denmark/',
                 "Ericsson to supply equipment and services for the 5G network (Mar 2019). UNVERIFIED: Ericsson's case study calls it TDC "
                 "NET's 'sole supplier' for 2G-5G RAN and core, but ericsson.com returned 403")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.sdxcentral.com/news/ericsson-ousts-huawei-as-tdcs-5g-vendor-in-denmark/',
                 "Ericsson takes over 'maintaining and expanding TDC's LTE network' (Mar 2019). Verified 2026-11-24"),
               R('Huawei', 'not_disclosed', 'https://www.sdxcentral.com/news/ericsson-ousts-huawei-as-tdcs-5g-vendor-in-denmark/',
                 'six-year LTE deal signed in 2014 (historical); share not stated. Verified 2026-11-24')],
         gov=[G('Denmark', 'Arbejdsmarkedets Tillægspension (ATP)', 'pension_fund', 16.7, 'DKT Holdings ApS', 'via_parent', '2022-12-31',
                'https://tdcgroup.com/media/qaidx3mm/dkth_annual-report-2022.pdf',
                "DKT Holdings annual report 2022, p.3 (latest shareholder split found). TDC NET's 2025 annual report (signed 5 Mar 2026, "
                "p.33) still names ATP, PKA and PFA as owners of 50% and Macquarie's May 2025 agreement to buy them out as pending; "
                "no completion found. Pension rule (2026-11-26): ATP was established by law in 1964 and the Minister of Employment "
                "appoints its boards (atp.dk)",
                chain='DKT Holdings ApS -> DK Telekommunikation ApS (100%) -> TDC Holding A/S (100%) -> TDC NET A/S (100%)')],
         gov_note=("PFA (16.7% of DKT Holdings via PFA Ophelia InvestCo I 2018 K/S) does not meet the pension rule (checked "
                   "2026-11-26): PFA Holding is owned by the PFA Foundation and its 1917 founding organisations, and its board is "
                   "elected by the annual general meeting (english.pfa.dk). PKA (16.7% via PKA Ophelia Holding K/S, managed by AIP "
                   "Management P/S) is NOT CONFIRMED either way: pka.dk renders its board and ownership pages only with JavaScript "
                   "and no statute or annual report of the PKA funds was found, so it is not coded pending a source. DISPUTED timing: if Macquarie's purchase has "
                   "closed, ATP is no longer a holder; the Danish company register (CVR 39186829) was not reachable by script"),
         gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/3/2023/ericsson-and-tdc-net-launch-first-5g-standalone-network-in-denmark',
                'dual-mode 5G core; first 5G SA network in Denmark (Aug 2023)'),
         first_contract=V('2019-03', 'https://www.sdxcentral.com/news/ericsson-ousts-huawei-as-tdcs-5g-vendor-in-denmark/',
                          'TDC selected Ericsson for its 5G network (19 Mar 2019 announcement)'),
         vendor_operates=V(True, 'https://www.ericsson.com/en/press-releases/3/2023/tdc-net-chooses-ericsson-5g-technology-to-reach-net-zero-targets',
                           'Nov 2023 agreement covers 5G RAN plus managed services, network operations, optimisation and field operations '
                           'through 2027 (per the search; ericsson.com returned 403, not checked)'),
         switches=[S('RAN', '4G', 'Huawei', 'Ericsson', '2019-03', 'not_confirmed', LR_DK_SWAP,
                     "Light Reading's swap-out table: 'TDC Denmark Mar-19 Ericsson Huawei RAN - Swedish vendor to replace Huawei as TDC rolls "
                     "out 5G'; Ericsson's case study dates the full RAN swap to 2019-2020 (unverified, 403). Verified 2026-11-24")]),
    dict(region='Western Europe', country='Denmark', operator_name='3 Denmark', core_operator_id='DK-3-denmark', name_note='Hi3G Denmark ApS; brand OiSTER',
         share=V(17.8, 'https://www.3.dk/globalassets/om-3/om-virksomheden/csr-rapporter/3_csr_rapport_eng_2020_4a.pdf',
                 "3's own 2020 CSR report: 1.46m customers and a 17.8% mobile market share (2020); no regulator figure by operator found, "
                 'and the report gives no other operator; not checked against the PDF', 2020),
         launch=V(2020, 'https://www.telecompaper.com/news/3-denmark-to-start-5g-in-copenhagen-in-december-expects-nationwide-coverage-by-mid-2022--1362179',
                  'phasing in 5G in parts of Copenhagen from December 2020 (report of 17 Nov 2020); matches the discovery list (2020-12)'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://regnskaber.cvrapi.dk/xhtml/82808526/amNsb3VkczovLzAzLzBkLzBmL2JlLzhkLzdiZTAtNDk5My05M2RjLTQ2NjU0NGMyN2M0ZA.pdf',
                 "Ericsson Danmark's 2024 annual report (registry filing): Ericsson supplied 3 Denmark's 3G/4G/5G radio equipment in the "
                 'network modernisation; no share stated')],
         ran4=[R('Ericsson', 'not_disclosed', 'https://regnskaber.cvrapi.dk/xhtml/82808526/amNsb3VkczovLzAzLzBkLzBmL2JlLzhkLzdiZTAtNDk5My05M2RjLTQ2NjU0NGMyN2M0ZA.pdf',
                 'same filing (3G/4G/5G radio); no share stated')],
         ran5_note="the mig|ran search answered for TDC NET, Telenor and Telia instead of 3 Denmark, so it adds nothing here",
         gov=[], gov_note='CK Hutchison (ultimate parent) has no state holder in the evidence', gov_dropped=[],
         core=ND('no 3 Denmark core vendor named'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Western Europe', country='Denmark', operator_name='TT-Network', core_operator_id='DK-tt-network',
         name_note=('TT-Netvaerket (TTN; Telenor calls it TN-Netvaerket): the joint network of Telenor Denmark and Norlys (which bought Telia '
                    'Denmark on 2 Apr 2024); one row for the joint network, per the core panel researcher decision'),
         share=ND('no regulator figure by operator in the evidence; the Nordic-Baltic statistics give only the largest operator (42% in 2024)'),
         launch=ND("no TT-Network commercial launch date in the evidence (Telia said in Oct 2020 that Denmark would launch later that month)"),
         ran5=[R('Nokia', 'all', 'https://www.nokia.com/newsroom/nokia-readies-tnn-denmark-for-ai-powered-5g-future/',
                 "Nokia 'signs a new four-year extension with TNN as sole supplier of 5G RAN and managed services across Denmark' (10 Nov 2025; "
                 "RAN basis). Verified 2026-11-24")],
         ran4=[], ran4_note=("TTN's 4G vendor is not stated. Strand Consult says two of Denmark's three networks were 100% on untrusted "
                             'vendors (about 62% of subscribers) without naming them, so no switch is coded'),
         gov=telenor_gov("Telenor ASA 50% of the TT-Netvaerket joint operation; the other 50% owner's state holders are not in the evidence",
                         parent_pct=50.0, pct=54.0, as_of='2025-12-31', url=TELENOR_AR25,
                         note='Telenor annual report 2025: Norwegian state 54% at 31 Dec 2025; Danish network joint operation 50% Telenor.'),
         gov_note=("the Swedish state's 41.1% of Telia Company is not counted: Telia's Danish business was sold to Norlys on 2 Apr 2024 and "
                   'Telenor names only "the other party" as co-owner. ' + FOLKETRYGD_NOTE),
         gov_dropped=[FOLKETRYGD_DROP],
         core=ND('no TT-Network core vendor named'),
         first_contract=V('2021-06', 'https://www.computerweekly.com/news/252502637/Telenor-Telia-tap-Nokia-for-5G-joint-network-roll-out-in-Denmark',
                          'TTN selected Nokia as sole 5G RAN vendor on 17 Jun 2021 (per the search; Computer Weekly returned 403, not checked)'),
         vendor_operates=V(True, 'https://www.nokia.com/newsroom/nokia-readies-tnn-denmark-for-ai-powered-5g-future/',
                           "Nokia is TNN's supplier of '5G RAN and managed services across Denmark' (10 Nov 2025). Verified 2026-11-24")),
]
