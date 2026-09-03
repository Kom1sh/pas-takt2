#!/usr/bin/env python3
"""Собирает index.html из шаблона, слайдов и вшитых шрифтов.

    python3 src/build.py

Правится только src/slides.html (содержание) и src/deck.tpl.html (оформление).
index.html — результат сборки, руками его трогать не надо.
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

tpl = (SRC / "deck.tpl.html").read_text(encoding="utf-8")
fonts = (SRC / "fonts.css").read_text(encoding="utf-8")
slides = (SRC / "slides.html").read_text(encoding="utf-8")

if "/*FONTS*/" not in tpl or "<!--SLIDES-->" not in tpl:
    raise SystemExit("в шаблоне нет якорей /*FONTS*/ и <!--SLIDES-->")

# Пробельные текстовые узлы между секциями в @media print порождают
# анонимные строчные боксы и выплёвывают лишнюю пустую страницу в PDF.
slides = re.sub(r">\s*\n\s*<!--[^>]*?-->\s*\n\s*<section", "><section", slides)
slides = re.sub(r"</section>\s+<section", "</section><section", slides)
slides = slides.strip()

out = tpl.replace("/*FONTS*/", fonts).replace("<!--SLIDES-->", slides)
out = re.sub(r"</section>\s+</div>", "</section></div>", out)
out = re.sub(r'<div id="wipe"></div>\s+<nav', '<div id="wipe"></div><nav', out)
out = re.sub(r"</nav>\s+<section", "</nav><section", out)
out = re.sub(r'<div id="deck">\s+', '<div id="deck">', out)

n = out.count('<section class="s')
(ROOT / "index.html").write_text(out, encoding="utf-8")
print(f"index.html собран: {len(out.encode()) // 1024} КБ, слайдов {n}")
