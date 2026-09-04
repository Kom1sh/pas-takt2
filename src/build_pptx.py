#!/usr/bin/env python3
"""Собирает takt2-gamedev.pptx в стиле деки: кремовая бумага, Onest, один акцент.

    python3 src/build_pptx.py            # → takt2-gamedev.pptx в корне репозитория

Иконки берутся из $CLAUDE_JOB_DIR/tmp/pptx/icons или из src/pptx-icons (см. ICONS).
"""
import os, re, json, pathlib, subprocess
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from PIL import Image
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from content import (MAP, FLOORS, PLAT_VS_SHOP, VS_PAIRS, CHAIN, CHAIN_NOTE, PIPELINE,
                     PIPELINE_ICONS, PIPELINE_NOTE, PIPELINE_ACCENT, MEASURE_FIGS, MEASURE_CARDS, MULTI,
                     MULTI_NOTE, MULTI_SUB, FAILTEST, CASES, TERMS, SOURCES, SOURCES_NOTE)

ROOT = pathlib.Path(__file__).resolve().parent.parent
ICONS = pathlib.Path(os.environ.get("PPTX_ICONS", ROOT / "src" / "pptx-icons"))
FONT = "Onest"

def C(h): return RGBColor.from_string(h.lstrip("#"))
PAPER, PAPER2, TILE = C("F1ECE3"), C("E7E1D5"), C("FFFFFF")
INK, MUTED, HAIR = C("16140F"), C("6B6558"), C("D3CCBE")
JET, FLAME, FLAME_INK, SAGE = C("14130F"), C("F26A1B"), C("B34405"), C("DCE2D9")
PAPER_ON_DARK = C("F1ECE3")

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
W, H = 13.333, 7.5
PAD = 0.65
CNT = [0]

# ── штриховые иконки → PNG через rsvg-convert ──────────────────────────────
UI = {
 "key":   '<circle cx="8" cy="8" r="4.6"/><path d="M11.3 11.3 L20.5 20.5"/><path d="M17.2 17.2l2.4 2.4"/><path d="M14.4 14.4l2.4 2.4"/>',
 "nomoney":'<rect x="2.5" y="6" width="19" height="12" rx="2"/><path d="M2.5 21.5 L21.5 2.5"/>',
 "compare":'<rect x="2.5" y="5" width="9" height="6" rx="1.4"/><rect x="2.5" y="14" width="15" height="6" rx="1.4"/><path d="M21.5 3.5v17"/>',
 "doc":   '<path d="M6 2.5h8l4 4v15H6z"/><path d="M14 2.5v4h4"/><path d="M9 12h6"/><path d="M9 16h6"/>',
 "layers":'<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 12.5 12 17.5l9.5-5"/><path d="M2.5 17 12 22l9.5-5"/>',
 "shield":'<path d="M12 2.5 4 6v6c0 5 3.4 8.4 8 9.5 4.6-1.1 8-4.5 8-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
 "eye":   '<path d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
 "funnel": '<path d="M2.5 4.5h19l-7.4 8.6V21l-4.2-2.6v-5.3z"/>',
 "unlock": '<rect x="4" y="10.5" width="16" height="10.5" rx="2"/><path d="M8 10.5V7a4 4 0 0 1 7.6-1.7"/>',
 "pen": '<path d="M4 20l3.2-.7L20 6.5a2.1 2.1 0 0 0-3-3L4.2 16.3z"/><path d="M15.5 5.5l3 3"/><path d="M4 20l.9-4"/>',
 "percent": '<path d="M19.5 4.5 4.5 19.5"/><circle cx="7.8" cy="7.8" r="2.9"/><circle cx="16.2" cy="16.2" r="2.9"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "no":    '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
 "play":  '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M10 9v6l5-3z"/>',
 "chain": '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l2.6-2.6a4.5 4.5 0 0 0-6.4-6.4L11.2 6.4"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0L5 12.6a4.5 4.5 0 0 0 6.4 6.4l1.4-1.4"/>',
 "ruler": '<path d="M3 17 17 3l4 4L7 21z"/><path d="M8 12l2 2"/><path d="M11 9l2 2"/><path d="M14 6l2 2"/>',
}
def ui_png(name, color="#F26A1B"):
    p = ICONS / f"ui_{name}_{color.lstrip('#')}.png"
    if not p.exists():
        svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="%s" '
               'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">%s</svg>' % (color, UI[name]))
        s = ICONS / f"ui_{name}.svg"; s.write_text(svg)
        subprocess.run(["rsvg-convert", "-w", "384", "-h", "384", "-o", str(p), str(s)], check=True)
    return str(p)

