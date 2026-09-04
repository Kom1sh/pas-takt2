#!/usr/bin/env python3
"""Прогон вёрстки деки перед отдачей. Обязательный шаг: ничего не отдаём без него.

    python3 src/qa.py            # поднимет сервер сам, проверит все слайды

Проверяет:
  · пустые слайды;
  · выход за нижний, верхний, правый и левый край кадра;
  · обрезанный текст (scrollHeight > clientHeight);
  · элементы, вылезшие за свою карточку;
и собирает контактный лист в /tmp/deck-qa/sheet.png.
"""
import json, subprocess, sys, os, re, pathlib, http.server, socketserver, threading, functools, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = pathlib.Path("/tmp/deck-qa")
PORT = 8791

class _Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

def serve():
    h = functools.partial(_Quiet, directory=str(ROOT))
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", PORT), h)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

def chrome(args, timeout=90):
    return subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                           "--force-prefers-reduced-motion", "--force-device-scale-factor=1",
                           "--window-size=1600,900"] + args,
                          capture_output=True, text=True, timeout=timeout)

def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.png"):
        f.unlink()
    srv = serve(); time.sleep(0.6)
    url = f"http://127.0.0.1:{PORT}/index.html"

    n_slides = (ROOT / "index.html").read_text(encoding="utf-8").count('<section class="s')
    print(f"слайдов в сборке: {n_slides}")

    # ── геометрия через встроенный хук ──
    r = chrome(["--virtual-time-budget=9000", "--dump-dom", url + "?qa=1"])
    m = re.search(r"<title>QA:(.*?)</title>", r.stdout, re.S)
    geom = json.loads(m.group(1)) if m else None

    # ── скриншоты и пиксельные проверки ──
    from PIL import Image, ImageDraw
    pix = {}
    for i in range(1, n_slides + 1):
        p = OUT / f"s{i:02d}.png"
        chrome(["--virtual-time-budget=6000", f"--screenshot={p}", f"{url}#{i}"])
        im = Image.open(p).convert("RGB")
        probs = []
        if 100 * sum(1 for v in im.convert("L").getdata() if v > 60) / (1600 * 900) < 1.0:
            probs.append("слайд пустой")
        ref = im.getpixel((8, 892))
        if sum(1 for q in im.crop((80, 888, 1520, 900)).getdata()
               if sum(abs(a - b) for a, b in zip(q, ref)) > 60) > 400:
            probs.append("контент у нижнего края")
        ref2 = im.getpixel((1594, 450))
        if sum(1 for q in im.crop((1590, 120, 1600, 860)).getdata()
               if sum(abs(a - b) for a, b in zip(q, ref2)) > 60) > 300:
            probs.append("контент у правого края")
        if probs:
            pix[i] = probs

    # ── отчёт ──
    bad = sorted(set(list((geom or {}).keys()) + [str(k) for k in pix]), key=int)
    print("\n" + "=" * 62)
    if not bad:
        print("ВЁРСТКА ЧИСТАЯ — дефектов не найдено")
    else:
        print(f"НАЙДЕНЫ ДЕФЕКТЫ на {len(bad)} слайдах:")
        for k in bad:
            print(f"\n  слайд {int(k):02d}")
            for msg in pix.get(int(k), []):
                print(f"    ! {msg}")
            for msg in (geom or {}).get(k, [])[:8]:
                print(f"    · {msg}")
    if geom is None:
        print("\nВНИМАНИЕ: геометрический хук не отработал, проверены только пиксели")
    print("=" * 62)

    # ── контактный лист ──
    fs = sorted(OUT.glob("s*.png"))
    W, H, cols = 470, 264, 3
    rows = (len(fs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * W + 5 * (cols + 1), rows * (H + 18) + 5), (140, 148, 140))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(fs):
        im = Image.open(f).convert("RGB").resize((W, H), Image.LANCZOS)
        c, rr = i % cols, i // cols
        x, y = 5 + c * (W + 5), 5 + rr * (H + 18)
        sheet.paste(im, (x, y))
        mark = "  ← ДЕФЕКТ" if str(i + 1) in bad else ""
        d.text((x + 3, y + H + 2), f"{i+1:02d}{mark}", fill=(160, 30, 20) if mark else (25, 25, 25))
    sheet.save(OUT / "sheet.png")
    print(f"контактный лист: {OUT}/sheet.png")
    srv.shutdown()
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
