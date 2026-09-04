#!/usr/bin/env python3
"""Генерирует src/slides.html.

Логотипы описаны данными, а не разметкой: плиток много и руками они разъезжаются.
Правится этот файл, затем `python3 src/make_slides.py && python3 src/build.py`.
"""
import pathlib, json
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


FUNNEL = ('<div class="fn"><div class="cap">ЭТАЖИ 01–07</div><div class="cone">'
          + "".join('<i style="top:%.2f%%"></i>' % (b*100/7.0) for b in range(1,7))
          + '</div><div class="neck"><b>08</b><s>ВИТРИНА</s></div>'
            '<div class="arw"></div><div class="out">ИГРОК</div></div>')

GATES = ["steam", "playstation", "xbox", "nintendoswitch", "appstore", "googleplay"]
OUTS  = ["virtuos", "room8", "keywords", "jali", "wolf3d"]

S = []
import math

# ── 01 обложка ───────────────────────────────────────────────────────────
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

# ── 02 что такое геймдев ─────────────────────────────────────────────────
S.append(('Что такое геймдев', '', top("Определение") + '''
  <h2 class="r" style="--i:0">Геймдев — отрасль, которая делает игры<br>и доводит их до игрока</h2>
  <div class="cards r" style="--i:1;grid-template-columns:1.5fr 1fr">
    <div class="card mid">''' + ui("play") + '''
      <p style="font-size:25px;line-height:1.42;color:var(--ink);max-width:none">Программные интерактивные системы, в которых пользователь <b>добровольно действует в рамках искусственных правил</b>, а система непрерывно отвечает на его действия, — с доведением продукта и его поддержки до аудитории <b>через цифровые площадки дистрибуции</b>.</p></div>
    <div class="card dark mid">''' + ui("no") + '''
      <h4>Не геймдев</h4>
      <p>Веб-дизайн, тренажёры и обучающие симуляторы, классические приложения, розничная продажа игр, настольные игры.</p></div>
  </div>'''))

# ── 03 объект конкуренции ────────────────────────────────────────────────
S.append(('Объект конкуренции', '', top("Понятие") + '''
  <h2 class="r" style="--i:0">Объект конкуренции — то,<br>обладание которым даёт преимущество</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card">''' + ui("key") + '''
      <h4>Право, стандарт,<br>опыт, внимание</h4>
      <p>Это можно удерживать. А пока удерживаешь — другим сюда хода нет.</p></div>
    <div class="card sage">''' + ui("nomoney") + '''
      <h4>Но не деньги<br>и не доля рынка</h4>
      <p>Это ресурс на входе и следствие на выходе. За них не дерутся — их получают.</p></div>
    <div class="card dark">''' + ui("compare") + '''
      <h4>Проверка: сравни<br>с этажом выше</h4>
      <p>Объект тот же — значит, это один уровень, а не два.</p></div>
  </div>'''))

# ── 04 раздел 01 ─────────────────────────────────────────────────────────
S.append(('Раздел 01 — карта', 'dark sec', '<div class="huge">01</div>' + top("Раздел 01") + '''
  <h1 class="r" style="--i:0">Карта<br>уровней</h1>
  <p class="note r" style="--i:1">Восемь этажей, на каждом свой объект конкуренции.</p>'''))