def ico(slug, on_dark=False):
    p = ICONS / (f"{slug}_paper.png" if on_dark and (ICONS / f"{slug}_paper.png").exists() else f"{slug}.png")
    return str(p)

# ── примитивы ──────────────────────────────────────────────────────────────
def new_slide(bg=PAPER):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = bg
    CNT[0] += 1
    return s

def rect(s, x, y, w, h, fill, radius=0.13, line=None, line_w=1.5):
    shp = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                             Inches(x), Inches(y), Inches(w), Inches(h))
    if radius: shp.adjustments[0] = min(0.5, radius / min(w, h))
    if fill is None: shp.fill.background()
    else: shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line is None: shp.line.fill.background()
    else: shp.line.color.rgb = line; shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp

def oval(s, x, y, d, fill):
    shp = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.fill.solid(); shp.fill.fore_color.rgb = fill; shp.line.fill.background(); shp.shadow.inherit = False
    return shp

def text(s, x, y, w, h, runs, size=14, color=INK, bold=False, align=PP_ALIGN.LEFT,
         anchor=MSO_ANCHOR.TOP, line=1.25, caps=False, spacing=None):
    """runs: строка или список (текст, {bold,color,size,url})."""
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = runs if isinstance(runs, list) and runs and isinstance(runs[0], list) else [runs]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = line
        if spacing: p.space_after = Pt(spacing)
        items = para if isinstance(para, list) else [para]
        for it in items:
            t, o = (it, {}) if isinstance(it, str) else it
            r = p.add_run(); r.text = t.upper() if caps else t
            f = r.font; f.name = FONT; f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold)
            f.color.rgb = o.get("color", color)
            if o.get("url"): r.hyperlink.address = o["url"]
    return tb

def pic(s, path, x, y, w=None, h=None):
    """Вписывает картинку в бокс w×h по пропорции, центрируя."""
    iw, ih = Image.open(path).size
    if w and h:
        k = min(w / iw, h / ih); pw, ph = iw * k, ih * k
        return s.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))
    return s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w) if w else None, Inches(h) if h else None)

