"""One-off patch: a Google Play icon button in the TUNO header. Until the app is listed it says it is coming soon;
set TUNO.live = true and it opens the store page."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("  .quick { display: grid;", """  .playbtn { background: var(--chip); }
  .playbtn svg { width: 22px; height: 22px; }
  .quick { display: grid;""")

rep("const flagUrl = (c) =>", """const PLAY_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#2D9CFF" d="M4 2.5 13 12 4 21.5z"/><path fill="#34D17A" d="M4 2.5 17.6 10.1 13 12z"/><path fill="#FFC83D" d="M17.6 10.1 21 12 17.6 13.9z"/><path fill="#F0525C" d="M4 21.5 13 12 17.6 13.9z"/></svg>';
const playBtn = () => `<a class="iconbtn playbtn" href="https://play.google.com/store/apps/details?id=${TUNO.app}" data-play target="_blank" rel="noopener" aria-label="Get the TUNO app on Google Play">${PLAY_ICON}</a>`;
const flagUrl = (c) =>""")

# Welcome header: Play icon before the info button
rep('<h1>TUNO</h1><a class="iconbtn about-btn"', '<h1>TUNO</h1>${playBtn()}<a class="iconbtn about-btn"')
# country header: Play icon at the end
rep('<img class="flag" src="${flagUrl(code)}" alt=""><h1>${esc(name)}</h1></div>', '<img class="flag" src="${flagUrl(code)}" alt=""><h1>${esc(name)}</h1>${playBtn()}</div>')

# until the listing exists the button explains instead of opening a dead page
rep("view.addEventListener('click', (e) => {\n", "view.addEventListener('click', (e) => {\n  if (e.target.closest('[data-play]') && !TUNO.live) { e.preventDefault(); toast('The TUNO app is coming soon to Google Play'); return; }\n")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('play button added')
