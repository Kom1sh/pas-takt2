#!/usr/bin/env python3
"""Генерирует src/slides.html.

Логотипы описаны данными, а не разметкой: плиток много и руками они разъезжаются.
Правится этот файл, затем `python3 src/make_slides.py && python3 src/build.py`.
"""
import pathlib

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
}


def ui(name, big=False):
    return ('<div class="badge"><svg class="ui" viewBox="0 0 24 24" aria-hidden="true">%s</svg></div>'
            % UI[name])


def ico(slug, size=None):
    st = 'color:%s' % BRAND.get(slug, INK)
    if size:
        st += ';width:%dpx;height:%dpx' % (size, size)
    return '<svg class="ic" style="%s"><use href="#i-%s"/></svg>' % (st, slug)


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


FUNNEL = '<div class="fn"><div class="cap">ЭТАЖИ 01–07</div><div class="cone"><i style="top:14.29%"></i><i style="top:28.57%"></i><i style="top:42.86%"></i><i style="top:57.14%"></i><i style="top:71.43%"></i><i style="top:85.71%"></i></div><div class="neck"><b>08</b><s>ВИТРИНА</s></div><div class="arw"></div><div class="out">ИГРОК</div></div>'

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

# ── 02 объект конкуренции ────────────────────────────────────────────────
S.append(('Объект конкуренции', '', top("Понятие") + '''
  <h2 class="r" style="--i:0">Объект конкуренции — то,<br>обладание чем даёт преимущество</h2>
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

# ── 03 раздел 01 ─────────────────────────────────────────────────────────
S.append(('Раздел 01 — карта', 'dark sec', '<div class="huge">01</div>' + top("Раздел 01") + '''
  <h1 class="r" style="--i:0">Карта<br>уровней</h1>
  <p class="note r" style="--i:1">Восемь этажей, на каждом свой объект конкуренции.</p>'''))

# ── 04 карта ─────────────────────────────────────────────────────────────
S.append(('Карта уровней', '', top("Схема · разметка карты") + '''
  <div class="maphead"><span></span><span>Уровень</span><span>Объект конкуренции</span><span>Кто стоит</span></div>
  <div class="map">'''
  + row("01", "Интеллектуальная<br>собственность", "Право делать этот мир и этих героев",
        ["nintendo", "sega", "cdprojekt"], "")
  + row("02", "Концепт", "Снижение риска до вложений",
        ["valve", "rockstargames"], "")
  + row("03", "Движки<br>и инструменты", "Производственный стандарт",
        ["unrealengine", "unity", "godotengine"], "")
  + row("04", "Компоненты<br>и аутсорс", "Опыт, обменянный на срок и цену",
        [], "")
  + row("05", "Разработка", "Игровой опыт",
        ["cdprojekt", "rockstargames", "riotgames", "valve"], "")
  + row("06", "Издание<br>и маркетинг", "Деньги и право на релиз",
        ["sony", "ubisoft", "ea", "squareenix"], "")
  + row("07", "Платформы<br>и железо", "Доступность",
        ["playstation", "xbox", "nintendoswitch", "apple", "android"], "")
  + row("08", "Витрины<br>и дистрибуция", "Внимание и привычка игрока",
        ["steam", "epicgames", "gogdotcom", "appstore"], "", neck=True)
  + '</div>'))

# ── 05 этаж 01 ───────────────────────────────────────────────────────────
S.append(('01 · Интеллектуальная собственность', '', top("Этаж 01 · интеллектуальная собственность") + '''
  <h2 class="r" style="--i:0">Если ты не Nintendo,<br>ты не сделаешь Mario</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card">''' + ui("key") + '''
      <h4>Право исключительное</h4>
      <p>У одного есть — у всех остальных нет. Купить нельзя, если владелец не продаёт.</p></div>
    <div class="card">''' + ui("clock") + '''
      <h4>Живёт десятилетиями</h4>
      <p>Mario 1985 года всё ещё закрывает этаж. Барьер входа не денежный, а юридический.</p></div>
    <div class="card sage">
      <div class="logos">''' + ico("cdprojekt", 58) + ico("nintendo", 58) + '''</div>
      <h4>Cyberpunk начинается здесь</h4>
      <p>CD&nbsp;Projekt не придумала Найт-Сити — взяла права у Майка Пондсмита.</p></div>
  </div>
  <p class="note after r" style="--i:2">Но горлышком этаж не является: зависят <b>не все</b>. Свою ИС можно создать с нуля — так появились Half-Life и Minecraft.</p>'''))

# ── 06 этаж 02 ───────────────────────────────────────────────────────────
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

# ── 07 этаж 04 ───────────────────────────────────────────────────────────
S.append(('04 · Компоненты и аутсорс', '', top("Этаж 04 · компоненты и аутсорс") + '''
  <h2 class="r" style="--i:0">Аутсорс продаёт опыт:<br>опыт → качество → цена → срок</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card">''' + ui("compare") + '''
      <h4>Отбор формальный</h4>
      <p>Титры похожих игр, фильтр по узкому профилю, арт-тест, пилот на реальном контенте — и только потом контракт.</p></div>
    <div class="card sage">''' + ui("layers") + '''
      <h4>Отдают артефакты,<br>а не «работу»</h4>
      <p>Cyberpunk собран из компонентов: механики, лицевая анимация, звук, QA — всё разными командами.</p></div>
    <div class="card dark">
      <div class="logos">''' + ico("rockstargames", 58) + '''</div>
      <h4>Контрмодель: Rockstar</h4>
      <p>Свои студии и свой движок RAGE. Внешнего арт-аутсорса почти нет — ценой закрытости.</p></div>
  </div>
  <p class="note after r" style="--i:2">Свой движок сокращает выбор подрядчиков: этаж 03 управляет этажом 04.</p>'''))

# ── 08 этаж 05 ───────────────────────────────────────────────────────────
S.append(('05 · Кто делает игру', '', top("Этаж 05 · разработка · исправление ошибки") + '''
  <h2 class="r" style="--i:0">Sony не делала «Человека-паука»</h2>
  <p class="lede mut r" style="--i:1;margin-top:16px;max-width:82ch">Игру сделала Insomniac&nbsp;Games — тогда независимая студия. Sony была только издателем и купила её лишь через год, в 2019-м, за $229&nbsp;млн.</p>
  <div class="cards c3 r" style="--i:2;margin-top:26px">
    <div class="card"><div class="kn">Разработчик</div>
      <div class="logos">''' + ico("cdprojekt", 50) + ico("rockstargames", 50) + ico("riotgames", 50) + '''</div>
      <h4>Игровой опыт</h4>
      <p>Дерётся за то, что игрок почувствует.</p></div>
    <div class="card"><div class="kn">Издатель</div>
      <div class="logos">''' + ico("sony", 50) + ico("ubisoft", 50) + ico("ea", 50) + '''</div>
      <h4>Деньги и право на релиз</h4>
      <p>Про ощущения игрока — вообще не он.</p></div>
    <div class="card dark"><div class="kn">Холдинг</div>
      <h4>Доли в тех, кто делает</h4>
      <p>Tencent взяла 93% Riot в 2011-м и весь остаток к 2015-му. Игр не делает сама.</p></div>
  </div>'''))

# ── 09 стена логотипов ───────────────────────────────────────────────────
def grp(cap, tiles, cols, hot=False):
    return ('<div class="wallgrp%s"><div class="cap">%s</div><div class="grid" '
            'style="grid-template-columns:repeat(%d,1fr)">%s</div></div>'
            % (" hot" if hot else "", cap, cols, "".join(tiles)))

S.append(('Мало игроков — ещё не горлышко', '', top("Кто стоит на карте") + '''
  <h2 class="r" style="--i:0;margin-bottom:22px">Мало игроков — ещё не горлышко.<br>Горлышко — когда их мало и заменить нельзя</h2>
  <div class="wall r" style="--i:1;grid-template-rows:repeat(2,1fr);grid-template-columns:1fr 1fr">'''
  + grp("03 · Движки · <b>три</b> закрывают 83% рынка · <em>заменяемы</em>",
        [tile("unrealengine"), tile("unity"), tile("godotengine"), tile("valve", name="Valve · Source")], 4)
  + grp("05 · Разработка · <b>тысячи</b> студий · <em>заменяемы</em>",
        [tile("cdprojekt"), tile("rockstargames"), tile("riotgames"), tile("valve")], 4)
  + grp("06 · Издание · <b>десятки</b> · <em>заменяемы, но дорого</em>",
        [tile("sony"), tile("ubisoft"), tile("ea"), tile("squareenix")], 4)
  + grp("08 · Витрины · <b>шесть</b> на весь мир · <em>не заменяемы</em>",
        [tile("steam", mark=True), tile("epicgames", mark=True), tile("gogdotcom", mark=True), tile("appstore", mark=True)], 4, hot=True)
  + '''</div>
  <p class="note after r" style="--i:2">Движков тоже мало — но с Quake можно уйти на GoldSrc. С витрины уйти некуда: без неё игры для игрока нет.</p>'''))

# ── 10 соседние этажи ────────────────────────────────────────────────────
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
      <div class="side" style="padding-left:26px"><div class="lb">06 · Издание</div><div class="tx">Дерётся за <em>деньги и право на релиз</em>, а не за ощущения</div></div>
    </div>
    <div class="vs r" style="--i:3">
      <div class="side"><div class="lb">07 · Платформа</div><div class="tx">Даёт <em>возможность запустить</em> — железо и API</div></div>
      <div class="mid">≠</div>
      <div class="side" style="padding-left:26px"><div class="lb">08 · Витрина</div><div class="tx">Даёт <em>попадание в поле зрения</em> — без неё игры для игрока нет</div></div>
    </div>
  </div>'''))