def top(s, pill, dark=False, hot=False):
    col = PAPER_ON_DARK if dark else INK
    border = C("6E6A5E") if dark else (C("8A4A28") if hot else INK)
    w = 0.115 * len(pill) + 0.5
    rect(s, PAD, 0.5, w, 0.32, None, radius=0.16, line=border, line_w=1.5)
    text(s, PAD, 0.5, w, 0.32, pill, size=9, bold=True, color=col, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, caps=True)
    text(s, W - PAD - 1.2, 0.5, 1.2, 0.32, f"{CNT[0]:02d} / {{N}}", size=10, bold=True,
         color=(C("9A968C") if dark else (C("8A4A28") if hot else MUTED)), align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

def h2(s, t, y=1.05, color=INK, size=36):
    text(s, PAD, y, W - 2 * PAD, 1.25, t, size=size, bold=True, color=color, line=1.05)

def note(s, t, y=6.75, color=MUTED):
    text(s, PAD, y, W - 2 * PAD, 0.45, t, size=12, color=color, line=1.3)

def card(s, x, y, w, h, kind="tile"):
    fill = {"tile": TILE, "sage": SAGE, "dark": JET, "hot": FLAME, "paper2": PAPER2}[kind]
    rect(s, x, y, w, h, fill, radius=0.16)
    return fill

def card_text(s, x, y, w, h, kind, title, body, kn=None, badge=None, logos=None, title_size=17, body_size=13):
    """Карточка: якорь сверху (бейдж-иконка или ряд логотипов), текст снизу."""
    card(s, x, y, w, h, kind)
    dark = kind in ("dark",); hot = kind == "hot"
    tcol = PAPER_ON_DARK if dark else INK
    bcol = C("C9C4B8") if dark else (C("3E2A1C") if hot else MUTED)
    kcol = FLAME if dark else (C("5A3416") if hot else FLAME_INK)
    px, py = x + 0.28, y + 0.28
    cy = py
    if kn:
        text(s, px, cy, w - 0.56, 0.25, kn, size=9, bold=True, color=kcol, caps=True); cy += 0.32
    if badge:
        d = 1.15
        oval(s, px, cy, d, (C("2A2822") if dark else (C("D9560F") if hot else PAPER2)))
        pic(s, badge, px + 0.26, cy + 0.26, d - 0.52, d - 0.52)
    if logos:
        lx = px; lh = 0.62
        for lp in logos:
            iw, ih = Image.open(lp).size; lw = min(1.25, lh * iw / ih)
            pic(s, lp, lx, cy, lw, lh); lx += lw + 0.18
    # текстовый блок прижат к низу; если якорь высокий — блок сдвигается под него
    import math
    anchor_bottom = cy + (1.15 if badge else (0.62 if logos else 0))
    avail = w - 0.56
    lines = sum(max(1, math.ceil(len(part) * title_size * 0.0095 / avail)) for part in title.split("\n"))
    th = 0.36 * lines * (title_size / 18) + 0.06
    body_h = 1.8
    block_h = th + 0.08 + body_h
    by = max(anchor_bottom + 0.18, y + h - 0.28 - block_h)
    text(s, px, by, w - 0.56, th, title, size=title_size, bold=True, color=tcol, line=1.08)
    text(s, px, by + th + 0.08, w - 0.56, min(body_h, y + h - 0.2 - (by + th + 0.08)), body, size=body_size, color=bcol, line=1.3)

def cards3(s, specs, y=2.45, h=4.15):
    gap = 0.2; w = (W - 2 * PAD - 2 * gap) / 3
    for i, sp in enumerate(specs):
        card_text(s, PAD + i * (w + gap), y, w, h, **sp)

# ── содержание ─────────────────────────────────────────────────────────────
def cover():
    s = new_slide(FLAME); top(s, "ПАС · ИТ-1 · 3 курс · 2026/27", hot=True)
    text(s, PAD, 2.1, 9, 1.8, "ГЕЙМДЕВ", size=96, bold=True, color=INK, line=1.0)
    text(s, PAD, 4.05, 8, 1.0, "Такт 2. Объекты конкуренции\nи бутылочные горлышки", size=22, bold=False, color=INK, line=1.2)
    s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(PAD), Inches(5.55), Inches(W - PAD), Inches(5.55)).line.color.rgb = C("8A4A28")
    text(s, PAD, 5.75, 6, 0.4, "Разбираем на Cyberpunk 2077 и CD Projekt", size=12, bold=True, color=INK)
    text(s, 7.2, 5.75, 5.5, 0.4, "8 этажей · 1 горлышко · прототип для правок", size=12, bold=True, color=INK, align=PP_ALIGN.RIGHT)

def section(num, title, sub):
    s = new_slide(JET); top(s, f"Раздел {num}", dark=True)
    text(s, W - PAD - 4.2, 0.35, 4.2, 2.6, num, size=150, bold=True, color=FLAME, align=PP_ALIGN.RIGHT, line=0.9)
    text(s, PAD, 3.4, 9, 2.0, title, size=64, bold=True, color=PAPER_ON_DARK, line=0.98, caps=True)
    text(s, PAD, 5.6, 9, 0.6, sub, size=14, color=C("B8B3A7"))

def slide_gamedev():
    s = new_slide(); top(s, "Определение"); h2(s, "Что такое геймдев")
    w1 = 7.2; w2 = W - 2 * PAD - w1 - 0.2
    card(s, PAD, 2.45, w1, 4.15, "tile")
    oval(s, PAD + 0.28, 2.73, 1.35, PAPER2); pic(s, ui_png("play"), PAD + 0.58, 3.03, 0.75, 0.75)
    text(s, PAD + 0.28, 4.45, w1 - 0.56, 2.0,
         [[ "Программные интерактивные системы, в которых пользователь ", ("добровольно действует в рамках искусственных правил", {"bold": True}),
            ", а система непрерывно отвечает на его действия, — с доведением продукта и его поддержки до аудитории ",
            ("через цифровые площадки дистрибуции", {"bold": True}), "."]], size=15, color=INK, line=1.3)
    card_text(s, PAD + w1 + 0.2, 2.45, w2, 4.15, "dark", "Не геймдев",
              "Веб-дизайн, тренажёры и обучающие симуляторы, классические приложения, розничная продажа игр, настольные игры.",
              badge=ui_png("no"))