# ── 05 карта ─────────────────────────────────────────────────────────────
S.append(('Карта уровней', '', top("Схема · разметка карты") + '''
  <div class="maphead"><span></span><span>Уровень</span><span>Объект конкуренции</span><span>Кто стоит</span></div>
  <div class="map">'''
  + row("01", "Интеллектуальная<br>собственность", "Право делать этот мир и этих героев", ["nintendo", "sega", "cdprojekt"], "")
  + row("02", "Концепт", "Снижение риска до вложений", ["valve", "rockstargames"], "")
  + row("03", "Движки<br>и инструменты", "Производственный стандарт", ["unrealengine", "unity", "godotengine"], "")
  + row("04", "Компоненты<br>и аутсорс", "Опыт, обменянный на срок и цену", ["virtuos", "room8", "keywords", "jali"], "")
  + row("05", "Разработка", "Игровой опыт", ["cdprojekt", "rockstargames", "riotgames", "valve"], "")
  + row("06", "Издание<br>и маркетинг", "Права на издание и релиз", ["sony", "ubisoft", "ea", "squareenix"], "")
  + row("07", "Платформы<br>и железо", "Доступность", ["playstation", "xbox", "nintendoswitch", "apple", "android"], "")
  + row("08", "Витрины<br>и дистрибуция", "Внимание и привычка игрока", GATES, "", neck=True)
  + '</div>'))

# ── 06 этаж 01 ───────────────────────────────────────────────────────────
S.append(('01 · Интеллектуальная собственность', '', top("Этаж 01 · интеллектуальная собственность") + '''
  <h2 class="r" style="--i:0">Мир и героев нельзя сделать<br>без права на них</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card">''' + brand("nintendo") + '''
      <h4>Если ты не Nintendo —<br>не сделаешь Mario</h4>
      <p>Право исключительное: у одного есть, у остальных нет. Mario 1985 года всё ещё закрывает этаж.</p></div>
    <div class="card">''' + ui("key") + '''
      <h4>Барьер не денежный,<br>а юридический</h4>
      <p>Купить нельзя, если владелец не продаёт. И живёт это право десятилетиями.</p></div>
    <div class="card sage">''' + brand("cdprojekt") + '''
      <h4>Cyberpunk начинается здесь</h4>
      <p>CD&nbsp;Projekt не придумала Найт-Сити — взяла права у Майка Пондсмита.</p></div>
  </div>
  <p class="note after r" style="--i:2">Но горлышком этаж не является: зависят <b>не все</b>. Свою ИС можно создать с нуля — так появились Half-Life и Minecraft.</p>'''))

# ── 07 этаж 02 ───────────────────────────────────────────────────────────
S.append(('02 · Концепт', '', top("Этаж 02 · концепт · новый уровень") + '''
  <h2 class="r" style="--i:0">Идею не продают. Продают<br>снижение риска вокруг неё</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card">''' + ui("doc") + '''
      <h4>Что такое концепт</h4>
      <p>Документ, по которому считают бюджет и сроки. «Хотим RPG про киберпанк» — это ещё не он.</p></div>
    <div class="card">''' + ui("shield") + '''
      <h4>За что платят</h4>
      <p>За то, чтобы не потратить три года впустую. Аналитика, креативная дирекция, проверка концепта.</p></div>
    <div class="card dark">''' + ui("layers") + '''
      <h4>Пондсмит стоит<br>на двух этажах</h4>
      <p>Владелец прав и внешний носитель концепта: он в титрах Cyberpunk в дизайн-документах и сюжете.</p></div>
  </div>
  <p class="note after r" style="--i:2">Один участник закрывает два этажа сразу — это и доказывает, что этажи не шаги пайплайна.</p>'''))

# ── 08 этаж 03 ───────────────────────────────────────────────────────────
S.append(('03 · Движки и инструменты', '', top("Этаж 03 · движки и инструменты") + '''
  <h2 class="r" style="--i:0">Движок выбирают один раз —<br>и живут в нём годами</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card"><div class="logos">''' + ico("unrealengine") + ico("unity") + ico("godotengine") + '''</div>
      <h4>Два движка — у 72% студий</h4>
      <p>Unreal — 42%, Unity — 30% по опросу GDC 2026. Godot — 8–10% релизов в Steam.</p></div>
    <div class="card sage">''' + ui("layers") + '''
      <h4>Стандарт, а не фишка</h4>
      <p>Под движок нанимают людей, строят пайплайн, покупают ассеты. Сменить — значит переучить студию.</p></div>
    <div class="card dark"><div class="logos">''' + ico("rockstargames") + ico("valve") + '''</div>
      <h4>Свой движок — своя изоляция</h4>
      <p>RAGE у Rockstar, Source у Valve. Закрытость ценой выбора подрядчиков.</p></div>
  </div>
  <p class="note after r" style="--i:2">Заменяем: Valve ушла с Quake и собрала GoldSrc. Больно, но можно — значит, не горлышко.</p>'''))

