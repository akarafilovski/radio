"""One-off patch: a "Get TUNO" card on the World Radio home, hidden until TUNO is on Google Play (TUNO.live in index.html)."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("const PICKS = [", """// The TUNO app (radio + TV + news from every country). The card stays hidden until the Play listing exists:
// set live to true as soon as https://play.google.com/store/apps/details?id=com.axar.tuno opens.
const TUNO = { live: false, app: 'com.axar.tuno' };
const PICKS = [""")
rep("    let hits = [];\n    if (term.length >= 2) {\n      hits = searchStations(term);",
    "    if (!term && TUNO.live) html += tunoCard();\n    let hits = [];\n    if (term.length >= 2) {\n      hits = searchStations(term);")
rep("async function renderHome() {", """function tunoCard() {
  return `<a class="tuno" href="https://play.google.com/store/apps/details?id=${TUNO.app}" target="_blank" rel="noopener">
    <img src="icons/tuno-192.png" alt="" width="56" height="56"><span class="tx"><b>Get the TUNO app</b><small>Radio, TV and news from every country. Free, no ads.</small></span><em>Google Play</em></a>`;
}

async function renderHome() {""")
rep("  footer { margin-top: auto;", """  .tuno { display: flex; align-items: center; gap: 14px; margin: 26px 0 6px; padding: 14px 16px; border-radius: 18px; background: var(--surface); border: 1px solid var(--border); text-decoration: none; color: var(--text); }
  .tuno img { width: 56px; height: 56px; border-radius: 14px; flex: none; }
  .tuno .tx { flex: 1; min-width: 0; }
  .tuno b { display: block; font-size: 16px; }
  .tuno small { color: var(--muted); font-size: 13px; }
  .tuno em { font-style: normal; font-weight: 700; font-size: 13px; background: var(--accent); color: var(--on-accent); border-radius: 999px; padding: 8px 14px; flex: none; }
  .tuno:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  footer { margin-top: auto;""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
