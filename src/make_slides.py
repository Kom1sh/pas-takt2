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
 "layers":'<path d="M12 3 2.5 8 12 13l9.5-5z"/><path d="M2.5 12.5 12 17.5l9.5-5"/><path d="M2.5 17 12 22l9.5-5"/>',
 "link":  '<path d="M10 14a4.5 4.5 0 0 0 6.4 0l2.6-2.6a4.5 4.5 0 0 0-6.4-6.4L11.2 6.4"/><path d="M14 10a4.5 4.5 0 0 0-6.4 0L5 12.6a4.5 4.5 0 0 0 6.4 6.4l1.4-1.4"/>',
 "shield":'<path d="M12 2.5 4 6v6c0 5 3.4 8.4 8 9.5 4.6-1.1 8-4.5 8-9.5V6z"/><path d="M9 12l2 2 4-4"/>',
 "eye":   '<path d="M1.5 12S5.5 5 12 5s10.5 7 10.5 7-4 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
 "funnel": '<path d="M2.5 4.5h19l-7.4 8.6V21l-4.2-2.6v-5.3z"/>',
 "unlock": '<rect x="4" y="10.5" width="16" height="10.5" rx="2"/><path d="M8 10.5V7a4 4 0 0 1 7.6-1.7"/>',
 "pen": '<path d="M4 20l3.2-.7L20 6.5a2.1 2.1 0 0 0-3-3L4.2 16.3z"/><path d="M15.5 5.5l3 3"/><path d="M4 20l.9-4"/>',
 "percent": '<path d="M19.5 4.5 4.5 19.5"/><circle cx="7.8" cy="7.8" r="2.9"/><circle cx="16.2" cy="16.2" r="2.9"/>',
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
                     PIPELINE, PIPELINE_ICONS, PIPELINE_NOTE, PIPELINE_ACCENT, MEASURE_FIGS, MEASURE_CARDS,
                     MULTI, MULTI_NOTE, MULTI_SUB, FAILTEST, CASES, TERMS, SOURCES,
                     SOURCES_NOTE, GATES, OUTS,
                     TRENDS_15, REGULATORS, REGULATORS_NOTE, MAP_15, SIT15_TITLE, SIT15_NOTE,
                     MAP_2, SIT2_TITLE, SIT2_NOTE, TRANSITION, TRANSITION_NOTE, POWER, POWER_TITLE,
                     TERMS_T3, SOURCES_T3)

FUNNEL = ('<div class="fn"><div class="cap">ЭТАЖИ 01–07</div><div class="cone">'
          + "".join('<i style="top:%.2f%%"></i>' % (b * 100 / 7.0) for b in range(1, 7))
          + '</div><div class="neck"><b>08</b><s>ВИТРИНА</s></div>'
            '<div class="arw"></div><div class="out">ИГРОК</div></div>')

def nl(t): return t.replace("\n", "<br>")

def anchor(icon, logos, kn):
    inner = ""
    if logos:
        cls = "logos solo" if len(logos) == 1 else "logos"
        inner += '<div class="%s">' % cls + "".join(ico(x) for x in logos) + "</div>"
    if icon: inner += ui(icon)
    if kn: inner += '<div class="kn">%s</div>' % kn
    return '<div class="anchor">%s</div>' % inner if inner else ""

def card(kind, kn, title, body, icon=None, logos=None):
    return '<div class="card %s">%s<h4>%s</h4><p>%s</p></div>' % (kind, anchor(icon, logos, kn), nl(title), body)

def maprow(no, nm, oj, logos, state=None, tag="", i=0):
    cls = "lvl" + (" " + state if state else "")
    tagh = '<span class="tag">%s</span>' % tag if tag else ""
    return ('<div class="%s r" style="--i:%d"><span class="no">%s</span><span class="nm">%s</span>'
            '<span class="oj">%s%s</span><span class="who">%s</span></div>'
            % (cls, i, no, nl(nm), oj, tagh, "".join(ico(x) for x in logos)))

def mapslide(title_html, rows, note, legend=None):
    h = '<div class="maphead"><span></span><span>Уровень</span><span>Объект конкуренции</span><span>Кто стоит</span></div>'
    body = "".join(maprow(no, nm, oj, lg, st, tg, 2 + k) for k, (no, nm, oj, lg, st, tg) in enumerate(rows))
    leg = ('<div class="maplegend r" style="--i:1">%s</div>' % "".join(
        '<span><i style="%s"></i>%s</span>' % (st, lab) for st, lab in legend)) if legend else ""
    tailn = '<p class="note after r" style="--i:12">%s</p>' % note if note else ""
    return title_html + leg + h + '<div class="map%s">' % (' dyn' if legend else '') + body + '</div>' + tailn

