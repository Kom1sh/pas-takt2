#!/usr/bin/env python3
"""Генерирует src/slides.html.

Логотипы описаны данными, а не разметкой: плиток много и руками они разъезжаются.
Правится этот файл, затем `python3 src/make_slides.py && python3 src/build.py`.
"""
import pathlib, json, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
RASTER = json.load(open(pathlib.Path(__file__).resolve().parent / "raster.json"))

INK = "#16140F"
# Фирменные цвета из Simple Icons. Белые и чёрные заменены на чернила:
# на белой плитке фирменный белый невидим, а чистый чёрный выглядит грязно.
BRAND = {
    "unity": INK, "unrealengine": "#0E1128", "godotengine": "#478CBF",
    "steam": INK, "epicgames": "#313131", "gogdotcom": "#86328A", "itchdotio": "#FA5C5C",
    "playstation": "#0070D1", "xbox": "#107C10", "nintendoswitch": "#E60012",
    "nintendo": "#E60012", "appstore": "#0D96F6", "googleplay": "#01875F",
    "apple": INK, "android": "#34A853", "ubisoft": INK, "ea": INK, "sony": INK,
    "riotgames": "#EB0029", "rockstargames": "#FCAF17", "cdprojekt": "#DC0D15",
    "valve": "#F74843", "vk": "#0077FF", "nvidia": "#76B900", "amd": "#ED1C24",
    "intel": "#0071C5", "sega": "#0089CF", "squareenix": "#ED1C24",
}
NAME = {
    "unity": "Unity", "unrealengine": "Unreal", "godotengine": "Godot", "steam": "Steam",
    "epicgames": "Epic Games", "gogdotcom": "GOG", "itchdotio": "itch.io",
    "playstation": "PlayStation", "xbox": "Xbox", "nintendoswitch": "Nintendo",
    "nintendo": "Nintendo", "appstore": "App Store", "googleplay": "Google Play",
    "apple": "iOS", "android": "Android", "ubisoft": "Ubisoft", "ea": "EA", "sony": "Sony",
    "riotgames": "Riot Games", "rockstargames": "Rockstar", "cdprojekt": "CD Projekt",
    "valve": "Valve", "vk": "VK Play", "nvidia": "NVIDIA", "amd": "AMD", "intel": "Intel",
    "sega": "Sega", "squareenix": "Square Enix",
    "virtuos": "Virtuos", "room8": "Room 8", "jali": "JALI", "wolf3d": "Wolf3D", "keywords": "Keywords",
}


# ── штриховые иконки для смысловых слайдов (свои, не брендовые) ────────────
UI = {
 "key":   '<circle cx="8" cy="8" r="4.6"/><path d="M11.3 11.3 L20.5 20.5"/><path d="M17.2 17.2l2.4 2.4"/><path d="M14.4 14.4l2.4 2.4"/>',
 "nomoney":'<rect x="2.5" y="6" width="19" height="12" rx="2"/><path d="M2.5 21.5 L21.5 2.5"/>',
 "compare":'<rect x="2.5" y="5" width="9" height="6" rx="1.4"/><rect x="2.5" y="14" width="15" height="6" rx="1.4"/><path d="M21.5 3.5v17"/>',
 "doc":   '<path d="M6 2.5h8l4 4v15H6z"/><path d="M14 2.5v4h4"/><path d="M9 12h6"/><path d="M9 16h6"/>',
 "gate":  '<path d="M3 21V9l9-6 9 6v12"/><path d="M9 21v-7h6v7"/><path d="M3 21h18"/>',
 "layers":'<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 12.5 12 17.5l9.5-5"/><path d="M2.5 17 12 22l9.5-5"/>',
 "link":  '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l2.6-2.6a4.5 4.5 0 0 0-6.4-6.4L11.2 6.4"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0L5 12.6a4.5 4.5 0 0 0 6.4 6.4l1.4-1.4"/>',
 "shield":'<path d="M12 2.5 4 6v6c0 5 3.4 8.4 8 9.5 4.6-1.1 8-4.5 8-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
 "eye":   '<path d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "no":    '<circle cx="12" cy="12" r="9"/><path d="M5.6 5.6l12.8 12.8"/>',
 "play":  '<rect x="2.5" y="4.5" width="19" height="15" rx="2.5"/><path d="M10 9v6l5-3z"/>',
}


def ui(name, big=False):
    return ('<div class="badge"><svg class="ui" viewBox="0 0 24 24" aria-hidden="true">%s</svg></div>'
            % UI[name])


