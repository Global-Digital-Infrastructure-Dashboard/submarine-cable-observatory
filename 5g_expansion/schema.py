"""Shared schema for the 5G expansion coding (Prof. Shen's reduced schema, as revised in her 2026-11 review).

Constructors used by the coded_batch*.py files:
  V(value, url, note='', year=None)  a sourced scalar value
  ND(note='')                        not_disclosed
  R(vendor, share, url, note='')     one RAN vendor (share: all / most / some / small / not_disclosed)
  G(...)                             one government stake (see below)
  S(...)                             one vendor switch

Source types are derived from the URL (SOURCE_TYPES_BY_DOMAIN, URL_OVERRIDES), so every fact from one
publisher gets the same type:
  company                  the operator, its parent, a vendor or a shareholder writing about itself
  government               regulators, ministries, parliaments, central banks, statistics agencies, ITU
  research_industry_group  think tanks, NGOs, analysts, industry associations, academic publishers
  news                     news media and trade press
  other                    aggregators, directories, wikis, blogs, document-sharing sites

Government stakes (one row per holder; never summed across holders or governments; never multiplied down
the chain). pct is a percentage of pct_of. basis is direct (held in the operator itself) or via_parent.
Rows below 5% are not recorded unless the holder has a board seat; such holders are listed in the
operator's gov_dropped list instead, so the exclusion is visible.
  holder_type        government_ministry / state_holding_company / sovereign_wealth_fund / pension_fund /
                     state_owned_company (the fifth type, for state-owned operating companies such as e&, VNPT or
                     Tojiktelecom; approved by Prof. Shen 2026-11-26). A municipality or other local government
                     holding shares itself is coded government_ministry with government_level = local.
  government_level   national / local (Prof. Shen, 2026-11-26): local = a municipality, county or province
  owner_body         state_owned_company rows: the government body that holds the company (ministry, state
                     investment agency, ...), with its source owner_body_url; '' when not found
  pension_rule       pension_fund rows (Prof. Shen's rule, 2026-11-26): a pension or social-security fund is
                     government-linked if it was set up by law to cover public employees or the general public
                     (law_coverage), or the government appoints its board or managers (gov_appoints_board), or
                     both. The basis must come from the fund's own website or its founding law, never a news
                     article; that source is the state_link_url
  state_link_basis   stated_in_source: a source says the holder is state-owned or state-controlled (that
                     source is state_link_url, which may differ from the stake's own source);
                     reference_list: only data/state_holders.csv makes the link
  parent_pct         for via_parent rows, the pct_of company's percentage of the operator when it holds the
                     operator directly; None when not disclosed or when the chain has more than one link (the
                     chain, with each link's percentage, is in chain)
  board_seat         yes / none_found / not_checked
"""
from urllib.parse import urlparse

GOV_THRESHOLD_PCT = 5.0
SHARE_CATEGORIES = ('all', 'most', 'some', 'small', 'not_disclosed')
HOLDER_TYPES = ('government_ministry', 'state_holding_company', 'sovereign_wealth_fund', 'pension_fund',
                'state_owned_company')
LINK_BASES = ('stated_in_source', 'reference_list')
BOARD_SEAT = ('yes', 'none_found', 'not_checked')
SOURCE_TYPES = ('company', 'government', 'research_industry_group', 'news', 'other')
GOV_LEVELS = ('national', 'local')
PENSION_RULES = ('law_coverage', 'gov_appoints_board', 'both')
SAMPLE_STATUS = ('main', 'pilot_only')   # pilot_only: kept but outside the main sample (Ukraine, Prof. Shen 2026-11-26)

# Canonical vendor names. A contract counterparty or predecessor company (NSN Israel, Alcatel-Lucent) is
# coded as the vendor group, and the name as found goes in the note.
VENDORS = ['Ericsson', 'Nokia', 'Huawei', 'ZTE', 'Samsung', 'Viettel High Tech', 'Rakuten Symphony', 'Mavenir',
           'Amdocs', 'Cisco', 'NEC', 'Fujitsu']