# ── 09 этаж 04 ───────────────────────────────────────────────────────────
S.append(('04 · Компоненты и аутсорс', '', top("Этаж 04 · компоненты и аутсорс") + '''
  <h2 class="r" style="--i:0">Аутсорс продаёт опыт:<br>опыт → качество → цена → срок</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card"><div class="logos" style="display:grid;grid-template-columns:repeat(3,auto);justify-content:start;gap:16px 26px">''' + "".join(ico(x) for x in OUTS) + '''</div>
      <h4>Сотни студий с узким профилем</h4>
      <p>Virtuos и Keywords — производство, Room&nbsp;8 — арт, JALI — лицевая анимация. Каждый продаёт своё.</p></div>
    <div class="card sage">''' + ui("compare") + '''
      <h4>Отбор формальный</h4>
      <p>Титры похожих игр, фильтр по профилю, арт-тест, пилот на реальном контенте — и только потом контракт.</p></div>
    <div class="card dark">''' + brand("rockstargames") + '''
      <h4>Контрмодель: Rockstar</h4>
      <p>Свои студии и свой движок. Внешнего арт-аутсорса почти нет — ценой закрытости.</p></div>
  </div>
  <p class="note after r" style="--i:2">Cyberpunk собран из компонентов внешних команд: механики, анимация, звук, QA — всё разными студиями.</p>'''))

# ── 10 этаж 05 ───────────────────────────────────────────────────────────
S.append(('05 · Разработка', '', top("Этаж 05 · разработка") + '''
  <h2 class="r" style="--i:0">Разработчик дерётся за то,<br>что игрок почувствует</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card"><div class="logos">''' + ico("cdprojekt") + ico("rockstargames") + ico("riotgames") + ico("valve") + '''</div>
      <h4>Кто делает саму игру</h4>
      <p>CD&nbsp;Projekt&nbsp;RED, Rockstar&nbsp;North, Riot, Valve, Insomniac. Самый населённый этаж — тысячи студий.</p></div>
    <div class="card sage">''' + ui("eye") + '''
      <h4>Игровой опыт,<br>а не «уникальный»</h4>
      <p>Watch&nbsp;Dogs и GTA качественно разные, но ни одна не уникальнее другой. Оценка лишняя.</p></div>
    <div class="card dark">''' + ui("layers") + '''
      <h4>Заменяем</h4>
      <p>Студий много, профили пересекаются. Игра переживает смену разработчика — Risk&nbsp;of&nbsp;Rain пережила.</p></div>
  </div>
  <p class="note after r" style="--i:2">Издатель и холдинг здесь не стоят — у них другой объект. Об этом следующий слайд.</p>'''))

# ── 11 этаж 06 ───────────────────────────────────────────────────────────
S.append(('06 · Издание', '', top("Этаж 06 · издание и маркетинг") + '''
  <h2 class="r" style="--i:0">Sony не делала «Человека-паука»</h2>
  <p class="lede mut r" style="--i:1;margin-top:16px;max-width:82ch">Игру сделала Insomniac&nbsp;Games — тогда независимая студия. Sony была только издателем и купила её лишь через год, в 2019-м, за $229&nbsp;млн.</p>
  <div class="cards c3 r" style="--i:2;margin-top:26px">
    <div class="card"><div class="kn">Издатель</div>
      <div class="logos">''' + ico("sony") + ico("ubisoft") + ico("ea") + ico("squareenix") + '''</div>
      <h4>Права на издание и релиз</h4>
      <p>Берёт игру и выводит её на рынок. Про ощущения игрока — вообще не он.</p></div>
    <div class="card sage"><div class="kn">Холдинг</div>''' + ui("layers") + '''
      <h4>Доли в тех, кто делает</h4>
      <p>Tencent взяла 93% Riot в 2011-м и весь остаток к 2015-му. Игр не делает сама.</p></div>
    <div class="card dark"><div class="kn">Ошибка старой карты</div>''' + ui("compare") + '''
      <h4>Издатель ≠ разработчик ≠ холдинг</h4>
      <p>Tencent и Sony стояли на «разработке». Три роли, три разных объекта конкуренции.</p></div>
  </div>'''))