def slide_object():
    s = new_slide(); top(s, "Понятие"); h2(s, "Объект конкуренции — то,\nобладание которым даёт преимущество")
    cards3(s, [
        dict(kind="tile", title="Право, стандарт,\nопыт, внимание", body="Это можно удерживать. А пока удерживаешь — другим сюда хода нет.", badge=ui_png("key")),
        dict(kind="sage", title="Но не деньги\nи не доля рынка", body="Это ресурс на входе и следствие на выходе. За них не дерутся — их получают.", badge=ui_png("nomoney")),
        dict(kind="dark", title="Проверка: сравни\nс этажом выше", body="Объект тот же — значит, это один уровень, а не два. Если объект нельзя измерить — мы его не называем.", badge=ui_png("compare")),
    ])

def slide_map():
    s = new_slide(); top(s, "Схема · разметка карты")
    y0 = 1.05; text(s, PAD + 0.55, y0, 2.4, 0.25, "УРОВЕНЬ", size=8.5, bold=True, color=MUTED)
    text(s, PAD + 3.05, y0, 4, 0.25, "ОБЪЕКТ КОНКУРЕНЦИИ", size=8.5, bold=True, color=MUTED)
    text(s, W - PAD - 3.6, y0, 3.6, 0.25, "КТО СТОИТ", size=8.5, bold=True, color=MUTED, align=PP_ALIGN.RIGHT)
    rh = 0.66; gap = 0.07; y = y0 + 0.32
    for i, (no, nm, oj, logos) in enumerate([(a, b.replace(chr(10), '\n'), c, d) for a, b, c, d in MAP]):
        neck = (no == "08")
        rect(s, PAD, y, W - 2 * PAD, rh, JET if neck else TILE, radius=0.12)
        col = FLAME if neck else MUTED
        text(s, PAD + 0.16, y, 0.4, rh, no, size=14, bold=True, color=col, anchor=MSO_ANCHOR.MIDDLE)
        text(s, PAD + 0.62, y, 2.4, rh, nm, size=13.5, bold=True, color=(FLAME if neck else INK), anchor=MSO_ANCHOR.MIDDLE, line=1.05)
        text(s, PAD + 3.05, y, 5.2, rh, oj, size=13.5, bold=True, color=(C("FF9A52") if neck else FLAME_INK), anchor=MSO_ANCHOR.MIDDLE)
        lh = 0.4; lx = W - PAD - 0.2
        for slug in reversed(logos):
            p = ico(slug, on_dark=neck); iw, ih = Image.open(p).size; lw = min(0.95, lh * iw / ih)
            lx -= lw; pic(s, p, lx, y + (rh - lh) / 2, lw, lh); lx -= 0.16
        y += rh + gap

def floor(no, name, obj, title, specs, cp):
    s = new_slide(); top(s, f"Этаж {no} · {name}"); h2(s, title)
    cards3(s, specs, y=2.35, h=4.1)
    text(s, PAD, 6.6, W - 2 * PAD, 0.6, [[("На примере Cyberpunk 2077: ", {"bold": True, "color": FLAME_INK}), cp]], size=12, color=MUTED, line=1.3)

def floors():
    for f in FLOORS:
        specs = []
        for kind, kn, title, body, icon, logos in f["cards"]:
            sp = dict(kind=kind, title=title, body=body)
            if kn: sp["kn"] = kn
            if icon: sp["badge"] = ui_png(icon)
            if logos: sp["logos"] = [ico(x, on_dark=(kind == "dark")) for x in logos[:4]]
            specs.append(sp)
        sl = new_slide(); top(sl, f["pill"]); h2(sl, f["title"])
        cards3(sl, specs, y=2.35, h=4.1)
        if f["no"] == "08":
            text(sl, PAD, 6.6, W - 2 * PAD, 0.6,
                 PLAT_VS_SHOP.replace("<b>", "").replace("</b>", ""), size=12, color=MUTED, line=1.3)
        else:
            text(sl, PAD, 6.6, W - 2 * PAD, 0.6,
                 [[("На примере Cyberpunk 2077: ", {"bold": True, "color": FLAME_INK}), f["cp"]]],
                 size=12, color=MUTED, line=1.3)


