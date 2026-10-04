"""Icons for every country in the radio catalog, in the Radio Croatia/Serbia/... app style:
white radio on a flag-coloured background with a round flag badge.

    python tools/make_icons.py

Writes icons/c/<cc>.png (160 px, used by the page), countries.json (code, accent, playable station count),
and 512 px Play-ready icons to ../_tools/_radio_all/<cc>.png for future store listings.
Our 12 apps keep their own hand-made icons (icons/<slug>.png).
"""
import colorsys
import io
import json
import os
import urllib.request

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = 'https://akarafilovski.github.io/tuno-data/radio/'
FLAGS = os.path.join(ROOT, 'tools', '_flags')
OUT_WEB = os.path.join(ROOT, 'icons', 'c')
OUT_PLAY = os.path.join(os.path.dirname(ROOT), '_tools', '_radio_all')
OURS = {'HR', 'RS', 'MK', 'SI', 'BG', 'RO', 'NL', 'GR', 'ME', 'BA', 'TR', 'HU'}
MIN_STATIONS = 3
S = 4


def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'aXar-radio-icons'})
    return urllib.request.urlopen(req, timeout=30).read()


def flag(cc):
    os.makedirs(FLAGS, exist_ok=True)
    p = os.path.join(FLAGS, cc.lower() + '.png')
    if not os.path.exists(p):
        open(p, 'wb').write(fetch(f'https://flagcdn.com/w640/{cc.lower()}.png'))
    return Image.open(p).convert('RGBA')


def colour(img):
    """The flag's main strong colour, darkened enough for white on top."""
    small = img.convert('RGB').resize((64, 40))
    counts = {}
    for px in small.getdata():
        h, l, s = colorsys.rgb_to_hls(*[c / 255 for c in px])
        if s < 0.35 or l > 0.85 or l < 0.08:
            continue
        key = (round(h * 24) % 24)
        counts.setdefault(key, []).append(px)
    if not counts:
        return (40, 44, 60)
    px = max(counts.values(), key=len)
    r, g, b = [sum(c[i] for c in px) / len(px) for i in range(3)]
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    l = min(l, 0.42)
    return tuple(int(c * 255) for c in colorsys.hls_to_rgb(h, l, max(s, 0.5)))


def accent(rgb):
    """A lighter version of the background colour, readable on black."""
    h, l, s = colorsys.rgb_to_hls(*[c / 255 for c in rgb])
    r, g, b = colorsys.hls_to_rgb(h, max(l, 0.62), min(1, s + 0.1))
    return '#%02X%02X%02X' % (int(r * 255), int(g * 255), int(b * 255))


def render(fl, bg, size=512):
    n = size * S
    k = n / 512
    img = Image.new('RGBA', (n, n), bg + (255,))
    d = ImageDraw.Draw(img)
    white = (255, 255, 255, 255)
    d.line([(150 * k, 36 * k), (372 * k, 124 * k)], fill=white, width=int(24 * k))
    d.ellipse([(150 - 12) * k, (36 - 12) * k, (150 + 12) * k, (36 + 12) * k], fill=white)
    d.rounded_rectangle([20 * k, 118 * k, 492 * k, 440 * k], radius=62 * k, fill=white)
    for cy in (188, 243, 298, 353, 408):
        d.rounded_rectangle([50 * k, (cy - 14) * k, 262 * k, (cy + 14) * k], radius=14 * k, fill=bg + (255,))
    cx, cy, r = 378 * k, 278 * k, 88 * k
    side = min(fl.size)
    x0 = (fl.size[0] - side) // 2
    sq = fl.crop((x0, 0, x0 + side, side)).resize((int(2 * r), int(2 * r)), Image.LANCZOS)
    mask = Image.new('L', sq.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, sq.size[0] - 1, sq.size[1] - 1], fill=255)
    d.ellipse([cx - r - 7 * k, cy - r - 7 * k, cx + r + 7 * k, cy + r + 7 * k], fill=(235, 235, 235, 255))
    img.paste(sq, (int(cx - r), int(cy - r)), mask)
    return img.resize((size, size), Image.LANCZOS)


def main():
    os.makedirs(OUT_WEB, exist_ok=True)
    os.makedirs(OUT_PLAY, exist_ok=True)
    index = json.loads(fetch(DATA + 'index.json'))['countries']
    out = []
    for c in index:
        cc = c['code']
        stations = json.loads(fetch(DATA + cc + '.json'))['stations']
        playable = sum(s['stream']['url'].startswith('https:') for s in stations)
        if playable < MIN_STATIONS:
            continue
        entry = {'code': cc, 'stations': playable}
        if cc not in OURS:
            try:
                fl = flag(cc)
            except Exception as e:
                print('no flag', cc, e)
                continue
            bg = colour(fl)
            icon = render(fl, bg)
            icon.save(os.path.join(OUT_PLAY, cc.lower() + '.png'), optimize=True)
            icon.resize((160, 160), Image.LANCZOS).save(os.path.join(OUT_WEB, cc.lower() + '.png'), optimize=True)
            entry['accent'] = accent(bg)
        out.append(entry)
        print(cc, playable)
    json.dump(out, open(os.path.join(ROOT, 'countries.json'), 'w'), separators=(',', ':'))
    print(len(out), 'countries')


if __name__ == '__main__':
    main()
