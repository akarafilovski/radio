"""One-off patch: the open support panel is compact enough to show everything at once on a phone (no scrolling inside it)."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


# ---- css: smaller QR, tighter spacing, taller allowance before any inner scroll is needed
rep("  .fixed .support .body { max-height: 64vh; overflow-y: auto; }",
    "  .fixed .support .body { max-height: calc(100dvh - 92px); overflow-y: auto; }")
rep("  .card { background: var(--card); border-radius: 16px; padding: 18px 16px 16px; display: grid; grid-template-columns: minmax(0, 1fr); gap: 0; }",
    "  .card { background: var(--card); border-radius: 16px; padding: 12px 14px 12px; display: grid; grid-template-columns: minmax(0, 1fr); gap: 0; }")
rep("  .qrbox { display: grid; justify-items: center; margin-bottom: 20px; }", "  .qrbox { display: grid; justify-items: center; margin-bottom: 10px; }")
rep("  .qrbox img { width: 180px; height: 180px; border-radius: 18px; background: #fff; padding: 10px; }",
    "  .qrbox img { width: 132px; height: 132px; border-radius: 14px; background: #fff; padding: 6px; }")
rep("  .addrrow { display: flex; align-items: center; gap: 12px; margin-top: 6px; }", "  .addrrow { display: flex; align-items: center; gap: 10px; margin-top: 2px; }")
rep("  .redn { margin: 10px 0 0; font-size: 13.5px; line-height: 1.35; color: #F6465D; }", "  .redn { margin: 4px 0 0; font-size: 13px; line-height: 1.3; color: #F6465D; }")
rep("  .dep hr { border: 0; border-top: 1px solid #3A424D; margin: 16px 0; width: 100%; }", "  .dep hr { border: 0; border-top: 1px solid #3A424D; margin: 8px 0; width: 100%; }")
rep("  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 12px; }", "  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 12px; }")
rep("  .grid2 .v { font-size: 15px; }", "  .grid2 .v { font-size: 14px; margin-top: 1px; }")
rep("  .fine { margin: 16px 0 0; font-size: 13px; line-height: 1.45; color: #848E9C; }", "  .fine { margin: 8px 0 0; font-size: 12.5px; line-height: 1.4; color: #848E9C; }")
rep("  .cbtn { all: unset; cursor: pointer; flex: none; width: 48px; height: 48px;", "  .cbtn { all: unset; cursor: pointer; flex: none; width: 44px; height: 44px;")

# ---- markup: the same facts in less space (Network and "same address" move into one short line)
rep('''<img id="dep-qr" src="icons/qr-sol.png" alt="QR code of the wallet address" width="180" height="180">''',
    '''<img id="dep-qr" src="icons/qr-sol.png" alt="QR code of the wallet address" width="132" height="132">''')
rep('''          <div><span class="k">Address for</span><span class="v">SOL and USDC</span></div>
          <div><span class="k">Network</span><span class="v">Solana</span></div>
''', '')
rep('''<p class="fine">Double-check every character before sending. Crypto transfers cannot be reversed. Only send on the Solana network.</p>''',
    '''<p class="fine">Same address for SOL and USDC, on the Solana network. Double-check every character: crypto transfers cannot be reversed.</p>''')
rep("note: 'Please note that SOL addresses are case sensitive.'", "note: 'SOL addresses are case sensitive.'")
rep("note: 'USDC is sent on the Solana network. The address is case sensitive.'", "note: 'Send USDC on the Solana network. Case sensitive.'")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