def slide_chain():
    s = new_slide(); top(s, "Этаж 08 · цепочка удержания"); h2(s, "Как время игрока превращается\nв издержки переключения")
    steps = CHAIN
    n = len(steps); gap = 0.22; w = (W - 2 * PAD - gap * (n - 1)) / n; y = 2.7; h = 2.2
    for i, (t, sub) in enumerate(steps):
        x = PAD + i * (w + gap); last = i == n - 1
        rect(s, x, y, w, h, FLAME if last else TILE, radius=0.14)
        text(s, x + 0.18, y + 0.25, w - 0.36, 1.1, t, size=14, bold=True, color=INK, line=1.08)
        text(s, x + 0.18, y + h - 0.75, w - 0.36, 0.55, sub, size=11, color=(C("3E2A1C") if last else MUTED))
        if not last:
            a = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x + w + 0.02), Inches(y + h / 2 - 0.1), Inches(gap - 0.04), Inches(0.2))
            a.fill.solid(); a.fill.fore_color.rgb = FLAME; a.line.fill.background()
    note(s, CHAIN_NOTE, y=5.5)

def slide_pipeline():
    s = new_slide(); top(s, "Этаж 08 · зависимость разработчика"); h2(s, "Что нужно разработчику,\nчтобы игра появилась на витрине")
    steps = PIPELINE
    n = len(steps); gap = 0.2; w = (W - 2 * PAD - gap * (n - 1)) / n; y = 2.6; h = 3.0
    for i, (t, sub) in enumerate(steps):
        x = PAD + i * (w + gap)
        rect(s, x, y, w, h, TILE, radius=0.14)
        text(s, x + 0.2, y + 0.22, 1.2, 0.3, f"ШАГ {i+1}", size=10, bold=True, color=FLAME_INK)
        pic(s, ui_png(PIPELINE_ICONS[i]), x + 0.2, y + 0.6, 0.62, 0.62)
        text(s, x + 0.2, y + 1.4, w - 0.4, 0.55, t, size=15, bold=True, color=INK, line=1.08)
        text(s, x + 0.2, y + 2.0, w - 0.4, h - 2.2, sub, size=11.5, color=MUTED, line=1.3)
    note(s, PIPELINE_NOTE, y=5.85)
    text(s, PAD, 6.5, W - 2 * PAD, 0.5, PIPELINE_ACCENT, size=12, color=FLAME_INK, bold=True)

def slide_multi():
    s = new_slide(); top(s, "Кто стоит на нескольких этажах"); h2(s, "Позиция на одном этаже —\nрычаг на другом")
    groups = MULTI
    gw = (W - 2 * PAD - 0.25) / 2
    for gi, (name, items) in enumerate(groups):
        gx = PAD + gi * (gw + 0.25); rect(s, gx, 2.45, gw, 2.75, PAPER2, radius=0.16)
        text(s, gx + 0.25, 2.62, gw - 0.5, 0.35, name, size=15, bold=True, color=INK)
        tw = (gw - 0.5 - 0.3) / 3
        for ti, (lab, slug, sub) in enumerate(items):
            tx = gx + 0.25 + ti * (tw + 0.15); rect(s, tx, 3.05, tw, 2.0, TILE, radius=0.13)
            pic(s, ico(slug), tx + tw / 2 - 0.42, 3.22, 0.84, 0.84)
            text(s, tx + 0.12, 4.15, tw - 0.24, 0.3, lab, size=9, bold=True, color=FLAME_INK, align=PP_ALIGN.CENTER, caps=True)
            text(s, tx + 0.12, 4.45, tw - 0.24, 0.5, sub, size=10.5, color=MUTED, align=PP_ALIGN.CENTER, line=1.2)
    text(s, PAD, 5.4, W - 2 * PAD, 1.2, MULTI_NOTE, size=13, color=MUTED, line=1.35)
    note(s, MULTI_SUB)

