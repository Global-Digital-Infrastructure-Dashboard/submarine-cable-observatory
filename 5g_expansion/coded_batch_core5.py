"""Core-94 migration batch core5 (Prof. Shen, 2026-11): Switzerland, Ireland and Portugal (10 operators) re-coded in
the expansion's three-file format, in-session on 2026-11-24, following coded_batch_core1.py.

Inputs: the core panel and its cached vendor/ownership searches (data/5g_searches.jsonl), the market-level share search
mig|mktshare|<market> and the per-operator mig|share / mig|ran searches (data/5g_expansion_searches.jsonl). Government
stakes re-express gov_stakes_core.py. Share categories: a stated % maps 100 = all, >50 most, 10-50 some, <10 small;
'sole'/'single vendor'/'all ... RAN products' wording maps to all; the note gives the basis and date. Every share
category and computed or re-dated figure was checked against the primary page at coding time
(5g_expansion/verify_2026-11-24_core5.csv).
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

register(domains={
    'company': ['swisscom.ch', 'sunrise.ch', 'salt.ch', 'huawei.com', 'eir.ie', 'three.ie', 'vodafone.ie', 'vodafone.pt', 'nos.pt',
                'meo.pt', 'bvb.ro', 'reports.investors.vodafone.com', 'eand.com'],
    'government': ['comcom.admin.ch', 'bakom.admin.ch', 'comreg.ie', 'anacom.pt', 'digital-strategy.ec.europa.eu'],
    'research_industry_group': ['analysysmason.com'],
    'news': ['rte.ie', 'irishtimes.com', 'swissinfo.ch', 'fiercewireless.com', 'techtimes.com', 'mobileeurope.co.uk', 'computerweekly.com',
             'lightreading.com'],
    'other': ['lukekehoe.com', 'cenerva.com'],
})

VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
VOD_DROPPED = ['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)']
ASSUMED = 'percentage of the operating subsidiary not stated; the earlier coding treated it as wholly owned'
EC_VOD = 'https://digital-strategy.ec.europa.eu/en/miscellaneous/vodafone-and-ericsson-sign-five-year-deal-deploy-programmable-5g-networks'
LR_VOD_TENDER = 'https://www.lightreading.com/open-ran/vodafone-site-tender-looks-badly-delayed-and-diminished'
VOD_ALL_NOTE = ("Light Reading: 'Ireland and Portugal, where Ericsson has previously supplied all Vodafone's RAN products' (not split by "
                "generation); under the 14 Oct 2025 agreement Ericsson 'will become Vodafone's sole radio access network (RAN) vendor' "
                "there (EC digital-strategy page, verified)")


def vod_gov(chain):
    return [G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 17.005026, 'Vodafone Group Plc',
              'via_parent', '2026-03-31', VODAFONE_AR,
              "Vodafone names e& without calling it state-owned; e&'s 2025 integrated report gives the Emirates Investment Authority 60%, "
              "ultimately controlled by the UAE Federal Government", link_url=E_AND_AR, chain=chain)]


# ---------------------------------------------------------------- market shares
COMCOM = 'https://www.comcom.admin.ch/en/market-share'
COMCOM_NOTE = ("ComCom, citing OFCOM's Statistical Observatory: share of mobile customers at end-2024 (Swisscom 53.1, Sunrise 23.6, "
               "Salt 17.7, others 5.5), including each operator's secondary brands; verified on the page")
COMREG = 'https://www.comreg.ie/industry/electronic-communications/market-information/quarterly-key-data-report/quarterly-key-data-report-q1-2026'
COMREG_NOTE = ("ComReg Quarterly Key Data Report, Q1 2026, mobile subscriptions excluding mobile broadband and M2M (eir 24.9, Three 27.6, "
               "Vodafone 32.0; including MBB/M2M: 14.6 / 49.9 / 26.6). UNVERIFIED: the ComReg page redirects without content under curl; "
               "the per-operator search labels eir's 24.9 as Q2 2026, so the quarter is Q1 or Q2 2026")
NOS_DECK = 'https://www.nos.pt/content/dam/nos/institucional/investidores/investidores_pt/apresenta%C3%A7%C3%B5es/apresentacoes/InstitutionalPresentation_20260331.pdf'
PT_NOTE = ("ANACOM mobile market share by subscriptions as reproduced in NOS's FY2025 institutional presentation (p.23, 'Source: ANACOM'), "
           "4Q25: MEO 36.0, NOS 31.1, Vodafone 27.6, Digi 3.3 (verified). WRONG in the market-level search: it gave MEO 36.9 / NOS 30.6 / "
           "Vodafone 28.0 / Digi 2.5 as 4Q25, but those are the deck's 4Q24 column. ANACOM's own Q3 2023 report (403 under curl) gave "
           "MEO 38.4 / NOS 29.5 / Vodafone 28.2 of active mobile accesses")

OPERATORS = [
    # ------------------------------------------------------------------ Switzerland
    dict(region='Western Europe', country='Switzerland', operator_name='Swisscom', core_operator_id='CH-swisscom',
         share=V(53.1, COMCOM, COMCOM_NOTE, 2024),
         launch=V(2019, 'https://www.swisscom.ch/content/dam/swisscom/en/about/news/2019/02/08-5g-start/08-5g-start-en.pdf',
                  "Swisscom's 5G start announcement (2019); the discovery list gives 2019-04"),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/news/2024/4/swisscom-selects-ericsson-to-future-proof-mobile-network',
                 "Ericsson selected for 5G RAN products under a multi-year agreement (11 Apr 2024). UNVERIFIED: an Ericsson case study "
                 "(Aug 2025) reportedly says '100% Ericsson Radio Access Network', but ericsson.com returned 403, so no share category")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/cases/2025/swisscom-and-ericsson-performance-partnership-driving-network-leadership',
                 "Ericsson solutions cover Swisscom's 4G LTE and 5G NR networks per the search answer. UNVERIFIED (403)")],
         gov=[G('Switzerland', 'Swiss Confederation', 'government_ministry', 51.0, 'Swisscom Ltd', 'direct', '2025-12-31',
                'https://www.swisscom.ch/content/dam/assets/about/investoren/berichte/documents/2026/financial-statements-2025-swisscom-ltd.pdf',
                '2025 financial statements; Swisscom is a special-status company under the Telecommunications Enterprise Act')],
         gov_dropped=[],
         core=V('Ericsson', 'https://www.lightreading.com/mobile-core/ericsson-cloud-boss-still-resists-a-nokia-move-in-the-5g-core',
                "Light Reading: Ericsson's core network applications on its cloud infrastructure are live at Swisscom (verified); Swisscom "
                "had moved its first million customers to a '5G SA Dual Mode Core' by Q2 2026. The core panel cited an aggregator (factrail.ai)"),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('core', '4G', 'Nokia', 'Ericsson', '2015', 'not_confirmed',
                     'https://www.analysysmason.com/globalassets/x_migrated-media/media/analysys_mason_swisscom_ericsson_case_study_mar2018_rma184.pdf',
                     "Analysys Mason case study (Mar 2018): Ericsson became Swisscom's end-to-end partner in 2015, when Swisscom 'swapped out the "
                     "Nokia core'. UNVERIFIED: the PDF now returns 404; wording from the search answer")]),
    dict(region='Western Europe', country='Switzerland', operator_name='Sunrise', core_operator_id='CH-sunrise',
         share=V(23.6, COMCOM, COMCOM_NOTE, 2024),
         launch=V(2019, 'https://www.huawei.com/ch-en/news/2019/switzerland-first-5g-sunrise-commercial-march',
                  "Huawei (Feb 2019): Sunrise 5G for 150 cities/villages 'will be released in March this year'; the discovery list "
                  "records ComCom's April 2019 launch"),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.huawei.com/ch-en/news/2019/switzerland-first-5g-sunrise-commercial-march',
                 "Huawei 'provides end to end innovative 5G commercial solution, including radio access network, transport network and "
                 "core network' (verified); no sole-supplier wording for 5G. Bloomberg's 'all-Huawei Swiss carrier' (swissinfo, 2020) "
                 "could not be checked (page 404)")],
         ran4=[R('Huawei', 'all', 'https://www.huawei.com/en/news/2015/12/Sunrise%20Achieves%20High%20Scores%20in%20Leading%20Independent%20Mobile%20Benchmark%20Test%20with%20Huawei%20Solutions',
                 "Huawei (Dec 2015): Sunrise selected 'Huawei as single vendor on building radio network' (verified); Strand Consult via "
                 "Light Reading (Jun 2020) also lists Sunrise among single-supplier Huawei 4G RAN deals")],
         ran4_note="Huawei says Sunrise 'changed technology partner' in 2012; the previous vendor is named only in a personal profile, so no switch is coded",
         gov=[], gov_dropped=[],
         gov_note='listed on SIX since the Nov 2024 spin-off from Liberty Global; controlling holder John C. Malone (individual); no state holder',
         core=V('Huawei', 'https://www.huawei.com/ch-en/news/2019/switzerland-first-5g-sunrise-commercial-march',
                'Huawei end-to-end 5G solution including the core network (2019, verified); the later 5G SA core vendor is not named'),
         first_contract=ND(),
         vendor_operates=V(True, 'https://www.huawei.com/en/news/2015/12/Sunrise%20Achieves%20High%20Scores%20in%20Leading%20Independent%20Mobile%20Benchmark%20Test%20with%20Huawei%20Solutions',
                           "Huawei 'providing the managed service' (Dec 2015, verified); a 2026 report describes the Huawei partnership as "
                           "including operation and maintenance")),
    dict(region='Western Europe', country='Switzerland', operator_name='Salt', core_operator_id='CH-salt-mobile',
         name_note='core panel name Salt Mobile (Salt Mobile SA)',
         share=V(17.7, COMCOM, COMCOM_NOTE, 2024),
         launch=V(2020, 'https://www.comcom.admin.ch/dam/en/sd-web/50TMyzHwJSiQ/%EF%BF%BD%C3%BF%3Ci%3E%3Ca%20href=',
                  "ComCom records Salt going live with 5G in August 2020 (discovery search). The URL is malformed as returned by the "
                  "search and was not checked; Salt had planned a 5G launch for H2 2019"),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.salt.ch/sites/default/files/2020-08/20190129_PR_Salt_5G-Nokia_EN.pdf',
                 "letter of intent for Nokia to roll out 5G (29 Jan 2019). UNVERIFIED: the PDF is an image without extractable text")],
         ran5_note=("not coded: Huawei, brought on board in 2019 under a 'dual network supplier strategy' (Light Reading, Mar 2020) with no "
                    "stated scope; Salt's 2024 annual report mentions a RAN equipment swap without naming the supplier"),
         ran4=[R('Nokia', 'not_disclosed', 'https://www.lightreading.com/5g/eurobites-nokia-attempts-to-land-a-5g-patents-punch',
                 "Nokia described as Salt's existing supplier (Mar 2020)")],
         gov=[], gov_dropped=[],
         gov_note='privately held; controlling parent NJJ Continental Holding SA (Xavier Niel); no state holder found',
         core=ND("Salt's Jan 2019 release reportedly says it 'has chosen Nokia to upgrade its radio and mobile core network'; the PDF is an "
                 "image and was not verified, so the core stays not_disclosed as in the core panel"),
         first_contract=ND('Nokia letter of intent 29 Jan 2019 (not verified; an LOI rather than a contract)'), vendor_operates=ND()),
    # ------------------------------------------------------------------ Ireland
    dict(region='Western Europe', country='Ireland', operator_name='eir', core_operator_id='IE-eircom-limited',
         name_note='core panel name Eircom Limited; brands eir, GoMo',
         share=V(24.9, COMREG, COMREG_NOTE, 2026),
         launch=V(2019, 'https://www.irishtimes.com/business/technology/eir-very-happy-with-huawei-as-supplier-for-5g-network-1.4153946',
                  "Irish Times (28 Jan 2020): 'Eir's 5G network, launched last year' (verified); the discovery list has no date"),
         ran5=[R('Huawei', 'all', 'http://www.lukekehoe.com/a-breath-of-fresh-eir.html',
                 "analyst blog (Oct 2019): 'the enlistment of Huawei to become the sole RAN vendor across 2G, 3G, 4G and 5G' (verified); "
                 "RTÉ (12 Nov 2018) and the Irish Times (Jan 2020) confirm Huawei radio access equipment without sole-supplier wording")],
         ran4=[R('Huawei', 'all', 'http://www.lukekehoe.com/a-breath-of-fresh-eir.html', 'same source: sole RAN vendor across 2G-5G, single-RAN rebuild (verified)')],
         gov=[], gov_dropped=[],
         gov_note=("private: NJJ Holding SAS (Xavier Niel) via Carraun/Wexford; 49.99% non-controlling interests in eircom Holdings (Ireland) "
                   "have unidentified holders, so no state holder can be ruled out"),
         core=V('Ericsson', 'https://www.irishtimes.com/business/technology/eir-very-happy-with-huawei-as-supplier-for-5g-network-1.4153946',
                "'the \"more sensitive\" core network equipment was being supplied by Sweden's Ericsson' (Jan 2020, verified); the core "
                "panel had not_disclosed"),
         first_contract=V('2018-11-12', 'https://www.rte.ie/news/business/2018/1112/1010284-eir-network-investment/',
                          "EUR 150m mobile upgrade announced: 'Radio access network equipment will be supplied by Huawei, while Ericsson will "
                          "continue as strategic partner for the core network' (verified); announcement date, signing date not stated"),
         vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Ericsson', 'Huawei', '2018-11-12', 'not_confirmed', 'http://www.lukekehoe.com/a-breath-of-fresh-eir.html',
                     "single-RAN programme 'ripping out legacy kit from vendors such as Ericsson' (Oct 2019, verified); Huawei RAN announced "
                     "12 Nov 2018 (RTÉ); completion not stated")]),
    dict(region='Western Europe', country='Ireland', operator_name='Three Ireland', core_operator_id='IE-three-ireland-hutchison-limited',
         name_note='core panel name Three Ireland (Hutchison) Limited',
         share=V(27.6, COMREG, COMREG_NOTE, 2026),
         launch=V(2020, 'https://www.gsma.com/get-involved/gsma-membership/gsma_resources/ireland-puts-5g-in-the-fast-lane/',
                  'GSMA: Three Ireland switched on 5G in September 2020. UNVERIFIED (403); not stated in the discovery list'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.fiercewireless.com/operators/three-ireland-first-to-join-ericsson-s-startup-5g-program',
                 'May 2021: Three Ireland chose Ericsson rather than Huawei for 5G; GSMA says Ericsson rebuilt over 1,000 RAN deployments; no share wording')],
         ran4=[R('Samsung', 'not_disclosed', 'http://www.lukekehoe.com/mapping-ireland-and-europes-path-to-5g.html',
                 "analyst blog (Feb 2019): 'Samsung for 4G'; it also reports a plan to replace Samsung 4G kit with Huawei, which no "
                 "later source confirms, so no switch is coded. Not checked against the page")],
         ran4_note='Nokia 2100 MHz macro equipment appears only in 2016 ComReg licence records',
         gov=[], gov_dropped=[], gov_note='100% CK Hutchison (Li Ka-shing Unity Trust 26.26%); no state holder',
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/3/2023/three-ireland-launches-next-evolution-5g-network-capability-for-businesses',
                '5G Standalone capability powered by Ericsson (20 Dec 2023); matches the core panel'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Western Europe', country='Ireland', operator_name='Vodafone Ireland', core_operator_id='IE-vodafone-ireland-limited',
         name_note='core panel name Vodafone Ireland Limited',
         share=V(32.0, COMREG, COMREG_NOTE, 2026),
         launch=V(2019, 'https://n.vodafone.ie/aboutus/press/vodafone-ireland-switches-on-first-5g-network-in-five-cities.html',
                  "commercial 5G on 13 Aug 2019, Ireland's first (Vodafone release)"),
         ran5=[R('Ericsson', 'not_disclosed', LR_VOD_TENDER, VOD_ALL_NOTE + " [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]")],
         ran4=[R('Ericsson', 'all', LR_VOD_TENDER, VOD_ALL_NOTE)],
         gov=vod_gov('Vodafone Group Plc -> Vodafone Ireland; ' + ASSUMED), gov_dropped=VOD_DROPPED,
         core=ND('Vodafone describes a cloud-native 5G SA core across Europe without naming the Irish supplier'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Portugal
    dict(region='Western Europe', country='Portugal', operator_name='MEO', core_operator_id='PT-meo',
         share=V(36.0, NOS_DECK, PT_NOTE, 2025),
         launch=ND("MEO says 5G was available from 1 Jan 2022 in all district capitals and the Azores and Madeira; ANACOM says commercial "
                   "offers began at the end of 2021; no MEO-specific launch date"),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.mobileeurope.co.uk/portugals-meo-signs-multi-year-5g-ran-contract-with-nokia/',
                 'multi-year 5G RAN contract (8 Jul 2024, verified): AirScale Massive MIMO, baseband and RRH plus MantaRay SON; no share wording')],
         ran5_note="Huawei was MEO's sole RAN supplier before the Nokia deal (TechTimes, citing Reuters), but no source states its 5G share",
         ran4=[R('Huawei', 'all', 'https://www.techtimes.com/articles/305075/20240528/nokia-poised-take-over-meos-5g-equipment-supply-huawei-report.htm',
                 "'Huawei has been MEO's sole RAN supplier. In 2G, 3G, and 4G, Huawei has a 100% market share' (May 2024, citing Reuters; "
                 "verified; Reuters itself returned 401). Being replaced by Nokia")],
         gov=[], gov_dropped=[], gov_note='Altice group (Next Alt S.à r.l., Patrick Drahi); no state holder',
         core=ND("MEO says Huawei was never in its 5G core; the core vendor is not named"),
         first_contract=V('2024-07-08', 'https://www.mobileeurope.co.uk/portugals-meo-signs-multi-year-5g-ran-contract-with-nokia/',
                          'Nokia 5G RAN contract announcement; the earlier 5G network vendor contract is not dated in the evidence'),
         vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Huawei', 'Nokia', '2024-07-08', 'not_confirmed',
                     'https://www.mobileeurope.co.uk/portugals-meo-signs-multi-year-5g-ran-contract-with-nokia/',
                     "the contract 'includes replacing 2G and 4G infrastructure and upgrading 5G' (verified); Nokia to replace Huawei 'in some "
                     "key markets in Portugal' (Reuters, 27 May 2024); MEO is claiming EUR 81.7m from the state for the replacement")]),
    dict(region='Western Europe', country='Portugal', operator_name='NOS', core_operator_id='PT-nos',
         share=V(31.1, NOS_DECK, PT_NOTE, 2025),
         launch=ND('ANACOM: commercial 5G offers began at the end of 2021 (not operator-specific); no NOS-specific date'),
         ran5=[], ran5_note='5G RAN vendor not named in any source',
         ran4=[], ran4_note='a Huawei 4G network and an Ericsson-to-Huawei swap appear only in a personal profile (not cited)',
         gov=[], gov_dropped=['Mubadala Investment Company 3.202% of NOS (Sep 2026, MarketScreener; 5.00% at end-2024; board seat not checked)'],
         gov_note=("DATA-QUALITY CAVEAT (carried from the core panel): the Mubadala stake rests on a single third-party listing that disagrees "
                   "with NOS's own 30 Sep 2025 shareholder table; it is below 5% either way. Direct holders Sonaecom 37.37% and a ZOPT-linked "
                   "26.07% are private; ultimate parent not established"),
         core=V('Nokia', 'https://www.nokia.com/newsroom/nokia-announces-5g-core-deal-and-network-as-code-platform-agreement-with-nos-portugal-to-drive-monetization/',
                '5G core deal announced 30 Jan 2024; matches the core panel'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Western Europe', country='Portugal', operator_name='Vodafone Portugal', core_operator_id='PT-vodafone-portugal',
         share=V(27.6, NOS_DECK, PT_NOTE, 2025),
         launch=V(2021, 'https://www.vodafone.pt/en/press-releases/2022/2/vodafone-portugal-announces-q3-results.html',
                  'commercial 5G from 30 Nov 2021 (Vodafone Portugal)'),
         ran5=[R('Ericsson', 'not_disclosed', LR_VOD_TENDER, VOD_ALL_NOTE + " [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]")],
         ran4=[R('Ericsson', 'all', LR_VOD_TENDER, VOD_ALL_NOTE)],
         gov=vod_gov('Vodafone Group Plc -> Vodafone Portugal; ' + ASSUMED), gov_dropped=VOD_DROPPED,
         core=V('Mavenir', 'https://www.computerweekly.com/news/252515550/Mavenir-takes-5G-packet-core-Open-RAN-tech-to-operators-in-Portugal-India',
                'converged 4G/5G packet core (Computer Weekly, 5 Apr 2022); matches the core panel'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Western Europe', country='Portugal', operator_name='DIGI Portugal', core_operator_id='PT-digi-portugal',
         share=V(3.3, NOS_DECK, PT_NOTE + '. The 3.3% is labelled Digi in the deck; a press summary of the same ANACOM report gives it as DIGI and NOWO together', 2025),
         launch=V(2024, 'https://www.bvb.ro/infocont/infocont26/DIGI_20260430222641_Digi-Communications-N-V---2025-Annual-Report.pdf',
                  'own 2G/4G/5G network, commercial service from 4 Nov 2024 (Digi annual reports)'),
         ran5=[R('Nokia', 'not_disclosed', 'https://cenerva.com/5G-news/digi-on-track-for-early-2024-launch-partnering-nokia-ericsson-zte-says-report/',
                 "pre-launch report: 'dual Scandinavian mobile network suppliers Nokia and Ericsson', no split; ZTE for fixed equipment only"),
               R('Ericsson', 'not_disclosed', 'https://cenerva.com/5G-news/digi-on-track-for-early-2024-launch-partnering-nokia-ericsson-zte-says-report/',
                 'same report')],
         ran4=[], ran4_note="the same pre-launch report does not split Nokia and Ericsson by generation; Digi's filings list both only as group suppliers",
         gov=[], gov_dropped=[], gov_note='Digi Communications N.V. (private control); no state holder',
         core=ND(), first_contract=ND(), vendor_operates=ND()),
]