# ── 11 раздел 02 ─────────────────────────────────────────────────────────
S.append(('Раздел 02 — горлышко', 'dark sec', '<div class="huge">02</div>' + top("Раздел 02") + '''
  <h1 class="r" style="--i:0">Бутылочное<br>горлышко</h1>
  <p class="note r" style="--i:1">Ищем его тестом отказом, а не по деньгам на этаже.</p>'''))

# ── 12 понятие горлышка ──────────────────────────────────────────────────
S.append(('Понятие горлышка', '', top("Понятие · бутылочное горлышко") + '''
  <h2 class="r" style="--i:0">Уровень, где мало игроков,<br>а зависят от них все</h2>
  <div class="cards r" style="--i:1;grid-template-columns:1.5fr 1fr;margin-top:24px">
    <div style="display:flex;flex-direction:column;gap:16px;min-height:0">
      <div class="card"><div class="kn">Признак 1</div>
        <h4>Мало игроков</h4>
        <p>Считаем не компании, а тех, к кому реально можно пойти. Сотня студий аутсорса — много. Шесть витрин — мало.</p></div>
      <div class="card"><div class="kn">Признак 2</div>
        <h4>Нет альтернативы</h4>
        <p>Можно заменить — больно, дорого, но можно — это не горлышко.</p></div>
      <div class="card hot"><div class="kn" style="color:rgba(22,20,15,.72)">Что удерживает</div>
        <h4>Барьер входа</h4>
        <p>Не деньги, а то, что деньгами не покупается: сетевой эффект и привычка.</p></div>
    </div>
    <div class="card" style="padding:24px">''' + FUNNEL + '''</div>
  </div>'''))

