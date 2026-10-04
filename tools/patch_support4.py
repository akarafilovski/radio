"""One-off patch: QR always visible at the top of the support panel, no QR toggle button."""
import os
import re

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# remove the old (hidden) QR box and the QR button
s = re.sub(r'      <div class="qrbox" id="qrbox" hidden>.*?</div>\n', '', s, count=1, flags=re.S)
s = re.sub(r'        <button type="button" class="ibtn qrbtn".*?</button>\n', '', s, count=1, flags=re.S)
# QR first in the panel
rep('<div class="body"><div class="panel">\n', '<div class="body"><div class="panel">\n      <div class="qrbox"><img src="icons/wallet-qr.png" alt="QR code of the Solana address" width="156" height="156"><p class="note">Scan with a wallet app, or copy the address below.</p></div>\n')
# JS for the toggle goes away
s = re.sub(r"  const qrBtn = root\.querySelector\('\.qrbtn'\);\n  qrBtn\.addEventListener\('click', \(\) => \{.*?\n  \}\);\n", '', s, count=1, flags=re.S)
s = s.replace("  .ibtn.qrbtn.on { background: var(--accent); color: #000; }\n", '')
s = s.replace(".qrbox { display: grid; justify-items: center; gap: 8px; text-align: center; } .qrbox[hidden] { display: none; }", ".qrbox { display: grid; justify-items: center; gap: 8px; text-align: center; }")
s = s.replace(".qrbox img { width: 160px; height: 160px;", ".qrbox img { width: 156px; height: 156px;")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('qrbtn left:', s.count('qrbtn'), 'qrbox:', s.count('qrbox'))
