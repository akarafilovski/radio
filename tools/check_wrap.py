from playwright.sync_api import sync_playwright
S = 'C:/Users/ALEKSA~1/AppData/Local/Temp/claude/D--Development-Android-Mudras/9ea4b5eb-2ec9-478a-a90e-4a035ab60d6d/scratchpad/'
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    for w in (320, 360, 390, 430, 820):
        pg = b.new_context(viewport={'width': w, 'height': 800}, device_scale_factor=2, is_mobile=w < 600, has_touch=w < 600).new_page()
        pg.goto('http://localhost:8766/')
        pg.wait_for_timeout(1500)
        pg.locator('.fixed .support .head').click()
        pg.wait_for_timeout(300)
        r = pg.evaluate("""() => [...document.querySelectorAll('.addr3 span')].map(e => [e.scrollWidth, e.clientWidth, Math.round(parseFloat(getComputedStyle(e).fontSize))])""")
        h = pg.evaluate("document.querySelector('.addr3').getBoundingClientRect().height")
        print(w, 'lines', r, 'height', round(h), 'clipped', any(a > c + 1 for a, c, _ in r))
        if w == 390:
            pg.locator('.fixed .support .body').evaluate('e => e.scrollTo(0, 220)')
            pg.screenshot(path=S + 'w390.png')
    b.close()
