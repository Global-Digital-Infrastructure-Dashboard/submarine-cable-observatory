"""Researcher coding of expansion batch 7 (Brazil, Suriname, Barbados, United Arab Emirates; 9 operators), coded in-session
on 2026-11-26 from the cached v2 searches in data/5g_expansion_searches.jsonl (plus core-panel cache entries for Telefónica's
and Telecom Italia's shareholders), under Prof. Shen's revised schema (see schema.py). Values come only from the cited
source; anything a source didn't state is not_disclosed. Share categories, computed figures and government stake
percentages were checked against the primary page at coding time; the per-fact log is
5g_expansion/verify_2026-11-26_batch7.csv (copies of the fetched pages in data/5g_direct/batch7/).
Not cited at all: Wikipedia, personal LinkedIn profiles, Scribd, eSIM/aggregator sites.

Batch notes:
- Brazil shares: Anatel's news releases in the cache are 2015-2016 data (pre-Oi breakup), so shares are computed from
  Anatel's own open-data access file (Sep 2026, all product types incl. M2M), read directly; Vivo's 20-F gives 38.1% at
  Dec 2025, matching the same file's Dec 2025 figure (38.10%).
- Huawei's share of Vivo/Claro/TIM 'networks' (Conexis via Light Reading, before May 2021) is a whole-network figure with
  no generation, so it is coded to 4G only (same rule as the core-panel TIM Italy decision of 2026-11-24).
- Launch dates: Claro and Vivo launched DSS 5G on LTE spectrum in July 2020, before the Nov 2021 auction; e& announced a
  commercial 5G network on 14 May 2018 (fixed-wireless service from Sep 2018, full mobile May 2019), coded 2018 as for
  Elisa (core panel). These are flagged for the lead researcher.
- e& and du: the Emirates Investment Authority is coded as a sovereign wealth fund holding directly (60% of e&, 50.1% of
  du). du's 19.7% holder DH 8 LLC (Dubai Holding's vehicle) is not coded: no source calls it state-owned and Dubai Holding
  is not on data/state_holders.csv.
"""
from schema import G, ND, R, V, register

CODED_AT = '2026-11-26'

ALGAR_AR = 'https://tic-cms-prod-br.s3.amazonaws.com/originals/report-algar-2022.pdf'
DU_AR = 'https://feeds.dfm.ae/documents/2026/Mar/19/9569a4e2-7b46-4b32-86c1-d71e637ed2b6/Du%20Integrated%20Annual.pdf'

register(
    domains={
        'government': ['anatel.gov.br', 'gov.br', 'uneca.org', 'digital-strategy.ec.europa.eu'],
        'company': ['sec.gov', 'telefonica.com', 'gruppotim.it', 'emarketstorage.it', 'cwc.com', 'digicelgroup.com', 'du.ae',
                    'eand.com', 'cision.com'],
        'news': ['lightreading.com', 'rcrwireless.com', 'mobileeurope.co.uk', 'khaleejtimes.com', 'cbc.bb', 'developingtelecoms.com'],
        'research_industry_group': ['ookla.com', 'comsoc.org', 'mtn-c.com', 'aiddata.org', 'samenacouncil.org', 'telegeography.com'],
    },
    overrides={
        # company reports hosted on a storage bucket and on the Dubai Financial Market's feed
        ALGAR_AR: 'company',
        DU_AR: 'company',
    },
)

# Brazil: Anatel open data, mobile accesses by economic group, September 2026 (computed by the researcher).
ANATEL_ZIP = 'https://www.anatel.gov.br/dadosabertos/paineis_de_dados/acessos/acessos_telefonia_movel.zip'
BR_NOTE = ("computed from Anatel open data (Acessos_Telefonia_Movel_2026_2S_Colunas.csv in the zip, read directly 2026-11-26), "
           "mobile accesses at Sep 2026 by economic group, all product types incl. M2M and points of service: Telefonica (Vivo) "
           "106,423,201; Telecom Americas (Claro) 92,817,027; Telecom Italia (TIM) 61,583,872; Algar 5,477,516; total 281,693,871 "
           "(Anatel's 3Q 2026 release: 280.5m). Dec 2025 from the same source: Vivo 38.10, Claro 33.11, TIM 22.92, Algar 1.86")
