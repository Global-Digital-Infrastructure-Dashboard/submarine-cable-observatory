"""Core-94 panel government stakes under Prof. Shen's ownership rule (2026-11 review), and the ownership_type
derived from them.

Her rule: record each government stake separately; keep direct and via-parent stakes apart; never sum across
governments. Each row below is one holder, with its percentage of the company it holds (pct_of), never
multiplied down the chain. Holders below 5% are not recorded unless they have a board seat; they are listed in
DROPPED. The facts come from the coded panel's own ownership evidence (data/5g_operator_panel.csv.insession.jsonl),
re-expressed at the parent level; `source` repeats that row's ownership source.

ownership_type (researcher decision 2026-11-23): the largest single government's effective stake decides it. A
government's own entities are combined (the Federal Republic of Germany with KfW, the French State with Bpifrance),
and via-parent stakes are multiplied through the chain as the panel did before (`factor`; 1.0 where the earlier
coding assumed a wholly owned subsidiary). Above 10% -> state_backed_minority, 50% or more -> state_owned.
ownership_type stays PROVISIONAL where any recorded holder's state link rests on data/state_holders.csv
(state_link_basis = reference_list) rather than on a source.

state_equity_pct (the old cross-government sum) is kept in the panel as a deprecated column.

  python3 gov_stakes_core.py          check, then write data/5g_operator_gov_stakes.csv and patch the panel's
                                      ownership columns in place (idempotent)
  python3 gov_stakes_core.py --dry    check and print the ownership changes only
"""
import csv, json, sys

PANEL = 'data/5g_operator_panel.csv'
STAKES_CSV = 'data/5g_operator_gov_stakes.csv'
CODED_LOG = 'data/5g_operator_panel.csv.insession.jsonl'
RULE_DATE = '2026-11-23'
GOV_THRESHOLD_PCT = 5.0
STATE_BACKED_PCT, STATE_OWNED_PCT = 10, 50
STATE_TYPES = ('state_owned', 'state_backed_minority')
NEW_COLUMNS = ['largest_government', 'largest_government_stake_pct', 'government_stakes_below_threshold']

PROVISIONAL_NOTE = ("ownership_type PROVISIONAL: a recorded holder's state link rests on data/state_holders.csv "
                    "(reference list), not on a source; pending Prof. Shen's review of that list")
OLD_PROVISIONAL_PREFIX = 'ownership_type PROVISIONAL:'
RULE_NOTE_PREFIX = 'ownership rule ' + RULE_DATE


def H(government, holder, holder_type, pct, pct_of, basis, as_of, source, link='stated_in_source', link_source='',
      parent_pct=None, chain='', factor=1.0, board_seat='not_checked', note=''):
    return dict(government=government, holder=holder, holder_type=holder_type, pct=pct, pct_of=pct_of, basis=basis,
                as_of=as_of, source=source, state_link_basis=link, state_link_source=link_source if link == 'stated_in_source' else '',
                parent_ownership_pct_of_operator=parent_pct, ownership_chain=chain, factor=factor, board_seat=board_seat, note=note)


# ---------------------------------------------------------------- shared parent-level facts
DT_AR = 'Deutsche Telekom Annual Report 2025 (shareholdings at 31 Dec 2025)'


def dt(source, factor=1.0, parent_pct=None, chain='', bund=14.1, kfw=14.2, as_of='2025-12-31', kfw_link='stated_in_source', note=''):
    return [H('Germany', 'Federal Republic of Germany', 'government_ministry', bund, 'Deutsche Telekom AG', 'via_parent', as_of, source,
              link_source=source, parent_pct=parent_pct, chain=chain, factor=factor, note=note),
            H('Germany', 'KfW', 'state_holding_company', kfw, 'Deutsche Telekom AG', 'via_parent', as_of, source,
              link=kfw_link, link_source=source, parent_pct=parent_pct, chain=chain, factor=factor, note=note)]


VOD_AR = 'Vodafone Group 2026 Annual Report (notified holdings at 31 Mar 2026)'
E_AND_LINK = 'e& Integrated Annual Report 2025: Emirates Investment Authority 60%, ultimately controlled by the UAE Federal Government'