# ── 12 этаж 07 ───────────────────────────────────────────────────────────
S.append(('07 · Платформы и железо', '', top("Этаж 07 · платформы и железо · новый уровень") + '''
  <h2 class="r" style="--i:0">Платформа даёт возможность запустить —<br>и отсекает тех, у кого её нет</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card"><div class="logos">''' + ico("playstation") + ico("xbox") + ico("nintendoswitch") + '''</div>
      <h4>Консоли</h4>
      <p>Закрытые экосистемы со своими правилами и сертификацией.</p></div>
    <div class="card sage"><div class="logos">''' + ico("apple") + ico("android") + '''</div>
      <h4>Мобайл</h4>
      <p>Самая большая аудитория — и свои ворота у каждой системы.</p></div>
    <div class="card dark">''' + ui("gate") + '''
      <h4>PC</h4>
      <p>Открытая платформа: Windows, Mac, Linux. Вышел на Windows и не вышел на Mac — потерял пару процентов.</p></div>
  </div>
  <p class="note after r" style="--i:2">Игра только под мобайл и игра везде — разная конкурентоспособность. Но платформы — данность: их не выбирают, под них делают.</p>'''))

# ── 13 этаж 08 ───────────────────────────────────────────────────────────
S.append(('08 · Витрины и дистрибуция', '', top("Этаж 08 · витрины и дистрибуция") + '''
  <h2 class="r" style="--i:0">Витрина решает,<br>существует ли игра для игрока</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card"><div class="logos">''' + "".join(ico(x) for x in GATES) + '''</div>
      <h4>Несколько крупных витрин</h4>
      <p>Steam, PlayStation&nbsp;Store, Xbox, eShop, App&nbsp;Store, Google&nbsp;Play — через них проходит почти весь рынок.</p></div>
    <div class="card sage">''' + ui("eye") + '''
      <h4>Внимание и привычка</h4>
      <p>Купленная библиотека не переносится. Игрок не уходит с витрины, даже если ему дают игры бесплатно.</p></div>
    <div class="card hot">''' + ui("gate") + '''
      <h4>Здесь горлышко</h4>
      <p>Почему именно здесь — разберём во втором разделе.</p></div>
  </div>'''))

# ── 14 стена: мало игроков ≠ горлышко ────────────────────────────────────
def grp(cap, tiles, cols, hot=False):
    return ('<div class="wallgrp%s"><div class="cap">%s</div><div class="grid" '
            'style="grid-template-columns:repeat(%d,1fr)">%s</div></div>'
            % (" hot" if hot else "", cap, cols, "".join(tiles)))

