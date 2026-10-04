"""One-off patch: country pages get real URLs (/radio/croatia/) through the History API instead of #/HR."""
import os

p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'index.html')
s = open(p, encoding='utf-8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


rep("  return { code, name: 'Radio ' + niceName(code),", "  return { code, name: c && c.name ? 'Radio ' + c.name : 'Radio ' + niceName(code),")
rep("""  const card = (a) => `<button class="app" data-code="${a.code}" type="button" style="--a:${a.accent}">
        <img src="${a.icon}" alt="" loading="lazy" width="44" height="44"><b>${esc(a.name.replace(/^Radio /, ''))}</b><small>${a.stations}</small></button>`;""",
    """  const card = (a) => `<a class="app" data-code="${a.code}" href="${slugOf(a.code)}/" style="--a:${a.accent}">
        <img src="${a.icon}" alt="" loading="lazy" width="44" height="44"><b>${esc(a.name.replace(/^Radio /, ''))}</b><small>${a.stations}</small></a>`;""")
rep("  document.title = name + ' · World Radio';", "  document.title = `${name}: listen to ${pick.stations} live stations online | World Radio`;")
rep("  $('back').addEventListener('click', () => { location.hash = ''; });", "  $('back').addEventListener('click', () => go(''));")
rep("  if (c) { location.hash = '#/' + c.dataset.code; return; }",
    "  if (c) {\n    if (c.tagName === 'A' && (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1)) return;\n    e.preventDefault(); go(c.dataset.code); return;\n  }")
rep("""function routeNow() {
  const m = /^#\/([A-Z]{2})$/.exec(location.hash);
  if (m) renderCountry(m[1]); else renderHome();
}
window.addEventListener('hashchange', routeNow);
routeNow();""", """const BASE = new URL('.', document.baseURI).pathname;
function slugOf(code) { const c = COUNTRIES.find((x) => x.code === code); return c ? c.slug : code.toLowerCase(); }
function go(code) {
  history.pushState(null, '', BASE + (code ? slugOf(code) + '/' : ''));
  routeNow();
}
async function routeNow() {
  await getCountries();
  const old = /^#\/([A-Z]{2})$/.exec(location.hash);   // links from before the country pages had their own address
  if (old) history.replaceState(null, '', BASE + slugOf(old[1]) + '/');
  const rest = location.pathname.startsWith(BASE) ? location.pathname.slice(BASE.length) : '';
  const slug = rest.replace(/index\.html$/, '').replace(/\/$/, '');
  const c = slug && COUNTRIES.find((x) => x.slug === slug);
  if (c) renderCountry(c.code); else renderHome();
}
window.addEventListener('popstate', routeNow);
routeNow();""")
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('patched')