S = []
rays = ('<svg class="rays" viewBox="0 0 200 200" fill="none" stroke="rgba(22,20,15,.34)" stroke-width=".7">'
        + "".join('<line x1="100" y1="100" x2="%.1f" y2="%.1f"/>'
                  % (100 + 150 * math.cos(a * math.pi / 24), 100 + 150 * math.sin(a * math.pi / 24)) for a in range(48))
        + '<circle cx="100" cy="100" r="46" stroke="rgba(22,20,15,.4)"/><circle cx="100" cy="100" r="72" stroke="rgba(22,20,15,.22)"/></svg>')

S.append(('Геймдев · финальный пленар', 'hot cover', rays + top("ПАС · ИТ-1 · 3 курс · финальный пленар") + '''
  <h1 class="r" style="--i:0">Геймдев</h1>
  <div class="sub r" style="--i:1">Карта уровней конкуренции:<br>сейчас, Ситуация 1.5 и Ситуация 2</div>
  <div class="meta-b r" style="--i:2"><span>Разбираем на Cyberpunk 2077 и CD Projekt</span><span>8 этажей · 1 горлышко · 2 сценария</span></div>'''))

S.append(('Границы: что такое геймдев', '', top("Блок 1 · границы отрасли") + '''
  <h2 class="r" style="--i:0">Что такое геймдев</h2>
  <div class="cards r" style="--i:1;grid-template-columns:1.5fr 1fr">
    <div class="card mid"><div class="anchor">''' + ui("play") + '''</div>
      <p style="font-size:25px;line-height:1.42;color:var(--ink);max-width:none">Программные интерактивные системы, в которых пользователь <b>добровольно действует в рамках искусственных правил</b>, а система непрерывно отвечает на его действия, — с доведением продукта и его поддержки до аудитории <b>через цифровые площадки дистрибуции</b>.</p></div>
    ''' + card("dark mid", None, "Не геймдев", "Веб-дизайн, тренажёры и обучающие симуляторы, классические приложения, розничная продажа игр, настольные игры.", "no") + '''
  </div>'''))

S.append(('Понятие: объект конкуренции', '', top("Блок 2 · понятие") + '''
  <h2 class="r" style="--i:0">Объект конкуренции — то,<br>обладание которым даёт преимущество</h2>
  <div class="cards c3 r" style="--i:1">'''
  + card("tile", None, "Право, стандарт,\nопыт, внимание", "Это можно удерживать. А пока удерживаешь — другим сюда хода нет.", "key")
  + card("sage", None, "Но не деньги\nи не доля рынка", "Это ресурс на входе и следствие на выходе. За них не дерутся — их получают.", "nomoney")
  + card("dark", None, "Проверка: сравни\nс этажом выше", "Объект тот же — значит, это один уровень, а не два. Если объект нельзя измерить — мы его не называем.", "compare")
  + '</div>'))

S.append(('Раздел 01 — карта сейчас', 'dark sec', '<div class="huge">01</div>' + top("Раздел 01") + '''
  <h1 class="r" style="--i:0">Карта<br>сейчас</h1>
  <p class="note r" style="--i:1">Вертикаль из восьми уровней и объект конкуренции на каждом.</p>'''))

S.append(('Карта уровней · сейчас', '', top("Блок 1–2 · вертикаль и объекты по этажам") +
  mapslide('', [(no, nm, oj, lg, None, "") for no, nm, oj, lg in MAP], None)))

S.append(('Объекты соседних этажей не совпадают', '', top("Блок 2 · проверка") + '''
  <h2 class="r" style="--i:0;margin-bottom:18px">Объекты соседних этажей<br>не совпадают</h2>
  <div style="display:flex;flex-direction:column;gap:11px;flex:1;min-height:0">'''
  + "".join('<div class="vs r" style="--i:%d"><div class="side"><div class="lb">%s</div><div class="tx">%s</div></div>'
            '<div class="mid">≠</div><div class="side" style="padding-left:22px"><div class="lb">%s</div><div class="tx">%s</div></div></div>'
            % (1 + i, a, at, b, bt) for i, (a, at, b, bt) in enumerate(VS_PAIRS))
  + '</div>'))

S.append(('Раздел 02 — горлышко', 'dark sec', '<div class="huge">02</div>' + top("Раздел 02") + '''
  <h1 class="r" style="--i:0">Горлышко<br>и власть</h1>
  <p class="note r" style="--i:1">Ищем тестом отказом, а не по деньгам на этаже.</p>'''))