S.append(('Мало игроков — ещё не горлышко', '', top("Кто стоит на карте") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Мало игроков — ещё не горлышко.<br>Горлышко — когда их мало и заменить нельзя</h2>
  <div class="wall r" style="--i:1;grid-template-rows:repeat(2,1fr);grid-template-columns:1fr 1fr">'''
  + grp("03 · Движки · <b>два</b> у 72% студий · <em>заменяемы</em>",
        [tile("unrealengine"), tile("unity"), tile("godotengine"), tile("valve", name="Valve · Source")], 4)
  + grp("05 · Разработка · <b>тысячи</b> студий · <em>заменяемы</em>",
        [tile("cdprojekt"), tile("rockstargames"), tile("riotgames"), tile("valve")], 4)
  + grp("06 · Издание · <b>десятки</b> · <em>заменяемы, но дорого</em>",
        [tile("sony"), tile("ubisoft"), tile("ea"), tile("squareenix")], 4)
  + grp("08 · Витрины · <b>единицы</b> крупных · <em>не заменяемы</em>",
        [tile(g, mark=True) for g in GATES], 6, hot=True)
  + '''</div>
  <p class="note after r" style="--i:2">Движков тоже мало — но с Quake можно уйти на GoldSrc. С витрины уйти некуда: без неё игры для игрока нет.</p>'''))

# ── 15 соседние этажи ────────────────────────────────────────────────────
S.append(('Соседние этажи не совпадают', '', top("Проверка · объекты различаются") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Соседние этажи легко склеить.<br>Вот чем они не совпадают</h2>
  <div style="display:flex;flex-direction:column;gap:16px;flex:1;min-height:0">
    <div class="vs r" style="--i:1">
      <div class="side"><div class="lb">03 · Движки</div><div class="tx">Продают <em>стандарт</em>: выбрал один раз — живёшь в нём годами</div></div>
      <div class="mid">≠</div>
      <div class="side" style="padding-left:26px"><div class="lb">04 · Аутсорс</div><div class="tx">Продают <em>срок</em>: торгуешься заново на каждом контракте</div></div>
    </div>
    <div class="vs r" style="--i:2">
      <div class="side"><div class="lb">05 · Разработка</div><div class="tx">Дерётся за <em>игровой опыт</em> — за то, что игрок почувствует</div></div>
      <div class="mid">≠</div>
      <div class="side" style="padding-left:26px"><div class="lb">06 · Издание</div><div class="tx">Дерётся за <em>права на издание</em>, а не за ощущения</div></div>
    </div>
    <div class="vs r" style="--i:3">
      <div class="side"><div class="lb">07 · Платформа</div><div class="tx">Даёт <em>возможность запустить</em> — железо и API</div></div>
      <div class="mid">≠</div>
      <div class="side" style="padding-left:26px"><div class="lb">08 · Витрина</div><div class="tx">Даёт <em>попадание в поле зрения</em> — без неё игры для игрока нет</div></div>
    </div>
  </div>'''))

# ── 16 раздел 02 ─────────────────────────────────────────────────────────
S.append(('Раздел 02 — горлышко', 'dark sec', '<div class="huge">02</div>' + top("Раздел 02") + '''
  <h1 class="r" style="--i:0">Бутылочное<br>горлышко</h1>
  <p class="note r" style="--i:1">Ищем его тестом отказом, а не по деньгам на этаже.</p>'''))

# ── 17 понятие горлышка ──────────────────────────────────────────────────
S.append(('Понятие горлышка', '', top("Понятие · бутылочное горлышко") + '''
  <h2 class="r" style="--i:0">Уровень, где мало игроков,<br>а зависят от них все</h2>
  <div class="cards r" style="--i:1;grid-template-columns:1.5fr 1fr;margin-top:24px">
    <div class="col">
      <div class="card"><div class="kn">Признак 1</div>
        <h4>Мало игроков</h4>
        <p>Считаем тех, к кому реально можно пойти. Сотня студий — много, несколько витрин — мало.</p></div>
      <div class="card"><div class="kn">Признак 2</div>
        <h4>Нет альтернативы</h4>
        <p>Можно заменить — больно, дорого, но можно — это не горлышко.</p></div>
      <div class="card hot"><div class="kn" style="color:rgba(22,20,15,.72)">Что удерживает</div>
        <h4>Барьер входа</h4>
        <p>Не деньги, а то, что деньгами не покупается: сетевой эффект и привычка.</p></div>
    </div>
    <div class="card" style="padding:24px">''' + FUNNEL + '''</div>
  </div>'''))