def ico(slug, size=None):
    if slug in RASTER:
        return '<img class="ic" src="%s" alt="%s">' % (RASTER[slug]["uri"], NAME.get(slug, slug))
    st = 'color:%s' % BRAND.get(slug, INK)
    if size:
        st += ';width:%dpx;height:%dpx' % (size, size)
    return '<svg class="ic" style="%s"><use href="#i-%s"/></svg>' % (st, slug)


def brand(slug):
    return '<div class="badge">' + ico(slug) + '</div>'


def tile(slug, wide=False, mark=False, name=None):
    cls = ("tile" + (" wide" if wide else "") + (" mark" if mark else ""))
    return ('<div class="%s">%s<span class="nmb">%s</span></div>'
            % (cls, ico(slug), name or NAME.get(slug, slug)))


def row(no, name, obj, slugs, txt, neck=False):
    logos = "".join(ico(s) for s in slugs)
    return ('<div class="lvl%s r" style="--i:%d"><span class="no">%s</span>'
            '<span class="nm">%s</span><span class="oj">%s</span>'
            '<span class="who">%s<span class="txt">%s</span></span></div>'
            % (" neck" if neck else "", 2 + int(no), no, name, obj, logos, txt))


def top(pill):
    return '<div class="top"><span class="pill">%s</span><span class="cnt"></span></div>' % pill


import math
from content import (MAP, FLOORS, PLAT_VS_SHOP, VS_PAIRS, CHAIN, CHAIN_NOTE,
                     PIPELINE, PIPELINE_NOTE, PIPELINE_ACCENT, MEASURE_FIGS, MEASURE_CARDS,
                     MULTI, MULTI_NOTE, MULTI_SUB, FAILTEST, CASES, TERMS, SOURCES,
                     SOURCES_NOTE, GATES, OUTS)

FUNNEL = ('<div class="fn"><div class="cap">ЭТАЖИ 01–07</div><div class="cone">'
          + "".join('<i style="top:%.2f%%"></i>' % (b * 100 / 7.0) for b in range(1, 7))
          + '</div><div class="neck"><b>08</b><s>ВИТРИНА</s></div>'
            '<div class="arw"></div><div class="out">ИГРОК</div></div>')

def nl(t):
    return t.replace("\n", "<br>")

def anchor(icon, logos, kn):
    inner = ""
    if logos:
        inner += '<div class="logos">' + "".join(ico(x) for x in logos) + "</div>"
    if icon:
        inner += ui(icon)
    if kn:
        inner += '<div class="kn">%s</div>' % kn
    return '<div class="anchor">%s</div>' % inner if inner else ""

def card(kind, kn, title, body, icon=None, logos=None):
    return ('<div class="card %s">%s<h4>%s</h4><p>%s</p></div>'
            % (kind, anchor(icon, logos, kn), nl(title), body))

S = []

rays = ('<svg class="rays" viewBox="0 0 200 200" fill="none" stroke="rgba(22,20,15,.34)" stroke-width=".7">'
        + "".join('<line x1="100" y1="100" x2="%.1f" y2="%.1f"/>'
                  % (100 + 150 * math.cos(a * math.pi / 24), 100 + 150 * math.sin(a * math.pi / 24))
                  for a in range(48))
        + '<circle cx="100" cy="100" r="46" stroke="rgba(22,20,15,.4)"/>'
          '<circle cx="100" cy="100" r="72" stroke="rgba(22,20,15,.22)"/></svg>')
S.append(('Геймдев · Такт 2', 'hot cover', rays + top("ПАС · ИТ-1 · 3 курс · 2026/27") + '''
  <h1 class="r" style="--i:0">Геймдев</h1>
  <div class="sub r" style="--i:1">Такт 2. Объекты конкуренции<br>и бутылочные горлышки</div>
  <div class="meta-b r" style="--i:2"><span>Разбираем на Cyberpunk 2077</span>
    <span>8 этажей · 1 горлышко</span></div>'''))

S.append(('Что такое геймдев', '', top("Определение") + '''
  <h2 class="r" style="--i:0">Что такое геймдев</h2>
  <div class="cards r" style="--i:1;grid-template-columns:1.5fr 1fr">
    <div class="card mid">''' + '<div class="anchor">' + ui("play") + '</div>' + '''
      <p style="font-size:25px;line-height:1.42;color:var(--ink);max-width:none">Программные интерактивные системы, в которых пользователь <b>добровольно действует в рамках искусственных правил</b>, а система непрерывно отвечает на его действия, — с доведением продукта и его поддержки до аудитории <b>через цифровые площадки дистрибуции</b>.</p></div>
    ''' + card("dark mid", None, "Не геймдев",
               "Веб-дизайн, тренажёры и обучающие симуляторы, классические приложения, розничная продажа игр, настольные игры.", "no") + '''
  </div>'''))

