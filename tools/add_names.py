"""Adds `name` and a url `slug` to every entry of countries.json (names from node's Intl.DisplayNames). Safe to re-run."""
import json, os, re, subprocess, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'countries.json')
data = json.load(open(p, encoding='utf-8'))
codes = [c['code'] for c in data]
js = "const n=new Intl.DisplayNames(['en'],{type:'region'});console.log(JSON.stringify(%s.map(c=>n.of(c))))" % json.dumps(codes)
names = json.loads(subprocess.check_output(['node', '-e', js]))
OVERRIDE = {'MK': 'Macedonia', 'BA': 'Bosnia', 'GB': 'United Kingdom', 'US': 'United States', 'HK': 'Hong Kong', 'MO': 'Macau',
            'CD': 'DR Congo', 'CG': 'Congo', 'CZ': 'Czechia', 'VA': 'Vatican City', 'PS': 'Palestine', 'TR': 'Turkey', 'MM': 'Myanmar'}
seen = set()
for c, n in zip(data, names):
    n = OVERRIDE.get(c['code']) or re.sub(r'\s*\(.*\)\s*', '', n).strip()
    base = re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', n).encode('ascii', 'ignore').decode().lower()).strip('-')
    slug = base if base not in seen else base + '-' + c['code'].lower()
    seen.add(slug)
    c['name'], c['slug'] = n, slug
json.dump(data, open(p, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=1)
print(len(data), [(c['code'], c['name'], c['slug']) for c in data[:6]])