LR_TEF = 'https://www.lightreading.com/mobile-core/telef-nica-lining-up-5g-core-vendors-for-brazil'
CONEXIS = ("Conexis Brasil Digital via Light Reading (28 May 2021): Huawei equipment in {pct} of the operator's 'networks' "
           "(basis: share of network equipment, generation and element not stated; reported before May 2021). Whole-network "
           "share coded to 4G only (decision 2026-11-24, as for TIM Italy); verified")
OOKLA = ("Ookla (2026): 'Huawei supplies significant portions of the 5G radio access network (RAN) for the country's three big "
         "operators' (not a share category)")
RCR_LTE = 'https://rcrwireless.com/20130425/americas/brazils-oi-launches-lte-services-investments-reach-400m-2'
VIVO_20F = 'https://www.sec.gov/Archives/edgar/data/1066119/000207097926000018/viv-20251231.htm'
TIM_20F = 'https://www.sec.gov/Archives/edgar/data/1826168/000129281426001915/timbform20f_2025.htm'
TEF_CGR = 'https://www.telefonica.com/en/wp-content/uploads/sites/5/2026/02/Annual-Report-Corporate-Gobernance-2025.pdf'
VIVO_CHAIN = ("Telefónica, S.A. 39.32% of Telefônica Brasil directly, plus Telefónica Latinoamérica Holding 37.74% and Telefónica "
              "Chile 0.06%: 77.13% direct and indirect (Vivo 20-F, 31 Dec 2025)")
TIM_CHAIN = ('Telecom Italia S.p.A. -> Telecom Italia Finance S.A. 100% -> TIM Brasil Serviços e Participações S.A. 100% -> '
             '68.19% of TIM S.A. (TIM 20-F, 31 Dec 2025)')
# United Arab Emirates: operator-reported mobile customers at end-2025 (TDRA publishes no operator split; computed).
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
E_AND_Q4 = 'https://www.eand.com/content/dam/eand/assets/docs/earning-release/2025/earning-release-q4-2025-en.pdf'
UAE_NOTE = ("computed from operator reports, mobile customers at end-2025: e& UAE 14.6m (e& Q4 2025 earnings release) and du "
            "9.7m (du integrated annual report 2025); total 24.3m in the two-operator market (MVNO brands Virgin Mobile and Swyp "
            "run on du and e&). du itself reports a 39.9% mobile market share. TDRA publishes no operator shares")
MTNC_UAE = 'https://www.mtn-c.com/uae-the-first-5g-market-in-mena/'
TELEGEO = 'https://resources.telegeography.com/tracking-5g-deployments-in-the-middle-east-and-africa'
EIA_TYPE = ("holder_type sovereign_wealth_fund is a researcher classification (data/state_holders.csv: 'federal sovereign "
            "fund'); the state link is the operator's own statement that the EIA is ultimately controlled by the UAE Federal "
            "Government")

