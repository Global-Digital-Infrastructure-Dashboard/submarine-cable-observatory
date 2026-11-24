"""Core-94 migration, batch core2 (Prof. Shen, 2026-11): Italy, Spain and the Netherlands (12 operators) re-coded in the
expansion's three-file format, in-session on 2026-11-24, following the calibration batch (coded_batch_core1.py).

Inputs: the core panel (data/5g_operator_panel.csv) and its cached vendor/ownership searches (data/5g_searches.jsonl),
plus the migration searches mig|mktshare|<market>, mig|share|<id> and mig|ran|<id> (data/5g_expansion_searches.jsonl).
Government stakes re-express gov_stakes_core.py's per-holder rows (two additions from evidence, listed below).
Share categories follow the user's rules (2026-11-23/24): a stated percentage maps 100% = all, >50% = most,
10-50% = some, <10% = small, with its basis (sites, traffic, RAN) and date in the note; 'majority' -> most,
'roughly evenly' -> some; otherwise not_disclosed. Every share category and computed figure was checked against the
primary page at coding time (5g_expansion/verify_2026-11-24_core2.csv).

Disagreements with the core panel / gov_stakes_core.py, coded here from the evidence:
- ES-masorange: Orange S.A. owns 100% of MasOrange since 8 Jun 2026, so the French State and Bpifrance reach it via
  Orange (researcher decision 2026-11-24; now also in gov_stakes_core.py).
- IT-vodafone-italia + IT-fastweb: merged into Fastweb S.p.A. on 1 Jan 2026 and coded as one Fastweb row (researcher
  decision 2026-11-24); the Swiss Confederation's 51% of Swisscom reaches it. gov_stakes_core.py now records the stake
  for IT-vodafone-italia too.
- ES-telefonica-moviles-espana: 5G (and 4G) RAN is Nokia and Ericsson 50% each (2021), not the core panel's
  'Nokia; Huawei' from Telefónica's Dec 2019 statement.
"""
from schema import G, ND, R, S, V, register

CODED_AT = '2026-11-24'

register(domains={
    'company': ['gruppotim.it', 'emarketstorage.it', 'swisscom.ch', 'fastwebvodafone.it', 'fastweb.it', 'windtre.it',
                'telefonica.com', 'vodafone.com', 'orange.com', 'orange.es', 'kpn.com', 'eand.com'],
    'government': ['agcom.it', 'cnmc.es', 'acm.nl', 'digital-strategy.ec.europa.eu'],
    'research_industry_group': ['zenodo.org', '5gitaly.eu'],
    'news': ['mobileeurope.co.uk', 'decode39.com', 'theregister.com', 'reuters.com', 'platformexecutive.com'],
})

VODAFONE_AR = 'https://reports.investors.vodafone.com/view/500231330/239/'
E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
TEF_CGR = 'https://www.telefonica.com/en/wp-content/uploads/sites/5/2026/02/Annual-Report-Corporate-Gobernance-2025.pdf'
ORANGE_XLSX = 'https://assets.orange.com/pm_12751_545_545865-jr7yvi3osw.xlsx'
SWISSCOM_AR = 'https://www.swisscom.ch/en/about/investors/annual-result.html.html'
AGCOM = 'https://www.agcom.it/sites/default/files/media/allegato/2026/OPEN%20DATA%20Oss.%203-2026.xlsx'
AGCOM_NOTE = ("AGCOM open data, Osservatorio 3/2026, table 1.8: share of 'human' SIMs (voice/data SIMs used by people, "
              "excluding M2M) at June 2026: Fastweb+Vodafone 25.16, Wind Tre 23.56, TIM 22.17, Iliad 16.14; verified in the "
              "file. The migration searches misread AGCOM (see verify log)")
CNMC = 'https://www.cnmc.es/sites/default/files/6162794.pdf'
CNMC_NOTE = ("CNMC 'Operadores principales 2025' (OP/DTSA/001/25), footnote 9: shares of mobile lines in 2024: Orange (MasOrange "
             "group) 41.1, Telefónica Móviles 25.9, Vodafone España 18.9, Digi Spain 9.7, Wewi 1.5; verified in the PDF")
