from playwright.sync_api import sync_playwright
S = 'C:/Users/ALEKSA~1/AppData/Local/Temp/claude/D--Development-Android-Mudras/9ea4b5eb-2ec9-478a-a90e-4a035ab60d6d/scratchpad/'
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True, permissions=['clipboard-read', 'clipboard-write'])
    pg = ctx.new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:8766/')
    pg.wait_for_timeout(2000)
    pg.locator('.fixed .support .head').click()
    pg.wait_for_timeout(400)
    pg.locator('.fixed .support .body').evaluate('e => e.scrollTo(0, 0)')
    pg.screenshot(path=S + 'a1.png')
    pg.locator('.fixed .support .body').evaluate('e => e.scrollTo(0, 99999)')
    pg.wait_for_timeout(200)
    pg.screenshot(path=S + 'a3.png')
    pg.locator('.cbtn').click()
    pg.wait_for_timeout(200)
    print('clipboard', pg.evaluate('navigator.clipboard.readText()'), 'qr visible', pg.locator('.qrbox').is_visible(), 'scrollW', pg.evaluate('document.documentElement.scrollWidth'), errs)
    b.close()