S.append(('Объект конкуренции', '', top("Понятие") + '''
  <h2 class="r" style="--i:0">Объект конкуренции — то,<br>обладание которым даёт преимущество</h2>
  <div class="cards c3 r" style="--i:1">'''
  + card("tile", None, "Право, стандарт,\nопыт, внимание", "Это можно удерживать. А пока удерживаешь — другим сюда хода нет.", "key")
  + card("sage", None, "Но не деньги\nи не доля рынка", "Это ресурс на входе и следствие на выходе. За них не дерутся — их получают.", "nomoney")
  + card("dark", None, "Проверка: сравни\nс этажом выше", "Объект тот же — значит, это один уровень, а не два. Если объект нельзя измерить — мы его не называем.", "compare")
  + '</div>'))

S.append(('Раздел 01 — карта', 'dark sec', '<div class="huge">01</div>' + top("Раздел 01") + '''
  <h1 class="r" style="--i:0">Карта<br>уровней</h1>
  <p class="note r" style="--i:1">Восемь этажей, на каждом свой объект конкуренции.</p>'''))

S.append(('Карта уровней', '', top("Схема · разметка карты") + '''
  <div class="maphead"><span></span><span>Уровень</span><span>Объект конкуренции</span><span>Кто стоит</span></div>
  <div class="map">'''
  + "".join(row(no, nl(nm), oj, logos, "", neck=(no == "08")) for no, nm, oj, logos in MAP)
  + '</div>'))

for f in FLOORS:
    body = (top(f["pill"]) + '\n  <h2 class="r" style="--i:0">%s</h2>\n' % nl(f["title"])
            + '  <div class="cards c3 r" style="--i:1">'
            + "".join(card(k, kn, t, b, ic, lg) for k, kn, t, b, ic, lg in f["cards"])
            + '</div>\n')
    if f["no"] == "08":
        body += '  <div class="pvs r" style="--i:2">%s</div>\n' % PLAT_VS_SHOP
    else:
        body += ('  <p class="note after r" style="--i:2"><b style="color:var(--flame-ink)">'
                 'На примере Cyberpunk 2077:</b> %s</p>\n' % f["cp"])
    S.append(("%s · %s" % (f["no"], f["title"].split(":")[0]), '', body))

S.append(('Цепочка удержания', '', top("Этаж 08 · цепочка удержания") + '''
  <h2 class="r" style="--i:0;margin-bottom:24px">Как время игрока превращается<br>в его пожизненную ценность</h2>
  <div class="cards r" style="--i:1;grid-template-columns:repeat(6,1fr);gap:12px">'''
  + "".join('<div class="card%s"><h4 style="font-size:20px">%s</h4><p style="font-size:16px">%s</p></div>'
            % (" hot" if i == len(CHAIN) - 1 else "", nl(t), sub) for i, (t, sub) in enumerate(CHAIN))
  + '</div>\n  <p class="note after r" style="--i:2">%s</p>' % CHAIN_NOTE))