SOURCE_TYPES_BY_DOMAIN = {
    'company': [
        'ericsson.com', 'nokia.com', 'zte.com.cn', 'ucell.uz', 'uztelecom.uz', 'safaricom.co.ke', 'airtelkenya.com',
        'airtelstream.net', 'airtel.africa', 'proximusnxt.lu', 'proximus-cdn.com', 'orange.lu', 'orange.com',
        'starhub.com', 'singteldigital.com', 'm1.com.sg', 'simba.sg', 'links.sgx.com', 'partner.co.il',
        'ir.bezeq.co.il', 'investors.cellcom.co.il', 'ooredoo.com', 'viettel.com.vn', 'vnpt.com.vn', 'vnpt.vn',
        'tstt.co.tt', 'bmobile.co.tt', 'reports.investors.vodafone.com', 'postgroup.lu', 'post.lu', 'megafon.tj',
        'antel.com.uy', 'almadar.ly', 'eand.com', 'prnewswire.com', 'linkedin.com',
        # funds writing about themselves (pension rule, 2026-11-26)
        'gepf.co.za', 'atp.dk', 'ap3.se', 'epf.lk', 'ilmarinen.fi', 'tdcgroup.com', 'tdcnet.dk',
    ],
    'government': [
        'ca.go.ke', 'vpcp.chinhphu.vn', 'gub.uy', 'ttparliament.org', 'nbim.no', 'itu.int', 'ilr.lu', 'gov.uz',
        'mst.gov.vn', 'mic.gov.vn', 'imda.gov.sg', 'cs.gov.tj', 'openinfo.uz',
        # pension and social-security funds and statute databases (Prof. Shen's pension rule, 2026-11-26)
        'ssc.gov.jo', 'lom.agc.gov.my', 'lovdata.no', 'riksdagen.se', 'daman.gov.qa', 'api.sejm.gov.pl',
    ],
    'research_industry_group': [
        'inss.org.il', 'freedomhouse.org', 'gsma.com', 'oxfordbusinessgroup.com', 'library.oapen.org',
        'china-index.io', 'telegeography.com', 'samenacouncil.org', 'eias.org', 'via.org.vn',
    ],
    'news': [
        'datacenterdynamics.com', 'developingtelecoms.com', 'techtrendske.co.ke', 'technewstt.com', 'lightreading.com',
        'libyaherald.com', 'vietnam.vn', 'trinidadexpress.com', 'telecompaper.com', 'businesstimes.com.sg',
        'asiaplus.news', 'asiaplustj.info', 'globes.co.il', 'economictimes.indiatimes.com', 'tuoitre.vn',
        'vietnamnews.vn', 'telecomtv.com', 'mobileworldlive.com', 'newsday.co.tt',
        'ecoi.net',  # ecoi.net reprints news articles (here Eurasianet)
    ],
    'other': ['telcobrief.com', 'tadviser.com', 'powertec.com.au', 'marketbeat.com', 'scribd.com', 'wikipedia.org'],
}
# Documents whose author differs from the host: company filings published on a government site.
URL_OVERRIDES = {
    'https://www.imda.gov.sg/-/media/imda/files/regulations-and-licensing/regulations/consultations/2025/simba-and-m1/annex-b-non-confidential-abbreviated-statement-submitted-by-simba-and-m1.pdf': 'company',
    'https://openinfo.uz/media/int_report/08c4d98a-95e7-4ee7-8771-8093b193f1f5.pdf': 'company',
    # Lyse AS annual report 2025, filed on Euronext Oslo
    'https://live.euronext.com/sites/default/files/company_press_releases/attachments_oslo/2026/03/25/669268_Lyse%20%C3%85rsrapport%202025.pdf': 'company',
}


