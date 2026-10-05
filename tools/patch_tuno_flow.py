"""One-off patch: the TUNO web app follows the Android app: Welcome page (Your country, Start listening, Favorites, Recent,
News, collapsed Countries) and country pages with Home / Radio / News tabs. No TV."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    assert s.count(a) == count, (s.count(a), a[:90])
    s = s.replace(a, b)


# ---------- CSS ----------
css = '''  /* Welcome and country home, like the app */
  .tiles { display: flex; gap: 10px; overflow-x: auto; scrollbar-width: none; margin: 0 -16px; padding: 0 16px 4px; }
  .tiles::-webkit-scrollbar { display: none; }
  .tile { all: unset; cursor: pointer; flex: none; width: calc(var(--s) * 1px); text-align: center; }
  .tile .logo { width: calc(var(--s) * 1px); height: calc(var(--s) * 1px); border-radius: 16px; }
  .tile b { display: block; margin-top: 6px; font: 600 12.5px 'Figtree', sans-serif; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .tile.on b { color: var(--accent); }
  .tile:focus-visible, .slot:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 14px; }
  .slots { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 9px; }
  .slot { all: unset; cursor: pointer; display: flex; align-items: center; background: var(--surface); border-radius: 14px; overflow: hidden; height: 62px; min-width: 0; }
  .slot .logo { width: 62px; height: 62px; border-radius: 0; }
  .slot b { flex: 1; min-width: 0; padding: 0 12px; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .slot svg { width: 20px; height: 20px; margin-right: 14px; color: var(--accent); flex: none; }
  .slot.on b { color: var(--accent); }
  .yourc { display: flex; align-items: center; gap: 14px; margin: 8px 0 4px; padding: 14px; border-radius: 20px; background: var(--surface);
    border: 1px solid color-mix(in srgb, var(--accent) 55%, transparent); text-decoration: none; color: inherit; cursor: pointer; }
  .yourc img.flag { width: 56px; height: 56px; border-radius: 50%; flex: none; }
  .yourc .tx { flex: 1; min-width: 0; }
  .yourc small { display: block; color: var(--accent); font: 800 11.5px 'Figtree', sans-serif; letter-spacing: .8px; text-transform: uppercase; }
  .yourc b { display: block; font: 700 20px 'Sora', sans-serif; }
  .yourc em { font-style: normal; color: var(--muted); font-size: 13px; }
  .yourc .go { background: var(--accent); color: var(--on-accent); font-weight: 700; border-radius: 999px; padding: 9px 18px; flex: none; }
  .nrow { display: flex; gap: 12px; align-items: center; padding: 8px 2px; text-decoration: none; color: inherit; border-radius: 12px; }
  .nrow:hover { background: var(--surface); }
  .nrow .ni { width: 44px; height: 44px; border-radius: 12px; background: var(--surface); display: grid; place-items: center; color: var(--muted); flex: none; }
  .nrow .ni svg { width: 22px; height: 22px; }
  .nrow .nt { flex: 1; min-width: 0; }
  .nrow .nt b { display: block; font-weight: 700; line-height: 1.3; }
  .nrow .nt small { color: var(--muted); font-size: 13px; }
  .ctabs { display: flex; gap: 8px; margin: 2px 0 12px; }
  .ctabs button { all: unset; cursor: pointer; padding: 8px 18px; border-radius: 999px; background: var(--chip); font-weight: 600; }
  .ctabs button.on { background: var(--accent); color: var(--on-accent); font-weight: 700; }
  .ctabs button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .quick { display: grid; grid-template-columns: repeat(auto-fill, minmax(78px, 1fr)); gap: 8px; }
'''
rep("  .toast { position: fixed;", css + "  .toast { position: fixed;")

# ---------- JS helpers ----------
helpers = '''// ---------- welcome helpers (country, recent countries, news) ----------
let recentCountries = load('radio.recentCountries', []);
function noteCountry(code) { recentCountries = [code, ...recentCountries.filter((c) => c !== code)].slice(0, 8); save('radio.recentCountries', recentCountries); }
let TZ = null;
async function detectCountry() {
  if (!TZ) { try { TZ = await (await fetch('tz.json')).json(); } catch (e) { TZ = {}; } }
  let code = null;
  try { code = TZ[Intl.DateTimeFormat().resolvedOptions().timeZone] || null; } catch (e) {}
  code = code || userCountry() || 'US';
  return COUNTRIES.some((c) => c.code === code) ? code : 'US';
}
const newsCache = {};
async function getNews(code) {
  if (!newsCache[code]) {
    try { newsCache[code] = (await (await fetch('https://akarafilovski.github.io/tuno-data/news/' + code + '.json')).json()).headlines || []; } catch (e) { newsCache[code] = []; }
  }
  return newsCache[code];
}
function ago(ms) {
  const m = Math.max(1, Math.round((Date.now() - ms) / 60000));
  return m < 60 ? m + 'm ago' : m < 1440 ? Math.round(m / 60) + 'h ago' : Math.round(m / 1440) + 'd ago';
}
ICON.news = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 9v11"/></svg>';
const newsRow = (h) => `<a class="nrow" href="${esc(h.url)}" target="_blank" rel="noopener noreferrer"><span class="ni">${ICON.news}</span><span class="nt"><b>${esc(h.title)}</b><small>${esc(h.source || '')}${h.publishedAtEpochMillis ? ' · ' + ago(h.publishedAtEpochMillis) : ''}</small></span></a>`;
const tile = (s, size) => `<button type="button" class="tile${current && current.id === s.id ? ' on' : ''}" data-id="${esc(s.id)}" data-size="${size}" style="--s:${size}">${logoHtml(s)}<b>${esc(s.name)}</b></button>`;
const slot = (s) => `<button type="button" class="slot${current && current.id === s.id ? ' on' : ''}" data-id="${esc(s.id)}">${logoHtml(s)}<b>${esc(s.name)}</b>${ICON.play}</button>`;
const yourCountry = (code) => `<a class="yourc" data-code="${code}" href="${slugOf(code)}/"><img class="flag" src="${flagUrl(code)}" alt="" width="56" height="56"><span class="tx"><small>Your country</small><b>${esc(countryName(code))}</b><em>Radio and news</em></span><span class="go">Open</span></a>`;

'''
rep("async function renderHome() {", helpers + "async function renderHome() {")

# ---------- new Welcome page ----------
a = s.index("  await Promise.all([getIndex(), getCountries()]);\n  if (route.code !== null) return;   // the user already moved on while this loaded")
b = s.index("async function renderCountry(code) {")
new_home = r'''  await Promise.all([getIndex(), getCountries()]);
  if (route.code !== null) return;   // the user already moved on while this loaded
  const mine = await detectCountry();
  if (route.code !== null) return;
  let starters = [];
  getCountry(mine).then((l) => {
    starters = l.filter((st) => st.stream.url.startsWith('https:')).slice(0, 6);
    if (route.code === null && homeDraw) homeDraw();
  }).catch(() => {});
  const q = $('q');
  const list = COUNTRIES.map((c) => app(c.code)).sort((a, b) => a.name.localeCompare(b.name));
  const card = (a) => `<a class="app" data-code="${a.code}" href="${slugOf(a.code)}/" style="--a:${a.accent}">
        <img class="flag" src="${flagUrl(a.code)}" alt="" loading="lazy" width="44" height="44"><b>${esc(a.name.replace(/^Radio /, ''))}</b><small>${a.stations}</small></a>`;
  const draw = () => {
    const term = q.value.trim().toLowerCase();
    const match = (a) => !term || a.name.toLowerCase().includes(term) || countryName(a.code).toLowerCase().includes(term) || a.code.toLowerCase() === term;
    const m = list.filter(match);
    const rec = recent.filter((r) => !isFav(r.id)).slice(0, 8);
    const returning = favs.length > 0 || recent.length > 0 || recentCountries.length > 0;
    const start = !recent.length && starters.length ? `<div class="label">Start listening</div><div class="slots">${starters.map(slot).join('')}</div>` : '';
    let html = '';
    if (!term) {
      if (!returning) html += yourCountry(mine) + start;
      html += `<div class="label">Favorites</div>`;
      html += favs.length ? `<div class="tiles">${favs.map((f) => tile(f, 84)).join('')}</div>`
        : returning ? '' : `<div class="favempty"><span>${ICON.star}</span><p>Your favorite stations will be here.<br>Tap the star next to a station to add it.</p></div>`;
      if (returning && !favs.length) html = html.replace('<div class="label">Favorites</div>', '');
      if (rec.length) html += `<div class="label">Recent</div><div class="tiles">${rec.map((r) => tile(r, 72)).join('')}</div>`;
      if (returning) html += start + '<div id="home-news"></div>';
    }
    if (m.length) {
      if (term) html += '<div class="label">Countries</div>';
      else html += `<button type="button" class="label fold${countriesOpen ? ' open' : ''}" data-toggle="countries" aria-expanded="${countriesOpen}">Countries<span>${m.length}</span>${ICON.chev}</button>`;
      if (term || countriesOpen) html += `<div class="apps">${m.map(card).join('')}</div>`;
      else {
        const quick = [...new Set([mine, ...recentCountries])].slice(0, 6).map((c) => list.find((x) => x.code === c)).filter(Boolean);
        html += `<div class="quick">${quick.map(card).join('')}</div>`;
      }
    }
    if (!term && TUNO.live) html += tunoCard();
    let hits = [];
    if (term.length >= 2) {
      hits = searchStations(term);
      const loading = prefetchState.done < prefetchState.total;
      html += `<div class="label">Stations</div>` + (hits.length ? `<div class="list">${hits.map(stationRow).join('')}</div>` : `<div class="empty">${loading ? 'Searching…' : 'No station found.'}</div>`);
      if (loading && hits.length) html += `<p class="note" style="text-align:center">Still searching: ${prefetchState.done} of ${prefetchState.total} countries</p>`;
    }
    $('home-lists').innerHTML = html || '<div class="empty">Nothing found.</div>';
    shown = hits.concat(favs, rec, recent, starters);
    if (!term && returning) getNews(mine).then((n) => {
      const box = $('home-news');
      if (box && route.code === null && n.length) box.innerHTML = '<div class="label">News</div>' + n.slice(0, 2).map(newsRow).join('');
    });
  };
  homeDraw = draw;
  q.addEventListener('input', () => { if (q.value.trim().length >= 2) prefetchAll(() => { if (q.isConnected && q.value.trim().length >= 2) draw(); }); draw(); });
  q.addEventListener('focus', () => prefetchAll(() => { if (q.isConnected && q.value.trim().length >= 2) draw(); }), { once: true });
  draw();
  window.scrollTo(0, 0);
}

'''
s = s[:a] + new_home + s[b:]

rep("let countriesOpen = load('radio.countriesOpen', true);", "let countriesOpen = load('radio.countriesOpen2', false);")
rep("save('radio.countriesOpen', countriesOpen);", "save('radio.countriesOpen2', countriesOpen);")

# ---------- country page: Home / Radio / News tabs ----------
rep('''    <div class="search">${ICON.search}<input id="q" type="search" placeholder="Search stations" autocomplete="off" aria-label="Search stations"></div></div>
    <div class="chips" id="chips"></div>
    <div id="stations"><div class="empty">Loading stations…</div></div>''',
    '''    </div>
    <div class="ctabs" id="ctabs"><button type="button" data-tab="home" class="on">Home</button><button type="button" data-tab="radio">Radio</button><button type="button" data-tab="news">News</button></div>
    <div id="ctab"><div class="empty">Loading…</div></div>''')
rep("  route = { code };\n  listState = { q: '', cat: 'all', limit: PAGE };", "  route = { code };\n  noteCountry(code);\n  listState = { q: '', cat: 'all', limit: PAGE };")
# the station list code becomes the Radio tab
rep("  $('back').addEventListener('click', () => goBack());\n  window.scrollTo(0, 0);\n  let stations;\n  try { stations = await getCountry(code); if (route.code !== code) return; } catch (e) { if (route.code !== code) return; $('stations').innerHTML =",
    "  $('back').addEventListener('click', () => goBack());\n  window.scrollTo(0, 0);\n  let stations;\n  try { stations = await getCountry(code); if (route.code !== code) return; } catch (e) { if (route.code !== code) return; $('ctab').innerHTML =")
rep("  const chips = $('chips');\n", "  function radioTab() {\n  $('ctab').innerHTML = `<div class=\"search\">${ICON.search}<input id=\"q\" type=\"search\" placeholder=\"Search stations\" autocomplete=\"off\" aria-label=\"Search stations\" value=\"${esc(listState.q)}\"></div><div class=\"chips\" id=\"chips\"></div><div id=\"stations\"></div>`;\n  const chips = $('chips');\n")
rep("  drawChips();\n  draw();\n  countryDraw = draw;\n}\n", '''  drawChips();
  draw();
  countryDraw = draw;
  }
  const starters = stations.slice(0, 6);
  let tab = 'home';
  function homeTab() {
    countryDraw = null;
    const rec = recent.filter((r) => !isFav(r.id)).slice(0, 8);
    let h = '';
    if (favs.length) h += `<div class="label">Favorites</div><div class="tiles">${favs.map((f) => tile(f, 84)).join('')}</div>`;
    if (rec.length) h += `<div class="label">Recent</div><div class="tiles">${rec.map((r) => tile(r, 72)).join('')}</div>`;
    if (!recent.length && starters.length) h += `<div class="label">Start listening</div><div class="slots">${starters.map(slot).join('')}</div>`;
    h += '<div id="c-news"></div>';
    $('ctab').innerHTML = h;
    shown = favs.concat(rec, starters, recent);
    getNews(code).then((n) => {
      const box = $('c-news');
      if (box && route.code === code && tab === 'home' && n.length) box.innerHTML = '<div class="label">News</div>' + n.slice(0, 2).map(newsRow).join('');
    });
  }
  function newsTab() {
    countryDraw = null;
    $('ctab').innerHTML = '<div class="empty">Loading…</div>';
    getNews(code).then((n) => {
      if (route.code !== code || tab !== 'news') return;
      $('ctab').innerHTML = n.length ? n.map(newsRow).join('') : '<div class="empty">No headlines for this country yet.</div>';
    });
  }
  function showTab(t) {
    tab = t;
    document.querySelectorAll('#ctabs button').forEach((b) => b.classList.toggle('on', b.dataset.tab === t));
    (t === 'radio' ? radioTab : t === 'news' ? newsTab : homeTab)();
  }
  $('ctabs').addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) showTab(b.dataset.tab); });
  showTab('home');
}
''')

# tiles and slots play a station like rows do
rep("  const row = e.target.closest('.row');\n  if (row) {\n    const s = findStation(row.dataset.id);", "  const row = e.target.closest('.row, .tile, .slot');\n  if (row) {\n    const s = findStation(row.dataset.id);")
rep('''function redrawRows() {
  document.querySelectorAll('.row').forEach((el) => {
    const s = findStation(el.dataset.id);
    if (s) el.outerHTML = stationRow(s);
  });
}''', '''function redrawRows() {
  document.querySelectorAll('.row').forEach((el) => {
    const s = findStation(el.dataset.id);
    if (s) el.outerHTML = stationRow(s);
  });
  document.querySelectorAll('.tile').forEach((el) => { const s = findStation(el.dataset.id); if (s) el.outerHTML = tile(s, el.dataset.size); });
  document.querySelectorAll('.slot').forEach((el) => { const s = findStation(el.dataset.id); if (s) el.outerHTML = slot(s); });
}''')
open(p, 'w', encoding='utf-8', newline='\n').write(s)

sp = os.path.join(ROOT, 'sw.js')
t = open(sp, encoding='utf-8').read()
assert t.count("axar-radio-v4") == 1
open(sp, 'w', encoding='utf-8', newline='\n').write(t.replace('axar-radio-v4', 'axar-radio-v5'))
print('flow patched')
