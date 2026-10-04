"""QR codes of the wallet address with the coin mark in the middle (like exchange deposit screens).

    python tools/make_qr.py   ->  icons/qr-sol.png, icons/qr-usdc.png
Error correction H keeps the code scannable with the logo on top. Check both with a phone before shipping.
"""
import os

import qrcode
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WALLET = '8x1G15KgVzHdTeVhULGPThfVfP68FeLiuTEy4AFmJRrT'
SIZE = 640
S = 4


def gradient(w, h, c1, c2):
    img = Image.new('RGB', (w, h))
    px = img.load()
    for y in range(h):
        for x in range(w):
            t = (x / w + y / h) / 2
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return img


def sol_mark(n):
    """Three slanted bars in the Solana purple-to-green gradient."""
    g = gradient(n, n, (153, 69, 255), (20, 241, 149))
    mask = Image.new('L', (n, n), 0)
    d = ImageDraw.Draw(mask)
    bar_h = n * 0.2
    skew = n * 0.14
    for i in range(3):
        y = n * 0.12 + i * n * 0.3
        left, right = n * 0.1, n * 0.9
        if i == 1:
            pts = [(left, y), (right - skew, y), (right, y + bar_h), (left + skew, y + bar_h)]
            pts = [(right - skew, y), (left, y), (left + skew, y + bar_h), (right, y + bar_h)]
            pts = [(left + skew, y), (right, y), (right - skew, y + bar_h), (left, y + bar_h)]
        else:
            pts = [(left + skew, y), (right, y), (right - skew, y + bar_h), (left, y + bar_h)] if i == 0 else \
                  [(left, y), (right - skew, y), (right, y + bar_h), (left + skew, y + bar_h)]
        d.polygon(pts, fill=255)
    g.putalpha(mask)
    return g


def usdc_mark(n):
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.ellipse([n * 0.05, n * 0.05, n * 0.95, n * 0.95], fill=(39, 117, 202, 255))
    # white ring and a simple dollar sign
    d.ellipse([n * 0.2, n * 0.2, n * 0.8, n * 0.8], outline=(255, 255, 255, 255), width=int(n * 0.05))
    d.line([(n * 0.5, n * 0.3), (n * 0.5, n * 0.7)], fill=(255, 255, 255, 255), width=int(n * 0.05))
    d.arc([n * 0.38, n * 0.36, n * 0.62, n * 0.52], 90, 360, fill=(255, 255, 255, 255), width=int(n * 0.05))
    d.arc([n * 0.38, n * 0.48, n * 0.62, n * 0.64], 270, 180, fill=(255, 255, 255, 255), width=int(n * 0.05))
    return img


def make(name, mark):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=2)
    q.add_data(WALLET)
    q.make(fit=True)
    img = q.make_image(fill_color='black', back_color='white').convert('RGBA').resize((SIZE, SIZE), Image.NEAREST)
    box = int(SIZE * 0.2)
    tile = Image.new('RGBA', (box * S, box * S), (0, 0, 0, 0))
    ImageDraw.Draw(tile).rounded_rectangle([0, 0, box * S - 1, box * S - 1], radius=int(box * S * 0.2), fill=(14, 14, 18, 255))
    m = mark(int(box * S * 0.7))
    tile.alpha_composite(m, ((box * S - m.width) // 2, (box * S - m.height) // 2))
    tile = tile.resize((box, box), Image.LANCZOS)
    img.alpha_composite(tile, ((SIZE - box) // 2, (SIZE - box) // 2))
    out = os.path.join(ROOT, 'icons', f'qr-{name}.png')
    img.convert('RGB').resize((360, 360), Image.LANCZOS).save(out, optimize=True)
    print(out)


if __name__ == '__main__':
    make('sol', sol_mark)
    make('usdc', usdc_mark)