def slide_vs():
    s = new_slide(); top(s, "Проверка · объекты различаются"); h2(s, "Объекты соседних этажей\nне совпадают")
    pairs = VS_PAIRS
    y = 2.35; h = 0.86
    for a, at, b, bt in pairs:
        rect(s, PAD, y, W - 2 * PAD, h, TILE, radius=0.14)
        half = (W - 2 * PAD - 0.8) / 2
        for k, (lab, t) in enumerate(((a, at), (b, bt))):
            x = PAD + 0.3 + k * (half + 0.8)
            text(s, x, y + 0.22, half - 0.2, 0.3, lab, size=9.5, bold=True, color=MUTED, caps=True)
            text(s, x, y + 0.55, half - 0.2, 0.6, t, size=14, bold=True, color=INK, line=1.15)
        text(s, PAD + 0.3 + half, y, 0.8, h, "≠", size=28, bold=True, color=FLAME, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        y += h + 0.12

def slide_neck_def():
    s = new_slide(); top(s, "Понятие · бутылочное горлышко"); h2(s, "Уровень, где мало игроков,\nа зависят от них все")
    lw = 7.4; specs = [("Признак 1", "Мало игроков", "Считаем тех, к кому реально можно пойти. Сотня студий — много, несколько витрин — мало.", "tile"),
                       ("Признак 2", "Нет альтернативы", "Можно заменить — больно, дорого, но можно — это не горлышко.", "tile"),
                       ("Что удерживает", "Барьер входа", "Не деньги, а то, что деньгами не покупается: сетевой эффект, библиотека, привычка.", "hot")]
    y = 2.5; ch = 1.28
    for kn, t, b, kind in specs:
        card(s, PAD, y, lw, ch, kind); dark = kind == "hot"
        text(s, PAD + 0.28, y + 0.2, lw - 0.56, 0.25, kn, size=9, bold=True, color=(C("5A3416") if dark else FLAME_INK), caps=True)
        text(s, PAD + 0.28, y + 0.47, lw - 0.56, 0.35, t, size=16, bold=True, color=INK)
        text(s, PAD + 0.28, y + 0.82, lw - 0.56, 0.45, b, size=11.5, color=(C("3E2A1C") if dark else MUTED), line=1.25)
        y += ch + 0.15
    # воронка
    fx = PAD + lw + 0.25; fw = W - PAD - fx; rect(s, fx, 2.5, fw, 4.15, TILE, radius=0.16)
    text(s, fx, 2.75, fw, 0.3, "ЭТАЖИ 01–07", size=9, bold=True, color=MUTED, align=PP_ALIGN.CENTER)
    cone = s.shapes.add_shape(MSO_SHAPE.TRAPEZOID, Inches(fx + 0.5), Inches(3.1), Inches(fw - 1.0), Inches(2.1))
    cone.rotation = 180; cone.adjustments[0] = 0.42; cone.fill.solid(); cone.fill.fore_color.rgb = PAPER2; cone.line.fill.background()
    for k in range(1, 7):
        yy = 3.1 + 2.1 * k / 7; ins = (fw - 1.0) * 0.42 * k / 7
        s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(fx + 0.5 + ins), Inches(yy), Inches(fx + fw - 0.5 - ins), Inches(yy)).line.color.rgb = TILE
    nw = (fw - 1.0) * 0.16 + 0.1; nx = fx + fw / 2 - nw / 2
    rect(s, nx, 5.2, nw, 0.7, FLAME, radius=0)
    text(s, nx, 5.22, nw, 0.4, "08", size=16, bold=True, color=INK, align=PP_ALIGN.CENTER)
    text(s, nx, 5.58, nw, 0.3, "ВИТРИНА", size=7, bold=True, color=C("3E2A1C"), align=PP_ALIGN.CENTER)
    a = s.shapes.add_shape(MSO_SHAPE.DOWN_ARROW, Inches(fx + fw / 2 - 0.12), Inches(5.95), Inches(0.24), Inches(0.4)); a.fill.solid(); a.fill.fore_color.rgb = FLAME; a.line.fill.background()
    text(s, fx, 6.35, fw, 0.3, "ИГРОК", size=10, bold=True, color=INK, align=PP_ALIGN.CENTER)