def vod(source=VOD_AR, factor=1.0, parent_pct=None, chain='', note=''):
    return [H('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 17.005026,
              'Vodafone Group Plc', 'via_parent', '2026-03-31', source, link_source=E_AND_LINK, parent_pct=parent_pct,
              chain=chain, factor=factor, note=note)]


VOD_DROPPED = ['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)']
ORANGE_URD = 'Orange 2025 Universal Registration Document (French State 13.39%, Bpifrance Participations 9.56% of Orange S.A.)'


def orange(source=ORANGE_URD, factor=1.0, parent_pct=None, chain='', basis='via_parent', as_of='2025-12-31'):
    kw = dict(parent_pct=parent_pct, chain=chain) if basis == 'via_parent' else {}
    return [H('France', 'French State', 'government_ministry', 13.39, 'Orange S.A.', basis, as_of, source, link_source=source, factor=factor, **kw),
            H('France', 'Bpifrance Participations', 'state_holding_company', 9.56, 'Orange S.A.', basis, as_of, source, link_source=source,
              factor=factor, **kw)]


def telia(source, factor=1.0, parent_pct=None, chain='', basis='via_parent', as_of='2025-12-31'):
    kw = dict(parent_pct=parent_pct, chain=chain) if basis == 'via_parent' else {}
    return [H('Sweden', 'Swedish State', 'government_ministry', 41.1, 'Telia Company AB', basis, as_of, source, link_source=source, factor=factor, **kw)]


def telenor(source, factor=1.0, parent_pct=None, chain='', pct=53.97, basis='via_parent', as_of='2026-02-27'):
    kw = dict(parent_pct=parent_pct, chain=chain) if basis == 'via_parent' else {}
    return [H('Norway', 'Government of Norway', 'government_ministry', pct, 'Telenor ASA', basis, as_of, source, link_source=source, factor=factor, **kw)]


def obag(source, factor=1.0, parent_pct=None, chain=''):
    return [H('Austria', 'Österreichische Beteiligungs AG (ÖBAG)', 'state_holding_company', 28.42, 'Telekom Austria AG', 'via_parent', '2025-12-31',
              source, link_source=source, parent_pct=parent_pct, chain=chain, factor=factor)]


def eand_ppf(source):
    return [H('United Arab Emirates', 'Emirates Telecommunications Group Company PJSC (e&)', 'state_owned_company', 50.0,
              'e& PPF Telecom Group B.V.', 'via_parent', '2025-12-31', source, link_source=source,
              chain='e& PPF Telecom Group B.V. -> PPF TMT Bidco 1 N.V. 100% -> operator (holding company for O2 Slovakia, Yettel Hungary, Yettel Bulgaria, Yettel Serbia)',
              note='50% plus one share; the accounts name the UAE Federal Government as ultimate controlling party')]


def telefonica(sepi, pif, source, factor=1.0, parent_pct=None, chain='', basis='via_parent', pif_holder='Public Investment Fund'):
    kw = dict(parent_pct=parent_pct, chain=chain) if basis == 'via_parent' else {}
    return [H('Spain', 'Sociedad Estatal de Participaciones Industriales (SEPI)', 'state_holding_company', sepi, 'Telefónica, S.A.', basis,
              '2025-12-31', source, link='reference_list', factor=factor, **kw),
            H('Saudi Arabia', pif_holder, 'sovereign_wealth_fund', pif, 'Telefónica, S.A.', basis, '2025-12-31', source,
              link='reference_list', factor=factor, **kw)]


TEF_CGR = 'Telefónica S.A. Annual Report on Corporate Governance 2025 (SEPI 10.00%, PIF 9.97% at 31 Dec 2025)'
ASSUMED = 'percentage of the operating subsidiary not stated; the earlier coding treated it as wholly owned (factor 1)'

# Researcher decision 2026-11-23: these two rows' own evidence did not state KfW's state link, but the same Deutsche
# Telekom filings coded in the other seven DT rows do, so KfW is stated_in_source here too (consistency).
KFW_LINK_NOTE = ("KfW's state link is stated in the Deutsche Telekom evidence of the other DT rows (PL, GR, CZ, HU, SK, US, HR); "
                 "this row's own ownership search did not state it")

