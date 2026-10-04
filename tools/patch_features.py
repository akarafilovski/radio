"""One-off patch: recently played on home, search for stations across all countries, sleep timer."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b, count=1):
    global s
    assert s.count(a) >= 1, a[:90]
    s = s.replace(a, b, count)


# ---------- player markup: sleep button and menu ----------
rep("""    <button class="pp" id="p-btn" type="button" aria-label="Play"></button>
  </div>
</div>""", """    <button class="sleepbtn" id="p-sleep" type="button" aria-label="Sleep timer" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg><small id="p-sleep-t"></small></button>
    <button class="pp" id="p-btn" type="button" aria-label="Play"></button>
  </div>
  <div class="sleepmenu" id="sleepmenu" hidden>
    <b>Sleep timer</b>
    <button type="button" data-min="15">15 minutes</button><button type="button" data-min="30">30 minutes</button>
    <button type="button" data-min="45">45 minutes</button><button type="button" data-min="60">1 hour</button>
    <button type="button" data-min="90">90 minutes</button><button type="button" data-min="0" class="off">Turn off</button>
  </div>
</div>""")

# ---------- css ----------
rep("  .toast {", """  .sleepbtn { all: unset; cursor: pointer; flex: none; width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center; background: var(--chip); position: relative; }
  .sleepbtn svg { width: 20px; height: 20px; } .sleepbtn.on { color: var(--accent); }
  .sleepbtn small { position: absolute; bottom: -3px; right: -5px; font-size: 10px; font-weight: 700; background: var(--accent); color: #000; border-radius: 999px; padding: 1px 5px; display: none; }
  .sleepbtn.on small { display: block; }
  .sleepbtn:focus-visible, .sleepmenu button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .sleepmenu { position: absolute; right: 12px; bottom: calc(100% + 8px); background: #222226; border: 1px solid var(--border); border-radius: 18px; padding: 8px; display: grid; min-width: 180px; box-shadow: 0 18px 50px rgba(0,0,0,.6); }
  .sleepmenu[hidden] { display: none; }
  .sleepmenu b { padding: 8px 12px 6px; font-size: 12px; letter-spacing: .6px; text-transform: uppercase; color: var(--muted); }
  .sleepmenu button { all: unset; cursor: pointer; padding: 11px 12px; border-radius: 10px; font-weight: 600; font-size: 15px; }
  .sleepmenu button:hover { background: var(--chip); } .sleepmenu .off { color: var(--muted); }
  .toast {""")

# ---------- lookups include recent stations ----------
rep("let route = { code: null };", """let route = { code: null };
const findStation = (id) => shown.find((x) => x.id === id) || favs.find((x) => x.id === id) || recent.find((x) => x.id === id);""")
rep("const s = shown.find((x) => x.id === el.dataset.id) || favs.find((x) => x.id === el.dataset.id);", "const s = findStation(el.dataset.id);")
rep("const s = shown.find((x) => x.id === favBtn.dataset.fav) || favs.find((x) => x.id === favBtn.dataset.fav);", "const s = findStation(favBtn.dataset.fav);")
rep("const s = shown.find((x) => x.id === row.dataset.id) || favs.find((x) => x.id === row.dataset.id);", "const s = findStation(row.dataset.id);")

# ---------- global station search ----------
rep("// ---------- favorites & recent ----------", """// ---------- search across all countries ----------
// The country files are fetched in the background the first time the search box is used (about 1.3 MB in total).
let prefetchState = { started: false, done: 0, total: 0 };
function prefetchAll(onProgress) {
  if (prefetchState.started) return;
  prefetchState = { started: true, done: 0, total: COUNTRIES.length };
  const queue = COUNTRIES.map((c) => c.code);
  let timer = null;
  const tick = () => { if (!timer) timer = setTimeout(() => { timer = null; onProgress(); }, 250); };
  const worker = async () => {
    while (queue.length) {
      const code = queue.shift();
      try { await getCountry(code); } catch (e) { /* skipped; the country page retries */ }
      prefetchState.done++;
      tick();
    }
    onProgress();
  };
  for (let i = 0; i < 6; i++) worker();
}
function searchStations(term) {
  const out = [];
  for (const list of Object.values(countryCache)) {
    for (const st of list) {
      if (!st.stream.url.startsWith('https:')) continue;
      const name = st.name.toLowerCase();
      const at = name.indexOf(term);
      if (at >= 0) out.push([at === 0 ? 0 : 1, name, st]);
    }
  }
  out.sort((a, b) => a[0] - b[0] || a[1].localeCompare(b[1]));
  return out.slice(0, 40).map((x) => x[2]);
}

// ---------- favorites & recent ----------""")

rep("""    if (m.length) html += `${!term ? '<div class="label">Countries</div>' : ''}<div class="apps">${m.map(card).join('')}</div>`;
    $('home-lists').innerHTML = html || '<div class="empty">No country found.</div>';
    shown = [];
  };""", """    const rec = recent.filter((r) => !isFav(r.id)).slice(0, 6);
    if (!term && rec.length) html += `<div class="label">Recently played</div><div class="list">${rec.map(stationRow).join('')}</div>`;
    if (m.length) html += `${!term ? '<div class="label">Countries</div>' : '<div class="label">Countries</div>'}<div class="apps">${m.map(card).join('')}</div>`;
    let hits = [];
    if (term.length >= 2) {
      hits = searchStations(term);
      const loading = prefetchState.done < prefetchState.total;
      html += `<div class="label">Stations</div>` + (hits.length ? `<div class="list">${hits.map(stationRow).join('')}</div>` : `<div class="empty">${loading ? 'Searching…' : 'No station found.'}</div>`);
      if (loading && hits.length) html += `<p class="note" style="text-align:center">Still searching: ${prefetchState.done} of ${prefetchState.total} countries</p>`;
    }
    $('home-lists').innerHTML = html || '<div class="empty">Nothing found.</div>';
    shown = hits.concat(favs, rec);
  };""")
rep("""  q.addEventListener('input', draw);
  draw();
  window.scrollTo(0, 0);
}""", """  q.addEventListener('input', () => { if (q.value.trim().length >= 2) prefetchAll(() => { if (q.isConnected && q.value.trim().length >= 2) draw(); }); draw(); });
  q.addEventListener('focus', () => prefetchAll(() => { if (q.isConnected && q.value.trim().length >= 2) draw(); }), { once: true });
  draw();
  window.scrollTo(0, 0);
}""")
rep('placeholder="Search a country" autocomplete="off" aria-label="Search a country"', 'placeholder="Search a country or station" autocomplete="off" aria-label="Search a country or station"')

# ---------- sleep timer ----------
rep("$('p-btn').addEventListener('click', togglePlay);", """$('p-btn').addEventListener('click', togglePlay);

// ---------- sleep timer ----------
let sleepEnd = 0;
let sleepTick = null;
function sleepLabel() {
  const left = Math.ceil((sleepEnd - Date.now()) / 60000);
  $('p-sleep-t').textContent = sleepEnd ? left + 'm' : '';
  $('p-sleep').classList.toggle('on', !!sleepEnd);
}
function setSleep(min) {
  clearInterval(sleepTick);
  sleepEnd = 0;
  if (min) {
    sleepEnd = Date.now() + min * 60000;
    sleepTick = setInterval(() => {
      if (Date.now() >= sleepEnd) {
        clearInterval(sleepTick);
        sleepEnd = 0;
        audio.pause();
        toast('Sleep timer: radio stopped');
      }
      sleepLabel();
    }, 1000);
    toast('Radio stops in ' + min + ' min');
  }
  sleepLabel();
  closeSleepMenu();
}
function closeSleepMenu() { $('sleepmenu').hidden = true; $('p-sleep').setAttribute('aria-expanded', 'false'); }
$('p-sleep').addEventListener('click', (e) => {
  e.stopPropagation();
  const menu = $('sleepmenu');
  menu.hidden = !menu.hidden;
  $('p-sleep').setAttribute('aria-expanded', String(!menu.hidden));
});
$('sleepmenu').addEventListener('click', (e) => {
  e.stopPropagation();
  const b = e.target.closest('button');
  if (b) setSleep(Number(b.dataset.min));
});
document.addEventListener('click', closeSleepMenu);""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