# ── 18 тест отказом ──────────────────────────────────────────────────────
CH = [
    ("Откажет движок", "Берёшь другой. Valve так и сделала: ушла с Quake и собрала GoldSrc.", "Альтернатива есть", False),
    ("Откажет подрядчик", "Меняешь. Рынок аутсорса — около $9&nbsp;млрд и сотни студий.", "Альтернатива есть", False),
    ("Откажет издатель", "Ищешь другого или идёшь без него. Игрок этого даже не заметит.", "Есть, но дорогая", False),
    ("Откажет витрина", "Игры не существует. Игрок физически не может её найти и купить.", "Альтернативы нет", True),
]
S.append(('Тест отказом', '', top("Цепочка зависимостей · тест отказом") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Что будет с цепочкой,<br>если этот уровень откажет</h2>
  <div class="chain">'''
  + "".join('<div class="ch%s r" style="--i:%d"><h4>%s</h4><p>%s</p><div class="verd">%s</div></div>'
            % (" dead" if d else "", 1 + i, t, b, v) for i, (t, b, v, d) in enumerate(CH))
  + '''</div>
  <p class="note after r" style="--i:6">Три уровня из четырёх заменяемы. Жёсткая зависимость ровно одна.</p>'''))

# ── 19 витрина как класс ─────────────────────────────────────────────────
S.append(('Горлышко — витрина как класс', 'dark', top("Горлышко · обоснование") + '''
  <h2 class="r" style="--i:0">Горлышко — не Steam.<br>Горлышко — <span style="color:var(--flame)">витрина как класс</span></h2>
  <div class="figs r" style="--i:1;margin-top:38px">
    <div class="fig"><div class="n">75%</div><div class="l">выручки PC-дистрибуции у Steam — это лишь PC-проекция горлышка</div></div>
    <div class="fig"><div class="n">2–3%</div><div class="l">у GOG — третьей витрины PC. Всё, что не Steam и не Epic, — крошки</div></div>
    <div class="fig"><div class="n">8–10%</div><div class="l">у Epic, который раздаёт игры бесплатно не первый год</div></div>
  </div>
  <div class="cards c2 r" style="--i:2;margin-top:40px">
    <div class="card dark mid" style="background:rgba(241,236,227,.08)">
      <h4>Что мешает войти</h4>
      <p>Купленная библиотека не переносится. Уйти — значит бросить всё, за что заплачено.</p></div>
    <div class="card dark mid" style="background:rgba(241,236,227,.08)">
      <h4>Честный контраргумент</h4>
      <p>Steam — только PC. Поэтому горлышко не компания, а <b>уровень</b>: в каждой экосистеме своя витрина.</p></div>
  </div>'''))

# ── 20 три кейса ─────────────────────────────────────────────────────────
CASES = [
    ("playstation", "Cyberpunk 2077", "6 месяцев вне PS Store",
     "Sony убрала игру 18 декабря 2020-го и вернула деньги всем. Вернулась 21 июня 2021-го.",
     "Акции CD&nbsp;Projekt — минус 20% за день"),
    ("apple", "Fortnite", "почти 5 лет вне App Store",
     "Apple удалила игру в августе 2020-го. Вернулась в американский App&nbsp;Store в мае 2025-го.",
     "Пять лет игры не существовало для iOS"),
    ("vk", "Atomic Heart", "только VK Play в РФ и СНГ",
     "На релизе в феврале 2023-го страница в Steam была недоступна в регионе.",
     "Больше трёх лет без Steam в России"),
]
S.append(('Когда витрина выключила игру', '', top("Горлышко · проверенные случаи") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Три раза, когда витрина просто<br>выключила готовую игру</h2>
  <div class="cards c3 r" style="--i:1">'''
  + "".join('<div class="card"><div class="badge">%s</div>'
            '<h4>%s</h4><div class="kn" style="margin:-6px 0 14px">%s</div>'
            '<p>%s</p><p style="margin-top:auto;padding-top:16px;color:var(--ink);font-weight:700">%s</p></div>'
            % (ico(s), t, sub, b, k) for s, t, sub, b, k in CASES)
  + '''</div>
  <p class="note after r" style="--i:2">Игра была готова и куплена. Отказал <b style="color:var(--flame-ink)">только уровень витрины</b> — и этого хватило.</p>'''))