STAKES = {
    # ------------------------------------------------ Deutsche Telekom group
    'DE-telekom-deutschland': dt(DT_AR, chain='Deutsche Telekom AG -> Telekom Deutschland GmbH; ' + ASSUMED, note=KFW_LINK_NOTE),
    'PL-t-mobile-polska': dt(DT_AR + '; T-Mobile Polska shareholder notice', chain='Deutsche Telekom AG -> T-Mobile Polska; ' + ASSUMED),
    'AT-t-mobile-austria': dt(DT_AR, chain='Magenta Telekom wholly owned within the Deutsche Telekom Group (answer statement)', note=KFW_LINK_NOTE),
    'GR-ote-cosmote-telekom-telekom': dt('Deutsche Telekom Annual Report 2025 (DT 54.38% of OTE; Bund 14.1% and KfW 14.2% of DT, 31 Dec 2025)',
                                         factor=0.5438, parent_pct=54.38, chain='Deutsche Telekom AG 54.38% of OTE (itself listed in Athens)'),
    'CZ-t-mobile-czech-republic': dt('Deutsche Telekom Interim Report 9M 2026 (30 Sep 2026)', bund=14.22, kfw=14.37, as_of='2026-09-30',
                                     chain='Deutsche Telekom AG -> T-Mobile Czech Republic; ' + ASSUMED),
    'HU-magyar-telekom': dt('Deutsche Telekom Annual Report 2025, note 19 (31 Dec 2025)', factor=0.6578,
                            chain='Deutsche Telekom AG ~65.78% indirect of Magyar Telekom (itself listed)'),
    'HR-hrvatski-telekom': dt(DT_AR + ", cross-referenced: HT's own ownership search did not return DT's shareholders; the same figures are coded in the other DT rows",
                              factor=0.546, chain="Deutsche Telekom AG -> DT Europe B.V. (DT's percentage not stated; treated as wholly owned) -> 54.6% of HT",
                              note=("recoded 2026-11-23 under Prof. Shen's rule (HT was the lead example for her parent question). "
                                    "Croatian War Veterans' Fund 7.1% NOT a state holder (researcher decision 2026-11-23): HT's 2025 "
                                    "annual report (pp. 8, 19, 29, EN and HR editions) names it without any state link while it attributes "
                                    "CERP's 1.9% to the Republic of Croatia; the earlier 'state link: source' came from the search summary")),
    'SK-slovak-telekom': dt('Deutsche Telekom Annual Report 2025, note 19 (31 Dec 2025)', chain='Deutsche Telekom AG -> Slovak Telekom; ' + ASSUMED),
    'US-t-mobile-usa': dt('Deutsche Telekom Annual Report 2025 (DT 52.6% of T-Mobile US; Bund 14.1% and KfW 14.2% of DT, 31 Dec 2025)',
                          factor=0.526, parent_pct=52.6, chain='Deutsche Telekom AG 52.6% of T-Mobile US (itself listed)'),
    # ------------------------------------------------ Vodafone group (Norges Bank 3.0004% dropped everywhere)
    'DE-vodafone': vod(chain="Vodafone Group Plc -> Vodafone GmbH; the group's percentage is not published; " + ASSUMED),
    'GB-vodafonethree': vod(VOD_AR + '; Vodafone release 30 Jul 2026', parent_pct=100.0,
                            note="Vodafone completed its buyout of CKHGT's 49% on 30 Jul 2026"),
    'IE-vodafone-ireland-limited': vod(chain='Vodafone Group Plc -> Vodafone Ireland; ' + ASSUMED),
    'PT-vodafone-portugal': vod(chain='Vodafone Group Plc -> Vodafone Portugal; ' + ASSUMED),
    'GR-vodafone-greece': vod(VOD_AR + '; Vodafone Group holding structure, 12 May 2026 (Greece 99.9%)', factor=0.999, parent_pct=99.9),
    'CZ-vodafone-czech-republic': vod(chain='Vodafone Group Plc -> Vodafone Czech Republic; ' + ASSUMED,
                                      note="Vega's Jul 2026 agreement to buy e&'s stake is not shown as completed"),
    'RO-vodafone-romania': vod(chain='Vodafone Group Plc -> Vodafone Romania; ' + ASSUMED),
    'NL-vodafoneziggo': vod(VOD_AR + '; Ziggo Group completion announcement, Aug 2026 (Vodafone 10% of Ziggo Group)', factor=0.1,
                            chain='Vodafone Group Plc 10% of Ziggo Group (Liberty Global took full control in Aug 2026) -> VodafoneZiggo'),
    # ------------------------------------------------ Telefónica
    'DE-telefonica-germany': telefonica(10.0, 9.97, TEF_CGR, factor=0.9684, parent_pct=96.84,
                                        chain='Telefónica, S.A. ~96.84% of Telefónica Deutschland'),
    'ES-telefonica-moviles-espana': telefonica(10.0, 9.999, 'Telefónica Annual Report on Corporate Governance 2025 (as of 31 Dec 2025)',
                                               chain='Telefónica, S.A. -> Telefónica Móviles España; ' + ASSUMED,
                                               pif_holder='Public Investment Fund (via Green Bridge Investment Company SCS and Saudi Telecom Company)'),
    'GB-telefonica-uk': telefonica(10.0, 9.97, TEF_CGR + '; Telefónica Individual Annual Accounts 2025', factor=0.5, parent_pct=50.0,
                                   chain='Telefónica, S.A. 50% of the VMED O2 UK joint venture with Liberty Global'),
    # ------------------------------------------------ Orange group
    'FR-orange-france': orange('Orange 2025 Universal Registration Document', basis='direct'),
    'PL-orange-polska': orange(ORANGE_URD + '; Orange Polska 2025 annual report (Orange S.A. 50.67%)', factor=0.5067, parent_pct=50.67),
    'BE-orange-belgium': orange(ORANGE_URD + '; Orange Belgium Annual Report 2025 (Atlas Services Belgium 76.29%)', factor=0.7629,
                                chain='Orange S.A. -> Atlas Services Belgium 76.29% of Orange Belgium'),
    'SK-orange-slovensko': orange('Orange S.A. AMF prospectus supplement, 9 Jun 2026 (31 Dec 2025)',
                                  chain='Orange S.A. -> Atlas Services Belgium -> 100% of Orange Slovensko'),
    # Researcher decision 2026-11-24 (migration): Orange S.A. owns 100% of MasOrange since 8 Jun 2026 (Lorca's 50% acquired).
    'ES-masorange': orange(ORANGE_URD + '; Light Reading, Sep 2026 (MasOrange now wholly owned by Orange)', parent_pct=100.0,
                           chain="Orange S.A. 100% of MasOrange since 8 Jun 2026 (a 50:50 joint venture with Lorca before)"),
    'RO-orange-romania': [
        H('Romania', 'Romanian Ministry of Research, Innovation and Digitalization', 'government_ministry', 20.0, 'Orange Romania', 'direct',
          '2025-12-31', 'Orange 2025 Universal Registration Document', link_source='Orange 2025 Universal Registration Document',
          note="recoded 2026-11-23 under Prof. Shen's rule (Orange Romania was the lead example for summing across states)"),
        *orange(ORANGE_URD + '; Orange 2025 consolidated financial statements (Orange S.A. 80%)', factor=0.8, parent_pct=80.0),
    ],
    # ------------------------------------------------ Telia, Telenor
    'SE-telia': telia('Telia Company, Shareholdings as of June 30, 2026', basis='direct', as_of='2026-06-30'),
    'NO-telia-norge': telia('Telia Company Annual Report 2025 (shareholders at 31 Dec 2025)', chain='Telia Company AB -> Telia Norge AS; ' + ASSUMED),
    'EE-telia-eesti': telia('Telia Company shareholdings as of 30 Jun 2026', as_of='2026-06-30', chain='Telia Company AB -> Telia Eesti; ' + ASSUMED),
    'LT-telia-lietuva': telia('Telia Company Annual Report 2025 (Swedish State 41.1%); Telia Lietuva Annual Report 2025 (Telia Company 88.15%)',
                              factor=0.8815, parent_pct=88.15),
    # Researcher decision 2026-11-24 (migration): treated as wholly owned by Telia Company, like Telia Norge / Telia Eesti.
    'FI-telia-finland': telia('Telia Company Annual Report 2025 (shareholders at 31 Dec 2025)', chain='Telia Company AB -> Telia Finland Oyj; ' + ASSUMED),
    'SE-telenor': telenor("Telenor's Share and Shareholders page, 27 Feb 2026", chain='Telenor ASA -> Telenor Sverige; percentage not stated; ' + ASSUMED),
    'NO-telenor-norge': telenor('Telenor ASA major shareholders as of 27 February 2026', chain='Telenor ASA -> Telenor Norge; ' + ASSUMED),
    'FI-dna': telenor('Telenor ASA, Shareholders as of 27 February 2026; DNA stock exchange release archive',
                      chain="Telenor ASA -> Telenor Finland Holding Oy (sole shareholder of DNA; Telenor's percentage of it not stated)"),
    'DK-tt-network': telenor('Telenor Annual Report 2025 (Norwegian state 54% of Telenor at 31 Dec 2025; Danish network joint operation 50% Telenor)',
                             pct=54.0, as_of='2025-12-31', factor=0.5, parent_pct=50.0,
                             chain="Telenor ASA 50% of the TT-Netværket joint operation; the other 50% owner's state holders are unknown"),
    # ------------------------------------------------ Swisscom, Proximus, A1, Elisa, 4iG, e& PPF, TIM, China
    'CH-swisscom': [H('Switzerland', 'Swiss Confederation', 'government_ministry', 51.0, 'Swisscom Ltd', 'direct', '2025-12-31',
                      'Swisscom Ltd 2025 Financial Statements (holding as of 31 Dec 2025)', link_source='Swisscom Ltd 2025 Financial Statements')],
    'IT-fastweb': [H('Switzerland', 'Swiss Confederation', 'government_ministry', 51.0, 'Swisscom Ltd', 'via_parent', '2025-12-31',
                     'Swisscom annual report / 2025 financial statements, major shareholders as of 31 Dec 2025',
                     link_source='Swisscom annual report 2025', chain='Swisscom Ltd -> Fastweb; ' + ASSUMED)],
    # Researcher decision 2026-11-24 (migration): Swisscom has owned Vodafone Italia since 31 Dec 2024; merged into Fastweb
    # S.p.A. on 1 Jan 2026. The core panel keeps both rows (not back-ported); the migrated files carry one Fastweb row.
    'IT-vodafone-italia': [H('Switzerland', 'Swiss Confederation', 'government_ministry', 51.0, 'Swisscom Ltd', 'via_parent', '2025-12-31',
                             'Swisscom annual report / 2025 financial statements, major shareholders as of 31 Dec 2025',
                             link_source='Swisscom annual report 2025', parent_pct=100.0,
                             chain='Swisscom Ltd 100% of Vodafone Italia since 31 Dec 2024; merged into Fastweb S.p.A. on 1 Jan 2026')],
    'BE-proximus': [H('Belgium', 'Federal Holding and Investment Company (SFPIM)', 'state_holding_company', 53.51, 'Proximus PLC', 'direct',
                      '2026-01', 'Proximus Integrated Annual Report 2025 (shareholder analysis Jan 2026)',
                      link_source='Proximus Integrated Annual Report 2025')],
    'AT-a1-telekom-austria': obag('A1 Telekom Austria Group Annual Financial Report 2025, shareholding at 31 Dec 2025',
                                  chain='Telekom Austria AG (listed) -> A1 Telekom Austria AG; ' + ASSUMED),
    'HR-a1-hrvatska': obag('A1 Telekom Austria Group Jahresfinanzbericht 2025 (31 Dec 2025)', parent_pct=100.0,
                           chain='A1 Hrvatska wholly owned by Telekom Austria AG; América Móvil holds 60.94% of Telekom Austria'),
    'BG-a1-bulgaria': obag('A1 Group Annual Financial Report 2025 (31 Dec 2025)', chain='Telekom Austria AG -> A1 Bulgaria; ' + ASSUMED),
    'FI-elisa': [H('Finland', 'Solidium Oy', 'state_holding_company', 10.04, 'Elisa Oyj', 'direct', '2026-08-14',
                   'Stocksummer shareholder data, 14 Aug 2026', link_source='Stocksummer shareholder data',
                   note='S&P puts the Finnish state at 10.5% (Mar 2026)')],
    'EE-elisa-eesti': [H('Finland', 'Finnish government (incl. Solidium Oy)', 'government_ministry', 10.5, 'Elisa Oyj', 'via_parent', '2026-03-24',
                         'S&P Global RatingsDirect tear sheet on Elisa Oyj, 10 Apr 2026', link_source='S&P Global RatingsDirect tear sheet',
                         chain='Elisa Oyj -> Elisa Eesti; ' + ASSUMED,
                         note="FLAG (threshold): 10.0% via Solidium per a second source (Oct 2026) would not cross 'above 10%'")],
    'HU-one-magyarorszag': [H('Hungary', 'Corvinus Nemzetközi Befektetési Zrt.', 'state_holding_company', 37.9, '4iG Távközlési Holding Zrt.',
                              'via_parent', '2026-03-31', '4iG consolidated report 2026 Q1 (31 Mar 2026)', link_source='4iG consolidated report 2026 Q1',
                              parent_pct=100.0, note="4iG Távközlési Holding is One's sole shareholder; no state holder of 4iG Plc.")],
    'HU-yettel-magyarorszag': eand_ppf('e& PPF Telecom Group B.V. FY2025 annual accounts'),
    'SK-o2-slovakia': eand_ppf('e& PPF Telecom Group B.V. FY2025 annual accounts'),
    'BG-yettel-bulgaria': eand_ppf('Yettel Bulgaria ESG Report 2025; e& Q4 2025 financial report (50% plus one share); e& Integrated Annual Report 2025 (EIA 60%)'),
    'IT-telecom-italia': [H('Italy', 'Poste Italiane S.p.A.', 'state_owned_company', 86.952, 'Telecom Italia S.p.A.', 'direct', '2026-09-30',
                            'TIM shareholders page (30 Sep 2026); Poste Italiane offer document, Jul 2026', link_source='TIM shareholders page',
                            note='Poste stake rose from 27.32% (Dec 2025); the CDP stake in Poste is not quantified')],
    'CN-china-mobile': [H('China', 'China Mobile Communications Group Co., Ltd. (CMCC)', 'state_owned_company', 68.75, 'China Mobile Limited',
                          'direct', '2025-12-31', 'China Mobile Limited 2025 annual report materials; US Federal Register, 10 Jun 2026',
                          link_source='US Federal Register, 10 Jun 2026 (CMCC directly owned and controlled by SASAC)')],
    'CN-china-unicom': [H('China', 'China United Network Communications Group Company Limited (Unicom Group)', 'state_owned_company', 80.67,
                          'China Unicom (Hong Kong)', 'via_parent', '2026-06-30', 'China Unicom (Hong Kong) interim report 2026 (30 Jun 2026)',
                          link_source='China Unicom 2025 annual report notes (SOE directly controlled by the PRC government)',
                          chain=('Unicom Group -> China United Network Communications Limited 53.52% + Unicom Group BVI 27.15% -> China Unicom '
                                 '(Hong Kong); the filing reports 80.67% as an indirect/deemed interest in the operator itself, so no '
                                 'multiplication (factor 1)'),
                          note='recoded direct -> via_parent 2026-11-24 (researcher decision); ownership_type unchanged')],
    'CN-china-telecom': [H('China', 'China Telecommunications Corporation', 'state_owned_company', 63.9, 'China Telecom Corporation Limited',
                           'direct', '2025-12-31', 'China Telecom 2025 annual report, changes in shares', link_source='China Telecom 2025 annual report'),
                         H('China', 'Guangdong Rising Holdings Group Co., Ltd.', 'state_owned_company', 5.24, 'China Telecom Corporation Limited',
                           'direct', '2025-12-31', 'China Telecom 2025 annual report, changes in shares', link_source='China Telecom 2025 annual report')],
    'CN-china-broadnet': [H('China', 'China Broadcasting Network Corporation', 'state_owned_company', 51.0, 'China Broadnet', 'direct', '2022-06-27',
                            'TelecomTV and RCR Wireless, 27 Jun 2022', link_source='TelecomTV and RCR Wireless, 27 Jun 2022'),
                          H('China', 'State Grid Information & Telecommunication Group', 'state_owned_company', None, 'China Broadnet', 'direct',
                            '2022-06-27', 'TelecomTV and RCR Wireless, 27 Jun 2022', link_source='TelecomTV and RCR Wireless, 27 Jun 2022',
                            note='share not stated; kept because it is a named strategic shareholder')],
}

