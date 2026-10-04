"""One-off patch: the footer sits at the bottom of the screen when the page content is short (everything collapsed)."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("  .wrap { max-width: 860px; margin: 0 auto; padding: max(14px, env(safe-area-inset-top)) 16px calc(110px + env(safe-area-inset-bottom)); }",
    "  .wrap { max-width: 860px; margin: 0 auto; min-height: 100dvh; display: flex; flex-direction: column; padding: max(14px, env(safe-area-inset-top)) 16px calc(20px + env(safe-area-inset-bottom)); }\n"
    "  body:has(#player.show) .wrap { padding-bottom: calc(110px + env(safe-area-inset-bottom)); }\n"
    "  #home-lists { margin-bottom: 30px; }")
rep("  footer { margin-top: 30px; padding-top: 16px;", "  footer { margin-top: auto; padding-top: 16px;")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
