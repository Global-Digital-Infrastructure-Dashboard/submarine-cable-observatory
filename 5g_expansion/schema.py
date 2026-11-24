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
                     state_owned_company (the fifth type covers state-owned operating companies such as e&,
                     VNPT or Tojiktelecom, which fit none of Prof. Shen's four; PENDING her approval, asked
                     2026-11-23)
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
    ],
    'government': [
        'ca.go.ke', 'vpcp.chinhphu.vn', 'gub.uy', 'ttparliament.org', 'nbim.no', 'itu.int', 'ilr.lu', 'gov.uz',
        'mst.gov.vn', 'mic.gov.vn', 'imda.gov.sg', 'cs.gov.tj', 'openinfo.uz',
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
    ],
    'other': ['telcobrief.com', 'tadviser.com', 'powertec.com.au', 'marketbeat.com', 'scribd.com', 'wikipedia.org'],
}
# Documents whose author differs from the host: company filings published on a government site.
URL_OVERRIDES = {
    'https://www.imda.gov.sg/-/media/imda/files/regulations-and-licensing/regulations/consultations/2025/simba-and-m1/annex-b-non-confidential-abbreviated-statement-submitted-by-simba-and-m1.pdf': 'company',
    'https://openinfo.uz/media/int_report/08c4d98a-95e7-4ee7-8771-8093b193f1f5.pdf': 'company',
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
      link_url=None, parent_pct=None, chain='', board_seat='not_checked'):
    assert holder_type in HOLDER_TYPES, holder_type
    assert basis in ('direct', 'via_parent'), basis
    assert link in LINK_BASES, link
    assert board_seat in BOARD_SEAT, board_seat
    assert pct is None or pct >= GOV_THRESHOLD_PCT or board_seat == 'yes', (holder, pct)
    assert basis == 'via_parent' or (parent_pct is None and not chain), holder
    return dict(government=government, holder=holder, holder_type=holder_type, pct=pct, pct_of=pct_of, basis=basis,
                as_of=as_of, source_url=url, state_link_basis=link,
                state_link_url=(link_url or url) if link == 'stated_in_source' else '',
                parent_ownership_pct_of_operator=parent_pct, ownership_chain=chain, board_seat=board_seat, note=note)


def S(element, generation, old_vendor, new_vendor, announced, completed, url, note=''):
    """A vendor switch: old_vendor's equipment replaced by new_vendor's. new_vendor may be 'not_disclosed';
    completed is a date/year or 'not_confirmed'."""
    assert element in ('RAN', 'core'), element
    assert old_vendor in VENDORS and (new_vendor in VENDORS or new_vendor == 'not_disclosed'), (old_vendor, new_vendor)
    return dict(element=element, generation=generation, old_vendor=old_vendor, new_vendor=new_vendor,
                announced=announced, completed=completed, source_url=url, note=note)
