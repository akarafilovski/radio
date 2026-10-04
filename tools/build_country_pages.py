"""Generates one crawlable page per country (<slug>/index.html), the pre-rendered home list, sitemap.xml and robots.txt.

    python tools/add_names.py            # once, names + slugs in countries.json
    python tools/build_country_pages.py  # after every change to index.html or the station lists
index.html stays the single source: every country page is a copy of it with its own title, description, canonical address,
structured data and a plain-HTML station list that the app replaces as soon as it starts.
"""
import html
import json
import os
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://axarapps.github.io/radio/'
DATA = 'https://akarafilovski.github.io/tuno-data/radio/'
e = html.escape

countries = json.load(open(os.path.join(ROOT, 'countries.json'), encoding='utf-8'))
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
MARK = re.compile(r'<!--prerender-->.*?<!--/prerender-->', re.S)


def fetch(c):
    with urllib.request.urlopen(DATA + c['code'] + '.json', timeout=60) as r:
        st = json.load(r)['stations']
    return [s for s in st if s['stream']['url'].startswith('https')]


with ThreadPoolExecutor(8) as ex:
    stations = dict(zip([c['code'] for c in countries], ex.map(fetch, countries)))

# ---- home: crawlable list of all countries
links = ''.join(f'<li><a href="{c["slug"]}/">Radio {e(c["name"])}</a> ({len(stations[c["code"]])} stations)</li>' for c in sorted(countries, key=lambda c: c['name']))
home_pre = ('<!--prerender--><div class="prerender"><h1>TUNO</h1><p>Listen to live radio from %d countries, free and without ads.</p><ul>%s</ul></div><!--/prerender-->'
            % (len(countries), links))
home = MARK.sub(lambda m: home_pre, src, count=1)
home = home.replace('Live radio from 239 countries', 'Live radio from %d countries' % len(countries)).replace('Live radio from 239 countries.', 'Live radio from %d countries.' % len(countries))
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf-8', newline='\n').write(home)


def sub(text, pattern, repl):
    new, n = re.subn(pattern, lambda m: repl, text, count=1)
    assert n == 1, pattern
    return new


for c in countries:
    st = stations[c['code']]
    n = len(st)
    name = c['name']
    url = f'{SITE}{c["slug"]}/'
    title = f'Radio {name}: listen to {n} live stations online | TUNO'
    desc = f'Listen to {n} live radio stations from {name} online, free and without ads. Music, news, talk and sports: search, tap and play.'
    ld = json.dumps({
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'TUNO', 'item': SITE},
                {'@type': 'ListItem', 'position': 2, 'name': f'Radio {name}', 'item': url}]},
            {'@type': 'ItemList', 'name': f'Radio stations in {name}', 'numberOfItems': min(n, 100),
             'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': s['name']} for i, s in enumerate(st[:100])]},
        ]}, ensure_ascii=False).replace('</', '<\/')
    items = ''.join(f'<li>{e(s["name"])}{" · " + e(s["category"]) if s.get("category") else ""}</li>' for s in st[:150])
    pre = (f'<!--prerender--><div class="prerender"><h1>Radio {e(name)}</h1><p>{n} live radio stations from {e(name)}, free and without ads. '
           f'<a href="./">All countries</a></p><ul>{items}</ul></div><!--/prerender-->')
    page = MARK.sub(lambda m: pre, home, count=1)
    page = sub(page, r'<title>.*?</title>', f'<title>{e(title)}</title>')
    page = sub(page, r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc, quote=True)}">')
    page = sub(page, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{e(title, quote=True)}">')
    page = sub(page, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{e(desc, quote=True)}">')
    page = sub(page, r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">')
    page = sub(page, r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">')
    page = sub(page, r'<meta charset="utf-8">', f'<meta charset="utf-8">\n<base href="../">')
    page = sub(page, r'</head>', f'<script type="application/ld+json">{ld}</script>\n</head>')
    d = os.path.join(ROOT, c['slug'])
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w', encoding='utf-8', newline='\n').write(page)

urls = [SITE, SITE + 'about.html'] + [f'{SITE}{c["slug"]}/' for c in sorted(countries, key=lambda c: c['slug'])]
open(os.path.join(ROOT, 'sitemap.xml'), 'w', encoding='utf-8', newline='\n').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'<url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w', newline='\n').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n')
print(len(countries), 'pages,', sum(len(v) for v in stations.values()), 'stations')