DROPPED = {
    **{oid: VOD_DROPPED for oid in STAKES if oid in (
        'DE-vodafone', 'GB-vodafonethree', 'IE-vodafone-ireland-limited', 'PT-vodafone-portugal', 'CZ-vodafone-czech-republic',
        'RO-vodafone-romania')},
    'GR-vodafone-greece': ['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)'],
    'NL-vodafoneziggo': ['Norges Bank 3.0004% of Vodafone Group Plc (2026-03-31; board seat not checked)'],
    'SE-telia': ['Norges Bank 1.7% of Telia Company AB (2026-06-30; board seat not checked)'],
    'FI-telia-finland': ['Norges Bank 1.7% of Telia Company AB (2026-06-30; board seat not checked)'],
    'NO-telenor-norge': ['Kuwait Investment Authority 0.53% of Telenor ASA (2026-02-27; board seat not checked)'],
    'HR-hrvatski-telekom': ['CERP (Restructuring and Sale Center) / Republic of Croatia 1.9% of Hrvatski Telekom (2025-12-31; board seat not checked)'],
    'SE-tele2': ['Norges Bank Investment Management 1.6% of Tele2 AB (2025-12-31; board seat not checked)'],
    'LT-tele2': ['Norges Bank Investment Management 1.69% of Tele2 AB (Nov 2026; board seat not checked)'],
    'PT-nos': ['Mubadala Investment Company 3.202% of NOS (Sep 2026, MarketScreener; 5.00% at end-2024; board seat not checked)'],
}

