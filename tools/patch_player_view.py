"""One-off patch: the TUNO web player view, like the app. Cover, name, city and LIVE chips, heart and sleep timer above
previous / play / next, share at the top right, the logo equalizer at the bottom. A page on narrow screens (tap the player
bar), a permanent pane on the right on wide screens."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:90])
    s = s.replace(a, b)


# ---------- state + hooks ----------
rep("let current = null;\nlet hls = null;", "let current = null;\nlet btnState = 'play';\nlet hls = null;")
rep("function setBtn(state) {\n  const b = $('p-btn');", "function setBtn(state) {\n  btnState = state;\n  renderPv();\n  const b = $('p-btn');")
rep("async function play(s) {\n  current = s;\n", "async function play(s) {\n  current = s;\n  computeNeighbors(s);\n")
rep("  $('p-sleep').classList.toggle('on', !!sleepEnd);\n}", "  $('p-sleep').classList.toggle('on', !!sleepEnd);\n  const pt = $('pv-timer');\n  if (pt) pt.classList.toggle('on', !!sleepEnd);\n}")
rep("window.addEventListener('popstate', routeNow);", "window.addEventListener('popstate', () => { if (pvOpen) { closePv(false); return; } routeNow(); });")

# ---------- markup ----------
rep('<div class="install" id="install"', '<div class="pview" id="pview" role="dialog" aria-label="Player"></div>\n\n<div class="install" id="install"')

# ---------- CSS ----------
css = '''  /* player view: a page on narrow screens, a pane on the right on wide screens */
  .pview { position: fixed; inset: 0; z-index: 35; background: var(--bg); transform: translateX(100%); visibility: hidden; transition: transform .38s cubic-bezier(.2,.8,.2,1), visibility 0s .38s; overflow: hidden; }
  .pview.show { transform: none; visibility: visible; transition: transform .38s cubic-bezier(.2,.8,.2,1); }
  html.pv-open, html.pv-open body { overflow: hidden; }
  .pbgimg { position: absolute; left: -20%; top: -20%; width: 140%; height: 140%; object-fit: cover; filter: blur(50px) saturate(1.3); opacity: .5; }
  .pbgfade { position: absolute; inset: 0; background: linear-gradient(rgba(10,16,32,.25), rgba(10,16,32,.9)); }
  .pscroll { position: absolute; inset: 0; overflow-y: auto; display: flex; justify-content: center; }
  .pin { width: min(100%, 520px); min-height: 100%; display: flex; flex-direction: column; align-items: center; padding: max(10px, env(safe-area-inset-top)) 18px calc(28px + env(safe-area-inset-bottom)); }
  .ptopr { width: 100%; display: flex; align-items: center; justify-content: space-between; min-height: 48px; }
  .ptopr .grp { display: flex; gap: 8px; margin-left: auto; }
  .pbtn { all: unset; cursor: pointer; width: 44px; height: 44px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.12); color: #fff; }
  .pbtn svg { width: 22px; height: 22px; }
  .pbtn:focus-visible, .pib:focus-visible, .pbig:focus-visible, .pchip:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .pcov { margin-top: auto; width: min(62vw, 300px, 36vh); aspect-ratio: 1; border-radius: 28px; overflow: hidden; background: var(--tile); display: grid; place-items: center;
    font: 800 64px 'Sora', sans-serif; color: var(--muted); box-shadow: 0 24px 50px rgba(0,0,0,.5); }
  .pcov img { width: 100%; height: 100%; object-fit: cover; }
  .pname { margin: 20px 0 0; font: 700 24px 'Sora', sans-serif; text-align: center; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .pchips { display: flex; gap: 10px; justify-content: center; margin-top: 10px; }
  .pchips span { background: rgba(255,255,255,.14); border-radius: 999px; padding: 6px 14px; font-weight: 600; font-size: 14px; }
  .pchips .live { color: #FF7A6A; font-weight: 800; }
  .pctlwrap { margin-top: auto; padding-top: 24px; width: 292px; position: relative; }
  .picons { position: relative; height: 46px; margin-bottom: 14px; }
  .pib { all: unset; cursor: pointer; position: absolute; top: 0; width: 46px; height: 46px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.12); color: #fff; }
  .pib svg { width: 22px; height: 22px; }
  .pib.fav { left: 66px; } .pib.timer { left: 180px; }
  .pib.on { color: var(--accent); }
  .pctl { display: flex; align-items: center; justify-content: space-between; }
  .pchip { all: unset; cursor: pointer; width: 74px; text-align: center; border-radius: 10px; padding: 4px 0; }
  .pchip .r { display: flex; align-items: center; justify-content: center; gap: 2px; color: rgba(255,255,255,.6); }
  .pchip .logo { width: 32px; height: 32px; border-radius: 9px; font-size: 13px; }
  .pchip b { display: block; margin-top: 4px; font: 700 11px 'Figtree', sans-serif; color: rgba(255,255,255,.6); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .pchip svg { width: 16px; height: 16px; }
  .pbig { all: unset; cursor: pointer; width: 84px; height: 84px; border-radius: 50%; background: #fff; color: #0A1020; display: grid; place-items: center; box-shadow: 0 10px 26px rgba(0,0,0,.45); }
  .pbig svg { width: 38px; height: 38px; }
  .pbig .spin { border-color: rgba(10,16,32,.25); border-top-color: #0A1020; }
  .pvlogo { margin-top: 30px; }
  .pvlogo .tmark { transform: scale(1.8); transform-origin: center; margin: 0; }
  .pvsleep { position: absolute; left: 50%; bottom: calc(100% - 38px); transform: translateX(-50%); z-index: 3; background: #222226; border: 1px solid var(--border); border-radius: 16px; padding: 8px; display: grid; gap: 2px; width: 190px; box-shadow: 0 14px 40px rgba(0,0,0,.6); }
  .pvsleep b { padding: 6px 10px; font-size: 13px; color: var(--muted); }
  .pvsleep button { all: unset; cursor: pointer; padding: 9px 10px; border-radius: 10px; font-weight: 600; }
  .pvsleep button:hover { background: var(--chip); }
  .pvsleep .off { color: var(--bad); }
  .pempty { margin: auto; text-align: center; color: var(--muted); display: grid; justify-items: center; gap: 14px; }
  .pempty b { font: 700 20px 'Sora', sans-serif; color: var(--text); }
  .pempty .tmark { transform: scale(2.4); margin: 0 0 10px; }
  @media (min-width: 900px) {
    .wrap { max-width: none; margin: 0; width: 56%; }
    .pview { left: 56%; z-index: 5; transform: none; visibility: visible; border-left: 1px solid var(--border); background: transparent; }
    .player { display: none !important; }
    body:has(#player.show) .wrap { padding-bottom: calc(20px + env(safe-area-inset-bottom)); }
    .pv-back { display: none !important; }
    .pbgfade { background: linear-gradient(rgba(10,16,32,.5), rgba(10,16,32,.92)); }
  }
'''
rep("  .btn.play {", css + "  .btn.play {")

# ---------- JS ----------
js = r'''// ---------- player view ----------
let nbr = { prev: null, next: null };
let pvOpen = false;
let pvSleepOpen = false;
async function computeNeighbors(st) {
  nbr = { prev: null, next: null };
  try {
    const list = (await getCountry(st.country)).filter((x) => x.stream.url.startsWith('https:'));
    const i = list.findIndex((x) => x.id === st.id);
    if (i >= 0 && list.length > 1) nbr = { prev: list[(i - 1 + list.length) % list.length], next: list[(i + 1) % list.length] };
  } catch (e) { /* no neighbours: the chips stay empty */ }
  if (current && current.id === st.id) renderPv();
}
const HEART = (on) => `<svg viewBox="0 0 24 24" fill="${on ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8.2 2.7 4.5 6.3 4.5c2 0 3.7 1.1 4.6 2.7h2.2c.9-1.6 2.6-2.7 4.6-2.7 3.6 0 5.4 3.7 3.9 7.2C19.5 16.4 12 21 12 21z"/></svg>`;
const MOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
const SHARE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.6 13.5 6.8 4M15.4 6.5l-6.8 4"/></svg>';
const LINK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>';
const CHEV_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 5l-7 7 7 7"/></svg>';
const CHEV_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 5l7 7-7 7"/></svg>';
function renderPv() {
  const el = $('pview');
  if (!el) return;
  const st = current;
  if (!st) {
    el.innerHTML = `<div class="pscroll"><div class="pin"><div class="ptopr"><button class="pbtn pv-back" type="button" data-pv="close" aria-label="Back">${ICON.back}</button></div><div class="pempty">${LOGO}<b>Pick a station</b><span>It opens here, next to the list.</span></div></div></div>`;
    return;
  }
  const url = st.logoUrl ? st.logoUrl.replace(/^http:/, 'https:') : '';
  const letter = esc((st.name || '?').replace(/[^\p{L}\p{N}]/gu, '').charAt(0).toUpperCase() || '?');
  const cover = url ? `<img src="${esc(url)}" alt="" referrerpolicy="no-referrer" onerror="this.parentNode.textContent='${letter}'">` : letter;
  const bg = url ? `<img class="pbgimg" src="${esc(url)}" alt="" referrerpolicy="no-referrer" onerror="this.remove()">` : '';
  const chip = (x, next) => x
    ? `<button class="pchip" type="button" data-pv="${next ? 'next' : 'prev'}" aria-label="${next ? 'Next' : 'Previous'} station: ${esc(x.name)}"><span class="r">${next ? '' : CHEV_L}${logoHtml(x)}${next ? CHEV_R : ''}</span><b>${esc(x.name)}</b></button>`
    : '<span class="pchip" style="cursor:default"></span>';
  const playing = btnState === 'pause';
  const bigIcon = btnState === 'loading' ? '<span class="spin"></span>' : playing ? ICON.pause : ICON.play;
  const sleepMenu = pvSleepOpen ? `<div class="pvsleep" id="pv-sleepmenu"><b>Sleep timer</b>${[15, 30, 45, 60, 90].map((m) => `<button type="button" data-min="${m}">${m === 60 ? '1 hour' : m + ' minutes'}</button>`).join('')}<button type="button" class="off" data-min="0">Turn off</button></div>` : '';
  el.innerHTML = `${bg}<div class="pbgfade"></div><div class="pscroll"><div class="pin">
    <div class="ptopr"><button class="pbtn pv-back" type="button" data-pv="close" aria-label="Back">${ICON.back}</button>
      <div class="grp"><button class="pbtn" type="button" data-pv="share" aria-label="Share">${SHARE}</button>${st.website ? `<a class="pbtn" href="${esc(st.website)}" target="_blank" rel="noopener noreferrer" aria-label="Website">${LINK}</a>` : ''}</div></div>
    <div class="pcov">${cover}</div>
    <h2 class="pname">${esc(st.name)}</h2>
    <div class="pchips">${st.region ? `<span>${esc(st.region)}</span>` : ''}<span class="live">● LIVE</span></div>
    <div class="pctlwrap">${sleepMenu}
      <div class="picons"><button class="pib fav${isFav(st.id) ? ' on' : ''}" type="button" data-pv="fav" aria-label="${isFav(st.id) ? 'Remove from favorites' : 'Add to favorites'}">${HEART(isFav(st.id))}</button>
        <button class="pib timer${sleepEnd ? ' on' : ''}" id="pv-timer" type="button" data-pv="timer" aria-label="Sleep timer">${MOON}</button></div>
      <div class="pctl">${chip(nbr.prev, false)}<button class="pbig" type="button" data-pv="play" aria-label="${playing ? 'Pause' : 'Play'}">${bigIcon}</button>${chip(nbr.next, true)}</div></div>
    <div class="pvlogo">${LOGO}</div>
  </div></div>`;
}
function openPv() {
  if (!current || matchMedia('(min-width: 900px)').matches) return;
  renderPv();
  pvOpen = true;
  $('pview').classList.add('show');
  document.documentElement.classList.add('pv-open');
  history.pushState({ app: 1, pv: 1 }, '', location.href);
}
function closePv(pop = true) {
  if (!pvOpen) return;
  pvOpen = false;
  pvSleepOpen = false;
  $('pview').classList.remove('show');
  document.documentElement.classList.remove('pv-open');
  if (pop && history.state && history.state.pv) history.back();
}
function shareStation(st) {
  const url = location.origin + BASE + (st.country ? slugOf(st.country) + '/' : '');
  const data = { title: st.name, text: 'Listening to ' + st.name + ' on TUNO', url };
  if (navigator.share) navigator.share(data).catch(() => {});
  else { try { navigator.clipboard.writeText(url); } catch (e) {} toast('Link copied'); }
}
$('pview').addEventListener('click', (e) => {
  const m = e.target.closest('[data-min]');
  if (m) { pvSleepOpen = false; setSleep(Number(m.dataset.min)); renderPv(); return; }
  const b = e.target.closest('[data-pv]');
  if (!b) { if (pvSleepOpen) { pvSleepOpen = false; renderPv(); } return; }
  const act = b.dataset.pv;
  if (act === 'close') closePv();
  else if (act === 'play') togglePlay();
  else if (act === 'prev' && nbr.prev) play(nbr.prev);
  else if (act === 'next' && nbr.next) play(nbr.next);
  else if (act === 'share' && current) shareStation(current);
  else if (act === 'timer') { pvSleepOpen = !pvSleepOpen; renderPv(); }
  else if (act === 'fav' && current) {
    toggleFav(current);
    toast(isFav(current.id) ? 'Added to favorites' : 'Removed from favorites');
    if (!route.code && homeDraw) homeDraw();
    else if (route.code && listState.cat === 'fav' && countryDraw) countryDraw();
    redrawRows();
    renderPv();
  }
});
$('player').addEventListener('click', (e) => { if (!e.target.closest('button')) openPv(); });
document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && pvOpen) closePv(); });
renderPv();

'''
rep("// ---------- support ----------", js + "// ---------- support ----------")
open(p, 'w', encoding='utf-8', newline='\n').write(s)

# the new cache name so phones pick it up
sp = os.path.join(ROOT, 'sw.js')
t = open(sp, encoding='utf-8').read()
assert t.count("axar-radio-v5") == 1
open(sp, 'w', encoding='utf-8', newline='\n').write(t.replace('axar-radio-v5', 'axar-radio-v6'))
print('player view added')
