"""Parse Wikipedia 'List of 5G NR networks' (revid saved alongside) into operator rows with launch status.
Status from band-cell background colours per the page legend: commercial SA #9EFF9E, commercial NSA #bfd,
pre-commercial SA #FFB, pre-commercial NSA #fdf2d5."""
import json, re, sys, csv, bs4
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))['parse']
s = bs4.BeautifulSoup(d['text'], 'html.parser')
COM = ('#9eff9e', '#bfd'); PRE = ('#ffb', '#fdf2d5')
rows_out = []
for h3 in s.find_all('h3'):
    cont = h3.get_text(strip=True)
    if cont not in ('Africa', 'Americas', 'Asia', 'Europe', 'Oceania'): continue
    t = h3.find_next('table')
    body = t.find('tbody') or t
    country = None
    for r in body.find_all('tr', recursive=False)[2:]:
        cells = r.find_all(['td', 'th'], recursive=False)
        if not cells: continue
        if cells[0].find(class_='flagicon') or (cells[0].get('rowspan') and len(cells) > 2 and not cells[0].find('table')):
            country = cells[0].get_text(' ', strip=True); cells = cells[1:]
        op = cells[0].get_text(' ', strip=True)
        op = re.sub(r'\s*\[.*?\]', '', op).strip()
        styles = ' '.join((x.get('style') or '').lower().replace(' ', '') for c in cells[1:] for x in [c] + c.find_all(True))
        com = any('background:' + k in styles or k in styles for k in COM)
        pre = any(k in styles for k in PRE)
        dates = re.findall(r'\((?:\s*)([A-Z][a-z]{2} \d{4})\s*\)', ' '.join(c.get_text(' ', strip=True) for c in cells[1:]))
        rows_out.append(dict(wiki_section=cont, country=country, operator=op,
                             status='commercial' if com else ('pre_commercial' if pre else 'unknown'),
                             launch_dates=';'.join(dates)))
with open(out, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows_out[0])); w.writeheader(); w.writerows(rows_out)
print('revid', d['revid'], 'rows', len(rows_out))
