"""Ilova ikonkasi, splash ekran va bildirishnoma belgisini yaratadi (GitHub Actions ichida ishlaydi)."""
import glob
import os
from PIL import Image, ImageDraw

RES = "android/app/src/main/res"
BLUE = (30, 79, 168)
GOLD = (240, 181, 69)
WHITE = (255, 255, 255)


def mark(d, cx, cy, s, width):
    pts = [(cx - 0.30 * s, cy + 0.02 * s), (cx - 0.08 * s, cy + 0.24 * s), (cx + 0.32 * s, cy - 0.22 * s)]
    d.line(pts, fill=WHITE, width=width, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - width / 2, p[1] - width / 2, p[0] + width / 2, p[1] + width / 2], fill=WHITE)


def icon(size, round_=False, fg_only=False):
    S = size * 4
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if fg_only:
        s = S * 0.42
    else:
        if round_:
            d.ellipse([0, 0, S - 1, S - 1], fill=BLUE)
        else:
            d.rounded_rectangle([0, 0, S - 1, S - 1], radius=S * 0.22, fill=BLUE)
        s = S * 0.62
    cx = cy = S / 2
    mark(d, cx, cy, s, int(s * 0.13))
    r = s * 0.11
    sx, sy = cx + s * 0.34, cy - s * 0.40
    d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=GOLD)
    return im.resize((size, size), Image.LANCZOS)


for k, m in {"mdpi": 1, "hdpi": 1.5, "xhdpi": 2, "xxhdpi": 3, "xxxhdpi": 4}.items():
    folder = f"{RES}/mipmap-{k}"
    os.makedirs(folder, exist_ok=True)
    icon(int(48 * m)).save(f"{folder}/ic_launcher.png")
    icon(int(48 * m), round_=True).save(f"{folder}/ic_launcher_round.png")
    icon(int(108 * m), fg_only=True).save(f"{folder}/ic_launcher_foreground.png")

for f in glob.glob(f"{RES}/drawable*/splash.png"):
    w, h = Image.open(f).size
    im = Image.new("RGB", (w, h), BLUE)
    ic = icon(int(min(w, h) * 0.28), fg_only=True)
    im.paste(ic, ((w - ic.width) // 2, (h - ic.height) // 2), ic)
    im.save(f)

bg = f"{RES}/values/ic_launcher_background.xml"
with open(bg) as fh:
    txt = fh.read()
with open(bg, "w") as fh:
    fh.write(txt.replace("#FFFFFF", "#1E4FA8"))

with open(f"{RES}/drawable/ic_stat_notify.xml", "w") as fh:
    fh.write("""<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp"
    android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#FFFFFFFF"
        android:pathData="M9,16.2L4.8,12l-1.4,1.4L9,19 21,7l-1.4,-1.4L9,16.2z"/>
</vector>
""")
print("Ikonkalar tayyor")
