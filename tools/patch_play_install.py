"""One-off patch: the Google Play icon moves from the header into the 'Install TUNO' banner (next to Install)."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


# header buttons out
rep('<h1>TUNO</h1>${playBtn()}<a class="iconbtn about-btn"', '<h1>TUNO</h1><a class="iconbtn about-btn"')
rep('<h1>${esc(name)}</h1>${playBtn()}</div>', '<h1>${esc(name)}</h1></div>')
rep("view.addEventListener('click', (e) => {\n  if (e.target.closest('[data-play]') && !TUNO.live) { e.preventDefault(); toast('The TUNO app is coming soon to Google Play'); return; }\n", "view.addEventListener('click', (e) => {\n")
rep("  .playbtn { background: var(--chip); }\n  .playbtn svg { width: 22px; height: 22px; }\n", "  .btn.play { display: flex; align-items: center; justify-content: center; gap: 8px; background: var(--chip); }\n  .btn.play svg { width: 18px; height: 18px; flex: none; }\n")
rep("const playBtn = () => `<a class=\"iconbtn playbtn\" href=\"https://play.google.com/store/apps/details?id=${TUNO.app}\" data-play target=\"_blank\" rel=\"noopener\" aria-label=\"Get the TUNO app on Google Play\">${PLAY_ICON}</a>`;\n", "")

# the banner: a Google Play button under Install
rep('''    <button class="btn main" id="install-go" type="button">Install</button>''', '''    <button class="btn main" id="install-go" type="button">Install</button>
    <a class="btn play" id="install-play" href="#" target="_blank" rel="noopener" aria-label="Get the TUNO app on Google Play"></a>''')
rep("  const go = $('install-go');\n", """  const go = $('install-go');
  const playLink = $('install-play');
  playLink.innerHTML = PLAY_ICON + 'Google Play';
  playLink.href = 'https://play.google.com/store/apps/details?id=' + TUNO.app;
  // until the app is listed the button only says so
  playLink.addEventListener('click', (e) => { if (!TUNO.live) { e.preventDefault(); toast('The TUNO app is coming soon to Google Play'); } });
""")
rep("      go.style.display = 'none';\n", "      go.style.display = 'none';\n      playLink.style.display = 'none';   // no Google Play on iPhone\n")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('moved to the install banner')