ACM_NOTE = ("ACM publishes ranges only: Q4 2025 KPN 25-30%, Odido 25-30%, VodafoneZiggo 20-25%, MVNOs 20-25% "
            "(Telecommonitor Q4 2025, via exp key mig|share|NL-odido); a range is not coded as a value")
LR_TIM = 'https://www.lightreading.com/5g/nokia-to-replace-ericsson-at-telecom-italia-5g-sites'
LR_SPAIN = 'https://www.lightreading.com/regulatory-politics/huawei-feels-the-enduring-love-of-spain-s-telcos-to-eu-s-horror'
LR_MO24 = 'https://www.lightreading.com/5g/masorange-to-scrap-huawei-and-zte-in-ericsson-open-ran-shift-report'
ME_TEF = 'https://www.mobileeurope.co.uk/telefonica-awards-ericsson-and-nokia-equal-deals-for-5g-sa-in-spain/'
ZENODO = 'https://zenodo.org/records/4621102/files/5GSupplyMarketTrends_BaselineReport.pdf'
DECODE39 = 'https://decode39.com/4465/less-china-in-italys-5g-draghi-reshapes-the-telcos-plans/'
LR_KPN19 = 'https://www.lightreading.com/5g/ericsson-the-unready-loses-kpn-to-huawei'
LR_TMNL = 'https://www.lightreading.com/5g/ericsson-to-replace-huawei-at-t-mobile-netherlands'
VOD_DROPPED = ['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)']


def swiss_gov(chain, parent_pct=100.0, note=''):
    return [G('Switzerland', 'Swiss Confederation', 'government_ministry', 51.0, 'Swisscom Ltd', 'via_parent', '2025-12-31', SWISSCOM_AR,
              "Swisscom's 2025 major-shareholder disclosure. " + note, parent_pct=parent_pct, chain=chain)]


def orange_gov(chain, parent_pct=None):
    return [G('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX,
              '21.04% of voting rights', parent_pct=parent_pct, chain=chain),
            G('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', 'via_parent', '2025-12-31', ORANGE_XLSX,
              "8.00% of voting rights; Orange's file groups it with the French State as the public sector", parent_pct=parent_pct, chain=chain)]


