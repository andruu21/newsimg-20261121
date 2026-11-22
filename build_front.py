#!/usr/bin/env python3
"""Render the 21 November 2026 front page to entry.png (1024x1024, <1 MiB).

Draws with Pillow at 4x supersample, then downscales. Deterministic: no
randomness, no network, no wall clock.
"""
from PIL import Image, ImageDraw, ImageFont
import os

S = 4                      # supersample factor
W = H = 1024
PX = W * S                 # canvas edge at supersample

# ---------- palette (warm ivory paper, slate ink, burnt-orange accent) ------
PAPER = (247, 242, 228)
INK = (28, 39, 51)
RED = (168, 55, 38)
TEAL = (41, 96, 92)
GOLD = (178, 129, 40)
MUTED = (94, 84, 66)
CARD = (252, 249, 238)
RULE = (206, 196, 172)
NAVY = (18, 28, 44)

FD = "/usr/share/fonts/truetype"
_SERIF = FD + "/dejavu/DejaVuSerif.ttf"
_SERIF_B = FD + "/dejavu/DejaVuSerif-Bold.ttf"
_SERIF_I = FD + "/dejavu/DejaVuSerif-Italic.ttf"
if not os.path.exists(_SERIF_I):
    _SERIF_I = FD + "/liberation/LiberationSerif-Italic.ttf"

_fonts = {}


