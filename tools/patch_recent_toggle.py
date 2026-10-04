"""One-off patch: the Recently played section on the home page can be collapsed; the choice is remembered."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b, 1)


rep("""    if (!term && rec.length) html += `<div class="label">Recently played</div><div class="list">${rec.map(stationRow).join('')}</div>`;""",
    """    if (!term && rec.length) {
      html += `<button type="button" class="label fold${recentOpen ? ' open' : ''}" data-toggle="recent" aria-expanded="${recentOpen}">Recently played<span>${rec.length}</span>${ICON.chev}</button>`;
      if (recentOpen) html += `<div class="list">${rec.map(stationRow).join('')}</div>`;
    }""")
rep("    shown = hits.concat(favs, rec);", "    shown = hits.concat(favs, rec, recent);")
rep("let homeDraw = null;", "let homeDraw = null;\nlet recentOpen = load('radio.recentOpen', true);")
rep("view.addEventListener('click', (e) => {\n", """view.addEventListener('click', (e) => {
  if (e.target.closest('[data-toggle="recent"]')) {
    recentOpen = !recentOpen;
    save('radio.recentOpen', recentOpen);
    if (homeDraw) homeDraw();
    return;
  }
""")
rep("  .label {", """  button.label.fold { all: unset; box-sizing: border-box; cursor: pointer; width: 100%; display: flex; align-items: center; gap: 8px; font: 700 13px 'Figtree', sans-serif; color: var(--muted); text-transform: uppercase; letter-spacing: .6px; margin: 22px 0 10px; }
  button.label.fold span { background: var(--chip); border-radius: 999px; padding: 1px 8px; font-size: 12px; letter-spacing: 0; }
  button.label.fold .chev { margin-left: auto; width: 20px; height: 20px; transition: transform .2s; transform: rotate(-90deg); color: var(--accent); }
  button.label.fold.open .chev { transform: none; }
  button.label.fold:focus-visible { outline: 2px solid var(--accent); outline-offset: 4px; border-radius: 6px; }
  .label {""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
