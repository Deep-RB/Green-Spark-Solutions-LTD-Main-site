#!/usr/bin/env python3
"""
Self-host the free-licence stock photos the templates used to hot-link.

The design build loaded six photos (rooftop solar, safe water, irrigation,
rural solar, rice, Nepal) straight from the Pexels and Unsplash image servers,
with a grey "Field photo" placeholder as the local fallback. On the live site
that meant a third-party request on most pages, a strict CSP showing the
placeholder instead, and the project pages - which only ever use the local
file - showing the placeholder as their hero.

This script, run once from gssl_site/ on a machine with internet access:

1. downloads each photo listed in static/img/photos/photos.json and writes
   <slot>-480/-960/-1440 in JPEG and WebP into static/img/photos/, replacing
   the placeholders;
2. rewrites every <picture data-photo="slot"> in templates/ to load those
   local files through {% static %}.

It is idempotent: a template that already points at local files is left alone.

    pip install Pillow
    python tools/self_host_photos.py            # download + rewrite
    python tools/self_host_photos.py --rewrite  # rewrite templates only

To replace a slot with GSSL's own photo later, overwrite the six files for
that slot (same names, 4:3) - no template change is needed.
"""

from __future__ import annotations

import argparse
import io
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PHOTOS = ROOT / "static" / "img" / "photos"
TEMPLATES = ROOT / "templates"
WIDTHS = (480, 960, 1600)

PICTURE = re.compile(
    r'<picture data-photo="(?P<slot>[a-z0-9-]+)">(?P<img><img src="https://images\.[^>]*>)</picture>'
)


def download(manifest: dict) -> None:
    from PIL import Image, ImageOps

    for slot, info in manifest.items():
        req = urllib.request.Request(
            info["download"], headers={"User-Agent": "Mozilla/5.0 (GSSL site build)"}
        )
        data = urllib.request.urlopen(req, timeout=60).read()
        im = Image.open(io.BytesIO(data)).convert("RGB")
        im = ImageOps.fit(im, (1920, 1440), Image.LANCZOS)
        for w in WIDTHS:
            r = im.resize((w, w * 3 // 4), Image.LANCZOS)
            r.save(PHOTOS / f"{slot}-{w}.jpg", quality=82, optimize=True, progressive=True)
            r.save(PHOTOS / f"{slot}-{w}.webp", quality=80, method=6)
        print(f"downloaded {slot:<18} {info['photographer']} / {info['provider']}")


def local_picture(m: re.Match) -> str:
    slot, img = m.group("slot"), m.group("img")
    sizes = re.search(r'sizes="([^"]*)"', img).group(1)
    alt = re.search(r'alt="([^"]*)"', img).group(1)
    lazy = ' loading="lazy"' if 'loading="lazy"' in img else ""

    def srcset(ext: str) -> str:
        return ", ".join(
            f"{{% static 'img/photos/{slot}-{w}.{ext}' %}} {w}w" for w in WIDTHS
        )

    return (
        f'<picture data-photo="{slot}">'
        f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
        f"<img src=\"{{% static 'img/photos/{slot}-960.jpg' %}}\" srcset=\"{srcset('jpg')}\" "
        f'sizes="{sizes}" width="960" height="720" alt="{alt}"{lazy} decoding="async">'
        f"</picture>"
    )


def rewrite() -> int:
    changed = 0
    for path in sorted(TEMPLATES.rglob("*.html")):
        src = path.read_text(encoding="utf-8")
        out, n = PICTURE.subn(local_picture, src)
        if n:
            if "{% load static %}" not in out:
                out = "{% load static %}" + out
            path.write_text(out, encoding="utf-8")
            print(f"rewrote {n:>2} photo(s) in {path.relative_to(ROOT)}")
            changed += n
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--rewrite", action="store_true", help="rewrite templates only")
    args = parser.parse_args()

    manifest = json.loads((PHOTOS / "photos.json").read_text(encoding="utf-8"))
    if not args.rewrite:
        download(manifest)
    n = rewrite()
    left = sum(
        len(re.findall(r'src="https://images\.(?:pexels|unsplash)\.com', p.read_text(encoding="utf-8")))
        for p in TEMPLATES.rglob("*.html")
    )
    print(f"{n} picture(s) switched to local files; {left} hot-linked photo(s) remain")
    return 1 if left else 0


if __name__ == "__main__":
    sys.exit(main())