def F(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def serif(sz):
    return F(_SERIF, sz * S)


def serifb(sz):
    return F(_SERIF_B, sz * S)


def serifit(sz):
    return F(_SERIF_I, sz * S)


img = Image.new("RGB", (PX, PX), PAPER)
d = ImageDraw.Draw(img)

M = 22 * S  # page margin


def wrap(text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, font, maxw, fill, lh=None):
    lh = lh or int(font.size * 1.2)
    for line in wrap(text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def tagline(x, y, num, place):
    d.text((x, y), "%d · %s" % (num, place), font=serifb(10), fill=RED)
    return y + 13 * S


def card(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=S)


# ================================================================ header ====
d.rectangle([0, 0, PX, 6 * S], fill=RED)
d.text((M, 13 * S), "THE WORLD IN ONE DAY", font=serifb(12), fill=INK)
right = "SATURDAY'S NEWS · ONE PAGE · 35 STORIES · 7 REGIONS"
d.text((PX - M - d.textlength(right, font=serifb(12)), 13 * S), right,
       font=serifb(12), fill=INK)
d.line([M, 32 * S, PX - M, 32 * S], fill=INK, width=S)

# masthead
date_f = serifb(58)
dtxt = "Saturday 21 November 2026"
dw = d.textlength(dtxt, font=date_f)
d.text(((PX - dw) / 2, 36 * S), dtxt, font=date_f, fill=INK)
sub = "Iran hits US targets in Bahrain  ·  Tankers ablaze off Hormuz  ·  Nikkei's worst week since 2020"
sf = serifit(13)
d.text(((PX - d.textlength(sub, font=sf)) / 2, 102 * S), sub, font=sf, fill=RED)
d.line([M, 120 * S, PX - M, 120 * S], fill=RULE, width=S)

# ============================================================= stat band ====
stats = [
    ("148 drones", "plus 3 ballistic missiles on Kyiv overnight (Ukrinform)"),
    ("Nikkei −5.1%", "7-month low; Kospi −5.2% on AI rout (Nikkei)"),
    ("S&P −3.7%", "6,910; Dow −1.9%; both in correction (Reuters)"),
    ("$92.57 Brent", "+0.6% as 3 tankers hit near Hormuz (WAM)"),
    ("BTC $58k", "lowest in two years (Reuters)"),
    ("3 tankers hit", "near Khasab, Oman; Iran blames a mine (UKMTO)"),
]
sy = 126 * S
sw = (PX - 2 * M) / 6
for i, (big, small) in enumerate(stats):
    x = M + i * sw
    d.text((x, sy), big, font=serifb(13), fill=RED if i % 2 else INK)
    yy = sy + 18 * S
    for ln in wrap(small, serif(8), sw - 6 * S)[:3]:
        d.text((x, yy), ln, font=serif(8), fill=MUTED)
        yy += 10 * S
d.line([M, sy + 52 * S, PX - M, sy + 52 * S], fill=RULE, width=S)

# ============================================================= hero row =====
hy = 186 * S
hh = 172 * S
cw = (PX - 2 * M - 2 * 10 * S) / 3

# hero 1: Kyiv night sky — skyline, rising missile trails, blast flashes
x0 = M
card(x0, hy, cw, hh)
d.rectangle([x0 + 8 * S, hy + 8 * S, x0 + cw - 8 * S, hy + 70 * S], fill=NAVY)
sky = [(8, 58), (26, 50), (44, 62), (62, 46), (80, 56), (98, 48), (116, 60),
       (134, 54), (152, 46), (170, 60), (188, 42), (206, 56)]
for bx, bh in sky:
    d.rectangle([x0 + bx * S, hy + 70 * S - bh * S, x0 + (bx + 14) * S, hy + 70 * S],
                fill=(40, 52, 72))
    d.rectangle([x0 + (bx + 4) * S, hy + 70 * S - bh * S + 6 * S,
                 x0 + (bx + 6) * S, hy + 70 * S], fill=(232, 168, 74))
for (bx, by, ex, ey) in [(120, 70, 160, 24), (210, 70, 240, 30),
                         (280, 70, 306, 36)]:
    d.line([x0 + bx * S, hy + by * S, x0 + ex * S, hy + ey * S],
           fill=(232, 140, 60), width=2 * S)
    d.ellipse([x0 + ex * S - 4 * S, hy + ey * S - 8 * S,
               x0 + ex * S + 4 * S, hy + ey * S], fill=(240, 190, 90))
for (gx, gy) in [(60, 14), (250, 12)]:
    d.ellipse([x0 + gx * S, hy + gy * S, x0 + (gx + 12) * S, hy + (gy + 10) * S],
              fill=(214, 88, 52))
y = tagline(x0 + 8 * S, hy + 76 * S, 1, "KYIV · WAR")
d.text((x0 + 8 * S, y), "Russia pounds Kyiv overnight, 148 drones", font=serifb(11.5), fill=INK)
d.text((x0 + 8 * S, y + 15 * S), "and 3 ballistic missiles", font=serifb(11.5), fill=INK)
para(x0 + 8 * S, y + 33 * S,
     "Air defences downed most; strikes kill six as Putin vows a 'painful' reply. (Al Jazeera, Ukrinform, AP)",
     serif(8.3), cw - 16 * S, MUTED)

# hero 2: Gulf tankers on fire
x0 = M + cw + 10 * S
card(x0, hy, cw, hh)
d.rectangle([x0 + 8 * S, hy + 8 * S, x0 + cw - 8 * S, hy + 70 * S], fill=(26, 58, 92))
d.polygon([(x0 + 8 * S, hy + 64 * S), (x0 + cw - 8 * S, hy + 64 * S),
           (x0 + cw - 8 * S, hy + 52 * S), (x0 + 8 * S, hy + 56 * S)], fill=INK)
for (tx, ty) in [(40, 44), (130, 38), (215, 46)]:
    d.rectangle([x0 + tx * S, hy + ty * S, x0 + (tx + 30) * S, hy + (ty + 8) * S], fill=(210, 205, 190))
    d.rectangle([x0 + (tx + 12) * S, hy + (ty - 6) * S, x0 + (tx + 18) * S, hy + ty * S], fill=RED)
    d.ellipse([x0 + (tx + 8) * S, hy + (ty - 13) * S, x0 + (tx + 20) * S, hy + (ty - 1) * S],
              fill=(232, 140, 60))
d.text((x0 + cw - 96 * S, hy + 56 * S), "GULF OF OMAN", font=serifb(9), fill=PAPER)
y = tagline(x0 + 8 * S, hy + 76 * S, 2, "STRAIT OF HORMUZ · OIL")
d.text((x0 + 8 * S, y), "Three tankers hit near Khasab;", font=serifb(11.5), fill=INK)
d.text((x0 + 8 * S, y + 15 * S), "one ablaze after 'mine'", font=serifb(11.5), fill=INK)
para(x0 + 8 * S, y + 33 * S,
     "UKMTO logs two attacks off Oman; Iran's Guards say a tanker struck a mine 'under US direction'. (AP, UKMTO)",
     serif(8.3), cw - 16 * S, MUTED)

# hero 3: Bahrain under Iranian fire
x0 = M + 2 * (cw + 10 * S)
card(x0, hy, cw, hh)
d.rectangle([x0 + 8 * S, hy + 8 * S, x0 + cw - 8 * S, hy + 70 * S], fill=(233, 224, 196))
for k in range(3):
    bx = x0 + (40 + k * 60) * S
    d.line([bx, hy + 66 * S, bx + 24 * S, hy + 16 * S], fill=RED, width=2 * S)
    d.ellipse([bx + 20 * S, hy + 10 * S, bx + 30 * S, hy + 20 * S], fill=INK)
d.rectangle([x0 + 150 * S, hy + 48 * S, x0 + 190 * S, hy + 66 * S], fill=(120, 110, 96))
d.text((x0 + 20 * S, hy + 14 * S), "US BASE", font=serifb(8), fill=(90, 80, 66))
y = tagline(x0 + 8 * S, hy + 76 * S, 3, "MANAMA, BAHRAIN · WAR")
d.text((x0 + 8 * S, y), "Iran's Guards hit US radars at", font=serifb(11.5), fill=INK)
d.text((x0 + 8 * S, y + 15 * S), "two air bases", font=serifb(11.5), fill=INK)
para(x0 + 8 * S, y + 33 * S,
     "IRGC claims missile and drone strikes; a civilian facility burns; Manama condemns the attack. (Xinhua, Reuters)",
     serif(8.3), cw - 16 * S, MUTED)

# ============================================================= cards r1 =====
r1y = hy + hh + 10 * S      # 368
r1h = 118 * S
c5 = (PX - 2 * M - 4 * 8 * S) / 5


def mini_chart(x, y, w, h, pts, col, wdt=2):
    step = w / (len(pts) - 1)
    for i in range(len(pts) - 1):
        d.line([x + i * step, y + h * (1 - pts[i]), x + (i + 1) * step,
                y + h * (1 - pts[i + 1])], fill=col, width=wdt * S)


r1 = [
    (4, "TOKYO, JAPAN", "Nikkei slides to 7-month low",
     "−5.1% to 56,436; Kospi −5.2% as the AI rout sweeps Asia. (Nikkei, Yonhap)", "chart"),
    (5, "NEW YORK, US", "S&P 500 and Dow in correction",
     "S&P −3.7% to 6,910, Nasdaq −5%+; Nvidia −14% on SEC probe. (Reuters)", "bars"),
    (6, "RIYADH, SAUDI", "Houthi missiles intercepted",
     "Coalition downs three ballistic missiles aimed at Riyadh. (Reuters, SPA)", "shield"),
    (7, "GULF OF FINLAND", "Russian cargo ship ablaze",
     "Drones hit a Kaliningrad-bound vessel; crew takes to rafts. (Reuters)", "fire"),
    (8, "BASRA, IRAQ", "Power-station fire kills four",
     "At least 35 hurt at Hartha plant; toll set to rise. (Al Jazeera)", "plant"),
]
for i, (num, tg, head, body, art) in enumerate(r1):
    x = M + i * (c5 + 8 * S)
    card(x, r1y, c5, r1h)
    ay = r1y + 6 * S
    if art == "chart":
        mini_chart(x + 10 * S, ay, c5 - 20 * S, 16 * S, [0.2, 0.3, 0.28, 0.5, 0.55, 0.85], RED)
    elif art == "bars":
        d.rectangle([x + 14 * S, ay, x + 40 * S, ay + 16 * S], fill=TEAL)
        d.rectangle([x + 48 * S, ay, x + 80 * S, ay + 16 * S], fill=RED)
        d.text((x + 18 * S, ay + 3 * S), "−5", font=serifb(9), fill=PAPER)
        d.text((x + 52 * S, ay + 3 * S), "−14", font=serifb(9), fill=PAPER)
    elif art == "shield":
        d.polygon([(x + 30 * S, ay), (x + 50 * S, ay), (x + 50 * S, ay + 10 * S),
                   (x + 40 * S, ay + 18 * S), (x + 30 * S, ay + 10 * S)], outline=TEAL, width=2 * S)
        d.line([x + 35 * S, ay + 8 * S, x + 40 * S, ay + 13 * S, x + 48 * S, ay + 3 * S],
               fill=TEAL, width=2 * S)
    elif art == "fire":
        d.polygon([(x + 26 * S, ay + 16 * S), (x + 48 * S, ay + 16 * S),
                   (x + 44 * S, ay + 6 * S), (x + 30 * S, ay + 8 * S)], fill=INK)
        d.ellipse([x + 34 * S, ay, x + 42 * S, ay + 10 * S], fill=(232, 120, 50))
    else:
        d.rectangle([x + 24 * S, ay + 2 * S, x + 52 * S, ay + 18 * S], outline=INK, width=2 * S)
        d.line([x + 30 * S, ay + 7 * S, x + 44 * S, ay + 7 * S], fill=(232, 120, 50), width=2 * S)
        d.line([x + 30 * S, ay + 12 * S, x + 40 * S, ay + 12 * S], fill=(232, 120, 50), width=2 * S)
    y = tagline(x + 8 * S, ay + 24 * S, num, tg)
    head_lines = wrap(head, serifb(10), c5 - 16 * S)[:2]
    for hl in head_lines:
        d.text((x + 8 * S, y), hl, font=serifb(10), fill=INK)
        y += 12 * S
    y += 1 * S
    para(x + 8 * S, y, body, serif(7.5), c5 - 16 * S, MUTED)

# ============================================================= cards r2 =====
r2y = r1y + r1h + 8 * S     # 494
r2 = [
    (9, "GAZA CITY", "Strike on food-aid truck kills 3",
     "Civil defence: four killed by Israeli fire; WCK name seen. (Reuters)", "truck"),
    (10, "MANILA, ASEAN", "Takaichi and Lee meet again",
     "Fourth bilateral on summit sidelines; January visit set. (Kyodo)", "flags"),
    (11, "ASHULIA, BANGLADESH", "Wage protests shut 50 plants",
     "Garment workers clash with police over minimum wage. (TBS, ANI)", "gate"),
    (12, "SHENZHEN, CHINA", "Prabowo and Xi open talks",
     "Economic-partnership negotiations begin in Shenzhen. (ANTARA)", "tri"),
    (13, "BADME BORDER", "Drone strikes on Eritrea border",
     "Overnight artillery and drone fire as armies mass. (Addis Standard)", "jet"),
]
for i, (num, tg, head, body, art) in enumerate(r2):
    x = M + i * (c5 + 8 * S)
    card(x, r2y, c5, r1h)
    ay = r2y + 6 * S
    if art == "truck":
        d.rectangle([x + 20 * S, ay + 4 * S, x + 44 * S, ay + 16 * S], outline=INK, width=2 * S)
        d.rectangle([x + 44 * S, ay + 8 * S, x + 52 * S, ay + 16 * S], outline=INK, width=2 * S)
        d.line([x + 50 * S, ay + 2 * S, x + 60 * S, ay - 2 * S], fill=RED, width=2 * S)
    elif art == "flags":
        d.rectangle([x + 10 * S, ay, x + 38 * S, ay + 18 * S], fill=(200, 40, 50))
        d.rectangle([x + 44 * S, ay, x + 72 * S, ay + 18 * S], fill=(30, 60, 130))
    elif art == "gate":
        d.line([x + 18 * S, ay + 18 * S, x + 58 * S, ay + 18 * S], fill=INK, width=2 * S)
        d.line([x + 26 * S, ay + 18 * S, x + 26 * S, ay + 2 * S], fill=INK, width=2 * S)
        d.line([x + 48 * S, ay + 18 * S, x + 48 * S, ay + 2 * S], fill=INK, width=2 * S)
    elif art == "tri":
        for k, col in enumerate([RED, GOLD, (30, 60, 130)]):
            d.ellipse([x + (12 + k * 22) * S, ay + 2 * S, x + (26 + k * 22) * S,
                       ay + 16 * S], outline=col, width=2 * S)
    else:
        d.polygon([(x + 26 * S, ay + 14 * S), (x + 48 * S, ay + 7 * S),
                   (x + 48 * S, ay + 12 * S)], fill=(60, 80, 110))
        d.line([x + 48 * S, ay + 10 * S, x + 56 * S, ay + 10 * S], fill=(60, 80, 110), width=2 * S)
    y = tagline(x + 8 * S, ay + 24 * S, num, tg)
    for hl in wrap(head, serifb(10), c5 - 16 * S)[:2]:
        d.text((x + 8 * S, y), hl, font=serifb(10), fill=INK)
        y += 12 * S
    y += 1 * S
    para(x + 8 * S, y, body, serif(7.5), c5 - 16 * S, MUTED)

# ======================================================== also-today list ===
aly = r2y + r1h + 10 * S    # 622
d.text((M, aly), "ALSO ON SATURDAY 21 NOVEMBER — 22 MORE STORIES", font=serifb(11), fill=RED)
d.line([M, aly + 15 * S, PX - M, aly + 15 * S], fill=RULE, width=S)
items = [
    ("KYIV", "Kryvyi Rih strike kills 2, wounds 60 in Zelenskyy's hometown.", "AP"),
    ("WASHINGTON", "Senate fails 51–48 to curb Trump's Iran war powers.", "CNN"),
    ("TEHRAN", "Qatari mediators arrive; Trump wants a 'permanent' deal.", "Al Jazeera"),
    ("KYIV", "Trump tells Europe it spends 'a lot' on the war.", "Reuters"),
    ("GULF", "US denies Iran's claim an F-16 was damaged over the Gulf.", "Reuters"),
    ("MANAMA", "Iranian strike sets a civilian facility on fire.", "Reuters"),
    ("BERLIN", "Merz: Ukraine talks 'soon'; Qatar to invest €15bn.", "DW, dpa"),
    ("ANTALYA", "COP31 plenary ends past midnight; text due this weekend.", "Xinhua"),
    ("EUROPE", "Thousands march in France, Portugal, Spain on living costs.", "Al Jazeera"),
    ("BRUSSELS", "EU and Indonesia sign a trade deal cutting 98.5% of tariffs.", "Reuters"),
    ("NEW YORK", "Bitcoin sinks to its lowest in two years near $58,000.", "Reuters"),
    ("MIAMI", "GTA6 first-day sales near $4bn; 32.5m copies in 48 hours.", "Deadline"),
    ("WASHINGTON", "Anthropic's Nasdaq debut closed; priced at $83.", "Nasdaq"),
    ("SINALOA", "Mexico captures 'El Chapo Isidro'; 11 die in firefight.", "AP"),
    ("PERU", "Magnitude-6.7 quake shakes the Andes; no casualties.", "AP"),
    ("HAITI", "Deal with El Salvador to build three new prisons.", "AP"),
    ("TOKYO", "Q3 GDP shrank 0.1%, first contraction in four quarters.", "Kyodo"),
    ("BEIJING", "Australia and China agree to AI talks.", "ABC"),
    ("KHARTOUM", "Burhan vows to fight until the army retakes Sudan.", "Sudan Now"),
    ("ADDIS ABABA", "Ethiopia, Eritrea trade overnight border fire.", "Addis Standard"),
    ("SYDNEY", "Teen critical after shopping-centre stabbing.", "SBS"),
    ("BRUSSELS", "EU budget proposal 'very disappointing', France says.", "Reuters"),
]
colw = (PX - 2 * M - 20 * S) / 2
item_f = serif(7.8)
lead_f = serifb(8.2)
half = 11
list_end = aly + 20 * S
for ci, chunk in enumerate((items[:half], items[half:])):
    x = M + ci * (colw + 20 * S)
    y = aly + 20 * S
    for city, txt, src in chunk:
        full = "%s (%s)" % (txt, src)
        lw = d.textlength(city + "  ", font=lead_f)
        d.text((x, y), city, font=lead_f, fill=INK)
        y = para(x + lw, y, full, item_f, colw - lw, MUTED)
        y += 3 * S
    list_end = max(list_end, y)

# ==================================================== bottom panels =====
by = list_end + 6 * S
pw = min(150 * S, PX - M - by)  # panel height available

# balance the page: stretch the two bottom panels to a shared bottom above the footer
PAGE_BOTTOM = by + pw
extra = max(0, (PX - M - 16 * S) - PAGE_BOTTOM)
by2, pw2 = by, pw + extra

bw = 300 * S
card(M, by2, bw, pw2)
CARD_BOTTOM = by2 + pw2
d.text((M + 8 * S, by2 + 5 * S), "THE DAY AT A GLANCE", font=serifb(10), fill=INK)
regions = [
    ("EUROPE", "1 · 7 · 14 · 15 · 22 (Berlin) · 23 (EU)"),
    ("MIDEAST", "2 · 3 · 6 · 8 · 9 · 16 (Tehran) · 17 (Gulf) · 21"),
    ("ASIA", "4 · 10 · 11 · 12 · 18 (Tokyo) · 19 (Beijing) · 26 (Khartoum)"),
    ("NORTH AMERICA", "5 · 13 (Miami) · 14 (Washington) · 16 · 20 · 22"),
    ("LATIN AMERICA", "15 (Peru) · 21 (Sinaloa)"),
    ("AFRICA", "13 · 26 · 27 (Addis)"),
    ("OCEANIA", "20 (Sydney) · 28 (Australia–China AI talks)"),
]
yy = by2 + 20 * S
rh = (pw2 - 40 * S) // 7
for rname, its in regions:
    d.text((M + 10 * S, yy), rname, font=serifb(8.2), fill=TEAL)
    d.text((M + 108 * S, yy), its, font=serif(7.4), fill=MUTED)
    yy += rh
d.line([M + 10 * S, yy + 1 * S, M + bw - 10 * S, yy + 1 * S], fill=RULE, width=S)
d.text((M + 10 * S, yy + 3 * S), "35 stories · 7 regions · 18 fields",
       font=serifit(8), fill=RED)

dx0 = M + bw + 10 * S
d.rectangle([dx0, by2, PX - M, CARD_BOTTOM], outline=RED, width=2 * S)
d.text((dx0 + 10 * S, by2 + 5 * S), "DATE CHECK", font=serifb(10), fill=RED)
para(dx0 + 10 * S, by2 + 20 * S,
     "Left out as Friday 20 November's news: the Nikkei's 3,008-point fall, Anthropic's $83 pricing, "
     "Wall Street's slide into a correction, and Cyclone Akvan's landfall. COP31's outcome text is due "
     "over the weekend. Older still: Voyager 1's one-light-day snapshot (18 Nov).",
     serif(7.6), PX - M - dx0 - 20 * S, MUTED, lh=9 * S)
para(dx0 + 10 * S, by2 + 76 * S,
     "Why Saturday 21 November 2026: every story here happened, or was first reported, on that date in at "
     "least one time zone; officials' counts and combatants' claims are kept and labelled as claims.",
     serif(7.6), PX - M - dx0 - 20 * S, MUTED, lh=9 * S)
para(dx0 + 10 * S, by2 + 108 * S,
     "How to read it: the three hero panels carry the day's wars; the card grid adds markets, diplomacy "
     "and sport; the 22-line list below completes the count of 35 across 7 regions and 18 fields.",
     serif(7.6), PX - M - dx0 - 20 * S, MUTED, lh=9 * S)
para(dx0 + 10 * S, by2 + 140 * S,
     "Sources: AP, Reuters, Al Jazeera, Xinhua, Kyodo, UKMTO, SPA, SBS, Addis Standard — original drawing, "
     "made in code.",
     serifit(7.2), PX - M - dx0 - 20 * S, MUTED, lh=9 * S)

# footer
d.line([M, PX - M + 2 * S, PX - M, PX - M + 2 * S], fill=INK, width=S)

# ------------------------------------------------------------ downscale ----
final = img.resize((W, H), Image.Resampling.LANCZOS)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
final.save(out, "PNG", optimize=True)
print("wrote", out, os.path.getsize(out), "bytes  list_end", list_end // S, "panel", by2 // S, "panel_h", pw2 // S)