S.append(('Понятие горлышка', '', top("Блок 3 · понятие") + '''
  <h2 class="r" style="--i:0">Уровень, где мало игроков,<br>а зависят от них все</h2>
  <div class="cards r" style="--i:1;grid-template-columns:1.5fr 1fr;margin-top:24px">
    <div class="col">'''
  + card("", "Признак 1", "Мало игроков", "Считаем тех, к кому реально можно пойти. Сотня студий — много, несколько витрин — мало.")
  + card("", "Признак 2", "Нет альтернативы", "Можно заменить — больно, дорого, но можно — это не горлышко.")
  + card("hot", "Что удерживает", "Барьер входа", "Не деньги, а то, что деньгами не покупается: накопленная библиотека и привычка.")
  + '''</div>
    <div class="card" style="padding:24px">''' + FUNNEL + '''</div>
  </div>'''))

S.append(('Тест отказом', '', top("Блок 3 · тест отказом") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Что будет с цепочкой,<br>если этот уровень откажет</h2>
  <div class="chain">'''
  + "".join('<div class="ch%s r" style="--i:%d"><h4>%s</h4><p>%s</p><div class="verd">%s</div></div>'
            % (" dead" if d else "", 1 + i, t, b, v) for i, (t, b, v, d) in enumerate(FAILTEST))
  + '''</div>
  <p class="note after r" style="--i:6">Три уровня из четырёх заменяемы. Жёсткая зависимость ровно одна — поэтому власть на восьмом этаже.</p>'''))

S.append(('Горлышко — уровень витрин', 'dark', top("Блок 3 · почему власть там") + '''
  <h2 class="r" style="--i:0">Горлышко — <span style="color:var(--flame)">уровень витрин</span>,<br>а не отдельная компания</h2>
  <div class="figs r" style="--i:1;margin-top:38px">
    <div class="fig"><div class="n">75%</div><div class="l">выручки PC-дистрибуции у Steam — это лишь PC-проекция горлышка</div></div>
    <div class="fig"><div class="n">2–3%</div><div class="l">у GOG — третьей витрины PC. Всё, что не Steam и не Epic, — крошки</div></div>
    <div class="fig"><div class="n">8–10%</div><div class="l">у Epic, который раздаёт игры бесплатно не первый год</div></div>
  </div>
  <div class="cards c2 r" style="--i:2;margin-top:40px">'''
  + card("dark mid", None, "Что мешает войти", "Купленная библиотека не переносится. Уйти — значит бросить всё, за что заплачено.")
  + card("dark mid", None, "Почему уровень, а не компания", "Steam — только PC. В каждой экосистеме своя витрина, и в каждой она монополист. Власть — у уровня.")
  + '</div>'))

S.append(('Три случая отключения игры', '', top("Блок 3 · проверенные случаи") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Три случая отключения<br>игры витриной</h2>
  <div class="cards c3 r" style="--i:1">'''
  + "".join('<div class="card"><div class="anchor"><div class="badge">%s</div><div class="kn">%s</div></div>'
            '<h4>%s</h4><p>%s</p><p style="margin-top:16px;color:var(--ink);font-weight:700">%s</p></div>'
            % (ico(sl), sb, t, b, k) for sl, t, sb, b, k in CASES)
  + '''</div>
  <p class="note after r" style="--i:2">Игра была готова и куплена. Отказал <b style="color:var(--flame-ink)">только уровень витрины</b> — и этого хватило.</p>'''))

S.append(('Раздел 03 — динамика', 'dark sec', '<div class="huge">03</div>' + top("Раздел 03") + '''
  <h1 class="r" style="--i:0">Запускаем<br>время</h1>
  <p class="note r" style="--i:1">Тренды и регуляторы. Две перерисованные карты и механизм перехода между ними.</p>'''))

S.append(('Тренды Ситуации 1.5', '', top("Блок 4 · Ситуация 1.5 · тренды") + '''
  <h2 class="r" style="--i:0">Три тренда, которые действуют<br>на цепочку уже сейчас</h2>
  <div class="cards c3 r" style="--i:1">'''
  + "".join(card("sage" if i == 0 else "tile", ev, t, b, ic) for i, (t, b, ic, ev) in enumerate(TRENDS_15))
  + '''</div>
  <p class="note after r" style="--i:2">Все три идут <b>сверху</b> — от владельцев движков, платформ и издателей, а не от запроса разработчиков.</p>'''))