# Corrections to the deprecated state_equity_pct / state_holders text that the per-holder rows supersede.
ROW_NOTES = {
    'HR-hrvatski-telekom': ("the Croatian War Veterans' Fund listed in state_holders is not a state holder (HT 2025 annual report "
                            "gives it no state link; researcher decision 2026-11-23), so state_equity_pct overstates the Croatian stake"),
}

# Where no government's stake crosses 10% any more, the type the operator has without state equity, from the
# panel's own evidence (the listed parent).
FALLBACK_TYPE = {
    'DE-telefonica-germany': ('listed', 'Telefónica, S.A. is listed'),
    'ES-telefonica-moviles-espana': ('listed', 'Telefónica, S.A. is listed'),
}

def effective(h):
    return None if h['pct'] is None else round(h['pct'] * h['factor'], 4)


def by_government(stakes):
    totals = {}
    for h in stakes:
        if h['pct'] is not None:
            totals[h['government']] = round(totals.get(h['government'], 0) + effective(h), 4)
    return totals


def derive(oid):
    """(ownership_type or None, largest government, its effective stake, provisional?) for one operator."""
    stakes = STAKES.get(oid)
    if not stakes:
        return None, '', None, False
    totals = by_government(stakes)
    gov, pct = max(totals.items(), key=lambda kv: kv[1]) if totals else ('', None)
    if pct is not None and pct >= STATE_OWNED_PCT:
        otype = 'state_owned'
    elif pct is not None and pct > STATE_BACKED_PCT:
        otype = 'state_backed_minority'
    else:
        otype = None  # no state type; the caller keeps or falls back to the non-state type
    provisional = otype in STATE_TYPES and any(h['state_link_basis'] == 'reference_list' for h in stakes)
    return otype, gov, pct, provisional


