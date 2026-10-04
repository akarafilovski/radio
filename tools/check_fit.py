import sys
from playwright.sync_api import sync_playwright
S = 'C:/Users/ALEKSA~1/AppData/Local/Temp/claude/D--Development-Android-Mudras/9ea4b5eb-2ec9-478a-a90e-4a035ab60d6d/scratchpad/'
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8766/'
SIZES = [(390, 844), (360, 740), (390, 700), (360, 640)]
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    for w, h in SIZES:
        pg = b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=2, is_mobile=True, has_touch=True).new_page()
        pg.goto(BASE)
        pg.wait_for_timeout(1500)
        pg.locator('.fixed .support .head').click()
        pg.wait_for_timeout(500)
        body = pg.locator('.support .body')
        sh, ch = pg.evaluate("(() => { const e = document.querySelector('.support .body'); return [e.scrollHeight, e.clientHeight]; })()")
        print(f'{w}x{h}: panel content {sh}px, visible {ch}px ->', 'everything fits' if sh <= ch + 1 else f'{sh - ch}px needs scrolling')
        if (w, h) == (390, 740) or (w, h) == (360, 740):
            pg.screenshot(path=S + f'fit_{w}x{h}.png')
    b.close()
