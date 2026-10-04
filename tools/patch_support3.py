"""One-off patch: address on one line (start ... last 8 characters) with copy and QR icon buttons at the end."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert a in s, a[:80]
    s = s.replace(a, b, 1)


# markup: one line with the buttons at its end
a = s.index('      <div class="label2">Wallet address</div>')
b = s.index('      <dl class="info"')
s = s[:a] + """      <div class="label2">Wallet address</div>
      <div class="addrline">
        <code class="addr1" title="${WALLET}"><span class="a-start">${WALLET.slice(0, -8)}</span><span class="a-end">${WALLET.slice(-8)}</span></code>
        <button type="button" class="ibtn copy" aria-label="Copy address"><svg class="i-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M5 15V6.5A2.5 2.5 0 0 1 7.5 4H15"/></svg><svg class="i-ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></button>
        <button type="button" class="ibtn qrbtn" aria-expanded="false" aria-label="Show QR code"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><path d="M14 14h3v3h-3zM20 14v.1M14 20h3M20 17v4"/></svg></button>
      </div>
      <div class="qrbox" id="qrbox" hidden><img src="icons/wallet-qr.png" alt="QR code of the Solana address" width="160" height="160"><p class="note">Scan with a wallet app on your phone.</p></div>
""" + s[b:]

# copy feedback: icon swap instead of button text
rep("""      const t = copy.querySelector('.ct');
      t.textContent = 'Copied';
      copy.classList.add('ok');
      setTimeout(() => { t.textContent = 'Copy address'; copy.classList.remove('ok'); }, 1800);""", """      copy.classList.add('ok');
      setTimeout(() => copy.classList.remove('ok'), 1800);""")

# css: drop chunked grid + big buttons, add the one-line row
a = s.index("  .addr { display: grid;")
b = s.index("  .info { margin: 0;")
s = s[:a] + """  .addrline { display: flex; align-items: center; gap: 8px; padding: 6px 6px 6px 14px; border-radius: 999px; background: #080808; border: 1px solid rgba(255,255,255,.08); }
  .addr1 { flex: 1; min-width: 0; display: flex; font: 600 13px/1 ui-monospace, 'SF Mono', Menlo, Consolas, monospace; color: #f2f2f6; }
  .a-start { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .a-end { flex: none; color: var(--accent); }
  .ibtn { all: unset; cursor: pointer; flex: none; width: 40px; height: 40px; border-radius: 50%; display: grid; place-items: center; background: rgba(255,255,255,.1); transition: transform .1s, background .2s; }
  .ibtn svg { width: 19px; height: 19px; } .ibtn:active { transform: scale(.92); }
  .ibtn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .ibtn.copy { background: var(--accent); color: #000; } .ibtn.copy .i-ok { display: none; } .ibtn.copy.ok { background: #3DD68C; } .ibtn.copy.ok .i-copy { display: none; } .ibtn.copy.ok .i-ok { display: block; }
  .ibtn.qrbtn.on { background: var(--accent); color: #000; }
  .qrbox { display: grid; justify-items: center; gap: 8px; text-align: center; } .qrbox[hidden] { display: none; }
  .qrbox img { width: 160px; height: 160px; border-radius: 16px; background: #fff; padding: 8px; }
""" + s[b:]
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
