
#!/usr/bin/env python3
"""Deterministic generator of /output/entry.png: front-page of Saturday 21 November 2026."""
import zlib, struct, math, random, sys

W = H = 1024
SS = 4  # supersample
SW = SH = W*SS

def rng(seed):
    return random.Random(seed)

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))

PAPER   = hex2rgb('#efe9dc')
INK     = hex2rgb('#1a1712')
RULE    = hex2rgb('#9a9284')
RED     = hex2rgb('#a3211c')
BLUE    = hex2rgb('#1d3f8f')
GREEN   = hex2rgb('#2e6e3c')
DKRED   = hex2rgb('#6e1412')
GRAY    = hex2rgb('#5c564c')
YELLOW  = hex2rgb('#d9a832')

buf = bytearray(PAPER*(SW*SH))

def px(x, y, c):
    if 0 <= x < SW and 0 <= y < SH:
        i = (y*SW + x)*3
        buf[i:i+3] = bytes(c)

def rect(x0, y0, x1, y1, c):
    x0=max(0,int(x0)); y0=max(0,int(y0)); x1=min(SW,int(x1)); y1=min(SH,int(y1))
    row = bytes(c)*(x1-x0)
    for y in range(y0, y1):
        i = (y*SW + x0)*3
        buf[i:i+len(row)] = row

def hline(x0, x1, y, c, t=SS):
    rect(x0, y, x1, y+t, c)

def vline(x, y0, y1, c, t=SS):
    rect(x, y0, x+t, y1, c)

def disc(cx, cy, r, c):
    r2 = r*r
    for y in range(int(cy-r), int(cy+r)+1):
        dy2 = (y-cy)**2
        if dy2 > r2: continue
        dx = int(math.sqrt(r2-dy2))
        rect(cx-dx, y, cx+dx, y+1, c)

def line(x0,y0,x1,y1,c,t=None):
    if t is None: t = SS
    steps = int(max(abs(x1-x0), abs(y1-y0))) + 1
    for s in range(steps):
        u = s/max(1,steps-1)
        rect(int(x0+(x1-x0)*u), int(y0+(y1-y0)*u), int(x0+(x1-x0)*u)+t, int(y0+(y1-y0)*u)+t, c)