E_AND_AR = 'https://www.eand.com/content/dam/eand/assets/docs/annual-report/2025/eand-integrated-annualreporten.pdf'
# The government body that holds each state-owned company (Prof. Shen, 2026-11-26), applied by G() to every
# state_owned_company row whose holder name contains the key. (owner body, source); '' where no source names one.
OWNER_BODIES = {
    'e&': ("Emirates Investment Authority (60% of e&; e& states the EIA is ultimately controlled by the UAE Federal "
           "Government)", E_AND_AR),
    'Emirates Telecommunications': None,  # alias of 'e&', filled below
    'VNPT': ("Ministry of Finance (represents the state's 100% ownership since the commission for state capital was "
             "dissolved on 28 Feb 2025; the Ministry of Science and Technology proposed taking it over in May 2026)",
             'https://bizhub.vietnamnews.vn/science-ministry-seeks-ownership-at-vnpt-post402691.html'),
    'Tojiktelecom': ("Communications Service under the Government of the Republic of Tajikistan ('the state communications "
                     "agency', Eurasianet, Nov 2018; government percentage not stated)",
                     'https://www.ecoi.net/de/dokument/2001374.html'),
    'Tunisie Telecom': ("Government of Tunisia (65% of Tunisie Telecom, per GO's 2025 report; the holding body is not named)",
                        'https://rizzofarrugia.com/wp-content/uploads/GO-2025-Annual-Report.pdf'),
    'China Mobile Communications Group': ('State-owned Assets Supervision and Administration Commission of the State Council (SASAC)',
                                          'https://doc.irasia.com/listco/hk/chinamobile/annual/2023/ar2023.pdf'),
    'China Telecommunications Corporation': ('State-owned Assets Supervision and Administration Commission of the State Council (SASAC), '
                                             'named as ultimate controller',
                                             'https://www.chinatelecom-h.com/en/ir/report/annual2025/annual2025_12.pdf'),
    'China Broadcasting Network': ('National Radio and Television Administration (named as the state authority behind the group)',
                                   'https://www.lightreading.com/asia/chinas-newest-operator-launches-into-5g-market/d/d-id/778557'),
}
OWNER_BODIES['Emirates Telecommunications'] = OWNER_BODIES['e&']

# Pension and social-security funds that meet Prof. Shen's rule (2026-11-26), each sourced from the fund's own website
# or its founding law (quotes in 5g_expansion/verify_2026-11-26_rules.csv). G() fills pension_rule and state_link_url
# for any pension_fund row whose holder name contains the key. Checked and NOT meeting the rule: Polish open pension
# funds (OFE: created and run by a private joint-stock pension company, Act on pension funds arts. 3, 27, 40) and
# Ilmarinen (a mutual insurer whose board is elected by its supervisory board, not appointed by government).
PENSION_FUNDS = {
    'Social Security Corporation': ('law_coverage', 'https://www.ssc.gov.jo/en/about-the-corporation/'),
    'Government Employees Pension Fund': ('law_coverage', 'https://www.gepf.co.za/about-us/who-is-gepf/'),
    'Employees Provident Fund Board': ('both', 'https://lom.agc.gov.my/ilims/upload/portal/akta/LOM/EN/Act%20452.pdf'),
    'ATP': ('both', 'https://www.atp.dk/en/about-us/board-representatives-and-atps-supervisory-board'),
    'Folketrygdfondet': ('both', 'https://lovdata.no/dokument/NL/lov/2007-06-29-44'),
    'Third Swedish National Pension Fund': ('both', 'https://www.ap3.se/en/om-ap3/styrelse'),
    'General Retirement & Social Insurance Authority': ('both', 'https://www.daman.gov.qa/English/AboutUs/Pages/Vision-and-Mission.aspx'),
    "Employees' Provident Fund (Sri Lanka)": ('both', 'https://epf.lk/?page_id=2'),
}


