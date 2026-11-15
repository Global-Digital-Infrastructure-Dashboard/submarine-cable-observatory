"""Print cached search answers + source URLs for one country (for in-session coding)."""
import json, sys, re
c = sys.argv[1]
for e in map(json.loads, open('data/5g_expansion_searches.jsonl')):
    _, layer, country, op = e['key'].split('|')
    if country != c: continue
    print(f"\n######## {op} :: {layer}")
    a = re.sub(r'\n{2,}', '\n', e['search']['answer'])
    print(a)
    print('URLS:', ' '.join(f"[{i+1}]{r.get('url')}" for i, r in enumerate(e['search']['results'])))