# ---- tiny 5x7 bitmap font, uppercase A-Z 0-9 punctuation ----
# Each glyph: list of 7 strings of 5 chars ('1' = ink)
F = {
'A':['01110','10001','10001','11111','10001','10001','10001'],
'B':['11110','10001','10001','11110','10001','10001','11110'],
'C':['01111','10000','10000','10000','10000','10000','01111'],
'D':['11110','10001','10001','10001','10001','10001','11110'],
'E':['11111','10000','10000','11110','10000','10000','11111'],
'F':['11111','10000','10000','11110','10000','10000','10000'],
'G':['01111','10000','10000','10111','10001','10001','01110'],
'H':['10001','10001','10001','11111','10001','10001','10001'],
'I':['11111','00100','00100','00100','00100','00100','11111'],
'J':['00111','00010','00010','00010','00010','10010','01100'],
'K':['10001','10010','10100','11000','10100','10010','10001'],
'L':['10000','10000','10000','10000','10000','10000','11111'],
'M':['10001','11011','10101','10101','10001','10001','10001'],
'N':['10001','11001','10101','10011','10001','10001','10001'],
'O':['01110','10001','10001','10001','10001','10001','01110'],
'P':['11110','10001','10001','11110','10000','10000','10000'],
'Q':['01110','10001','10001','10001','10101','10010','01101'],
'R':['11110','10001','10001','11110','10100','10010','10001'],
'S':['01111','10000','10000','01110','00001','00001','11110'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
'U':['10001','10001','10001','10001','10001','10001','01110'],
'V':['10001','10001','10001','10001','10001','01010','00100'],
'W':['10001','10001','10001','10101','10101','11011','10001'],
'X':['10001','10001','01010','00100','01010','10001','10001'],
'Y':['10001','10001','01010','00100','00100','00100','00100'],
'Z':['11111','00001','00010','00100','01000','10000','11111'],
'0':['01110','10001','10011','10101','11001','10001','01110'],
'1':['00100','01100','00100','00100','00100','00100','01110'],
'2':['01110','10001','00001','00110','01000','10000','11111'],
'3':['11110','00001','00001','01110','00001','00001','11110'],
'4':['00010','00110','01010','10010','11111','00010','00010'],
'5':['11111','10000','11110','00001','00001','10001','01110'],
'6':['00110','01000','10000','11110','10001','10001','01110'],
'7':['11111','00001','00010','00100','01000','01000','01000'],
'8':['01110','10001','10001','01110','10001','10001','01110'],
'9':['01110','10001','10001','01111','00001','00010','01100'],
'.':['00000','00000','00000','00000','00000','00110','00110'],
',':['00000','00000','00000','00000','00110','00110','01100'],
':':['00000','00110','00110','00000','00110','00110','00000'],
'-':['00000','00000','00000','11111','00000','00000','00000'],
'%':['10001','00010','00100','00100','01000','10001','00000'],
'$':['00100','01111','10100','01110','00101','11110','00100'],
'+':['00000','00100','00100','11111','00100','00100','00000'],
'[':['01100','01000','01000','01000','01000','01000','01100'],
']':['00110','00010','00010','00010','00010','00010','00110'],
'\'':['00100','00100','00000','00000','00000','00000','00000'],
'"':['01010','01010','00000','00000','00000','00000','00000'],
'!':['00100','00100','00100','00100','00100','00000','00100'],
'?':['01110','10001','00001','00110','00000','00000','00100'],
'/':['00001','00010','00010','00100','01000','01000','10000'],
'(':['00110','01000','01000','01000','01000','01000','00110'],
')':['01100','00010','00010','00010','00010','00010','01100'],
'*':['00000','01010','00100','11111','00100','01010','00000'],
'=':['00000','00000','11111','00000','11111','00000','00000'],
'>':['01000','00100','00010','00001','00010','00100','01000'],
'<':['00010','00100','01000','10000','01000','00100','00010'],
' ':['00000','00000','00000','00000','00000','00000','00000'],
}
MISS = set()

def char_w(ch, size):
    return (6 if ch not in ' ' else 6)*size

def text(x, y, s, c=INK, size=SS, tracking=1):
    """x,y = top-left in supersampled coords; size in px per font pixel."""
    cx = x
    for ch in s.upper():
        g = F.get(ch)
        if g is None:
            MISS.add(ch); g = F['?']
        for gy, row in enumerate(g):
            for gx, b in enumerate(row):
                if b == '1':
                    rect(cx+gx*size, y+gy*size, cx+(gx+1)*size, y+(gy+1)*size, c)
        cx += (5+tracking)*size
    return cx

def text_w(s, size=SS, tracking=1):
    return len(s)*(5+tracking)*size

def center_text(cx, y, s, c, size=SS):
    text(cx - text_w(s,size)//2, y, s, c, size)

def right_text(rx, y, s, c, size=SS):
    text(rx - text_w(s,size), y, s, c, size)

# ================= layout =================
M = 24*SS      # outer margin
CW = SW - 2*M  # content width

# masthead
rect(0, 0, SW, 8*SS, INK)
center_text(SW//2, 12*SS, 'THE WORLD DAILY', INK, 9*SS)
center_text(SW//2, 12*SS + 9*SS*7 + 3*SS, 'SATURDAY, NOVEMBER 21, 2026', RED, 4*SS)
hline(M, SW-M, 12*SS + 9*SS*7 + 3*SS + 4*SS*7 + 4*SS, INK, 2*SS)

y = 12*SS + 9*SS*7 + 3*SS + 4*SS*7 + 8*SS

# headline band (Kyiv hero takes the widest slot: two columns wide)
HEAD1 = 'RUSSIAN MISSILES LAND IN NATO POLAND'
HEAD2 = 'WAR HITS KYIV + KRYVYI RIH: 8 CIVILIANS KILLED'
KYIV = 'KYIV: MASS DRONE + MISSILE ATTACK'
def fit_text(x, yy, s, c, size, maxw):
    while text_w(s, size) > maxw and size > SS:
        size -= SS
    text(x, yy, s, c, size)
    return size
text(M, y, 'UKRAINE WAR', RED, 4*SS); y += 4*SS*7 + 2*SS
s1 = fit_text(M, y, HEAD1, INK, 6*SS, CW); y += s1*7 + 2*SS
s2 = fit_text(M, y, HEAD2, INK, 5*SS, CW); y += s2*7 + 3*SS
hline(M, SW-M, y, INK, SS); y += 4*SS

# --- Kyiv hero (left 60%) : skyline with windows, missile trails, flashes ---
hx0, hx1 = M, M + int(CW*0.60)
hy0 = y
hy1 = y + 186*SS
rect(hx0, hy0, hx1, hy1, hex2rgb('#0e1226'))
r = rng(21)
horizon = hy1 - 22*SS
# 12 buildings
bx = hx0 + 3*SS
buildings = []
for i in range(12):
    bw = int((hx1-hx0-6*SS)/12) - SS
    bh = int((26 + (i%4)*14 + r.randint(0,10)) * SS)
    bx2 = min(bx + bw, hx1 - 2*SS)
    top = horizon - bh
    col = hex2rgb('#1b2340') if i%2==0 else hex2rgb('#222b52')
    rect(bx, top, bx2, horizon, col)
    # lit windows
    wy = top + 4*SS
    while wy < horizon - 3*SS:
        wx = bx + 2*SS
        while wx < bx2 - 2*SS:
            if r.random() < 0.55:
                rect(wx, wy, wx+2*SS, wy+3*SS, YELLOW if r.random()<0.8 else hex2rgb('#e8d8a0'))
            wx += 4*SS
        wy += 6*SS
    buildings.append((bx, top, bx2))
    bx = bx2 + SS
# dome of Kyiv landmark silhouette
disc(hx0 + 10*SS, horizon - 40*SS, 8*SS, hex2rgb('#2a3560'))
rect(hx0+9*SS, horizon-40*SS, hx0+11*SS, horizon, hex2rgb('#2a3560'))
# missile trails
for k in range(5):
    tx = hx0 + int((hx1-hx0)*(0.12+0.19*k)) + r.randint(-10,10)*SS
    line(tx, horizon, tx + 9*SS, hy0 + 6*SS, hex2rgb('#c8cfe8'), 2*SS)
    # blast flash
    fx, fy = tx + 9*SS, hy0 + 6*SS
    disc(fx, fy, 4*SS, hex2rgb('#f2d16b'))
    disc(fx, fy, 2*SS, hex2rgb('#fff3c0'))
# air-defence tracer
line(hx0+6*SS, horizon-4*SS, hx0+2*SS, hy0+16*SS, hex2rgb('#7fd0ff'), SS)
# label
ks = 3*SS
while text_w(KYIV, ks) > (hx1-hx0)-14*SS and ks > SS: ks -= SS
rect(hx0+2*SS, hy0+2*SS, hx0+2*SS+text_w(KYIV,ks)+6*SS, hy0+2*SS+ks*7+4*SS, INK)
text(hx0+5*SS, hy0+4*SS, KYIV, hex2rgb('#f2e9d0'), ks)
hline(hx0, hx1, hy1, INK, 2*SS)
fit_text(hx0, hy1+3*SS, '400+ DRONES, 110 MISSILES FIRED OVERNIGHT', GRAY, 4*SS, hx1-hx0)

# --- right column: stat band + secondary heroes ---
rx0 = hx1 + 10*SS
rx1 = SW - M
ry = y
def statband(yy, label, value, vcol):
    BH = 26*SS
    rect(rx0, yy, rx1, yy+BH, INK)
    rect(rx0+SS, yy+SS, rx0+8*SS, yy+BH-SS, vcol)
    vs = 3*SS
    while text_w(value, vs) + text_w(label, 3*SS) + 28*SS > (rx1-rx0) and vs > SS:
        vs -= SS
    text(rx0+12*SS, yy+(BH-3*SS*7)//2, label, PAPER, 3*SS)
    right_text(rx1-4*SS, yy+(BH-vs*7)//2, value, vcol, vs)
    return yy + BH + 2*SS

ry = statband(ry, 'NIKKEI', '-5.1%', RED)
ry = statband(ry, 'SP500', '-2.9%', RED)
ry = statband(ry, 'NASDAQ', '-2.6%', RED)
ry = statband(ry, 'BTC', 'SUB $60K', RED)
ry = statband(ry, 'BRENT', '+1.4%', GREEN)
ry += 6*SS

# Poland hero (map-ish): radar arcs + missile marks
py0 = ry
py1 = ry + 62*SS
rect(rx0, py0, rx1, py1, hex2rgb('#dfe6ee'))
# Poland silhouette (rough pentagon)
r = rng(7)
poly = [(0.20,0.15),(0.72,0.10),(0.92,0.45),(0.62,0.92),(0.18,0.80)]
pts = [(rx0+int((rx1-rx0)*px_), py0+int((py1-py0)*py_)) for px_,py_ in poly]
for i in range(len(pts)):
    line(pts[i][0], pts[i][1], pts[(i+1)%len(pts)][0], pts[(i+1)%len(pts)][1], BLUE, 3*SS)
# impact X marks
for mx,my in [(0.45,0.55),(0.58,0.42),(0.36,0.38)]:
    ix, iy = rx0+int((rx1-rx0)*mx), py0+int((py1-py0)*my)
    line(ix-4*SS, iy-4*SS, ix+4*SS, iy+4*SS, RED, 3*SS)
    line(ix-4*SS, iy+4*SS, ix+4*SS, iy-4*SS, RED, 3*SS)
lbl = 'MISSILES IN POLAND'
rect(rx0+2*SS, py0+2*SS, rx0+2*SS+text_w(lbl,3*SS)+4*SS, py0+2*SS+3*SS*7+3*SS, BLUE)
text(rx0+4*SS, py0+3*SS, lbl, PAPER, 3*SS)
def rtext(yy, s, c=GRAY, size=4*SS):
    words = s.split(); linebuf = ''
    for w_ in words:
        cand = (linebuf+' '+w_).strip()
        if text_w(cand, size) > (rx1-rx0) and linebuf:
            text(rx0, yy, linebuf, c, size); yy += size*7 + 1*SS
            linebuf = w_
        else:
            linebuf = cand
    if linebuf:
        text(rx0, yy, linebuf, c, size); yy += size*7 + 1*SS
    return yy

ry = py1 + 4*SS
ry = rtext(ry, '2 MISSILES AND A DRONE HIT NEAR NATO DRILLS') + 3*SS
hline(rx0, rx1, ry, RULE, SS); ry += 4*SS

# Hormuz hero: tankers + flames on sea
ty0 = ry
ty1 = ry + 62*SS
rect(rx0, ty0, rx1, ty1, hex2rgb('#123a5e'))
# sea
for i in range(8):
    wy = ty1 - 20*SS + i*2*SS
    rect(rx0, wy, rx1, wy+SS, hex2rgb('#1e5c8a'))
# tankers
for k,(txf, tyf) in enumerate([(0.25,0.72),(0.58,0.66),(0.82,0.74)]):
    tx_ = rx0 + int((rx1-rx0)*txf); ty_ = ty0 + int((ty1-ty0)*tyf)
    rect(tx_-14*SS, ty_, tx_+14*SS, ty_+6*SS, INK)
    rect(tx_-4*SS, ty_-5*SS, tx_+4*SS, ty_, INK)
    # fire
    disc(tx_, ty_-8*SS, 5*SS, hex2rgb('#e86a1f'))
    disc(tx_, ty_-8*SS, 2*SS, hex2rgb('#ffd166'))
lbl = '3 TANKERS HIT'
rect(rx0+2*SS, ty0+2*SS, rx0+2*SS+text_w(lbl,3*SS)+4*SS, ty0+2*SS+3*SS*7+3*SS, DKRED)
text(rx0+4*SS, ty0+3*SS, lbl, PAPER, 3*SS)
ry = ty1 + 4*SS
ry = rtext(ry, 'IRAN-US WAR: MQ-9 DRONE DOWNED. QATAR TALKS STALL') + 3*SS

bottom_hero_end = max(hy1 + 3*SS + 3*SS*7, ry)
y = bottom_hero_end + 4*SS
hline(M, SW-M, y, INK, 2*SS); y += 5*SS

# ---- story grid: 5 columns x N rows of briefs with big tags ----
stories = [
 ('MIDEAST','HOUTHI MISSILES AT RIYADH INTERCEPTED - 3RD DAY OF ALERTS', RED),
 ('MIDEAST','IRGC SHOWS NEW UNDERGROUND MISSILE LAUNCHER', RED),
 ('EUROPE','NATO: POLAND VIOLATION "GRAVE" - RUTTE TO VISIT', BLUE),
 ('EUROPE','KRYVYI RIH STRUCK: 2 DEAD, 60 WOUNDED', BLUE),
 ('AMERICAS','S+P 500 AND DOW IN CORRECTION ON AI SELLOFF', GREEN),
 ('AMERICAS','NVIDIA -14% ON SEC PROBE REPORT', GREEN),
 ('AMERICAS','BRAZIL STOCKS -13.7% AFTER LULA WIN', GREEN),
 ('ASIA','GTA6 SELLS $3.79BN DAY ONE - RECORD', YELLOW),
 ('ASIA','KOREA PARTY MOVES TO IMPEACH TOP JUSTICE', YELLOW),
 ('ASIA','JAPAN GDP -0.1%; BOJ DECEMBER HIKE LIVE', YELLOW),
 ('ASIA','HONG KONG ENTERS BEAR MARKET -20%', YELLOW),
 ('EUROPE','ECB HOLDS 2.5%; DECEMBER HIKE IN PLAY', BLUE),
 ('AMERICAS','TRUMP-PUTIN-XI SUMMIT: FLAIR OVER SUBSTANCE', GREEN),
 ('MIDEAST','SAUDI STRIKES HODEIDAH PORT', RED),
 ('AFRICA','ETHIOPIA-ERITREA BORDER FIRE FLARES', RED),
 ('AFRICA','SUDAN: 2230 CIVILIANS KILLED IN 2026 - UN', RED),
 ('ASIA','CHINA Q3 GDP +4.5% BEATS FORECASTS', YELLOW),
 ('AMERICAS','JIO IPO DRAWS 22X DEMAND', GREEN),
 ('EUROPE','DENMARK EXPPELS RUSSIAN ATTACHE', BLUE),
 ('MIDEAST','US DENIES IRAN F-16 CLAIM', RED),
 ('ASIA','JAPAN WEIGHS 60T YEN DEFENSE PLAN', YELLOW),
 ('AMERICAS','FED HOLDS 3.75-4% IN 10-2 VOTE', GREEN),
 ('EUROPE','FRANCE SPREADS WIDEN ON FISCAL WORRY', BLUE),
 ('ASIA','KOSPI -5.2%, NIKKEI 6-MONTH LOW', YELLOW),
]
cols = 3
GUT = 12*SS
colw = (CW - (cols-1)*GUT)//cols
col_x = [M + i*(colw+GUT) for i in range(cols)]
BRIEF = 4*SS
# shrink size until the longest word fits the column
while max(text_w(w_, BRIEF) for s2 in stories for w_ in s2[1].split()) > colw - 4*SS and BRIEF > SS:
    BRIEF -= SS
def story_lines(story, size):
    words = story.split(); lines = []; linebuf = ''
    for w_ in words:
        cand = (linebuf+' '+w_).strip()
        if text_w(cand, size) > colw - 4*SS and linebuf:
            lines.append(linebuf); linebuf = w_
        else:
            linebuf = cand
    if linebuf: lines.append(linebuf)
    return lines
FOOT_H = 40*SS
def emit(stories):
    rowy = [y]*cols
    for idx,(tag, story, tc) in enumerate(stories):
        c = idx % cols
        x = col_x[c]; yy = rowy[c]
        yy += 4*SS*7 + 5*SS
        yy += len(story_lines(story, BRIEF))*(BRIEF*7 + 1*SS) + 4*SS
        rowy[c] = yy
    return max(rowy)
n = len(stories)
while n > 8 and emit(stories[:n]) + FOOT_H > SH:
    n -= 1
stories = stories[:n]
rowy = [y]*cols
for idx,(tag, story, tc) in enumerate(stories):
    c = idx % cols
    x = col_x[c]; yy = rowy[c]
    rect(x, yy, x+text_w(tag,BRIEF)+6*SS, yy+BRIEF*7+4*SS, tc)
    text(x+3*SS, yy+2*SS, tag, PAPER, BRIEF)
    yy += BRIEF*7 + 6*SS
    for ln in story_lines(story, BRIEF):
        text(x, yy, ln, INK, BRIEF); yy += BRIEF*7 + 2*SS
    yy += 6*SS
    # separator rule under each story
    hline(x, x+colw, yy, RULE, SS)
    yy += 6*SS
    rowy[c] = yy
grid_end = max(rowy)
# vertical panel rules between columns
for c in range(1, cols):
    vline(col_x[c] - GUT//2, y, grid_end, RULE, SS)
hline(M, SW-M, grid_end + 2*SS, INK, 2*SS)

# footer: main ticker band
fy = grid_end + 8*SS
rect(M, fy, SW-M, fy+18*SS, INK)
tick = 'IN BRIEF: HORMUZ CHOKED - OIL UP - BITCOIN $57.9K - YEN 158.5 - AI ROUT TOKYO TO WALL ST'
ts = fit_text(M+8*SS, fy+4*SS, tick, YELLOW, 3*SS, CW-16*SS)
fy += ts*7 + 12*SS
right_text(SW-M, fy, 'PAGE ONE - NOVEMBER 21, 2026', GRAY, 3*SS)

# ---- downsample 4x with box filter ----
out = bytearray(W*H*3)
for oy in range(H):
    for ox in range(W):
        r_ = g_ = b_ = 0
        for sy in range(SS):
            base = ((oy*SS+sy)*SW + ox*SS)*3
            for sx in range(SS):
                i = base + sx*3
                r_ += buf[i]; g_ += buf[i+1]; b_ += buf[i+2]
        n = SS*SS
        o = (oy*W + ox)*3
        out[o] = r_//n; out[o+1] = g_//n; out[o+2] = b_//n

# ---- encode PNG ----
def png_chunk(tag, data):
    c = struct.pack('>I', len(data)) + tag + data
    return c + struct.pack('>I', zlib.crc32(tag+data) & 0xffffffff)

raw = b''.join(b'\x00' + bytes(out[y*W*3:(y+1)*W*3]) for y in range(H))
ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
png = b'\x89PNG\r\n\x1a\n' + png_chunk(b'IHDR', ihdr) + png_chunk(b'IDAT', zlib.compress(raw, 9)) + png_chunk(b'IEND', b'')

import os
dest = sys.argv[1] if len(sys.argv) > 1 else '/output/entry.png'
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest,'wb').write(png)
print(f'wrote {dest} {len(png)} bytes {W}x{H} missing_glyphs={sorted(MISS)}')
