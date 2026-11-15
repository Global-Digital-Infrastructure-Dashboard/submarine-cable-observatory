"""Region tagging + seeded half-draw. Method: within each region, sort country names alphabetically,
shuffle with random.Random(SEED), take the first ceil(n/2). Core-27 markets are added regardless (union)."""
import csv, math, random, sys, platform
import pandas as pd
SEED = 20261115
CORE27 = ['Germany','Sweden','United Kingdom','France','Italy','Spain','Netherlands','Poland','Belgium','Austria',
 'Switzerland','Norway','Denmark','Finland','Ireland','Portugal','Greece','Czechia','Romania','Hungary','Croatia',
 'Slovakia','Bulgaria','Estonia','Lithuania','United States','China']
TERRITORIES = ['Reunion','Saint-Martin','Puerto Rico US Virgin Islands','Bermuda','Cayman Islands','Faroe Islands',
 'Hong Kong','Macau','Guam N. Mariana Islands','French Polynesia']
NORTH_AMERICA = ['United States','Canada']
R = {
 'Middle East': ['Bahrain','Iran','Israel','Jordan','Kuwait','Oman','Qatar','Saudi Arabia','United Arab Emirates','Turkey'],
 'Central Asia & Eastern Europe': ['Armenia','Georgia','Kazakhstan','Tajikistan','Uzbekistan','Russia','Ukraine','Poland',
   'Czechia','Slovakia','Hungary','Romania','Bulgaria','Estonia','Latvia','Lithuania','Croatia','Slovenia','Serbia',
   'Montenegro','North Macedonia'],
 'Western Europe': ['Andorra','Austria','Belgium','Cyprus','Denmark','Finland','France','Germany','Greece','Iceland',
   'Ireland','Italy','Luxembourg','Malta','Monaco','Netherlands','Norway','Portugal','San Marino','Spain','Sweden',
   'Switzerland','United Kingdom'],
}
SECTION_DEFAULT = {'Africa': 'Africa', 'Americas': 'Latin America & Caribbean', 'Asia': 'Asia-Pacific', 'Oceania': 'Asia-Pacific'}
ops = pd.read_csv(sys.argv[1]); ops['country'] = ops.country.str.replace('\xa0', ' '); ops = ops[ops.status == 'commercial']
countries = ops.drop_duplicates('country')[['wiki_section', 'country']]
explicit = {c: r for r, cs in R.items() for c in cs}
rows = []
for sec, c in countries.itertuples(index=False):
    if c in TERRITORIES: region = 'EXCLUDED: territory'
    elif c in NORTH_AMERICA: region = 'North America (outside six regions)'
    else: region = explicit.get(c) or SECTION_DEFAULT.get(sec) or 'UNMAPPED'
    rows.append(dict(country=c, wiki_section=sec, region=region, core27=c in CORE27))
df = pd.DataFrame(rows)
assert not (df.region == 'UNMAPPED').any(), df[df.region == 'UNMAPPED']
assert set(CORE27) <= set(df.country), set(CORE27) - set(df.country)
df['shuffle_pos'] = None; df['drawn'] = False
for region in ['Africa','Middle East','Asia-Pacific','Central Asia & Eastern Europe','Latin America & Caribbean','Western Europe']:
    names = sorted(df.loc[df.region == region, 'country'])
    random.Random(SEED).shuffle(names)
    k = math.ceil(len(names) / 2)
    for i, n in enumerate(names):
        df.loc[df.country == n, 'shuffle_pos'] = i + 1
        df.loc[df.country == n, 'drawn'] = i < k
df['selected'] = df.drawn | df.core27
df['selection_basis'] = df.apply(lambda r: 'draw+core27' if r.drawn and r.core27 else 'draw' if r.drawn else 'core27' if r.core27 else '', axis=1)
df.sort_values(['region', 'shuffle_pos']).to_csv(sys.argv[2], index=False)
print('python', platform.python_version(), 'seed', SEED)
print(df.groupby('region').agg(n=('country','size'), drawn=('drawn','sum'), core27=('core27','sum'), selected=('selected','sum')))
print('TOTAL selected', df.selected.sum())
