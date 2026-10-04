import os
import sys

from playwright.sync_api import sync_playwright

S = 'C:/Users/ALEKSA~1/AppData/Local/Temp/claude/D--Development-Android-Mudras/9ea4b5eb-2ec9-478a-a90e-4a035ab60d6d/scratchpad/'
BASE = sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8766/'
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome', args=['--autoplay-policy=no-user-gesture-required'])
    pg = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True).new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto(BASE)
    pg.wait_for_timeout(2500)
    print('labels', pg.locator('.label').all_inner_texts())
    pg.screenshot(path=S + 'f1.png')
    pg.locator('.fixed .support .head').click()
    pg.wait_for_timeout(500)
    pg.screenshot(path=S + 'f2.png')
    pg.locator('.fixed .support .head').click()
    pg.goto(BASE + '#/RS')
    pg.wait_for_timeout(2500)
    pg.locator('.fav').nth(0).click()
    pg.locator('.fav').nth(3).click()
    pg.locator('.chip', has_text='Favorites').click()
    pg.wait_for_timeout(300)
    print('country favs', pg.locator('.row').count())
    pg.locator('#back').click()
    pg.wait_for_timeout(1200)
    print('home favs', pg.locator('.row').count(), 'errors', errs)
    pg.screenshot(path=S + 'f3.png')
    b.close()
