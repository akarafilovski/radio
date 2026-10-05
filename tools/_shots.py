import json
import os
import subprocess
import sys
import time

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, '_shots')
os.makedirs(OUT, exist_ok=True)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8123'], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.2)
errors = []
try:
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome')
        ctx = b.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, timezone_id='Europe/Belgrade', locale='en-US')
        pg = ctx.new_page()
        pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.goto('http://localhost:8123/')
        pg.wait_for_timeout(3500)
        pg.screenshot(path=os.path.join(OUT, '1_first.png'))
        # open the country, then back
        pg.click('.yourc')
        pg.wait_for_timeout(2500)
        pg.screenshot(path=os.path.join(OUT, '2_country_home.png'))
        pg.click('#ctabs [data-tab=radio]')
        pg.wait_for_timeout(800)
        pg.screenshot(path=os.path.join(OUT, '3_radio.png'))
        pg.click('#ctabs [data-tab=news]')
        pg.wait_for_timeout(2000)
        pg.screenshot(path=os.path.join(OUT, '4_news.png'))
        # favorite + recent, back to Welcome
        st = pg.evaluate('''() => JSON.parse(localStorage.getItem('radio.favs') || '[]').length''')
        pg.click('#ctabs [data-tab=radio]')
        pg.wait_for_timeout(600)
        pg.click('.row .fav >> nth=0')
        pg.click('.row .fav >> nth=1')
        pg.click('#back')
        pg.wait_for_timeout(2500)
        pg.screenshot(path=os.path.join(OUT, '5_returning.png'), full_page=True)
        b.close()
finally:
    srv.terminate()
print('errors:', errors[:8])