def register(domains=None, overrides=None, vendors=None):
    """Called by a coded_batch module at import: its own new publisher domains ({type: [domain, ...]}), URL
    overrides ({url: type}) and canonical vendor names, so batches coded in parallel don't edit this file."""
    for stype, ds in (domains or {}).items():
        assert stype in SOURCE_TYPES, stype
        SOURCE_TYPES_BY_DOMAIN[stype].extend(ds)
    URL_OVERRIDES.update(overrides or {})
    VENDORS.extend(v for v in (vendors or []) if v not in VENDORS)


def source_type(url):
    if not url:
        return ''
    if url in URL_OVERRIDES:
        return URL_OVERRIDES[url]
    host = urlparse(url).netloc.lower()
    for stype, domains in SOURCE_TYPES_BY_DOMAIN.items():
        if any(host == d or host.endswith('.' + d) for d in domains):
            return stype
    raise KeyError(f'no source type for {host} ({url}); add it to SOURCE_TYPES_BY_DOMAIN')


def V(value, url, note='', year=None):
    return dict(status='value', value=value, year=year, source_url=url, note=note)


def ND(note=''):
    return dict(status='not_disclosed', value=None, year=None, source_url='', note=note)


def R(vendor, share, url, note=''):
    assert vendor in VENDORS, vendor
    assert share in SHARE_CATEGORIES, share
    return dict(vendor=vendor, share_category=share, source_url=url, note=note)


def G(government, holder, holder_type, pct, pct_of, basis, as_of, url, note='', link='stated_in_source',
      link_url=None, parent_pct=None, chain='', board_seat='not_checked', level='national', owner_body='',
      owner_body_url='', pension_rule=''):
    assert holder_type in HOLDER_TYPES, holder_type
    assert basis in ('direct', 'via_parent'), basis
    assert link in LINK_BASES, link
    assert board_seat in BOARD_SEAT, board_seat
    assert pct is None or pct >= GOV_THRESHOLD_PCT or board_seat == 'yes', (holder, pct)
    assert basis == 'via_parent' or (parent_pct is None and not chain), holder
    assert level in GOV_LEVELS, level
    if holder_type == 'state_owned_company' and not owner_body:
        found = [v for k, v in OWNER_BODIES.items() if k in holder and v]
        if found:
            owner_body, owner_body_url = found[0]
    assert holder_type == 'state_owned_company' or not owner_body, (holder, 'owner_body is for state_owned_company rows')
    assert bool(owner_body) == bool(owner_body_url), (holder, 'owner_body needs owner_body_url')
    if holder_type == 'pension_fund' and not pension_rule:
        found = [v for k, v in PENSION_FUNDS.items() if k in holder]
        if found:
            pension_rule, link_url, link = found[0][0], found[0][1], 'stated_in_source'
    if holder_type == 'pension_fund':
        assert pension_rule in PENSION_RULES and link == 'stated_in_source' and link_url, (holder, 'pension rule + fund source')
    else:
        assert not pension_rule, holder
    return dict(government=government, holder=holder, holder_type=holder_type, pct=pct, pct_of=pct_of, basis=basis,
                as_of=as_of, source_url=url, state_link_basis=link,
                state_link_url=(link_url or url) if link == 'stated_in_source' else '',
                parent_ownership_pct_of_operator=parent_pct, ownership_chain=chain, board_seat=board_seat,
                government_level=level, owner_body=owner_body, owner_body_url=owner_body_url, pension_rule=pension_rule,
                note=note)


def S(element, generation, old_vendor, new_vendor, announced, completed, url, note=''):
    """A vendor switch: old_vendor's equipment replaced by new_vendor's. new_vendor may be 'not_disclosed';
    completed is a date/year or 'not_confirmed'."""
    assert element in ('RAN', 'core'), element
    assert old_vendor in VENDORS and (new_vendor in VENDORS or new_vendor == 'not_disclosed'), (old_vendor, new_vendor)
    return dict(element=element, generation=generation, old_vendor=old_vendor, new_vendor=new_vendor,
                announced=announced, completed=completed, source_url=url, note=note)