def apply_ownership(row):
    """Rewrite one panel row's ownership columns in place (used by build_row and by the patch below)."""
    oid = row['operator_id']
    notes = [n for n in row['notes'].split(' | ') if n and n != 'none'
             and not n.startswith(OLD_PROVISIONAL_PREFIX) and not n.startswith(RULE_NOTE_PREFIX)]
    otype, gov, pct, provisional = derive(oid)
    if oid in STAKES or oid in DROPPED:
        if otype:
            row['ownership_type'] = otype
        elif row['ownership_type'] in STATE_TYPES:
            row['ownership_type'] = FALLBACK_TYPE[oid][0]
        row['largest_government'] = gov or 'none'
        row['largest_government_stake_pct'] = f'{pct:g}' if pct is not None else 'not_applicable'
        detail = f"largest single government {gov} {pct:g}%" if gov else 'no government stake of 5% or more'
        extra = f"; {FALLBACK_TYPE[oid][1]}" if oid in FALLBACK_TYPE and not otype else ''
        notes.append(f"{RULE_NOTE_PREFIX} (Prof. Shen): per-holder stakes in {STAKES_CSV}, never summed across governments; "
                     f"ownership_type from the {detail} (a government's own entities combined, via-parent stakes multiplied); "
                     f"state_equity_pct is the deprecated cross-government sum{extra}"
                     + (f"; {ROW_NOTES[oid]}" if oid in ROW_NOTES else ''))
    else:
        row['largest_government'] = 'none'
        row['largest_government_stake_pct'] = 'not_applicable'
    row['government_stakes_below_threshold'] = '; '.join(DROPPED.get(oid, [])) or 'none'
    row['ownership_type_provisional'] = 'yes' if provisional else 'no'
    if provisional:
        notes.append(PROVISIONAL_NOTE)
    row['notes'] = ' | '.join(notes) or 'none'
    return row


