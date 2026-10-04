"""Playwright check of the per-country addresses (needs `python -m http.server 8123` in radio-web)."""
from playwright.sync_api import sync_playwright
B = 'http://localhost:8123/'
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    pg = b.new_page(viewport={'width': 400, 'height': 800})
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(B + 'croatia/'); pg.wait_for_selector('#stations .row', timeout=30000)
    print('direct:', pg.title(), '|', pg.inner_text('h1'), '|', pg.locator('#stations .row').count(), 'rows')
    pg.click('#back'); pg.wait_for_selector('.app'); print('back ->', pg.url, pg.title())
    pg.click('.app[data-code="DE"]'); pg.wait_for_selector('#stations .row', timeout=30000); print('tile ->', pg.url, pg.inner_text('h1'))
    pg.go_back(); pg.wait_for_selector('.app'); print('popstate ->', pg.url)
    pg.goto(B + '#/RS'); pg.wait_for_selector('#stations .row', timeout=30000); print('legacy ->', pg.url, pg.inner_text('h1'))
    pg.goto(B + 'serbia/'); pg.wait_for_selector('#stations .row', timeout=30000)
    pg.click('#stations .row'); pg.wait_for_timeout(1500)
    pg.click('#back'); pg.wait_for_selector('.app')
    print('player kept:', pg.evaluate("document.getElementById('player').classList.contains('show')"))
    print('errors:', errs)
    b.close()