# ── 13 тест отказом ──────────────────────────────────────────────────────
CH = [
    ("Откажет движок", "Берёшь другой. Valve так и сделала: ушла с Quake и собрала GoldSrc.", "Альтернатива есть", False),
    ("Откажет подрядчик", "Меняешь. Сектор — $14,7&nbsp;млрд и сотни студий.", "Альтернатива есть", False),
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

# ── 14 витрина как класс ─────────────────────────────────────────────────
S.append(('Горлышко — витрина как класс', 'dark', top("Горлышко · обоснование") + '''
  <h2 class="r" style="--i:0">Горлышко — не Steam.<br>Горлышко — <span style="color:var(--flame)">витрина как класс</span></h2>
  <div class="figs r" style="--i:1;margin-top:38px">
    <div class="fig"><div class="n">75%</div><div class="l">выручки PC-дистрибуции у Steam — это лишь PC-проекция горлышка</div></div>
    <div class="fig"><div class="n">6</div><div class="l">витрин в мире. Мимо них игры не существует</div></div>
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

# ── 15 три кейса ─────────────────────────────────────────────────────────
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
  + "".join('<div class="card"><div class="logos">%s</div>'
            '<h4>%s</h4><div class="kn" style="margin:-6px 0 14px">%s</div>'
            '<p>%s</p><p style="margin-top:auto;padding-top:16px;color:var(--ink);font-weight:700">%s</p></div>'
            % (ico(s, 70), t, sub, b, k) for s, t, sub, b, k in CASES)
  + '''</div>
  <p class="note after r" style="--i:2">Игра была готова и куплена. Отказал <b style="color:var(--flame-ink)">только уровень витрины</b> — и этого хватило.</p>'''))

# ── 16 скрытые горлышки ──────────────────────────────────────────────────
S.append(('Скрытые горлышки', '', top("Скрытые горлышки") + '''
  <h2 class="r" style="--i:0">Горлышко не обязано стоять там,<br>где много выручки</h2>
  <div class="cards c3 r" style="--i:1">
    <div class="card">''' + ui("shield") + '''
      <h4>Сертификация<br>и возрастной рейтинг</h4>
      <p>Не прошёл ESRB или PEGI — на консоль не вышел. Обойти нельзя.</p></div>
    <div class="card">''' + ui("nomoney") + '''
      <h4>Деньги издателя</h4>
      <p>Команда сильная, права есть, игры нет. Для инди горлышко — шестой этаж, а не восьмой.</p></div>
    <div class="card">''' + ui("clock") + '''
      <h4>Мощности подрядчиков</h4>
      <p>Cyberpunk сорвал не аутсорс, а скоуп и старые консоли. Но конвейер студий — признак нехватки.</p></div>
  </div>
  <p class="note after r" style="--i:2">Горлышко ищется не по деньгам на этаже, а по отсутствию альтернативы у тех, кто зависит.</p>'''))

# ── 17 открытый вопрос ───────────────────────────────────────────────────
S.append(('Открытый вопрос', 'hot', top("Открытый вопрос · выносим в зал") + '''
  <h2 class="r" style="--i:0;font-size:80px;font-weight:900;letter-spacing:-.038em;line-height:1.0">Где граница рынка —<br>там и горлышко</h2>
  <div class="cards c3 r" style="--i:1;margin-top:44px">
    <div class="card"><div class="kn">Рынок = PC</div>
      <h4>Горлышко — Steam</h4>
      <p>75% выручки, альтернатив практически нет.</p></div>
    <div class="card"><div class="kn">Рынок = гейминг целиком</div>
      <h4>Горлышек шесть</h4>
      <p>И каждое монополист в своей экосистеме.</p></div>
    <div class="card dark"><div class="kn">Чего мы не решили</div>
      <h4>Витрины — один этаж или три?</h4>
      <p>Не склеили ли мы три разных рынка с одинаковым последним шагом?</p></div>
  </div>'''))

# ── 18 понятия ───────────────────────────────────────────────────────────
GL = [
    ("Конкуренция", "Борьба за то, чего на всех не хватает. Всегда за что-то конкретное."),
    ("Барьер входа", "Что мешает новому игроку занять уровень. Чем выше — тем дольше держится горлышко."),
    ("Объект конкуренции", "То, обладание чем даёт преимущество. На каждом этаже свой."),
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
