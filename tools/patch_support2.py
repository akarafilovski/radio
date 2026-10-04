"""One-off patch: support panel without QR; token tabs, chunked address, info rows, warning callout."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()

a = s.index("function supportHtml() {")
b = s.index("// ---------- routing ----------")
s = s[:a] + """const TOKENS = {
  sol: { coin: 'S', name: 'Solana', ticker: 'SOL', network: 'Solana', min: '0.001 SOL' },
  usdc: { coin: '$', name: 'USD Coin', ticker: 'USDC', network: 'Solana (SPL token)', min: '0.001 USDC' },
};
function supportHtml() {
  const chunks = WALLET.match(/.{1,4}/g).map((c) => `<span>${c}</span>`).join('');
  const tab = (id, label) => `<button type="button" class="tab" data-token="${id}" role="tab"><i class="coin ${id}">${TOKENS[id].coin}</i>${label}</button>`;
  return `<div class="support" id="support">
    <button type="button" class="head" aria-expanded="false"><span class="heart"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 21s-7.5-4.6-9.6-9.3C.9 8.2 2.7 4.5 6.3 4.5c2 0 3.7 1.1 4.6 2.7h2.2c.9-1.6 2.6-2.7 4.6-2.7 3.6 0 5.4 3.7 3.9 7.2C19.5 16.4 12 21 12 21z"/></svg></span>
      <span class="t"><b>Support our work</b><span>Free, no ads. A tip keeps it running.</span></span>${ICON.chev}</button>
    <div class="body"><div class="panel">
      <div class="tabs" role="tablist">${tab('sol', 'SOL')}${tab('usdc', 'USDC')}</div>
      <div class="label2">Wallet address</div>
      <div class="addr" aria-label="${WALLET}">${chunks}</div>
      <button type="button" class="copy"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="11" height="11" rx="2.5"/><path d="M5 15V6.5A2.5 2.5 0 0 1 7.5 4H15"/></svg><span class="ct">Copy address</span></button>
      <dl class="info" id="support-info"></dl>
      <div class="warn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3 2.5 20h19z"/><path d="M12 10v4.5M12 17.6v.1"/></svg>
        <p>Double-check every character before sending. Crypto transfers cannot be reversed.</p></div>
    </div></div></div>`;
}
function wireSupport() {
  const root = $('support');
  root.querySelector('.head').addEventListener('click', (e) => { const o = root.classList.toggle('open'); e.currentTarget.setAttribute('aria-expanded', String(o)); });
  const info = $('support-info');
  const pick = (id) => {
    const t = TOKENS[id];
    root.querySelectorAll('.tab').forEach((b) => { const on = b.dataset.token === id; b.classList.toggle('on', on); b.setAttribute('aria-selected', String(on)); });
    info.innerHTML = `<div><dt>Token</dt><dd>${t.name} (${t.ticker})</dd></div><div><dt>Network</dt><dd>${t.network}</dd></div>
      <div><dt>Minimum</dt><dd>more than ${t.min}</dd></div><div><dt>Note</dt><dd>Address is case sensitive</dd></div>`;
  };
  root.querySelectorAll('.tab').forEach((b) => b.addEventListener('click', () => pick(b.dataset.token)));
  pick('sol');
  const copy = root.querySelector('.copy');
  copy.addEventListener('click', () => {
    const done = () => {
      toast('Address copied');
      const t = copy.querySelector('.ct');
      t.textContent = 'Copied';
      copy.classList.add('ok');
      setTimeout(() => { t.textContent = 'Copy address'; copy.classList.remove('ok'); }, 1800);
    };
    if (navigator.clipboard) navigator.clipboard.writeText(WALLET).then(done, done); else done();
  });
}