S.append(('Пайплайн выхода на витрину', '', top("Этаж 08 · зависимость разработчика") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Что нужно разработчику,<br>чтобы игра появилась на витрине</h2>
  <div class="cards r" style="--i:1;grid-template-columns:repeat(5,1fr);gap:13px">'''
  + "".join('<div class="card"><div class="anchor"><div class="kn" style="font-size:24px;color:var(--flame)">%d</div></div>'
            '<h4 style="font-size:21px">%s</h4><p style="font-size:16px">%s</p></div>'
            % (i + 1, t, b) for i, (t, b) in enumerate(PIPELINE))
  + '</div>\n  <p class="note after r" style="--i:2">%s<br><b style="color:var(--flame-ink)">%s</b></p>'
    % (PIPELINE_NOTE, PIPELINE_ACCENT)))

S.append(('Измеримость объекта', 'dark', top("Этаж 08 · чем измеряем объект") + '''
  <h2 class="r" style="--i:0">Если объект нельзя измерить —<br>мы его не называем</h2>
  <div class="figs r" style="--i:1;margin-top:34px">'''
  + "".join('<div class="fig"><div class="n">%s</div><div class="l">%s</div></div>' % (n, l) for n, l in MEASURE_FIGS)
  + '</div>\n  <div class="cards c2 r" style="--i:2;margin-top:36px">'
  + "".join(card("dark mid", None, t, b) for t, b in MEASURE_CARDS) + '</div>'))

def grp2(cap, tiles, cols, hot=False):
    return ('<div class="wallgrp%s"><div class="cap">%s</div><div class="grid" '
            'style="grid-template-columns:repeat(%d,1fr)">%s</div></div>'
            % (" hot" if hot else "", cap, cols, "".join(tiles)))

S.append(('Позиция на одном этаже — рычаг на другом', '', top("Кто стоит на нескольких этажах") + '''
  <h2 class="r" style="--i:0;margin-bottom:20px">Позиция на одном этаже —<br>рычаг на другом</h2>
  <div class="cards c2 r" style="--i:1;flex:0 0 auto">'''
  + "".join(
      '<div class="card"><div class="anchor"><div class="kn">%s</div></div>'
      '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px">%s</div></div>'
      % (name, "".join(
          '<div style="background:var(--paper-2);border-radius:12px;padding:14px 12px;text-align:center">'
          '<div style="font-size:12px;font-weight:700;letter-spacing:.06em;color:var(--muted);'
          'text-transform:uppercase;margin-bottom:10px">%s</div>'
          '<div style="display:flex;justify-content:center;margin-bottom:10px">%s</div>'
          '<div style="font-size:14px;font-weight:700;line-height:1.2">%s</div></div>'
          % (lab, ico(slug), sub) for lab, slug, sub in items))
      for name, items in MULTI)
  + '''</div>
  <p class="note after r" style="--i:2">%s</p>
  <p class="note r" style="--i:3;margin-top:10px">%s</p>''' % (MULTI_NOTE, MULTI_SUB)))

S.append(('Соседние этажи не совпадают', '', top("Проверка · объекты различаются") + '''
  <h2 class="r" style="--i:0;margin-bottom:18px">Объекты соседних этажей<br>не совпадают</h2>
  <div style="display:flex;flex-direction:column;gap:11px;flex:1;min-height:0">'''
  + "".join('<div class="vs r" style="--i:%d"><div class="side"><div class="lb">%s</div><div class="tx">%s</div></div>'
            '<div class="mid">≠</div><div class="side" style="padding-left:22px"><div class="lb">%s</div>'
            '<div class="tx">%s</div></div></div>' % (1 + i, a, at, b, bt)
            for i, (a, at, b, bt) in enumerate(VS_PAIRS))
  + '</div>'))

S.append(('Раздел 02 — горлышко', 'dark sec', '<div class="huge">02</div>' + top("Раздел 02") + '''
  <h1 class="r" style="--i:0">Бутылочное<br>горлышко</h1>
  <p class="note r" style="--i:1">Ищем его тестом отказом, а не по деньгам на этаже.</p>'''))

S.append(('Понятие горлышка', '', top("Понятие · бутылочное горлышко") + '''
  <h2 class="r" style="--i:0">Уровень, где мало игроков,<br>а зависят от них все</h2>
  <div class="cards r" style="--i:1;grid-template-columns:1.5fr 1fr;margin-top:24px">
    <div class="col">'''
  + card("", "Признак 1", "Мало игроков", "Считаем тех, к кому реально можно пойти. Сотня студий — много, несколько витрин — мало.")
  + card("", "Признак 2", "Нет альтернативы", "Можно заменить — больно, дорого, но можно — это не горлышко.")
  + card("hot", "Что удерживает", "Барьер входа", "Не деньги, а то, что деньгами не покупается: накопленная библиотека и привычка.")
  + '''</div>
    <div class="card" style="padding:24px">''' + FUNNEL + '''</div>
  </div>'''))

S.append(('Тест отказом', '', top("Цепочка зависимостей · тест отказом") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Что будет с цепочкой,<br>если этот уровень откажет</h2>
  <div class="chain">'''
  + "".join('<div class="ch%s r" style="--i:%d"><h4>%s</h4><p>%s</p><div class="verd">%s</div></div>'
            % (" dead" if d else "", 1 + i, t, b, v) for i, (t, b, v, d) in enumerate(FAILTEST))
  + '''</div>
  <p class="note after r" style="--i:6">Три уровня из четырёх заменяемы. Жёсткая зависимость ровно одна.</p>'''))