def slide_failtest():
    s = new_slide(); top(s, "Цепочка зависимостей · тест отказом"); h2(s, "Тест отказом\nпо четырём уровням")
    items = FAILTEST
    gap = 0.2; w = (W - 2 * PAD - 3 * gap) / 4; y = 2.5; h = 3.8
    for i, (t, b, v, dead) in enumerate(items):
        x = PAD + i * (w + gap); rect(s, x, y, w, h, JET if dead else TILE, radius=0.16)
        text(s, x + 0.25, y + 0.28, w - 0.5, 0.7, t, size=16, bold=True, color=(FLAME if dead else INK), line=1.1)
        text(s, x + 0.25, y + 1.05, w - 0.5, 1.9, b, size=12.5, color=(C("C9C4B8") if dead else MUTED), line=1.3)
        text(s, x + 0.25, y + h - 0.7, w - 0.5, 0.45, v, size=13, bold=True, color=(FLAME if dead else INK))
    note(s, "Три уровня из четырёх заменяемы. Жёсткая зависимость ровно одна.")

def slide_class():
    s = new_slide(JET); top(s, "Горлышко · обоснование", dark=True)
    text(s, PAD, 1.05, W - 2 * PAD, 1.25, [["Горлышко — ", ("уровень витрин", {"color": FLAME}), ",\nа не отдельная компания"]], size=36, bold=True, color=PAPER_ON_DARK, line=1.05)
    figs = [("75%", "выручки PC-дистрибуции у Steam — это лишь PC-проекция горлышка"), ("2–3%", "у GOG — третьей витрины PC. Всё, что не Steam и не Epic, — крошки"), ("8–10%", "у Epic, который раздаёт игры бесплатно не первый год")]
    w = (W - 2 * PAD) / 3
    for i, (n, l) in enumerate(figs):
        x = PAD + i * w
        text(s, x, 2.75, w - 0.4, 1.0, n, size=58, bold=True, color=FLAME, line=0.95)
        text(s, x, 3.8, w - 0.5, 0.8, l, size=12, color=C("B8B3A7"), line=1.3)
    for i, (t, b) in enumerate([("Что мешает войти", "Купленная библиотека не переносится. Уйти — значит бросить всё, за что заплачено."),
                                 ("Контраргумент", "Steam — только PC. Поэтому горлышко не компания, а уровень: в каждой экосистеме своя витрина.")]):
        x = PAD + i * ((W - 2 * PAD) / 2 + 0.1); w2 = (W - 2 * PAD) / 2 - 0.1
        rect(s, x, 4.9, w2, 1.6, C("232119"), radius=0.14)
        text(s, x + 0.28, 5.1, w2 - 0.56, 0.4, t, size=15, bold=True, color=PAPER_ON_DARK)
        text(s, x + 0.28, 5.55, w2 - 0.56, 0.9, b, size=12, color=C("B8B3A7"), line=1.3)

def slide_cases():
    s = new_slide(); top(s, "Горлышко · проверенные случаи"); h2(s, "Три случая отключения\nигры витриной")
    cases = CASES
    cards3(s, [dict(kind="tile", title=t, body=b + "  " + k, kn=sub, badge=ico(sl)) for sl, t, sub, b, k in cases], y=2.45, h=3.95)
    note(s, "Игра была готова и куплена. Отказал только уровень витрины — и этого хватило.")

def slide_hidden():
    s = new_slide(); top(s, "Скрытые горлышки"); h2(s, "Скрытые горлышки:\nсертификация, издатель, мощности")
    cards3(s, [dict(kind="tile", title="Сертификация\nи возрастной рейтинг", body="Не прошёл ESRB или PEGI — на консоль не вышел. Обойти нельзя.", badge=ui_png("shield")),
               dict(kind="tile", title="Нет издателя —\nнет игры", body="Команда сильная, права есть, а издателя нет. Для инди горлышко — шестой этаж, а не восьмой.", badge=ui_png("no")),
               dict(kind="tile", title="Мощности подрядчиков", body="Cyberpunk сорвал не аутсорс, а скоуп и старые консоли. Но конвейер студий — признак нехватки.", badge=ui_png("clock"))], y=2.45, h=3.95)
    note(s, "Горлышко ищется не по выручке этажа, а по отсутствию альтернативы у тех, кто зависит.")