""" + s[b:]

css = """  .support { border-radius: 22px; background: linear-gradient(135deg, color-mix(in srgb, var(--accent) 22%, #111) 0%, #141414 70%); border: 1px solid color-mix(in srgb, var(--accent) 35%, transparent); overflow: hidden; }
  .support .head { all: unset; box-sizing: border-box; cursor: pointer; width: 100%; display: flex; align-items: center; gap: 12px; padding: 12px 14px; }
  .support .head:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
  .support .heart { width: 38px; height: 38px; border-radius: 50%; display: grid; place-items: center; flex: none; background: var(--accent); color: #000; animation: beat 2.4s ease-in-out infinite; }
  .support .heart svg { width: 20px; height: 20px; }
  @keyframes beat { 0%, 70%, 100% { transform: scale(1); } 80% { transform: scale(1.12); } 90% { transform: scale(1.02); } }
  .support .t { flex: 1; min-width: 0; } .support .t b { display: block; font: 700 15px 'Sora', sans-serif; } .support .t span { font-size: 12.5px; color: var(--muted); }
  .support .chev { color: var(--accent); transition: transform .25s; flex: none; } .support.open .chev { transform: rotate(180deg); }
  .support .body { display: none; padding: 0 12px 12px; } .support.open .body { display: block; animation: drop .25s ease; }
  @keyframes drop { from { opacity: 0; transform: translateY(-6px); } to { opacity: 1; transform: none; } }
  .panel { background: rgba(0,0,0,.5); border: 1px solid var(--border); border-radius: 18px; padding: 12px; display: grid; gap: 12px; }
  .tabs { display: grid; grid-template-columns: 1fr 1fr; gap: 4px; padding: 4px; border-radius: 999px; background: rgba(255,255,255,.07); }
  .tab { all: unset; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 9px 8px; border-radius: 999px; font: 700 14px 'Figtree', sans-serif; color: var(--muted); transition: background .2s, color .2s; }
  .tab.on { background: var(--accent); color: #000; }
  .tab:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
  .coin { width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; font: 800 12px 'Sora', sans-serif; font-style: normal; flex: none; color: #fff; }
  .coin.sol { background: linear-gradient(135deg, #9945FF, #14F195); color: #000; } .coin.usdc { background: #2775CA; }
  .label2 { font: 700 11px 'Figtree', sans-serif; letter-spacing: .8px; text-transform: uppercase; color: var(--muted); margin-bottom: -4px; }
  .addr { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px 8px; padding: 12px; border-radius: 14px; background: #080808; border: 1px solid rgba(255,255,255,.06); }
  .addr span { font: 600 14px/1.3 ui-monospace, 'SF Mono', Menlo, Consolas, monospace; color: #f2f2f6; text-align: center; letter-spacing: .3px; padding: 5px 0; border-radius: 8px; background: rgba(255,255,255,.05); }
  .addr span:nth-child(odd) { color: var(--accent); }
  .copy { all: unset; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; padding: 12px; border-radius: 999px; background: var(--accent); color: #000; font-weight: 700; font-size: 15px; transition: transform .1s, background .2s; }
  .copy svg { width: 18px; height: 18px; } .copy:active { transform: scale(.97); } .copy.ok { background: #3DD68C; }
  .copy:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }
  .info { margin: 0; display: grid; border-radius: 14px; overflow: hidden; background: rgba(255,255,255,.04); }
  .info > div { display: flex; justify-content: space-between; gap: 12px; padding: 10px 12px; font-size: 13.5px; }
  .info > div + div { border-top: 1px solid rgba(255,255,255,.06); }
  .info dt { color: var(--muted); } .info dd { margin: 0; font-weight: 600; text-align: right; }
  .warn { display: flex; gap: 10px; align-items: flex-start; padding: 10px 12px; border-radius: 14px; background: rgba(255,170,60,.1); border: 1px solid rgba(255,170,60,.28); color: #ffd9a6; }
  .warn svg { width: 20px; height: 20px; flex: none; margin-top: 1px; color: #ffb84d; } .warn p { margin: 0; font-size: 13px; line-height: 1.4; }
"""
a = s.index("  .support { border-radius: 20px;")
b = s.index("  .favempty {")
s = s[:a] + css + s[b:]
s = s.replace("  .note { font-size: 12.5px; color: var(--muted); margin: 0; } .note.warn { padding: 0 2px; }\n", "  .note { font-size: 12.5px; color: var(--muted); margin: 0; }\n")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
