"""One-off patch: full wallet address on two lines, copy button at the end."""
import os
import re

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()

old = re.search(r'        <code class="addr1".*?</code>\n', s, flags=re.S)
assert old
s = s.replace(old.group(0), '        <code class="addr2" title="${WALLET}"><span>${WALLET.slice(0, 22)}</span><span class="a-end">${WALLET.slice(22)}</span></code>\n', 1)

a = s.index("  .addrline {")
b = s.index("  .ibtn {")
s = s[:a] + """  .addrline { min-width: 0; display: flex; align-items: center; gap: 10px; padding: 10px 10px 10px 14px; border-radius: 18px; background: #080808; border: 1px solid rgba(255,255,255,.08); }
  .addr2 { flex: 1; min-width: 0; display: grid; gap: 4px; font: 600 15px/1.2 ui-monospace, 'SF Mono', Menlo, Consolas, monospace; color: #f2f2f6; letter-spacing: .2px; }
  .addr2 span { white-space: nowrap; overflow: hidden; text-overflow: clip; }
  .a-end { color: var(--accent); }
""" + s[b:]
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok', s.count('addr1'))