OPERATORS = [
    # ------------------------------------------------------------------ Italy
    dict(region='Western Europe', country='Italy', operator_name='TIM', core_operator_id='IT-telecom-italia',
         name_note='Telecom Italia S.p.A. (core panel name Telecom Italia)',
         share=V(22.17, AGCOM, AGCOM_NOTE + "; TIM's own 2025 annual report gives 25.9% of total lines incl. M2M (Q3 2025)", 2026),
         launch=ND('no source in the evidence dates the commercial launch; the discovery list is also not_disclosed'),
         ran5=[R('Nokia', 'not_disclosed', LR_TIM, "Light Reading (17 Nov 2025): Nokia's share of TIM's RAN was 'somewhere north of 20%' and the new "
                 "three-year deal 'boosts it by 40 percentage points', i.e. above 60% of the RAN (computed; basis: share of TIM's RAN, all "
                 "generations), 'entirely at the expense of Ericsson' [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Ericsson', 'not_disclosed', LR_TIM, 'still supplies 5G RAN products under a Feb 2025 agreement; its remaining share is not stated'),
               R('Huawei', 'not_disclosed', 'https://www.platformexecutive.com/news/mobile-telecoms-infrastructure/tim-chief-executive-says-not-a-problem-to-develop-5g-without-huawei/',
                 "Platform Executive (Mar 2026) describes Huawei in a supporting role; Light Reading (Nov 2025) calls TIM's reliance on Huawei unclear")],
         ran5_note=("a 2022 planned mix (Ericsson 53 / Nokia 27 / Huawei 20, later Ericsson 70 / Nokia 30; Decode39) was a plan and is "
                    "superseded by the Nov 2025 Nokia deal; Strand Consult puts Chinese vendors at 35% of Italy's 5G RAN (national, end-2024)"),
         ran4=[R('Huawei', 'most', LR_TIM, "Strand Consult via Light Reading: Huawei 'accounted for about 55% of the operator's 4G sites' before "
                 "5G launched in 2019 (basis: 4G sites, pre-2019)"),
               R('Nokia', 'most', LR_TIM, "above 60% of TIM's RAN after the Nov 2025 three-year deal ('somewhere north of 20%' plus 40 percentage points; computed; basis: share of TIM's RAN, all generations, Light Reading 17 Nov 2025). DATED: Huawei's 55% is pre-2019, so the two 'most' rows describe different years [decision 2026-11-24: all-generation share, coded to 4G only]")],
         ran4_note=("TIM's CEO (Sep 2020, Reuters) called Ericsson the 'main' provider with Nokia and Huawei in smaller roles; Reuters "
                    "could not be fetched (401), so Ericsson/Nokia 4G are not coded"),
         gov=[G('Italy', 'Poste Italiane S.p.A.', 'state_owned_company', 86.952, 'Telecom Italia S.p.A.', 'direct', '2026-09-30',
                'https://www.gruppotim.it/en/investors/shares/shareholders.html',
                "Poste rose from 27.32% (Dec 2025); Poste's offer document says CDP, its significant holder, is controlled by Italy's Ministry of "
                "Economy and Finance; the CDP stake in Poste is not quantified",
                link_url='https://www.emarketstorage.it/sites/default/files/comunicati/2026-07/20260719_186982.pdf')],
         gov_dropped=[],
         core=V('Ericsson', LR_TIM, "Ericsson 'is also the provider of the operator's 5G core' (Light Reading, 17 Nov 2025); a 2026 tender for a "
                "future 5G core excluded Huawei, winner not reported"),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '5G', 'Ericsson', 'Nokia', '2025-11-17', 'not_confirmed', LR_TIM,
                     "three-year Nokia deal adding about 40 points of RAN share 'entirely at the expense of Ericsson'"),
                   S('RAN', '5G', 'Huawei', 'Ericsson', '2021-04-29', 'not_confirmed', DECODE39,
                     "Reuters (29 Apr 2021, via search; page blocked) reported TIM seeking to cancel Huawei's 5G RAN contract and split it "
                     "between Ericsson and Nokia; Decode39 (2022) describes TIM divesting Huawei toward Ericsson 70 / Nokia 30"),
                   S('RAN', '5G', 'Huawei', 'Nokia', '2021-04-29', 'not_confirmed', DECODE39, 'same plan as the Huawei -> Ericsson row')]),
    dict(region='Western Europe', country='Italy', operator_name='Wind Tre', core_operator_id='IT-wind-tre', name_note='brand WINDTRE',
         share=V(23.56, AGCOM, AGCOM_NOTE, 2026),
         launch=ND("only the 5G standalone launch is dated (14 Jan 2026, Ericsson/EC); the earlier non-standalone launch is not dated in the evidence"),
         ran5=[R('Ericsson', 'not_disclosed', ZENODO, "'Wind Tre chose Ericsson and ZTE' for its 5G-ready network (2021 report); no split"),
               R('ZTE', 'not_disclosed', ZENODO, 'same report')],
         ran4=[R('ZTE', 'not_disclosed', 'https://www.zte.com.cn/global/about/magazine/zte-technologies/2019/6-en/success-stories/1.html',
                 'ZTE Uni-RAN for 2G/3G/4G integration since Dec 2016 (ZTE, Nov 2019)'),
               R('Ericsson', 'not_disclosed', 'https://www.lightreading.com/5g/amid-the-rubble-of-l-aquila-zte-tries-to-rebuild',
                 "introduced as 'a second supplier' after Wind Tre de-scoped ZTE's RAN agreement in 2018")],
         gov=[], gov_note='CK Hutchison (Li family 30.43%); no state holder', gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/3/2026/wind-tre-selects-ericsson-for-core-network-modernization',
                'dual-mode 5G Core for 4G, NSA and SA under a 2026-2032 agreement (3 Mar 2026); the 2025 SA core was also built with Ericsson'),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G', 'ZTE', 'Ericsson', '2018', 'not_confirmed', 'https://www.lightreading.com/5g/amid-the-rubble-of-l-aquila-zte-tries-to-rebuild',
                     "partial: Wind Tre 'gave notice to ZTE Italia of a partial termination and de-scoping' and handed some work to Ericsson; "
                     'generation not stated (coded 4G, the network then in service)')]),
    dict(region='Western Europe', country='Italy', operator_name='Iliad Italia', core_operator_id='IT-iliad-italia',
         share=V(16.14, AGCOM, AGCOM_NOTE + "; iliad's own 2025 report gives about 15.6% excl. M2M at end-Sep 2025", 2026),
         launch=ND("a search says 2020 without a source; the discovery list has no date"),
         ran5=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-partners-with-iiiad-group-to-roll-out-5g-in-france-and-italy/',
                 'AirScale RAN under the Feb 2020 5G agreement (France and Italy together), renewed Dec 2024; the only named vendor, no share wording')],
         ran4=[R('Nokia', 'not_disclosed', 'https://www.nokia.com/newsroom/nokia-partners-with-iiiad-group-to-roll-out-5g-in-france-and-italy/',
                 "Nokia had supplied iliad's 3G/4G network in Italy since 2018")],
         gov=[], gov_note='Niel family via iliad Holding; no state holder', gov_dropped=[],
         core=V('Nokia', 'https://www.nokia.com/newsroom/nokia-extends-long-term-partnership-with-iliad-group/', 'cloud-native 4G/5G core (Dec 2024 agreement)'),
         first_contract=V('2020-02', 'https://www.nokia.com/newsroom/nokia-partners-with-iiiad-group-to-roll-out-5g-in-france-and-italy/',
                          'Nokia 5G rollout agreement for France and Italy (announcement month)'),
         vendor_operates=ND()),
    # Researcher decision 2026-11-24: Vodafone Italia (core IT-vodafone-italia) and Fastweb (core IT-fastweb) merged into
    # Fastweb S.p.A. on 1 Jan 2026, so they are one row here (two rows would double-count the operator in per-country
    # analysis). The core panel keeps both rows. Network facts are Vodafone Italia's: Fastweb had no own 5G RAN.
    dict(region='Western Europe', country='Italy', operator_name='Fastweb', core_operator_id='IT-fastweb; IT-vodafone-italia',
         name_note='Fastweb S.p.A., formerly Vodafone Italia and Fastweb (Vodafone Italia merged into Fastweb on 1 Jan 2026; brands Fastweb and Vodafone)',
         share=V(25.16, AGCOM, AGCOM_NOTE + '; combined Fastweb+Vodafone (Vodafone Italia merged into Fastweb on 1 Jan 2026)', 2026),
         launch=V(2019, 'https://www.5gitaly.eu/partner/vodafone/', "predecessor Vodafone Italia's 5G launch; exact date not stated; matches the "
                  "discovery list (2019). A search dates a Fastweb 5G launch to 27 Dec 2025, but its cited press kit is a 2020 plan document"),
         ran5=[R('Nokia', 'not_disclosed', ZENODO, "Vodafone Italia's network: the 5G supply-market baseline report (2021) says Vodafone Italy's "
                 "commercial 5G used 'equipment from Nokia and Huawei'; Decode39 (2022) places Nokia in northern Italy"),
               R('Huawei', 'not_disclosed', ZENODO, 'same report (Vodafone Italia); Decode39 (2022) places Huawei in central and southern Italy')],
         ran5_note=("vendors are the predecessor Vodafone Italia's; pre-merger Fastweb named no supplier (Huawei, Ericsson, Samsung and ZTE "
                    "were only 'in the running', 2019) and shared WindTre's 5G RAN. Golden Power conditions (Decode39, 2022) require "
                    "gradual replacement of Chinese radio equipment at end of life within six years; no switch is dated"),
         ran4=[], ran4_note='4G RAN vendors not stated (Vodafone Italia or Fastweb)',
         gov=swiss_gov('Swisscom Ltd -> Swisscom (Switzerland) Ltd -> 100% of Fastweb S.p.A. (Vodafone Italia owned by Swisscom from 31 Dec 2024, merged in on 1 Jan 2026)'),
         gov_note=("one Swiss Confederation row for the merged operator; before the merger the core panel recorded it for Fastweb only "
                   "(Vodafone Italia's stake added in gov_stakes_core.py, researcher decision 2026-11-24)"),
         gov_dropped=[],
         core=ND("Vodafone Italia's 2022 plan (Decode39 citing Il Sole 24 Ore): Ericsson ~40%, Juniper ~40%, Huawei 10%, Nokia 10% of the "
                 'core; a multi-vendor plan, not a single vendor'),
         first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Spain
    dict(region='Western Europe', country='Spain', operator_name='Movistar', core_operator_id='ES-telefonica-moviles-espana',
         name_note='Telefónica Móviles España, S.A.U. (core panel name)',
         share=V(25.9, CNMC, CNMC_NOTE + "; Telefónica's own 20-F estimate is 27.5% (2024)", 2024),
         launch=V(2020, 'https://www.telefonica.com/en/communication-room/press-room/telefonica-switches-on-5g-and-75-of-the-spanish-population-will-obtain-a-signal-this-year/',
                  '5G switched on 1 Sep 2020; matches the discovery list (2020-09)'),
         ran5=[R('Nokia', 'some', ME_TEF, "Mobile Europe (20 Jul 2021): equal 5G SA deals in the 3.5 GHz and 700 MHz bands; Telefónica: 'in the UK, as "
                 "in Spain, the networks are 50% between Nokia and Ericsson' (basis: network split, 2021)"),
               R('Ericsson', 'some', ME_TEF, 'same: 50% (basis: network split, 2021)')],
         ran5_note=("CORE-PANEL DISAGREEMENT: the core panel codes 'Nokia; Huawei' from Telefónica's Dec 2019 statement (Light Reading); the "
                    "2021 award supersedes it. Strand Consult's 38% Chinese share of Spain's 5G RAN (2022) is national"),
         ran4=[R('Nokia', 'some', ME_TEF, "the 5G split follows the existing 3G/4G vendors ('maintained by the 4G providers'); 50% (2021)"),
               R('Ericsson', 'some', ME_TEF, 'same: 50% (2021)')],
         gov=[G('Spain', 'Sociedad Estatal de Participaciones Industriales (SEPI)', 'state_holding_company', 10.0, 'Telefónica, S.A.', 'via_parent',
                '2025-12-31', TEF_CGR, 'state link from data/state_holders.csv', link='reference_list',
                chain="Telefónica, S.A. -> Telefónica Móviles España; percentage of the operating subsidiary not stated"),
              G('Saudi Arabia', 'Public Investment Fund (via Green Bridge Investment Company SCS and Saudi Telecom Company)', 'sovereign_wealth_fund',
                9.999, 'Telefónica, S.A.', 'via_parent', '2025-12-31', TEF_CGR, 'state link from data/state_holders.csv', link='reference_list',
                chain="Telefónica, S.A. -> Telefónica Móviles España; percentage of the operating subsidiary not stated")],
         gov_dropped=[],
         core=V('Huawei', 'https://www.lightreading.com/5g/telef-nica-hooked-on-huawei-years-after-clean-network-vow',
                'standalone 5G core for the consumer business; contract reportedly renewed to 2030'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Western Europe', country='Spain', operator_name='Vodafone España', core_operator_id='ES-vodafone-espana',
         share=V(18.9, CNMC, CNMC_NOTE + '; with Wewi (bought by Vodafone) CNMC later gives 20.4% for 2024 (OP/DTSA/002/25, not checked)', 2024),
         launch=ND("the discovery list gives 2019-06 and a migration search says 2020, neither with a source in the evidence"),
         ran5=[R('Huawei', 'not_disclosed', LR_SPAIN, "Strand Consult via Light Reading (Sep 2026): high-risk vendors, 'chiefly Huawei', had a 91% share of "
                 "Vodafone Spain's 5G RAN; Huawei's own share is not stated. UNVERIFIED: Cinco Días (16 Aug 2025) reportedly gives Huawei 70% "
                 "with Ericsson the rest, but returned 403"),
               R('Ericsson', 'not_disclosed', LR_SPAIN, "the non-Huawei supplier in the Cinco Días report (unverified); share not stated")],
         ran4=[R('Huawei', 'not_disclosed', LR_MO24, "Strand Consult (2020) via Light Reading: Chinese vendors supplied 'about 80% of its 4G RAN'; not split by vendor")],
         gov=[], gov_note='100% owned by Zegona Communications plc since 2024; no state holder', gov_dropped=[],
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/3/2025/vodafone-spain-to-deploy-standalone-5g-core-network-for-consumers-with-ericsson',
                'standalone dual-mode 5G core (Mar 2025); Huawei supplies software elements of the non-standalone 5G'),
         first_contract=ND(), vendor_operates=ND()),
    dict(region='Western Europe', country='Spain', operator_name='MasOrange', core_operator_id='ES-masorange', name_note='MásOrange, S.L.',
         share=V(41.1, CNMC, CNMC_NOTE + ' (Orange designated for the MasOrange group, MásMóvil shares added)', 2024),
         launch=V(2020, 'https://www.ericsson.com/en/press-releases/2020/9/orange-launches-ericsson-powered-5g-in-spain',
                  'Orange Spain (now part of MasOrange) launched Ericsson-powered 5G in Sep 2020; matches the discovery list (2020-09)'),
         ran5=[R('Huawei', 'not_disclosed', LR_MO24, "Expansión via Light Reading (30 Jul 2024): Huawei 'about 54% of the RAN' (basis: RAN sites, all generations) [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('Ericsson', 'not_disclosed', LR_MO24, "the remainder, about 42% (computed: 100 - 54 - 4; basis: RAN sites, Jul 2024) [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]"),
               R('ZTE', 'not_disclosed', LR_MO24, "'about 4% of the MasOrange footprint' (Jul 2024). DISPUTED: Light Reading's Sep 2026 retelling of the same "
                 "Expansión report gives ZTE 12%; coded the 2024 original [decision 2026-11-24: the share covers the whole RAN, not 5G specifically, so it is coded to 4G only; 5G share not_disclosed]")],
         ran5_note=("a later report (DCD) gives Ericsson 57% / Huawei 43% after partial implementation of the switch, but it returned 403 "
                    "(UNVERIFIED); Strand Consult put high-risk vendors at 58% of MasOrange's 5G RAN (2025)"),
         ran4=[R('Huawei', 'most', LR_MO24, "Expansión via Light Reading (30 Jul 2024): Huawei 'about 54% of the RAN' (basis: RAN sites, all generations); the former Orange Spain relied on 'a mixture of Huawei and Ericsson for its 4G radio access network' [decision 2026-11-24: all-generation share, coded to 4G only]"),
               R('Ericsson', 'some', LR_MO24, "the remainder, about 42% (computed: 100 - 54 - 4; basis: RAN sites, all generations, Jul 2024) [decision 2026-11-24: all-generation share, coded to 4G only]"),
               R('ZTE', 'small', LR_MO24, "'about 4% of the MasOrange footprint' (Jul 2024; DISPUTED: 12% in Light Reading's Sep 2026 retelling) [decision 2026-11-24: all-generation share, coded to 4G only]")],
         gov=orange_gov('Orange S.A. 100% of MasOrange since 8 Jun 2026 (Lorca\'s 50% acquired; 50:50 joint venture before)', parent_pct=100.0),
         gov_note=("Added in the migration (researcher decision 2026-11-24, now also in gov_stakes_core.py): MasOrange's ownership evidence "
                   "(and Light Reading, Sep 2026: 'now wholly owned by Orange') makes Orange the 100% owner"),
         gov_dropped=[],
         core=V('Ericsson', 'https://www.orange.com/en/press-release/orange-selects-suppliers-for-its-5g-stand-alone-5g-sa-networks-in-europe-234893',
                "Orange's 5G SA supplier selection (Feb 2022); Ericsson dual-mode core for the 2023 SA launch and a unified MasOrange SA core (Feb 2026)"),
         first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G/5G', 'ZTE', 'Ericsson', '2024-07', 'deadline 2027-12-31', LR_MO24,
                     "Expansión via Light Reading: ZTE (about 4% of the footprint, Basque region) 'will be removed by the end of 2027 and replaced by Ericsson'"),
                   S('RAN', '4G/5G', 'Huawei', 'Ericsson', '2024-07', 'deadline 2027-12-31', LR_MO24,
                     "Huawei to fall from about 54% to roughly 39% of the RAN, replaced by Ericsson (Extremadura, Andalusia, Canary Islands per LR Sep 2026); "
                     "partial implementation reported later (DCD, unverified)"),
                   S('RAN', '4G/5G', 'Ericsson', 'ZTE', '2020', 'not_confirmed', LR_MO24,
                     "Orange Spain: ZTE 'subsequently entered service in parts of the Basque territory, replacing Ericsson, according to sources'")]),
    dict(region='Western Europe', country='Spain', operator_name='Digi Spain', core_operator_id='ES-digi-spain',
         share=V(9.7, CNMC, CNMC_NOTE + "; Digi's own 2025 report gives 11.1% at 30 Sep 2025 (attributed to CNMC)", 2024),
         launch=ND('5G service runs over Telefónica spectrum and RAN sharing; no launch date in the evidence (discovery five_g_status = none)'),
         ran5=[], ran5_note="no RAN vendor named: Digi uses its own ~1,122 macro sites plus Telefónica's network under RAN and spectrum sharing",
         ran4=[], ran4_note='same',
         gov=[], gov_note='controlled by Zoltán Teszári via Digi Communications N.V.; no state holder', gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND()),
    # ------------------------------------------------------------------ Netherlands
    dict(region='Western Europe', country='Netherlands', operator_name='KPN', core_operator_id='NL-kpn',
         share=ND(ACM_NOTE),
         launch=ND('the discovery list gives 2020-07; no source in the migration evidence dates the launch'),
         ran5=[R('Huawei', 'not_disclosed', LR_KPN19, "Huawei RAN equipment selected in 2019 to modernise the network and prepare for 5G. UNVERIFIED: a search "
                 "calls Huawei KPN's 'sole supplier' citing The Register (Oct 2020), but the fetched page does not contain that wording")],
         ran4=[R('Huawei', 'not_disclosed', LR_KPN19, "KPN's CEO: 'swapping equipment in The Hague area ... installed the latest Huawei RAN equipment' (2019)")],
         ran4_note="Ericsson's ageing 4G equipment (built 2013-2014) was being replaced; its remaining share is not stated",
         gov=[], gov_note='no state holder in the core evidence', gov_dropped=[],
         core=V('Ericsson', 'https://www.kpn.com/overons/nieuws/en/kpn-renews-core-of-mobile-network/', "KPN release 'KPN renews core of mobile network' (15 Oct 2020)"),
         first_contract=ND("the Apr 2019 Huawei RAN deal was a modernisation 'preparing for 5G'; the Ericsson 5G core selection is dated 15 Oct 2020"),
         vendor_operates=ND(),
         switches=[S('RAN', '4G', 'Ericsson', 'Huawei', '2019-04', 'not_confirmed', LR_KPN19,
                     "Huawei began replacing Ericsson equipment in The Hague region in 2019 (Light Reading, 2019; 'KPN ... dropped Ericsson', LR Jun 2020)")]),
    dict(region='Western Europe', country='Netherlands', operator_name='Odido', core_operator_id='NL-odido', name_note='formerly T-Mobile Netherlands',
         share=ND(ACM_NOTE),
         launch=ND('the discovery list gives 2020; no source in the migration evidence dates the launch'),
         ran5=[R('Ericsson', 'all', LR_TMNL, "Light Reading (Jul 2022): T-Mobile Netherlands named 'Ericsson ... as the sole vendor of its 5G network'; "
                 "a spokesperson called Ericsson 'the main 5G supplier in the RAN replacing Huawei'")],
         ran4=[R('Ericsson', 'not_disclosed', LR_TMNL, "Ericsson 'as the sole supplier' was to renew the 3G/4G equipment, replacing Huawei; deployment from Feb 2023, "
                 'completion planned for summer 2024 (not confirmed in a checked source)')],
         ran4_note="Huawei built the LTE network (2013 SingleRAN contract, 5,000 sites) and is being replaced",
         gov=[], gov_note='private equity (Apax took full control in 2026); no state holder', gov_dropped=[],
         core=ND(), first_contract=ND(), vendor_operates=ND(),
         switches=[S('RAN', '4G/5G', 'Huawei', 'Ericsson', '2022-07', 'not_confirmed', LR_TMNL,
                     'Ericsson to replace Huawei in the RAN (3G/4G renewal and 5G); a Jan 2024 report says the swap was done (not checked)')]),
    dict(region='Western Europe', country='Netherlands', operator_name='VodafoneZiggo', core_operator_id='NL-vodafoneziggo',
         share=ND(ACM_NOTE),
         launch=V(2020, 'https://www.ericsson.com/en/press-releases/2020/4/vodafoneziggo-launches-5g-with-ericsson-spectrum-sharing',
                  'launched 5G with Ericsson spectrum sharing (Apr 2020); matches the discovery list (2020-04); the page returned 403 at coding time'),
         ran5=[R('Ericsson', 'not_disclosed', 'https://digital-strategy.ec.europa.eu/en/miscellaneous/netherlands-signs-three-year-5g-network-modernisation-agreement-between-vodafoneziggo-and-ericsson',
                 "three-year modernisation of 3,000 sites incl. 3.5 GHz (Nov 2025). UNVERIFIED: the core panel's 'all-Ericsson footprint' and 'sole macro "
                 "radio supplier' (Ericsson releases, Oct 2025 and Oct 2017) could not be checked (403); the EC page has no exclusivity wording")],
         ran4=[R('Ericsson', 'not_disclosed', 'https://www.ericsson.com/en/press-releases/2017/10/ericsson-and-vodafoneziggo-prepare-for-5g-readiness',
                 'the core panel codes the 4G legacy RAN as Ericsson (2017 release, not checked: 403)')],
         gov=[G('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 17.005026, 'Vodafone Group Plc',
                'via_parent', '2026-03-31', VODAFONE_AR,
                "Vodafone names e& without calling it state-owned; e&'s 2025 integrated report gives the Emirates Investment Authority 60%, "
                "ultimately controlled by the UAE Federal Government", link_url=E_AND_AR,
                chain='Vodafone Group Plc 10% of Ziggo Group (Liberty Global took full control in Aug 2026) -> VodafoneZiggo')],
         gov_dropped=VOD_DROPPED,
         core=V('Ericsson', 'https://www.ericsson.com/en/press-releases/2018/2/vodafoneziggo-deploys-ericsson-packet-core-to-manage-future-data-demands',
                'Ericsson packet core (Feb 2018); the core panel cites the Apr 2020 5G launch with Ericsson'),
         first_contract=ND(), vendor_operates=ND()),
]
