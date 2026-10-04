from playwright.sync_api import sync_playwright
S = 'C:/Users/ALEKSA~1/AppData/Local/Temp/claude/D--Development-Android-Mudras/9ea4b5eb-2ec9-478a-a90e-4a035ab60d6d/scratchpad/'
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    pg = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True).new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:8766/')
    pg.wait_for_timeout(2000)
    pg.locator('.fixed .support .head').click()
    pg.wait_for_timeout(300)
    print('qr hidden before', pg.locator('#qrbox').is_hidden())
    pg.locator('.qrbtn').click()
    pg.wait_for_timeout(300)
    print('qr visible after', pg.locator('#qrbox').is_visible(), 'img ok', pg.evaluate("document.querySelector('#qrbox img').naturalWidth"), errs)
    pg.screenshot(path=S + 'q1.png')
    b.close()