def check():
    """Per government, the recorded stakes' effective total must match the earlier coding's multiplied holders for
    that state, except where a holder was dropped under the 5% rule or added in this recode (EXPECTED)."""
    coded = {}
    for line in open(CODED_LOG):
        e = json.loads(line)
        coded[e['row_id']] = e['fields']['state_equity']
    rows = {r['operator_id']: r for r in csv.DictReader(open(PANEL))}
    problems = []
    for oid, stakes in STAKES.items():
        if oid not in rows:
            problems.append(f'{oid}: not in the panel')
            continue
        for h in stakes:
            if not (h['pct'] is None or h['pct'] >= GOV_THRESHOLD_PCT or h['board_seat'] == 'yes'):
                problems.append(f'{oid}: {h["holder"]} below the threshold')
        se = coded.get(rows[oid]['row_id'])
        old = {}
        for h in (se['value']['holders'] if se and se['status'] == 'value' else []):
            if h['pct'] is not None:
                old[h['state']] = round(old.get(h['state'], 0) + h['pct'], 4)
        for gov, total in by_government(stakes).items():
            want = EXPECTED.get((oid, gov), old.get(gov))
            if want is None or abs(want - total) > 0.03:
                problems.append(f'{oid}: {gov} effective {total} vs coded {old.get(gov)}')
    return problems