# ── 21 скрытые горлышки ──────────────────────────────────────────────────
S.append(('Скрытые горлышки', '', top("Скрытые горлышки") + '''
  <h2 class="r" style="--i:0">Горлышко не обязано стоять там,<br>где много выручки</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card">''' + ui("shield") + '''
      <h4>Сертификация<br>и возрастной рейтинг</h4>
      <p>Не прошёл ESRB или PEGI — на консоль не вышел. Обойти нельзя.</p></div>
    <div class="card">''' + ui("no") + '''
      <h4>Нет издателя —<br>нет игры</h4>
      <p>Команда сильная, права есть, а издателя нет. Для инди горлышко — шестой этаж, а не восьмой.</p></div>
    <div class="card">''' + ui("clock") + '''
      <h4>Мощности подрядчиков</h4>
      <p>Cyberpunk сорвал не аутсорс, а скоуп и старые консоли. Но конвейер студий — признак нехватки.</p></div>
  </div>
  <p class="note after r" style="--i:2">Горлышко ищется не по выручке этажа, а по отсутствию альтернативы у тех, кто зависит.</p>'''))

# ── 22 открытый вопрос ───────────────────────────────────────────────────
S.append(('Открытый вопрос', 'hot', top("Открытый вопрос · выносим в зал") + '''
  <h2 class="r" style="--i:0;font-size:80px;font-weight:900;letter-spacing:-.038em;line-height:1.0">Где граница рынка —<br>там и горлышко</h2>
  <div class="cards c3 r" style="--i:1;margin-top:44px">
    <div class="card"><div class="kn">Рынок = PC</div>
      <h4>Горлышко — Steam</h4>
      <p>75% выручки, альтернатив практически нет.</p></div>
    <div class="card"><div class="kn">Рынок = гейминг целиком</div>
      <h4>Горлышек несколько</h4>
      <p>По одному на экосистему — и каждое монополист в своей.</p></div>
    <div class="card dark"><div class="kn">Чего мы не решили</div>
      <h4>Витрины — один этаж или три?</h4>
      <p>Не склеили ли мы три разных рынка с одинаковым последним шагом?</p></div>
  </div>'''))

