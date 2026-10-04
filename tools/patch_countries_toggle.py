"""One-off patch: Countries section on the radio home can be collapsed (remembered); support sheet content starts at the top."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


# support sheet: start under the header instead of centered, and compress a bit earlier on short screens
rep("  .support.open .body { flex: 1; display: flex; flex-direction: column; justify-content: center;", "  .support.open .body { flex: 1; display: flex; flex-direction: column; justify-content: flex-start;")
rep("  @media (max-height: 720px) {", "  @media (max-height: 780px) {")

# countries: collapsible header when not searching
rep("""    if (m.length) html += `${!term ? '<div class="label">Countries</div>' : '<div class="label">Countries</div>'}<div class="apps">${m.map(card).join('')}</div>`;""",
    """    if (m.length) {
      if (term) html += '<div class="label">Countries</div>';
      else html += `<button type="button" class="label fold${countriesOpen ? ' open' : ''}" data-toggle="countries" aria-expanded="${countriesOpen}">Countries<span>${m.length}</span>${ICON.chev}</button>`;
      if (term || countriesOpen) html += `<div class="apps">${m.map(card).join('')}</div>`;
    }""")
rep("let favsOpen = load('radio.favsOpen', true);", "let favsOpen = load('radio.favsOpen', true);\nlet countriesOpen = load('radio.countriesOpen', true);")
rep("""    if (fold.dataset.toggle === 'recent') { recentOpen = !recentOpen; save('radio.recentOpen', recentOpen); }
    else { favsOpen = !favsOpen; save('radio.favsOpen', favsOpen); }""",
    """    if (fold.dataset.toggle === 'recent') { recentOpen = !recentOpen; save('radio.recentOpen', recentOpen); }
    else if (fold.dataset.toggle === 'countries') { countriesOpen = !countriesOpen; save('radio.countriesOpen', countriesOpen); }
    else { favsOpen = !favsOpen; save('radio.favsOpen', favsOpen); }""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
