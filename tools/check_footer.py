from playwright.sync_api import sync_playwright
S = 'C:/Users/ALEKSA~1/AppData/Local/Temp/claude/D--Development-Android-Mudras/9ea4b5eb-2ec9-478a-a90e-4a035ab60d6d/scratchpad/'
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--autoplay-policy=no-user-gesture-required'])
    pg = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True).new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://localhost:8766/')
    pg.evaluate("localStorage.setItem('radio.favsOpen','false'); localStorage.setItem('radio.recentOpen','false'); localStorage.setItem('radio.countriesOpen','false')")
    pg.reload(); pg.wait_for_timeout(2000)
    r = pg.evaluate("(() => { const f = document.querySelector('footer').getBoundingClientRect(); return [Math.round(f.bottom), innerHeight]; })()")
    print('all collapsed: footer bottom', r[0], 'of', r[1], '->', 'at the bottom' if r[1] - r[0] < 40 else 'NOT at the bottom')
    pg.screenshot(path=S + 'footer_collapsed.png')
    pg.evaluate("localStorage.setItem('radio.countriesOpen','true')"); pg.reload(); pg.wait_for_timeout(2000)
    r2 = pg.evaluate("(() => { const f = document.querySelector('footer').getBoundingClientRect(); return [Math.round(f.top), document.documentElement.scrollHeight]; })()")
    print('countries open: footer top', r2[0], 'page height', r2[1], '(footer after the list, page scrolls)')
    pg.goto('http://localhost:8766/#/RS'); pg.wait_for_timeout(2500)
    pg.locator('.row').first.click(); pg.wait_for_timeout(3500)
    pg.locator('#back').click(); pg.wait_for_timeout(1500)
    pad = pg.evaluate("parseFloat(getComputedStyle(document.querySelector('.wrap')).paddingBottom)")
    print('with the player bar: bottom padding', round(pad), 'px (room for the bar)', errs)
    b.close()