S.append(('Регуляторы', '', top("Блок 4 · Ситуация 1.5 · регуляторы") + '''
  <h2 class="r" style="--i:0;margin-bottom:20px">Четыре типа регуляторов</h2>
  <div class="cards c4 r" style="--i:1">'''
  + "".join('<div class="card%s"><div class="anchor">%s</div><h4>%s</h4><p>%s</p></div>'
            % (" hot" if i == 3 else "", ui(ic), t, b) for i, (t, b, ic) in enumerate(REGULATORS))
  + '''</div>
  <p class="note after r" style="--i:2">%s</p>''' % REGULATORS_NOTE))

S.append(('Карта · Ситуация 1.5', '', top("Блок 4 · Ситуация 1.5 · карта") +
  mapslide('<h2 class="r" style="--i:0;font-size:36px;margin-bottom:8px">%s</h2>' % nl(SIT15_TITLE), MAP_15, SIT15_NOTE,
           legend=[("background:#F26A1B", "усиливается"), ("background:#D3CCBE", "сокращается"), ("background:#14130F", "горлышко")])))

S.append(('Карта · Ситуация 2', '', top("Блок 5 · Ситуация 2 · карта") +
  mapslide('<h2 class="r" style="--i:0;font-size:36px;margin-bottom:8px">%s</h2>' % nl(SIT2_TITLE), MAP_2, SIT2_NOTE,
           legend=[("background:#F26A1B", "усиливается"), ("background:#FBF9F4;border-left:4px solid #16140F;border-radius:3px", "поглотил соседний этаж"), ("background:#14130F", "горлышко")])))

S.append(('Механизм перехода', '', top("Блок 6 · механизм перехода") + '''
  <h2 class="r" style="--i:0;margin-bottom:14px">За счёт чего карта переходит<br>из 1.5 в 2</h2>
  <div class="pipe r" style="--i:1">'''
  + '<div class="ar"></div>'.join(
      '<div class="st mid%s"><div class="no">%02d</div><h5>%s</h5><p>%s</p></div>'
      % (" last" if i == len(TRANSITION) - 1 else "", i + 1, nl(t), b) for i, (t, b) in enumerate(TRANSITION))
  + '''</div>
  <p class="note after r" style="--i:2">%s</p>''' % TRANSITION_NOTE))

S.append(('Место силы', 'hot', top("Блок 7 · где в индустрии место силы") + ('''
  <h2 class="r" style="--i:0">%s</h2>
  <div class="cards c3 r" style="--i:1">''' % nl(POWER_TITLE))
  + "".join(card(k, kn, t, b, ic) for k, kn, t, b, ic in POWER)
  + '''</div>
  <p class="note after r" style="--i:2">Кто стоит на обоих центрах силы — витрине и движке, — тот и определяет правила для остальных этажей.</p>'''))

ALLSRC = SOURCES_T3 + SOURCES
HALF = len(ALLSRC) // 2 + len(ALLSRC) % 2
def src_col(items):
    return "".join('<div class="srow"><span class="num">%s</span><a class="lnk" href="%s" target="_blank" rel="noopener">%s</a>'
                   '<span class="whr">%s</span></div>' % (n, url, dom, w) for n, w, dom, url in items)
S.append(('Источники', '', top("Источники всех чисел") + ('''
  <h2 class="r" style="--i:0;font-size:42px;margin-bottom:14px">Откуда взяты числа</h2>
  <div class="srcgrid r" style="--i:1">
    <div><div class="hd">Число · где в деке · источник</div>%s</div>
    <div><div class="hd">Число · где в деке · источник</div>%s</div>
  </div>
  <p class="note after r" style="--i:2">%s</p>''' % (src_col(ALLSRC[:HALF]), src_col(ALLSRC[HALF:]), SOURCES_NOTE))))

S.append(('Понятия', '', top("Понятия тактов 2 и 3") + '''
  <h2 class="r" style="--i:0;font-size:42px;margin-bottom:14px">Понятия, которыми пользовались</h2>
  <div class="gl" style="grid-template-columns:1fr 1fr 1fr">'''
  + "".join('<div class="gi r" style="--i:%d"><dt>%s</dt><dd>%s</dd></div>' % (1 + i, t, b) for i, (t, b) in enumerate(TERMS + TERMS_T3))
  + '</div>'))

# ── сборка ───────────────────────────────────────────────────────────────
out = []
for title, cls, b in S:
    out.append('<section class="%s" data-t="%s">%s</section>' % (("s " + cls).strip(), title, b))
pathlib.Path(__file__).resolve().parent.joinpath("slides.html").write_text("".join(out), encoding="utf-8")
print("слайдов:", len(S))
