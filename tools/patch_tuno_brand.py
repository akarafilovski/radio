"""One-off patch: World Radio becomes TUNO (same address): midnight blue, logo mark, round flags, glow and dancing bars while a station plays."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANDROID = os.path.dirname(ROOT)


def read(p):
    return open(p, encoding='utf-8').read()


def write(p, s):
    open(p, 'w', encoding='utf-8', newline='\n').write(s)


p = os.path.join(ROOT, 'index.html')
s = read(p)


def rep(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:80])
    s = s.replace(a, b)


s = s.replace('World Radio', 'TUNO')
rep('<meta name="theme-color" content="#000000">', '<meta name="theme-color" content="#0A1020">')
rep('--bg: #000; --surface: #161616; --tile: #1C1C1F; --border: rgba(255,255,255,.08);', '--bg: #0A1020; --surface: #131C32; --tile: #131C32; --border: rgba(130,160,255,.14);')
rep('--text: #fff; --muted: #A8A8B2; --dim: #555560;', '--text: #EEF1F8; --muted: #B5BDD3; --dim: #6B7592;')
rep('<body>\n', '<body>\n<div id="glow" aria-hidden="true"></div>\n')

css = '''  /* light behind the page: calm when idle, drifting while a station plays */
  #glow { position: fixed; inset: 0; z-index: 0; pointer-events: none; transition: opacity .9s;
    background: radial-gradient(70% 38% at 18% -4%, rgba(76,100,255,.24), transparent 70%), radial-gradient(60% 34% at 92% 2%, rgba(125,105,255,.18), transparent 68%); }
  body.playing #glow { background: radial-gradient(70% 38% at 18% -4%, rgba(76,100,255,.40), transparent 70%), radial-gradient(60% 34% at 92% 2%, rgba(125,105,255,.34), transparent 68%);
    animation: drift 14s linear infinite; }
  @keyframes drift { 0%, 100% { transform: translate(0, 0) scale(1); } 25% { transform: translate(3%, 1.5%) scale(1.05); } 50% { transform: translate(0, 3%) scale(1); } 75% { transform: translate(-3%, 1.5%) scale(1.05); } }
  .wrap { position: relative; z-index: 1; }
  .logo { display: flex; align-items: center; gap: 2.5px; height: 28px; margin-right: 2px; }
  .logo i { display: block; width: 3.4px; height: calc(var(--h) * 1px); border-radius: 2px; background: linear-gradient(#FFD6B4, #EB6428); }
  body.playing .logo i { animation: bar var(--d) ease-in-out infinite alternate; }
  @keyframes bar { from { transform: scaleY(.45); } to { transform: scaleY(1); } }
  .top h1 { color: #FFB68C; font-weight: 900; }
  .app img.flag, .top img.flag { border-radius: 50%; box-shadow: none; }
  .support.open { background: #0A1020; }
'''
rep('  .toast { position: fixed;', css + '  .toast { position: fixed;')

# header: logo mark instead of the old icon; flags instead of the radio icons
rep('<div class="top"><img src="icons/app-192.png" alt=""><h1>TUNO</h1>', '<div class="top">${LOGO}<h1>TUNO</h1>')
rep('async function renderHome() {', '''const LOGO = '<span class="logo" aria-hidden="true">' + [[7.7, 560], [11.6, 700], [16.4, 480], [22.2, 760], [28, 600], [22.2, 720], [16.4, 520], [11.6, 660], [7.7, 580]]
  .map(([h, d]) => `<i style="--h:${h};--d:${d}ms"></i>`).join('') + '</span>';
const flagUrl = (c) => 'https://akarafilovski.github.io/tuno-data/flags/' + c.toLowerCase() + '.png';

async function renderHome() {''')
rep('<img src="${a.icon}" alt="" loading="lazy" width="44" height="44">', '<img class="flag" src="${flagUrl(a.code)}" alt="" loading="lazy" width="44" height="44">')
rep('<img src="${pick.icon}" alt=""><h1>${esc(name)}</h1>', '<img class="flag" src="${flagUrl(code)}" alt=""><h1>${esc(name)}</h1>')

# playing state drives the glow and the bars
rep("audio.addEventListener('playing', () => { setBtn('pause'); showPlayer(); redrawRows(); });", "audio.addEventListener('playing', () => { setBtn('pause'); showPlayer(); redrawRows(); document.body.classList.add('playing'); });")
rep("audio.addEventListener('pause', () => { setBtn('play'); redrawRows(); });", "audio.addEventListener('pause', () => { setBtn('play'); redrawRows(); });\n['pause', 'ended', 'error', 'emptied'].forEach((ev) => audio.addEventListener(ev, () => document.body.classList.remove('playing')));")
write(p, s)

# manifest
mp = os.path.join(ROOT, 'manifest.webmanifest')
m = json.loads(read(mp))
m['name'] = 'TUNO'
m['short_name'] = 'TUNO'
m['description'] = 'Live radio from 191 countries. Free, no ads.'
m['background_color'] = '#0A1020'
m['theme_color'] = '#0A1020'
write(mp, json.dumps(m, indent=2) + '\n')

# service worker: new cache so the new icons replace the old ones
sp = os.path.join(ROOT, 'sw.js')
t = read(sp)
assert t.count("axar-radio-v3") == 1
write(sp, t.replace('axar-radio-v3', 'axar-radio-v4'))

# the rest of the site's own text
for f in ('privacy.html', 'README.md', os.path.join('tools', 'build_country_pages.py')):
    fp = os.path.join(ROOT, f)
    write(fp, read(fp).replace('World Radio', 'TUNO'))
for f in (os.path.join('GamesWeb', 'tools', 'make_about.py'), os.path.join('WellnessWeb', 'build.py'), os.path.join('axarapps-site', 'index.html')):
    fp = os.path.join(ANDROID, f)
    write(fp, read(fp).replace('World Radio', 'TUNO'))
print('rebranded')
