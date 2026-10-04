"""One-off patch: the Favorites section on the home page can be collapsed too; the choice is remembered."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b, 1)


rep("""    if (!term) html += `<div class="label">Favorites</div>` + (favs.length
      ? `<div class="list">${favs.map(stationRow).join('')}</div>`
      : `<div class="favempty"><span>${ICON.star}</span><p>Your favorite stations will be here.<br>Tap the star next to a station to add it.</p></div>`);""",
    """    if (!term) {
      html += `<button type="button" class="label fold${favsOpen ? ' open' : ''}" data-toggle="favs" aria-expanded="${favsOpen}">Favorites${favs.length ? `<span>${favs.length}</span>` : ''}${ICON.chev}</button>`;
      if (favsOpen) html += favs.length
        ? `<div class="list">${favs.map(stationRow).join('')}</div>`
        : `<div class="favempty"><span>${ICON.star}</span><p>Your favorite stations will be here.<br>Tap the star next to a station to add it.</p></div>`;
    }""")
rep("let recentOpen = load('radio.recentOpen', true);", "let recentOpen = load('radio.recentOpen', true);\nlet favsOpen = load('radio.favsOpen', true);")
rep("""  if (e.target.closest('[data-toggle="recent"]')) {
    recentOpen = !recentOpen;
    save('radio.recentOpen', recentOpen);
    if (homeDraw) homeDraw();
    return;
  }""", """  const fold = e.target.closest('[data-toggle]');
  if (fold) {
    if (fold.dataset.toggle === 'recent') { recentOpen = !recentOpen; save('radio.recentOpen', recentOpen); }
    else { favsOpen = !favsOpen; save('radio.favsOpen', favsOpen); }
    if (homeDraw) homeDraw();
    return;
  }""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
