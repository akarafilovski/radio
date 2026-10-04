import sys
from playwright.sync_api import sync_playwright
S = 'C:/Users/ALEKSA~1/AppData/Local/Temp/claude/D--Development-Android-Mudras/9ea4b5eb-2ec9-478a-a90e-4a035ab60d6d/scratchpad/'
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8766/'
TAG = sys.argv[2] if len(sys.argv) > 2 else 'fit'
SIZES = [(390, 844), (360, 740), (390, 700), (360, 640)]
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    for w, h in SIZES:
        pg = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, is_mobile=True, has_touch=True).new_page()
        pg.goto(BASE)
        pg.wait_for_timeout(1500)
        pg.locator('.support .head').click()
        pg.wait_for_timeout(500)
        sh, ch, pos, top = pg.evaluate("(() => { const e = document.querySelector('.support'); const r = e.getBoundingClientRect(); return [e.scrollHeight, e.clientHeight, getComputedStyle(e).position, Math.round(r.height)]; })()")
        print(f'{w}x{h}: sheet {top}px tall ({pos}), content {sh}px ->', 'everything visible' if sh <= ch + 1 else f'{sh - ch}px scrolls')
        if (w, h) in ((390, 844), (360, 640)):
            pg.screenshot(path=S + f'{TAG}_{w}x{h}.png')
        if (w, h) == (390, 844):
            pg.locator('.closelbl').click()
            pg.wait_for_timeout(300)
            print('   closed again:', pg.evaluate("document.querySelector('.support').classList.contains('open')") is False, '| page scroll unlocked:', pg.evaluate("getComputedStyle(document.documentElement).overflow") != 'hidden')
    b.close()
