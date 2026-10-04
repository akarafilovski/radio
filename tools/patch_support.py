"""One-off patch: always-visible favorites (home section + country chip) and a restyled support bar."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


rep("""    if (!term && favs.length) html += `<div class="label">Favorites</div><div class="list">${favs.map(stationRow).join('')}</div>`;
    if (m.length) html += `${!term && favs.length ? '<div class="label">Countries</div>' : ''}<div class="apps">${m.map(card).join('')}</div>`;""",
    """    if (!term) html += `<div class="label">Favorites</div>` + (favs.length
      ? `<div class="list">${favs.map(stationRow).join('')}</div>`
      : `<div class="favempty"><span>${ICON.star}</span><p>Your favorite stations will be here.<br>Tap the star next to a station to add it.</p></div>`);
    if (m.length) html += `${!term ? '<div class="label">Countries</div>' : ''}<div class="apps">${m.map(card).join('')}</div>`;""")

rep("""  const cats = ['all', ...Object.keys(CATEGORY).filter((k) => stations.some((s) => s.category === k))];""",
    """  const cats = ['all', 'fav', ...Object.keys(CATEGORY).filter((k) => stations.some((s) => s.category === k))];""")
rep("""  const drawChips = () => { chips.innerHTML = cats.length > 2 ? cats.map((c) => `<button class="chip${listState.cat === c ? ' on' : ''}" data-cat="${c}" type="button">${c === 'all' ? 'All' : CATEGORY[c]}</button>`).join('') : ''; };""",
    """  const drawChips = () => { chips.innerHTML = cats.map((c) => `<button class="chip${listState.cat === c ? ' on' : ''}" data-cat="${c}" type="button">${c === 'all' ? 'All' : c === 'fav' ? '★ Favorites' : CATEGORY[c]}</button>`).join(''); };""")
rep("""    const list = stations.filter((s) => (listState.cat === 'all' || s.category === listState.cat) &&""",
    """    const list = stations.filter((s) => (listState.cat === 'all' || (listState.cat === 'fav' ? isFav(s.id) : s.category === listState.cat)) &&""")
rep("""      : '<div class="empty">No station found.</div>';
    if (appOnly)""",
    """      : `<div class="empty">${listState.cat === 'fav' ? 'No favorites here yet. Tap the star next to a station.' : 'No station found.'}</div>`;
    if (appOnly)""")
rep("""      if (!route.code && homeDraw) homeDraw(); else favBtn.classList.toggle('on', isFav(s.id));""",
    """      if (!route.code && homeDraw) homeDraw();
      else if (route.code && listState.cat === 'fav' && countryDraw) countryDraw();
      else favBtn.classList.toggle('on', isFav(s.id));""")
rep("let homeDraw = null;", "let homeDraw = null;\nlet countryDraw = null;")
rep("""  drawChips();
  draw();
}""", """  drawChips();
  draw();
  countryDraw = draw;
}""")

a = s.index("function supportHtml() {")
b = s.index("function wireSupport() {")
s = s[:a] + """function supportHtml() {
  const token = (cls, coin, label, net, min) => `<div class="token ${cls}">
      <div class="th"><span class="coin">${coin}</span><div><b>${label}</b><small>${net}</small></div></div>
      <div class="addr"><code>${WALLET}</code></div>
      <button type="button" class="copy"><span class="ct">Copy address</span></button>
      <p class="note">Send more than ${min}. Solana addresses are case sensitive.</p></div>`;
  return `<div class="support" id="support">
    <button type="button" aria-expanded="false"><span class="heart"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8.2 2.7 4.5 6.3 4.5c2 0 3.7 1.1 4.6 2.7h2.2c.9-1.6 2.6-2.7 4.6-2.7 3.6 0 5.4 3.7 3.9 7.2C19.5 16.4 12 21 12 21z"/></svg></span>
      <span class="t"><b>Support our work</b><span>Free, no ads. A tip keeps it running.</span></span>${ICON.chev}</button>
    <div class="body">
      <div class="qr"><img src="icons/wallet-qr.png" alt="QR code of the Solana address" width="132" height="132"><p class="note">Scan with your wallet app, or copy the address below.</p></div>
      ${token('sol', 'S', 'Solana', 'SOL', '0.001 SOL')}${token('usdc', '$', 'USD Coin', 'USDC on the Solana network', '0.001 USDC')}
      <p class="note warn">Double-check every character of the address before sending. Crypto transfers cannot be reversed.</p></div></div>`;
}
""" + s[b:]
rep("""  s.querySelectorAll('.copy').forEach((b) => b.addEventListener('click', () => {
    const done = () => toast('Address copied');
    if (navigator.clipboard) navigator.clipboard.writeText(WALLET).then(done, done); else done();
  }));""", """  s.querySelectorAll('.copy').forEach((b) => b.addEventListener('click', () => {
    const done = () => {
      toast('Address copied');
      const t = b.querySelector('.ct');
      t.textContent = 'Copied ✓';
      b.classList.add('ok');
      setTimeout(() => { t.textContent = 'Copy address'; b.classList.remove('ok'); }, 1800);
    };
    if (navigator.clipboard) navigator.clipboard.writeText(WALLET).then(done, done); else done();
  }));""")

css = """  .support { border-radius: 20px; background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 22%, #111) 0%, #141414 70%); border: 1px solid color-mix(in srgb, var(--accent) 35%, transparent); overflow: hidden; }
  .support > button { all: unset; box-sizing: border-box; cursor: pointer; width: 100%; display: flex; align-items: center; gap: 12px; padding: 12px 14px; }
  .support > button:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
  .support .heart { width: 38px; height: 38px; border-radius: 50%; display: grid; place-items: center; flex: none; background: var(--accent); color: #000; animation: beat 2.4s ease-in-out infinite; }
  .support .heart svg { width: 20px; height: 20px; }
  @keyframes beat { 0%, 70%, 100% { transform: scale(1); } 80% { transform: scale(1.12); } 90% { transform: scale(1.02); } }
  .support .t { flex: 1; min-width: 0; } .support .t b { display: block; font: 700 15px 'Sora', sans-serif; } .support .t span { font-size: 12.5px; color: var(--muted); }
  .support .chev { color: var(--accent); transition: transform .25s; flex: none; } .support.open .chev { transform: rotate(180deg); }
  .support .body { display: none; padding: 2px 14px 16px; } .support.open .body { display: grid; gap: 12px; animation: drop .25s ease; }
  @keyframes drop { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  .qr { display: grid; justify-items: center; gap: 8px; text-align: center; }
  .qr img { width: 132px; height: 132px; border-radius: 16px; background: #fff; padding: 8px; }
  .token { background: rgba(0,0,0,.45); border: 1px solid var(--border); border-radius: 16px; padding: 12px; display: grid; gap: 10px; }
  .token .th { display: flex; align-items: center; gap: 10px; }
  .token .th b { display: block; font-size: 15px; } .token .th small { color: var(--muted); font-size: 12px; }
  .token .coin { width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center; font: 800 16px 'Sora', sans-serif; color: #fff; flex: none; }
  .token.sol .coin { background: linear-gradient(135deg, #9945FF, #14F195); color: #000; }
  .token.usdc .coin { background: #2775CA; }
  .token .addr { background: #0b0b0b; border-radius: 12px; padding: 10px 12px; }
  .token code { font: 500 12.5px/1.45 ui-monospace, Menlo, monospace; word-break: break-all; color: #e8e8ee; }
  .token .copy { all: unset; cursor: pointer; text-align: center; padding: 11px; border-radius: 999px; background: var(--accent); color: #000; font-weight: 700; font-size: 14px; transition: transform .1s; }
  .token .copy:active { transform: scale(.97); } .token .copy.ok { background: #3DD68C; }
  .note { font-size: 12.5px; color: var(--muted); margin: 0; } .note.warn { padding: 0 2px; }
  .favempty { display: flex; align-items: center; gap: 14px; padding: 14px 16px; border-radius: 18px; background: var(--surface); border: 1px dashed rgba(255,255,255,.14); }
  .favempty span { width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; background: var(--chip); color: var(--accent); flex: none; }
  .favempty svg { width: 22px; height: 22px; } .favempty p { margin: 0; color: var(--muted); font-size: 14px; }
"""
a = s.index("  .support { border-radius: 20px;")
b = s.index("  footer {")
s = s[:a] + css + s[b:]
for old in ("  .fixed .support .t b { font-size: 14px; }\n", "  .fixed .support .t span { font-size: 12px; }\n", "  .fixed .support > button { padding: 10px 14px; }\n"):
    s = s.replace(old, "")
rep("  .fixed .support .body { max-height: 52vh; overflow-y: auto; }", "  .fixed .support .body { max-height: 58vh; overflow-y: auto; }")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
