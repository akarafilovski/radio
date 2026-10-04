"""One-off patch: undo the compact sizes and open the support panel as a full-screen sheet (same design, QR sized to the screen)."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


# ---- back to the original sizes
rep("  .card { background: var(--card); border-radius: 16px; padding: 12px 14px 12px;", "  .card { background: var(--card); border-radius: 16px; padding: 18px 16px 16px;")
rep("  .qrbox { display: grid; justify-items: center; margin-bottom: 10px; }", "  .qrbox { display: grid; justify-items: center; margin-bottom: 20px; }")
rep("  .qrbox img { width: 132px; height: 132px; border-radius: 14px; background: #fff; padding: 6px; }",
    "  .qrbox img { width: clamp(110px, calc(100dvh - 560px), 190px); height: auto; aspect-ratio: 1; border-radius: 18px; background: #fff; padding: 10px; }")
rep("  .addrrow { display: flex; align-items: center; gap: 10px; margin-top: 2px; }", "  .addrrow { display: flex; align-items: center; gap: 12px; margin-top: 6px; }")
rep("  .redn { margin: 4px 0 0; font-size: 13px; line-height: 1.3; color: #F6465D; }", "  .redn { margin: 10px 0 0; font-size: 13.5px; line-height: 1.35; color: #F6465D; }")
rep("  .dep hr { border: 0; border-top: 1px solid #3A424D; margin: 8px 0; width: 100%; }", "  .dep hr { border: 0; border-top: 1px solid #3A424D; margin: 16px 0; width: 100%; }")
rep("  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 6px 12px; }", "  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 12px; }")
rep("  .grid2 .v { font-size: 14px; margin-top: 1px; }", "  .grid2 .v { font-size: 15px; }")
rep("  .fine { margin: 8px 0 0; font-size: 12.5px; line-height: 1.4; color: #848E9C; }", "  .fine { margin: 16px 0 0; font-size: 13px; line-height: 1.45; color: #848E9C; }")
rep("  .cbtn { all: unset; cursor: pointer; flex: none; width: 44px; height: 44px;", "  .cbtn { all: unset; cursor: pointer; flex: none; width: 48px; height: 48px;")
rep('''<img id="dep-qr" src="icons/qr-sol.png" alt="QR code of the wallet address" width="132" height="132">''',
    '''<img id="dep-qr" src="icons/qr-sol.png" alt="QR code of the wallet address" width="190" height="190">''')
rep('''          <div><span class="k">Minimum</span><span class="v" id="dep-min"></span></div>
''', '''          <div><span class="k">Minimum</span><span class="v" id="dep-min"></span></div>
          <div><span class="k">Address for</span><span class="v">SOL and USDC</span></div>
          <div><span class="k">Network</span><span class="v">Solana</span></div>
''')
rep('''<p class="fine">Same address for SOL and USDC, on the Solana network. Double-check every character: crypto transfers cannot be reversed.</p>''',
    '''<p class="fine">Double-check every character before sending. Crypto transfers cannot be reversed. Only send on the Solana network.</p>''')
rep("note: 'SOL addresses are case sensitive.'", "note: 'Please note that SOL addresses are case sensitive.'")
rep("note: 'Send USDC on the Solana network. Case sensitive.'", "note: 'USDC is sent on the Solana network. The address is case sensitive.'")

# ---- the bar no longer blurs (a blur would trap the full-screen sheet inside the bar) and the old body limit goes
rep("  .fixed .support .body { max-height: calc(100dvh - 92px); overflow-y: auto; }\n", "")
s = s.replace("backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);", "")

# ---- full-screen sheet when open
rep("  .favempty {", """  .support.open { position: fixed; inset: 0; z-index: 100; margin: 0; border: 0; border-radius: 0; overflow-y: auto; -webkit-overflow-scrolling: touch;
    padding-top: env(safe-area-inset-top); background: #14100d; display: flex; flex-direction: column; }
  .support.open .head { flex: none; width: auto; margin: 6px 6px 0; }
  .support.open .body { flex: 1; display: flex; flex-direction: column; justify-content: center; padding: 6px 14px calc(16px + env(safe-area-inset-bottom)); }
  .support.open .dep { width: min(100%, 520px); margin-inline: auto; }
  html.support-open, html.support-open body { overflow: hidden; }
  html.support-open .fixed { z-index: 200; }
  .closelbl { display: none; font-size: 14px; font-weight: 700; color: var(--accent); padding: 8px 14px; border-radius: 999px; background: rgba(255,255,255,.1); }
  .support.open .closelbl { display: inline-block; }
  @media (max-height: 720px) {
    .card { padding: 14px 14px 12px; } .qrbox { margin-bottom: 12px; } .dep hr { margin: 10px 0; } .grid2 { gap: 8px 12px; } .fine { margin-top: 10px; } .redn { margin-top: 6px; }
  }
  .favempty {""")

# ---- script: open/close with scroll lock, Close button, Escape
rep("""  root.querySelector('.head').addEventListener('click', (e) => { const o = root.classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', String(o)); });""",
    """  const head = root.querySelector('.head');
  const host = root.parentElement;
  const setOpen = (open) => {
    // the bar keeps its place in the page while the sheet covers the screen
    host.style.minHeight = open ? host.offsetHeight + 'px' : '';
    root.classList.toggle('open', open);
    document.documentElement.classList.toggle('support-open', open);
    head.setAttribute('aria-expanded', String(open));
    if (open) root.scrollTop = 0;
  };
  head.addEventListener('click', () => setOpen(!root.classList.contains('open')));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });""")
rep("""      <span class="t"><b>Support our work</b><span>Free, no ads. A tip keeps it running.</span></span>${ICON.chev}</button>""",
    """      <span class="t"><b>Support our work</b><span>Free, no ads. A tip keeps it running.</span></span><span class="closelbl">Close</span>${ICON.chev}</button>""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
