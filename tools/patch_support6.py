"""One-off patch: support panel in the style of the Binance deposit screen."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()

# ---------- markup + script ----------
a = s.index("const TOKENS = {")
b = s.index("// ---------- routing ----------")
s = s[:a] + """const TOKENS = {
  sol: { coin: 'S', name: 'Solana', ticker: 'SOL', network: 'Solana', min: '0.001 SOL', qr: 'icons/qr-sol.png', note: 'Please note that SOL addresses are case sensitive.' },
  usdc: { coin: '$', name: 'USD Coin', ticker: 'USDC', network: 'Solana', min: '0.001 USDC', qr: 'icons/qr-usdc.png', note: 'USDC is sent on the Solana network. The address is case sensitive.' },
};
function supportHtml() {
  const tab = (id) => `<button type="button" class="tab" data-token="${id}" role="tab"><i class="coin ${id}">${TOKENS[id].coin}</i>${TOKENS[id].ticker}</button>`;
  const hl = (t) => `<b>${t}</b>`;
  return `<div class="support" id="support">
    <button type="button" class="head" aria-expanded="false"><span class="heart"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8.2 2.7 4.5 6.3 4.5c2 0 3.7 1.1 4.6 2.7h2.2c.9-1.6 2.6-2.7 4.6-2.7 3.6 0 5.4 3.7 3.9 7.2C19.5 16.4 12 21 12 21z"/></svg></span>
      <span class="t"><b>Support our work</b><span>Free, no ads. A tip keeps it running.</span></span>${ICON.chev}</button>
    <div class="body"><div class="dep">
      <div class="tabs" role="tablist">${tab('sol')}${tab('usdc')}</div>
      <div class="netcard"><span class="k">Network</span><span class="v"><i id="dep-net-t">SOL</i> <em id="dep-net-n">Solana</em></span></div>
      <div class="card">
        <div class="qrbox"><img id="dep-qr" src="icons/qr-sol.png" alt="QR code of the wallet address" width="180" height="180"></div>
        <div class="k">Deposit Address</div>
        <div class="addrrow">
          <div class="addr3" title="${WALLET}"><i>${WALLET.slice(0, 6)}</i>${WALLET.slice(6, -6)}<i>${WALLET.slice(-6)}</i></div>
          <button type="button" class="cbtn" aria-label="Copy address"><svg class="i-copy" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M4 16V6a2 2 0 0 1 2-2h10"/></svg><svg class="i-ok" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></button>
        </div>
        <p class="redn" id="dep-note"></p>
        <hr>
        <div class="grid2">
          <div><span class="k">Token</span><span class="v" id="dep-token"></span></div>
          <div><span class="k">Minimum</span><span class="v" id="dep-min"></span></div>
          <div><span class="k">Same address for</span><span class="v">SOL and USDC</span></div>
          <div><span class="k">Confirmations</span><span class="v">1 (a few seconds)</span></div>
        </div>
        <p class="fine">Double-check every character before sending. Crypto transfers cannot be reversed. Only send on the Solana network.</p>
      </div>
    </div></div></div>`;
}
function wireSupport() {
  const root = $('support');
  root.querySelector('.head').addEventListener('click', (e) => { const o = root.classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', String(o)); });
  const pick = (id) => {
    const t = TOKENS[id];
    root.querySelectorAll('.tab').forEach((b) => { const on = b.dataset.token === id; b.classList.toggle('on', on); b.setAttribute('aria-selected', String(on)); });
    $('dep-qr').src = t.qr;
    $('dep-net-t').textContent = t.ticker;
    $('dep-net-n').textContent = t.network;
    $('dep-note').textContent = t.note;
    $('dep-token').textContent = t.name + ' (' + t.ticker + ')';
    $('dep-min').textContent = '>' + t.min;
  };
  root.querySelectorAll('.tab').forEach((b) => b.addEventListener('click', () => pick(b.dataset.token)));
  pick('sol');
  const copy = root.querySelector('.cbtn');
  copy.addEventListener('click', () => {
    const done = () => {
      toast('Address copied');
      copy.classList.add('ok');
      setTimeout(() => copy.classList.remove('ok'), 1800);
    };
    if (navigator.clipboard) navigator.clipboard.writeText(WALLET).then(done, done); else done();
  });
}

""" + s[b:]

# ---------- css ----------
a = s.index("  .panel {")
b = s.index("  .favempty {")
s = s[:a] + """  .dep { --by: #FCD535; --card: #2B3139; --card2: #1E2329; display: grid; grid-template-columns: minmax(0, 1fr); gap: 10px; }
  .tabs { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; padding: 4px; border-radius: 12px; background: var(--card2); }
  .tab { all: unset; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 10px 8px; border-radius: 9px; font: 700 14px 'Figtree', sans-serif; color: #848E9C; transition: background .2s, color .2s; }
  .tab.on { background: var(--card); color: var(--by); }
  .tab:focus-visible { outline: 2px solid var(--by); outline-offset: 2px; }
  .coin { width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; font: 800 12px 'Sora', sans-serif; font-style: normal; flex: none; color: #fff; }
  .coin.sol { background: linear-gradient(135deg, #9945FF, #14F195); color: #000; } .coin.usdc { background: #2775CA; }
  .dep .k { display: block; font-size: 13px; color: #848E9C; }
  .dep .v { display: block; font-weight: 700; font-size: 16px; color: #EAECEF; margin-top: 4px; }
  .netcard { background: var(--card); border-radius: 14px; padding: 12px 16px; }
  .netcard .v { font-size: 20px; margin-top: 2px; } .netcard .v i { font-style: normal; } .netcard .v em { font-style: normal; font-weight: 500; font-size: 13px; color: #848E9C; margin-left: 4px; }
  .card { background: var(--card); border-radius: 16px; padding: 18px 16px 16px; display: grid; grid-template-columns: minmax(0, 1fr); gap: 0; }
  .qrbox { display: grid; justify-items: center; margin-bottom: 20px; }
  .qrbox img { width: 180px; height: 180px; border-radius: 18px; background: #fff; padding: 10px; }
  .addrrow { display: flex; align-items: center; gap: 12px; margin-top: 6px; }
  .addr3 { flex: 1; min-width: 0; font: 600 18px/1.3 'Figtree', sans-serif; color: #EAECEF; word-break: break-all; letter-spacing: .1px; }
  .addr3 i { font-style: normal; color: var(--by); }
  .cbtn { all: unset; cursor: pointer; flex: none; width: 48px; height: 48px; border-radius: 50%; display: grid; place-items: center; background: #363D47; color: #EAECEF; transition: transform .1s, background .2s; }
  .cbtn svg { width: 22px; height: 22px; } .cbtn:active { transform: scale(.92); } .cbtn:focus-visible { outline: 2px solid var(--by); outline-offset: 2px; }
  .cbtn .i-ok { display: none; } .cbtn.ok { background: var(--by); color: #000; } .cbtn.ok .i-copy { display: none; } .cbtn.ok .i-ok { display: block; }
  .redn { margin: 10px 0 0; font-size: 13.5px; line-height: 1.35; color: #F6465D; }
  .dep hr { border: 0; border-top: 1px solid #3A424D; margin: 16px 0; width: 100%; }
  .grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 16px 12px; }
  .grid2 .v { font-size: 15px; }
  .fine { margin: 16px 0 0; font-size: 13px; line-height: 1.45; color: #848E9C; }
""" + s[b:]
s = s.replace("  .fixed .support .body { max-height: 62vh; overflow-y: auto; }", "  .fixed .support .body { max-height: 64vh; overflow-y: auto; }")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
