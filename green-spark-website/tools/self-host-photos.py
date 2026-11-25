#!/usr/bin/env python3
"""Self-host the stock photos used by the photo cards.

The photo cards currently load free-licence photos from Unsplash / Pexels
(listed in assets/img/photos/photos.json). Run this once on a computer or
server with internet access to download them into the local photo slots
and point every page at the local files (no third-party requests, works with
a strict Content-Security-Policy img-src 'self'):

    pip install Pillow
    python3 tools/self-host-photos.py

To use your own photo for one slot instead:  tools/make-photo-sizes.py
"""
import json, re, glob, io, pathlib, urllib.request
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
PH = ROOT / "assets/img/photos"
manifest = json.loads((PH / "photos.json").read_text())

for slot, info in manifest.items():
    req = urllib.request.Request(info["download"], headers={"User-Agent": "Mozilla/5.0 (GSSL site build)"})
    data = urllib.request.urlopen(req, timeout=60).read()
    im = ImageOps.fit(Image.open(io.BytesIO(data)).convert("RGB"), (1920, 1440), Image.LANCZOS)
    for w in (960, 480):
        r = im.resize((w, w * 3 // 4), Image.LANCZOS)
        r.save(PH / f"{slot}-{w}.jpg", quality=82, optimize=True, progressive=True)
        r.save(PH / f"{slot}-{w}.webp", quality=80)
    print("downloaded", slot, "-", info["photographer"], "/", info["provider"])

def local(m):
    slot, img = m.group(1), m.group(2)
    sizes = re.search(r'sizes="([^"]*)"', img).group(1)
    alt = re.search(r'alt="([^"]*)"', img).group(1)
    lazy = ' loading="lazy"' if 'loading="lazy"' in img else ""
    b = f"../assets/img/photos/{slot}"
    return (f'<picture><source type="image/webp" srcset="{b}-480.webp 480w, {b}-960.webp 960w" sizes="{sizes}">'
            f'<img src="{b}-960.jpg" srcset="{b}-480.jpg 480w, {b}-960.jpg 960w" sizes="{sizes}" width="960" height="720" alt="{alt}"{lazy} decoding="async"></picture>')

for f in glob.glob(str(ROOT / "website/*.html")) + [str(ROOT / "components/index.html")]:
    s = open(f, encoding="utf-8").read()
    s2 = re.sub(r'<picture data-photo="([a-z0-9-]+)">(<img [^>]*>)</picture>', local, s)
    if s2 != s:
        open(f, "w", encoding="utf-8").write(s2)
print("Pages now use the local photo files. Remove the Unsplash/Pexels sentence from privacy.html if you like.")
