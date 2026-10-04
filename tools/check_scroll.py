from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--autoplay-policy=no-user-gesture-required'])
    for h in (844, 740, 640):
        pg = b.new_context(viewport={'width': 390, 'height': h}, device_scale_factor=2, is_mobile=True, has_touch=True).new_page()
        pg.goto('http://localhost:8766/')
        pg.evaluate("localStorage.setItem('radio.favsOpen','false'); localStorage.setItem('radio.recentOpen','false'); localStorage.setItem('radio.countriesOpen','false')")
        for playing in (False, True):
            if playing:
                pg.goto('http://localhost:8766/#/RS'); pg.wait_for_timeout(2500)
                pg.locator('.row').first.click(); pg.wait_for_timeout(3000)
                pg.locator('#back').click(); pg.wait_for_timeout(1200)
            else:
                pg.reload(); pg.wait_for_timeout(1800)
            info = pg.evaluate("""() => { const d = document.documentElement, w = document.querySelector('.wrap'), cs = getComputedStyle(w);
              return { inner: innerHeight, doc: d.scrollHeight, wrap: Math.round(w.getBoundingClientRect().height), minH: cs.minHeight, padB: cs.paddingBottom, padT: cs.paddingTop, bodyH: document.body.scrollHeight }; }""")
            print(h, 'player' if playing else 'no player', info, '-> extra', info['doc'] - info['inner'])
    b.close()