def slide_open():
    s = new_slide(FLAME); top(s, "Открытый вопрос · выносим в зал", hot=True)
    h2(s, "Открытый вопрос:\nгде проходит граница рынка")
    cw = 4.6; gap = 0.25; x0 = (W - 2 * cw - gap) / 2; y = 3.3; h = 1.9
    for i, (kn, t, b) in enumerate([("Рынок = PC", "Горлышко — Steam", "75% выручки, альтернатив практически нет."),
                                     ("Рынок = гейминг целиком", "Горлышек несколько", "По одному на экосистему — и каждое монополист в своей.")]):
        x = x0 + i * (cw + gap); rect(s, x, y, cw, h, TILE, radius=0.16)
        text(s, x + 0.28, y + 0.28, cw - 0.56, 0.25, kn, size=9, bold=True, color=FLAME_INK, caps=True)
        text(s, x + 0.28, y + 0.6, cw - 0.56, 0.45, t, size=18, bold=True, color=INK)
        text(s, x + 0.28, y + 1.1, cw - 0.56, 0.7, b, size=13, color=MUTED, line=1.3)

SRC = SOURCES
def slide_sources():
    s = new_slide(); top(s, "Источники всех чисел"); h2(s, "Откуда взяты числа", size=30)
    rows = len(SRC) + 1; tb = s.shapes.add_table(rows, 3, Inches(PAD), Inches(1.95), Inches(W - 2 * PAD), Inches(4.9)).table
    tb.columns[0].width = Inches(6.6); tb.columns[1].width = Inches(2.2); tb.columns[2].width = Inches(W - 2 * PAD - 8.8)
    def cell(r, c, t, size=10, bold=False, color=INK, url=None):
        ce = tb.cell(r, c); ce.fill.solid(); ce.fill.fore_color.rgb = TILE if r else PAPER2
        ce.margin_left = ce.margin_right = Inches(0.1); ce.margin_top = ce.margin_bottom = Inches(0.04)
        tf = ce.text_frame; tf.word_wrap = True; p = tf.paragraphs[0]; run = p.add_run(); run.text = t
        run.font.name = FONT; run.font.size = Pt(size); run.font.bold = bold; run.font.color.rgb = color
        if url: run.hyperlink.address = url
    for c, hdr in enumerate(("ЧИСЛО", "ГДЕ В ДЕКЕ", "ИСТОЧНИК")): cell(0, c, hdr, 8.5, True, MUTED)
    for r, (n, w, dom, url) in enumerate(SRC, 1):
        cell(r, 0, n, 10, True); cell(r, 1, w, 10, False, MUTED); cell(r, 2, dom, 10, True, FLAME_INK, url)
    note(s, SOURCES_NOTE, y=6.9)

def slide_terms():
    s = new_slide(); top(s, "Понятия такта 2"); h2(s, "Понятия, которыми пользовались", size=30)
    gl = TERMS
    w = (W - 2 * PAD - 0.2) / 2; h = 1.35
    for i, (t, b) in enumerate(gl):
        x = PAD + (i % 2) * (w + 0.2); y = 2.0 + (i // 2) * (h + 0.15)
        rect(s, x, y, w, h, TILE, radius=0.14)
        text(s, x + 0.28, y + 0.25, w - 0.56, 0.4, t, size=15, bold=True, color=INK)
        text(s, x + 0.28, y + 0.68, w - 0.56, 0.6, b, size=12, color=MUTED, line=1.3)

# ── порядок ────────────────────────────────────────────────────────────────
cover(); slide_gamedev(); slide_object(); section("01", "Карта\nуровней", "Восемь этажей, на каждом свой объект конкуренции.")
slide_map(); floors(); slide_chain(); slide_pipeline(); slide_multi(); slide_vs()
section("02", "Бутылочное\nгорлышко", "Ищем его тестом отказом, а не по деньгам на этаже.")
slide_neck_def(); slide_failtest(); slide_class(); slide_cases(); slide_hidden(); slide_open(); slide_sources(); slide_terms()

# проставляем общее число слайдов в счётчики
N = len(prs.slides)
for sl in prs.slides:
    for sh in sl.shapes:
        if sh.has_text_frame and "{N}" in sh.text_frame.text:
            for p in sh.text_frame.paragraphs:
                for r in p.runs: r.text = r.text.replace("{N}", str(N))
out = ROOT / "takt2-gamedev.pptx"; prs.save(out)
print("сохранено:", out.name, "| слайдов:", N, "| размер:", out.stat().st_size // 1024, "КБ")