S.append(('Горлышко — уровень витрин', 'dark', top("Горлышко · обоснование") + '''
  <h2 class="r" style="--i:0">Горлышко — <span style="color:var(--flame)">уровень витрин</span>,<br>а не отдельная компания</h2>
  <div class="figs r" style="--i:1;margin-top:38px">
    <div class="fig"><div class="n">75%</div><div class="l">выручки PC-дистрибуции у Steam — это лишь PC-проекция горлышка</div></div>
    <div class="fig"><div class="n">2–3%</div><div class="l">у GOG — третьей витрины PC. Всё, что не Steam и не Epic, — крошки</div></div>
    <div class="fig"><div class="n">8–10%</div><div class="l">у Epic, который раздаёт игры бесплатно не первый год</div></div>
  </div>
  <div class="cards c2 r" style="--i:2;margin-top:40px">'''
  + card("dark mid", None, "Что мешает войти", "Купленная библиотека не переносится. Уйти — значит бросить всё, за что заплачено.")
  + card("dark mid", None, "Контраргумент", "Steam — только PC. Поэтому горлышко не компания, а <b>уровень</b>: в каждой экосистеме своя витрина.")
  + '</div>'))

S.append(('Три случая отключения игры', '', top("Горлышко · проверенные случаи") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Три случая отключения<br>игры витриной</h2>
  <div class="cards c3 r" style="--i:1">'''
  + "".join('<div class="card"><div class="anchor"><div class="badge">%s</div><div class="kn">%s</div></div>'
            '<h4>%s</h4><p>%s</p><p style="margin-top:16px;color:var(--ink);font-weight:700">%s</p></div>'
            % (ico(sl), sub, t, b, k) for sl, t, sub, b, k in CASES)
  + '''</div>
  <p class="note after r" style="--i:2">Игра была готова и куплена. Отказал <b style="color:var(--flame-ink)">только уровень витрины</b> — и этого хватило.</p>'''))

S.append(('Скрытые горлышки', '', top("Скрытые горлышки") + '''
  <h2 class="r" style="--i:0">Скрытые горлышки:<br>сертификация, издатель, мощности</h2>
  <div class="cards c3 r" style="--i:1">'''
  + card("tile", None, "Сертификация\nи возрастной рейтинг", "Не прошёл ESRB или PEGI — на консоль не вышел. Обойти нельзя.", "shield")
  + card("tile", None, "Нет издателя —\nнет игры", "Команда сильная, права есть, а издателя нет. Для инди горлышко — шестой этаж, а не восьмой.", "no")
  + card("tile", None, "Мощности подрядчиков", "Cyberpunk сорвал не аутсорс, а скоуп и старые консоли. Но конвейер студий — признак нехватки.", "clock")
  + '''</div>
  <p class="note after r" style="--i:2">Горлышко ищется не по выручке этажа, а по отсутствию альтернативы у тех, кто зависит.</p>'''))

S.append(('Открытый вопрос', 'hot', top("Открытый вопрос · выносим в зал") + '''
  <h2 class="r" style="--i:0;font-size:80px;font-weight:900;letter-spacing:-.038em;line-height:1.0">Открытый вопрос:<br>где проходит граница рынка</h2>
  <div class="cards c2 r" style="--i:1;margin-top:auto;width:1040px;align-self:center;flex:0 0 auto">'''
  + card("mid", "Рынок = PC", "Горлышко — Steam", "75% выручки, альтернатив практически нет.")
  + card("mid", "Рынок = гейминг целиком", "Горлышек несколько", "По одному на экосистему — и каждое монополист в своей.")
  + '</div>\n  <div class="mt"></div>'))

S.append(('Источники', '', top("Источники всех чисел") + '''
  <h2 class="r" style="--i:0;font-size:44px;margin-bottom:16px">Откуда взяты числа</h2>
  <div class="srcwrap r" style="--i:1"><table class="src">
    <thead><tr><th>Число</th><th>Где в деке</th><th>Источник</th></tr></thead>
    <tbody>'''
  + "".join('<tr><td class="c1">%s</td><td class="c2">%s</td><td class="c3">'
            '<a href="%s" target="_blank" rel="noopener">%s</a></td></tr>' % (n, w, url, dom)
            for n, w, dom, url in SOURCES)
  + '''</tbody></table></div>
  <p class="note after r" style="--i:2">%s</p>''' % SOURCES_NOTE))

S.append(('Понятия такта 2', '', top("Понятия такта 2") + '''
  <h2 class="r" style="--i:0;font-size:44px;margin-bottom:16px">Понятия, которыми пользовались</h2>
  <div class="gl">'''
  + "".join('<div class="gi r" style="--i:%d"><dt>%s</dt><dd>%s</dd></div>' % (1 + i, t, b)
            for i, (t, b) in enumerate(TERMS))
  + '</div>'))

# ── сборка ───────────────────────────────────────────────────────────────
out = []
for title, cls, b in S:
    out.append('<section class="%s" data-t="%s">%s</section>' % (("s " + cls).strip(), title, b))
pathlib.Path(__file__).resolve().parent.joinpath("slides.html").write_text("".join(out), encoding="utf-8")
print("слайдов:", len(S))
