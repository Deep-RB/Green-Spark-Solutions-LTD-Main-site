#!/usr/bin/env python3
"""Drop a real field photo into a photo slot.

Usage:  python3 tools/make-photo-sizes.py path/to/photo.jpg clean-cooking
Writes assets/img/photos/<slot>-480|960.jpg and .webp (4:3, centre crop).
Slots: clean-cooking rooftop-solar safe-water solar-irrigation rural-solar
       low-emission-rice ics-phase-1 ics-phase-2 ics-phase-3 monitoring
       stove-manufacturing nepal-scoping team
Needs Pillow:  pip install Pillow
"""
import sys, pathlib
from PIL import Image, ImageOps

src, slot = sys.argv[1], sys.argv[2]
out = pathlib.Path(__file__).resolve().parent.parent / "assets/img/photos"
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
im = ImageOps.fit(im, (1920, 1440), Image.LANCZOS, centering=(0.5, 0.5))
for w in (960, 480):
    r = im.resize((w, w * 3 // 4), Image.LANCZOS)
    r.save(out / f"{slot}-{w}.jpg", quality=82, optimize=True, progressive=True)
    r.save(out / f"{slot}-{w}.webp", quality=80)
print("Updated", slot)