OPERATORS = [
    # ------------------------------------------------------------------ Brazil
    dict(region='Latin America & Caribbean', country='Brazil', operator_name='Vivo', name_note='Telefônica Brasil S.A. (brand Vivo)',
         share=V(37.78, ANATEL_ZIP, BR_NOTE + "; Vivo's 20-F: 38.1% at 31 Dec 2025 'according to information from ANATEL'", 2026),
         launch=V(2020, LR_TEF,
                  "Light Reading (28 May 2021): 'Vivo launched an early 5G network in July last year, utilizing dynamic spectrum sharing "
                  "(DSS) technology from Ericsson and Huawei' on surplus 3G/4G spectrum (verified); the source does not use the word "
                  "commercial. 3.5 GHz 5G followed the Nov 2021 auction (Anatel: 5G implementation began July 2022)"),
         ran5=[R('Ericsson', 'not_disclosed', LR_TEF, "DSS technology for the July 2020 early 5G network (verified)"),
               R('Huawei', 'not_disclosed', LR_TEF, "DSS technology for the July 2020 early 5G network (verified). " + OOKLA)],
         ran5_note=("Light Reading (May 2021) says Telefónica is 'moving away from Huawei' in Brazil; a 2022 tender to replace Huawei "
                    "benefiting Nokia (academic book, OAPEN) could not be fetched (403), so no Nokia row or switch is coded. Open RAN "
                    "work with Altiostar and Mavenir was pilots"),
         ran4=[R('Huawei', 'most', LR_TEF, CONEXIS.format(pct='65%')),
               R('Ericsson', 'not_disclosed', RCR_LTE, "RCR Wireless (25 Apr 2013): 'Vivo and Claro have chosen Ericsson and Huawei to supply "
                 "their LTE networks' (verified)")],
         gov=[G('Spain', 'Sociedad Estatal de Participaciones Industriales (SEPI)', 'state_holding_company', 10.0, 'Telefónica, S.A.',
                'via_parent', '2025-12-31', TEF_CGR, 'same figure as the core-panel Telefónica rows; state link from data/state_holders.csv',
                link='reference_list', chain=VIVO_CHAIN),
              G('Saudi Arabia', 'Public Investment Fund', 'sovereign_wealth_fund', 9.97, 'Telefónica, S.A.', 'via_parent', '2025-12-31',
                TEF_CGR, 'same figure as the core-panel Telefónica rows; state link from data/state_holders.csv', link='reference_list',
                chain=VIVO_CHAIN)],
         gov_note=("Telefónica's holdings in Vivo verified in Vivo's 20-F (31 Dec 2025). parent_pct is left empty because Telefónica holds "
                   "Vivo both directly (39.32%) and through subsidiaries; no Brazilian state holder"),
         gov_dropped=[],
         core=ND("Light Reading (May 2021): Mavenir, Nokia and Oracle are partners for the 'upcoming standalone 5G network' (a plan; "
                 "verified); the production 5G core or NSA EPC vendor is not stated"),
         first_contract=ND('the July 2020 DSS launch with Ericsson and Huawei has no contract date'),
         vendor_operates=ND("Ericsson's two-year managed-services contract (June 2005) predates 5G and no renewal was found; Ericsson's 2021 "
                            "deal is charging/BSS, not network operation")),
    dict(region='Latin America & Caribbean', country='Brazil', operator_name='Claro', name_note='Claro S.A. (América Móvil)',
         share=V(32.95, ANATEL_ZIP, BR_NOTE, 2026),
         launch=V(2020, 'https://www.samenacouncil.org/samena_daily_news?news=81748',
                  "SAMENA (11 Nov 2020): 'Claro launched 5G services in limited areas in Sao Paulo and Rio de Janeiro on July 14' [2020], "
                  "using Ericsson DSS on its LTE-A spectrum (verified). A government calendar lists a 'Lançamento do 5G – Claro' event on "
                  "30 Jun 2022 (3.5 GHz)"),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.samenacouncil.org/samena_daily_news?news=81748',
                 "Ericsson DSS for the July 2020 5G launch (verified)"),
               R('Huawei', 'not_disclosed', 'https://digital-strategy.ec.europa.eu/en/miscellaneous/claro-brasil-activates-5g-advanced-networks-major-sporting-venues',
                 "EC 5G Observatory (17 Oct 2025): Claro's 5G Advanced networks at sporting venues 'are powered by equipment from Ericsson, "
                 "Huawei and Nokia' (verified). " + OOKLA),
               R('Nokia', 'not_disclosed', 'https://digital-strategy.ec.europa.eu/en/miscellaneous/claro-brasil-activates-5g-advanced-networks-major-sporting-venues',
                 "same page (verified); SAMENA (Nov 2020) also says the '5G expansion plan will use gear from Ericsson, Nokia and Huawei'")],
         ran4=[R('Huawei', 'most', LR_TEF, CONEXIS.format(pct='55%')),
               R('Ericsson', 'not_disclosed', RCR_LTE, "RCR Wireless (25 Apr 2013): Claro chose Ericsson and Huawei for LTE (verified)"),
               R('Nokia', 'not_disclosed', 'https://rcrwireless.com/20171004/5g/brazil-deploys-lte-advanced-pro-toward-5g-tag5',
                 "RCR Wireless (4 Oct 2017): for LTE Advanced Pro 'Claro worked with suppliers Ericsson, Huawei and Nokia' (verified)")],
         gov=[], gov_note=("América Móvil holds Claro Brasil; its >5% holders are the Slim family and BlackRock (private), as for the batch 4 "
                           "Claro Dominicana row"),
         gov_dropped=['Norges Bank Investment Management 0.07% of America Movil (2025-12-31; board seat not checked)'],
         core=ND('no source names the 5G core or NSA EPC vendor'),
         first_contract=ND("Ericsson's 5 Aug 2020 DSS announcement (ericsson.com, 403) is a launch announcement after the 14 Jul 2020 "
                           "launch, not a contract date"),
         vendor_operates=ND('a Huawei managed-services project appears only in a personal LinkedIn profile (not cited)')),
    dict(region='Latin America & Caribbean', country='Brazil', operator_name='TIM', name_note='TIM S.A. (Telecom Italia group)',
         share=V(21.86, ANATEL_ZIP, BR_NOTE, 2026),
         launch=V(2022, TIM_20F,
                  "TIM 20-F 2025: '2022 was marked by the launch of 5G technology in Brazil ... We ended 2025 having launched 5G technology "
                  "in 1,089 cities' (verified); TIM's own launch date is not stated. TIM's Nov 2020 DSS use was a trial; it planned "
                  "3.5 GHz activations in all capitals by the July 2022 deadline (SAMENA, Dec 2021)"),
         ran5=[R('Ericsson', 'not_disclosed', 'https://www.rcrwireless.com/20211209/5g/tim-brasil-kicks-off-5g-network-rollout-ericsson-huawei-report',
                 "RCR Wireless (9 Dec 2021): 'TIM confirmed that Ericsson and Huawei will be the suppliers of equipment for its 5G network' (verified)"),
               R('Huawei', 'not_disclosed', 'https://www.rcrwireless.com/20211209/5g/tim-brasil-kicks-off-5g-network-rollout-ericsson-huawei-report',
                 "same report (verified); Feb 2026 contracts with Nokia and Huawei to swap 6,500 4G/5G sites (TIM 6-K). " + OOKLA),
               R('Nokia', 'not_disclosed', 'https://www.mobileeurope.co.uk/tim-brasil-picks-nokia-to-expand-5g-next-year/',
                 "Mobile Europe (19 Aug 2024): Nokia to 'expand its 5G RAN coverage across 15 Brazilian states from January 2025' (verified); "
                 "Nokia (2 Mar 2026) extends the partnership across 14 states")],
         ran5_note=("BNamericas (Aug 2024) reports Nokia and Huawei winning a new 5G tender at Ericsson's expense; UNVERIFIED (403), so no "
                     "vendor switch is coded"),
         ran4=[R('Huawei', 'some', LR_TEF, CONEXIS.format(pct='45%')),
               R('Ericsson', 'not_disclosed', RCR_LTE, "RCR Wireless (25 Apr 2013): 'TIM tapped Ericsson, Huawei and NSN as vendors' for LTE (verified)"),
               R('Nokia', 'not_disclosed', 'https://www.sec.gov/Archives/edgar/data/1826168/000129281426000489/timb20260224_6k1.htm',
                 "TIM 6-K (24 Feb 2026): 'Contracts signed with Nokia and Huawei • Swap of 6,500 4G/5G sites across 15 state capitals and "
                 "metropolitan areas through 2027' (verified; split between the two and the replaced vendor not stated); NSN named for "
                 "LTE in 2013 (RCR Wireless)")],
         gov=[G('Italy', 'Poste Italiane S.p.A.', 'state_owned_company', 86.952, 'Telecom Italia S.p.A.', 'via_parent', '2026-09-30',
                'https://www.gruppotim.it/en/investors/shares/shareholders.html',
                "same figure and state link as the core-panel TIM row (verified 2026-11-26): Poste rose from 27.32% (Dec 2025, TIM 20-F); "
                "Poste's offer document says CDP, its significant holder, is controlled by Italy's Ministry of Economy and Finance; the CDP "
                "stake in Poste is not quantified",
                link_url='https://www.emarketstorage.it/sites/default/files/comunicati/2026-07/20260719_186982.pdf', chain=TIM_CHAIN)],
         gov_note="TIM S.A. reports no other holder above 5% (20-F 2025); no Brazilian state holder",
         gov_dropped=[],
         core=ND("Reuters (2020): TIM excluded Huawei from a 5G core tender (Cisco, Ericsson, Nokia, Mavenir, Affirmed invited), winner not "
                 "reported; SAMENA (Dec 2021) says the core was 'ready' for 5G without naming the vendor"),
         first_contract=ND("SAMENA (25 Dec 2021): TIM 'signed a radio access networks (RAN) deal with ... Ericsson and ... Huawei last year' "
                           "(i.e. 2020; verified), but the deal's date and 5G scope are not stated"),
         vendor_operates=ND("Nokia's 2024 deal includes deployment, optimisation and technical support, not network operation")),
    dict(region='Latin America & Caribbean', country='Brazil', operator_name='Algar', name_note='Algar Telecom S.A. (formerly CTBC)',
         share=V(1.94, ANATEL_ZIP, BR_NOTE + "; Anatel's 2021 report gave Algar 1.2%", 2026),
         launch=V(2021, 'https://techblog.comsoc.org/2021/12/page/3/',
                  "IEEE ComSoc blog (16 Dec 2021): 'a commercial Non Standalone (NSA) 5G service using its newly acquired 2.3GHz spectrum. "
                  "The 5G network went live on 15 December' (verified); Algar's 2022 report: 'first operator to launch 5G in Brazil, in 2021'"),
         ran5=[], ran5_note=("no 5G RAN vendor named: Nokia supported a 5G demonstration in Uberaba two weeks before launch (ComSoc), and a "
                             "2025 Telecoms.com interview on a Huawei 5G partnership could not be fetched (403)"),
         ran4=[], ran4_note="Huawei has supplied Algar's wireless network since its 2004 GSM rollout (Telecoms.com, 403, unverified); no LTE vendor named",
         gov=[G('Singapore', 'GIC (via Archy LLC)', 'sovereign_wealth_fund', 25.30, 'Algar Telecom S.A.', 'direct', '2022', ALGAR_AR,
                "Algar Telecom integrated report 2022, p.7: 'Entry of Archy LLC, an affiliate of the GIC (Singapore sovereign wealth fund) "
                "as a shareholder of Algar Telecom, with a 25.30% equity interest in the total capital' (entry listed under 2010-2019); "
                "p.33 shareholding structure: Algar S.A. 67.74%, Archy LLC 25.30%, others 6.96% (verified). Newest filing found; GIC's "
                "percentage of Archy LLC is not stated")],
         gov_note="Algar S.A. (67.74%) is the Garcia family holding; no Brazilian state holder",
         gov_dropped=[],
         core=ND("ComSoc: the NSA launch involved investment in the 'network core and service platforms'; vendor not named"),
         first_contract=ND('the Nokia demonstration (late Nov 2021) is not described as a contract'),
         vendor_operates=ND("AudioCodes' managed Microsoft Teams service is a business-voice service, not network operation")),
    # ------------------------------------------------------------------ Suriname
    dict(region='Latin America & Caribbean', country='Suriname', operator_name='Telesur',
         name_note='Telecommunicatiebedrijf Suriname (Telesur), state-owned',
         share=ND('no regulator or operator subscriber figures found for Telesur or Digicel'),
         launch=V(2019, 'https://developingtelecoms.com/telecom-business/operator-news/10284-telesur-starts-promoting-5g-network-with-data-tariffs.html',
                  "Developing Telecoms (13 Nov 2020): 'commercial 5G network has been live in the nation's capital of Paramaribo since December "
                  "2019' (verified)"),
         ran5=[], ran5_note=("TechNewsTT (3 Aug 2019) reports Telesur planned to deliver 5G with Huawei by Oct 2019; UNVERIFIED (403), and a "
                             "plan, so not coded"),
         ran4=[R('Huawei', 'not_disclosed', 'https://china.aiddata.org/projects/97696',
                 "equipment supply and implementation contracts with Huawei International and Huawei Technologies (T&T) (28 Sep 2012, 1 Sep 2014) "
                 "for the '3G and 4G Wireless Project', financed by a Bank of China loan (verified)")],
         gov=[G('Suriname', 'Government of the Republic of Suriname', 'government_ministry', 100.0, 'Telesur', 'direct',
                'n.d.',
                'https://dtri.uneca.org/v1/uploads/country-profile/sur-country-profile-en.pdf',
                "as_of n.d.: report undated (latest data cited 2023); the rule dates from the Telecommunications Act 2004. ECLAC Suriname country report (UN DTRI): 'the Wet Telecommunicatievoorzieningen (Telecommunications Act) of 2004 establishes "
                "the government as the only shareholder of TELESUR' (verified); 100% is the researcher's reading of 'only shareholder'; the "
                "holding ministry is not named")],
         gov_dropped=[],
         core=ND('Huawei is named only for the planned 5G deployment (Aug 2019), not as core vendor'),
         first_contract=ND(),
         vendor_operates=ND("Cerillion's managed BSS/OSS service is not network operation")),
    # ------------------------------------------------------------------ Barbados
    dict(region='Latin America & Caribbean', country='Barbados', operator_name='FLOW',
         name_note='Cable and Wireless (Barbados) Limited (Liberty Latin America)',
         share=ND('the Telecommunications Unit publishes no operator subscription counts or shares'),
         launch=V(2025, 'https://www.cbc.bb/news/local-news/historic-first-for-flow-with-introduction-of-5g/',
                  "CBC (14 Oct 2025): 'the historic introduction of its 5G mobile network in Barbados, becoming the first telecom provider' (verified)"),
         ran5=[], ran5_note="no 5G RAN vendor named; Ericsson appears only in a 2017 group-level 5G prototype test",
         ran4=[], ran4_note='no LTE vendor named (4G launched 22 Mar 2017)',
         gov=[], gov_note="Liberty Latin America (listed) owns Cable & Wireless; its 10-K and proxy name no state holder",
         gov_dropped=[],
         core=ND('no source names the 5G core or NSA EPC vendor'),
         first_contract=ND('Ericsson 5G prototype collaboration (Oct 2017) was a test'),
         vendor_operates=ND("WRONG IN SEARCH: Ericsson's three-year contract 'operating and managing the Flow mobile network' in 12 markets incl. "
                            "Barbados is dated 12 Jul 2016, not 29 May 2025 (cwc.com, verified); it predates 5G and no renewal was found")),
    dict(region='Latin America & Caribbean', country='Barbados', operator_name='Digicel', name_note='Digicel (Barbados) Limited',
         share=ND('the Telecommunications Unit publishes no operator subscription counts or shares'),
         launch=ND("Digicel's Barbados 5G+ terms (updated 19 Nov 2025) show 5G+ available to prepaid and postpaid customers but give no launch "
                   "date (verified); CBC calls FLOW (14 Oct 2025) the first 5G provider on the island"),
         ran5=[], ran5_note='no 5G RAN vendor named',
         ran4=[R('ZTE', 'not_disclosed', 'https://www.samenacouncil.org/samena_daily_news?news=67212',
                 "SAMENA (7 Mar 2018): 'Digicel Barbados has signed an agreement with ZTE to expand its 4G-LTE network throughout the island' "
                 "(verified); not described as sole supplier")],
         ran4_note="an Ericsson-to-Huawei switch reported in 2016 concerns the Digicel Play fixed network, not mobile RAN",
         gov=[], gov_note=("no state holder: Digicel's 2024 SEC Form T-3 shows Denis O'Brien entities with a majority of Digicel Group "
                           "Holdings; Digicel (Barbados) Limited sits under Digicel Eastern Caribbean (75%)"),
         gov_dropped=[],
         core=ND('Ericsson and Huawei are listed as business-technology partners without a core role'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ United Arab Emirates
    dict(region='Middle East', country='United Arab Emirates', operator_name='e& (Etisalat)',
         name_note='Emirates Telecommunications Group Company PJSC (e&), UAE operations',
         share=V(60.08, E_AND_Q4, UAE_NOTE, 2025),
         launch=V(2018, 'https://www.khaleejtimes.com/business/etisalat-unveils-commercial-5g-network',
                  "Khaleej Times (14 May 2018): 'the launch of the first commercial 5G wireless network in the UAE'; commercial fixed devices "
                  "and services from Sep 2018 (verified). Full commercial mobile 5G followed in May 2019 (TeleGeography). Coded 2018 as for "
                  "Elisa in the core panel; researcher decision flagged"),
         ran5=[R('Huawei', 'not_disclosed', 'https://www.lightreading.com/open-ran/afghanistan-gets-open-ran-africa-asia-eye-it',
                 "Light Reading (Apr 2021): 'Etisalat signed a contract with Huawei in February 2019 for its 5G roll out in the UAE' (verified)"),
               R('Ericsson', 'not_disclosed', MTNC_UAE,
                 "MTN Consulting (15 Nov 2019): 'Etisalat awarded contracts to both Huawei and Ericsson for the rollout of its 5G mobile network "
                 "in February 2019' (verified); Ericsson's own releases (Feb 2019 5G radio; May 2025 multi-year 5G radio expansion) returned 403"),
               R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/etisalat-and-nokia-provide-ultra-fast-5g-broadband-services-in-the-uae/',
                 "Nokia (21 Apr 2021): Etisalat 'together with Nokia, as a key partner, has deployed 5G network' (verified)")],
         ran5_note=("MTN Consulting: 'Ericsson, Huawei and Nokia are key suppliers to Etisalat, and all involved in the telco's 5G buildout'; "
                    "no shares. WRONG IN SEARCH: the Jan 2020 Light Reading open RAN article does not say the Dubai RAN was 'provided by "
                    "Ericsson'; its open RAN suppliers (Altiostar, Cisco, NEC) are not coded"),
         ran4=[], ran4_note='no source names a 4G/LTE vendor with a generation; Nokia Cloud RAN (Jan 2024) was a trial',
         gov=[G('United Arab Emirates', 'Emirates Investment Authority (EIA)', 'sovereign_wealth_fund', 60.0,
                'Emirates Telecommunications Group Company PJSC (e&)', 'direct', '2025-12-31', E_AND_AR,
                "e& integrated annual report 2025, p.175: EIA 5,218,052,400 shares, 60%; p.186: the Federal Government transferred its 60% "
                "to the EIA, 'which is ultimately controlled by the UAE Federal Government'; the EIA also holds the Special Share. Board: "
                "the EIA appoints 7 of 11 directors (corporate governance report 2025, p.4). " + EIA_TYPE,
                link_url=E_AND_AR, board_seat='yes')],
         gov_note=("The report classifies 61.0% of shares as UAE-government-held; only the EIA (60%) is named, so the remaining 1.0 point is "
                   "not attributed to any holder"),
         gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/5/2020/etisalat-selects-ericsson-for-5g-network-core-expansion',
                "Ericsson (23 Nov 2020, per the search): Etisalat selected Ericsson's 5G Core incl. User Data Management; a May 2025 Ericsson "
                "release extends this to further dual-mode 5G Core applications. UNVERIFIED: ericsson.com returned 403; the 2020 scope may be "
                "UDM only. NSA EPC vendor not named"),
         first_contract=ND("Huawei and Ericsson 5G contracts date from Feb 2019 (verified), but the commercial 5G network was announced in "
                           "May 2018, so Feb 2019 is not shown to be the first contract"),
         vendor_operates=ND("MTN Consulting: the key vendors 'are sometimes engaged on a multi-year, managed services basis' (verified), without "
                            "naming the vendor or scope")),
    dict(region='Middle East', country='United Arab Emirates', operator_name='du',
         name_note='Emirates Integrated Telecommunications Company PJSC (EITC), brand du',
         share=V(39.92, DU_AR, UAE_NOTE, 2025),
         launch=V(2019, TELEGEO, "TeleGeography: 'Du launched 5G in June 2019, just days after Etisalat' (commercial mobile; verified)"),
         ran5=[R('Huawei', 'not_disclosed', MTNC_UAE, "MTN Consulting (15 Nov 2019): 'Huawei and Nokia are du's 5G network suppliers' (verified)"),
               R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-expands-dus-5g-network-to-enable-enhanced-broadband-for-more-customers-in-uae/',
                 "four-year 5G expansion deal (16 Mar 2021): Nokia deploys the new 5G sites with SRAN and AirScale (verified); named a 5G "
                 "supplier in 2019 (MTN Consulting)"),
               R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2021/2/united-arab-emirates-du-selects-ericsson-5g-ran',
                 "Ericsson (22 Feb 2021): du selects Ericsson 5G RAN as part of a network expansion and modernisation (per the search); "
                 "UNVERIFIED: ericsson.com returned 403")],
         ran5_note="Nokia calls itself 'a key RAN provider for du, including all the major cities' (not a share category)",
         ran4=[], ran4_note='no source names a 4G/LTE RAN vendor',
         gov=[G('United Arab Emirates', 'Emirates Investment Authority (EIA)', 'sovereign_wealth_fund', 50.1,
                'Emirates Integrated Telecommunications Company PJSC (du)', 'direct', '2025-12-31', DU_AR,
                "du integrated annual report 2025, p.119: EIA 2,271,728,899 shares, 50.1%; p.156: 'Emirates Investment Authority owns 50.1% "
                "of the company shares which is ultimately controlled by UAE Federal Government'; six directors are listed as "
                "'Representing: Emirates Investment Authority' (verified). " + EIA_TYPE,
                board_seat='yes')],
         gov_note=("NOT CODED, needs a researcher decision: DH 8 LLC 19.7% (2025 report; 'Dubai Holdings's shareholding in du' was moved to "
                   "DH 8 LLC in 2025). The report does not say DH 8 LLC or Dubai Holding is state-owned, and Dubai Holding is not on "
                   "data/state_holders.csv. The co-founder Emirates Communications and Technologies Company LLC has two board "
                   "representatives; its owner and stake are not stated"),
         gov_dropped=["Mamoura Diversified Global Holding PJSC (Mubadala subsidiary): sold 7.55% of du in a 2025 secondary offering, '75% of "
                      "their stake'; the remainder is not in du's 5%-or-more list at 2025-12-31 (percentage not stated; no board representative listed)"],
         core=ND("Huawei is du's existing evolved packet core vendor and in Feb 2018 was chosen to upgrade the data core to CloudEPC that can "
                 "'evolve to 5G core' (verified); no source says it is the 5G core or the EPC used for 5G"),
         first_contract=ND('the Huawei CloudEPC deal (Feb 2018) is a 5G-ready data-core upgrade, not a 5G contract'),
         vendor_operates=ND("Ericsson's three-year managed-services deal (29 Oct 2009, GSM/WCDMA) predates 5G; Hayat Communications' 2023 "
                            "managed-services deal appears only in a LinkedIn post and Hayat is not an equipment vendor")),
]