# Deliberate differences from the earlier coding: HT now counts the German state via DT (absent before); Croatia
# drops out (CERP's 1.9% is below 5%, and the War Veterans' Fund is not a state holder).
# Migration decisions 2026-11-24: Telia Finland, MasOrange and Vodafone Italia had no coded state equity (not_disclosed);
# their parent-level stakes are added here.
EXPECTED = {('HR-hrvatski-telekom', 'Germany'): round(28.3 * 0.546, 4),
            ('FI-telia-finland', 'Sweden'): 41.1,
            ('ES-masorange', 'France'): round(13.39 + 9.56, 4),
            ('IT-vodafone-italia', 'Switzerland'): 51.0}


def main(dry=False):
    problems = check()
    if problems:
        sys.exit('\n'.join(problems))
    rows = list(csv.DictReader(open(PANEL)))
    fields = list(rows[0])
    fields = [c for c in fields if c not in NEW_COLUMNS]
    at = fields.index('state_equity_source') + 1
    fields[at:at] = NEW_COLUMNS
    changes = []
    for r in rows:
        before = (r['ownership_type'], r['ownership_type_provisional'])
        apply_ownership(r)
        if before != (r['ownership_type'], r['ownership_type_provisional']):
            changes.append(f"{r['operator_id']}: {before[0]}/{before[1]} -> {r['ownership_type']}/{r['ownership_type_provisional']} "
                           f"({r['largest_government']} {r['largest_government_stake_pct']})")
    print(f'{len(changes)} rows change ownership_type or provisional flag:')
    print('\n'.join(changes))
    if dry:
        return
    with open(PANEL, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    names = {r['operator_id']: (r['market'], r['operator_name']) for r in rows}
    out = []
    for oid, stakes in STAKES.items():
        for h in stakes:
            out.append(dict(operator_id=oid, market=names[oid][0], operator_name=names[oid][1],
                            **{k: ('' if v is None else v) for k, v in h.items() if k != 'factor'},
                            effective_pct_for_classification='' if h['pct'] is None else effective(h)))
    with open(STAKES_CSV, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    print(f'{PANEL}: patched; {STAKES_CSV}: {len(out)} rows ({len(STAKES)} operators); dropped-holder lists for {len(DROPPED)} operators')


if __name__ == '__main__':
    main(dry='--dry' in sys.argv)