# ── источники ────────────────────────────────────────────────────────────
S.append(('Источники', '', top("Источники всех чисел") + '''
  <h2 class="r" style="--i:0;margin-bottom:20px">Откуда взяты числа</h2>
  <div class="srcwrap r" style="--i:1"><table class="src">
    <thead><tr><th>Число</th><th>Где в деке</th><th>Источник</th></tr></thead>
    <tbody><tr><td class="c1">Unreal 42%, Unity 30% — основной движок студий</td><td class="c2">этаж 03, карта</td><td class="c3"><a href="https://shattered.io/unreal-engine-6-unity-market-share-2026" target="_blank" rel="noopener">shattered.io</a> <span class="x">· опрос GDC 2026</span></td></tr><tr><td class="c1">Godot 8–10% релизов в Steam</td><td class="c2">этаж 03</td><td class="c3"><a href="https://shattered.io/unreal-engine-6-unity-market-share-2026" target="_blank" rel="noopener">shattered.io</a> <span class="x">· Q1 2026</span></td></tr><tr><td class="c1">Steam 74–75% PC-дистрибуции; Epic 8–10%; GOG 2–3%</td><td class="c2">горлышко</td><td class="c3"><a href="https://levvvel.com/statistics/pc-gaming" target="_blank" rel="noopener">levvvel.com</a> <span class="x">· 2025</span></td></tr><tr><td class="c1">Аутсорс ≈ $9 млрд, 2025</td><td class="c2">тест отказом</td><td class="c3"><a href="https://www.verifiedmarketreports.com/product/game-outsourcing-service-market/" target="_blank" rel="noopener">verifiedmarketreports.com</a> <span class="x">· оценки других отчётов: $4–9 млрд</span></td></tr><tr><td class="c1">Sony купила Insomniac за $229 млн, август 2019</td><td class="c2">этаж 06</td><td class="c3"><a href="https://gameworldobserver.com/2020/02/11/sony-paid-229m-insomniac-games" target="_blank" rel="noopener">gameworldobserver.com</a> <span class="x">· по отчётности Sony</span></td></tr><tr><td class="c1">Tencent: 93% Riot в 2011, 100% к концу 2015</td><td class="c2">этаж 06</td><td class="c3"><a href="https://techcrunch.com/2015/12/16/tencent-takes-full-control-of-league-of-legends-creator-riot-games/" target="_blank" rel="noopener">techcrunch.com</a></td></tr><tr><td class="c1">Cyberpunk вне PS Store 18.12.2020 — 21.06.2021; акции CD Projekt −20%</td><td class="c2">кейсы</td><td class="c3"><a href="https://www.cnbc.com/2020/12/18/sony-pulls-cyberpunk-2077-from-playstation-store-after-backlash.html" target="_blank" rel="noopener">cnbc.com</a> <span class="x">· возврат: engadget.com</span></td></tr><tr><td class="c1">Fortnite вне App Store: август 2020 — май 2025</td><td class="c2">кейсы</td><td class="c3"><a href="https://www.cnbc.com/2025/05/20/apple-fortnite-app-store-epic-games.html" target="_blank" rel="noopener">cnbc.com</a></td></tr><tr><td class="c1">Atomic Heart только в VK Play с 21.02.2023; в Steam РФ — 08.2026</td><td class="c2">кейсы</td><td class="c3"><a href="https://habr.com/ru/news/687214/" target="_blank" rel="noopener">habr.com · 4pda.to</a> <span class="x">· 4pda.to/2026/08/04/459645</span></td></tr><tr><td class="c1">Super Mario Bros. — 1985</td><td class="c2">этаж 01</td><td class="c3"><a href="https://www.nintendo.com/us/store/products/super-mario-bros-nes-nintendo-switch-online/" target="_blank" rel="noopener">nintendo.com</a></td></tr></tbody></table></div>
  <p class="note after r" style="--i:2">Даты и суммы по Cyberpunk, Fortnite, Atomic Heart и Insomniac сверены по двум независимым публикациям каждая.</p>'''))

# ── понятия ───────────────────────────────────────────────────────────
GL = [
    ("Конкуренция", "Борьба за то, чего на всех не хватает. Всегда за что-то конкретное."),
    ("Барьер входа", "Что мешает новому игроку занять уровень. Чем выше — тем дольше держится горлышко."),
    ("Объект конкуренции", "То, обладание которым даёт преимущество. На каждом этаже свой."),
    ("Зависимость в цепочке", "Насколько жёстко уровень нуждается в соседнем. Меряется отказом."),
    ("Бутылочное горлышко", "Уровень, где мало игроков, а зависят от них все."),
    ("Уровень", "Место, где есть свой объект конкуренции. Не шаг процесса."),
]
S.append(('Понятия такта 2', '', top("Понятия такта 2") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Понятия, которыми пользовались</h2>
  <div class="gl">'''
  + "".join('<div class="gi r" style="--i:%d"><dt>%s</dt><dd>%s</dd></div>' % (1 + i, t, b)
            for i, (t, b) in enumerate(GL))
  + '</div>'))


# ── сборка ───────────────────────────────────────────────────────────────
out = []
for title, cls, body in S:
    c = ("s " + cls).strip()
    out.append('<section class="%s" data-t="%s">%s</section>' % (c, title, body))
html = "".join(out)
pathlib.Path(__file__).resolve().parent.joinpath("slides.html").write_text(html, encoding="utf-8")
print("слайдов:", len(S))
