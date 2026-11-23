#!/usr/bin/env python3
"""Render 'The World Today' — a one-image front page summing up
Tuesday 24 November 2026. Build-time only: uses Pillow to draw the PNG.
The graded program (main.py) is stdlib-only and just copies entry.png.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 2400, 3200
PAPER = (246, 241, 229)
INK = (17, 17, 17)
RED = (178, 34, 34)
GREY = (90, 86, 76)
RULE = (40, 40, 40)
SKY_TOP = (38, 52, 84)
SKY_BOT = (214, 138, 74)
SUN = (232, 196, 120)

def font(path, size):
    return ImageFont.truetype(path, size)

DJ = "/usr/share/fonts/truetype/dejavu/"
LB = "/usr/share/fonts/truetype/liberation/"
SERIF_B = lambda s: font(DJ + "DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font(DJ + "DejaVuSerif.ttf", s)
SERIF_I = lambda s: font(LB + "LiberationSerif-Italic.ttf", s)
SANS_B = lambda s: font(DJ + "DejaVuSans-Bold.ttf", s)
SANS = lambda s: font(DJ + "DejaVuSans.ttf", s)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

def text_wrap(text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(text, fnt, x, y, max_w, leading, fill=INK):
    for ln in text_wrap(text, fnt, max_w):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def rule(y, weight=3, x0=90, x1=2310, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=weight)
    return y + weight

def kicker(x, y, text, size=34):
    d.text((x, y), text, font=SANS_B(size), fill=RED)
    return y + size + 12

def headline(x, y, lines, size=112, leading=122):
    f = SERIF_B(size)
    for ln in lines:
        d.text((x, y), ln, font=f, fill=INK)
        y += leading
    return y

def story_head(x, y, text, width, size=48):
    f = SERIF_B(size)
    for ln in text_wrap(text, f, width):
        d.text((x, y), ln, font=f, fill=INK)
        y += size + 8
    return y

# ---------- frame ----------
d.rectangle([28, 28, W - 29, H - 29], outline=INK, width=4)
d.rectangle([44, 44, W - 45, H - 45], outline=INK, width=1)

# ---------- masthead ----------
y = 78
d.text((W // 2, y), "THE WORLD TODAY", font=SERIF_B(190),
       fill=INK, anchor="ma")
y += 215
d.text((W // 2, y), "ONE IMAGE  ·  THE WHOLE DAY", font=SANS(34),
       fill=GREY, anchor="ma")
y += 62
y = rule(y, 8)
y = rule(y + 6, 2)
y += 18
d.text((90, y), "TUESDAY, 24 NOVEMBER 2026", font=SANS_B(36), fill=INK)
d.text((W // 2, y), "FRONT PAGE", font=SANS_B(36), fill=INK, anchor="ma")
d.text((2310, y), "No. 328", font=SANS_B(36), fill=INK, anchor="ra")
y += 58
y = rule(y, 2)

# ---------- lead story: COP31 ----------
y += 32
y = kicker(90, y, "CLIMATE  —  COP31 · ANTALYA, TÜRKIYE", 34)
y = headline(90, y, ["TALKS COLLAPSE AS", "FOSSIL FUELS GO", "UNNAMED"])
y += 4
deck = ("After a fortnight of haggling, the UN climate summit ends with no deal — "
        "the draft text never once mentions the fuels warming the planet.")
y = para(deck, SERIF_I(42), 90, y, 2130, 54, fill=(60, 58, 50))
y += 12

# --- illustration: the empty summit hall at dusk (panel height 440) ---
ix0, iy0, ix1, iy1 = 90, y, 2310, y + 400
for yy in range(iy0, iy0 + 270):
    t = (yy - iy0) / 270
    r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
    g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
    b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
    d.line([(ix0, yy), (ix1, yy)], fill=(r, g, b))
# pale sun, half-hidden by smoke
cx, cy, cr = 1780, iy0 + 130, 105
d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=SUN)
for ox, oy, r in [(1520, iy0 + 85, 105), (1630, iy0 + 150, 130),
                  (1840, iy0 + 105, 115), (1960, iy0 + 170, 100)]:
    d.ellipse([ox - r, oy - r * 0.55, ox + r, oy + r * 0.55], fill=(52, 58, 78))
# skyline silhouettes, baseline iy0+300
for bx, bw, bh in [(150, 120, 130), (330, 90, 190), (480, 140, 100),
                   (2050, 110, 160), (2200, 60, 100)]:
    d.rectangle([ix0 + bx, iy0 + 270 - bh, ix0 + bx + bw, iy0 + 270],
                fill=(16, 19, 32))
# ground band
d.rectangle([ix0, iy0 + 270, ix1, iy1], fill=(24, 28, 44))
# banner across the hall, struck through
d.rectangle([ix0 + 350, iy0 + 185, ix1 - 350, iy0 + 221], fill=(232, 222, 196))
d.text(((ix0 + ix1) // 2, iy0 + 191),
       "“WHERE DIALOGUE BECOMES ACTION”", font=SANS_B(28),
       fill=(40, 40, 40), anchor="ma")
d.line([(ix0 + 380, iy0 + 203), (ix1 - 380, iy0 + 203)], fill=RED, width=4)
# long empty table + chairs
ty = iy0 + 290
d.rectangle([ix0 + 350, ty, ix1 - 350, ty + 22], fill=(120, 96, 60))
for i in range(7):
    chx = ix0 + 430 + i * 220
    d.rectangle([chx, ty + 30, chx + 90, ty + 78], fill=(150, 122, 78),
                outline=(30, 24, 18), width=2)
    d.rectangle([chx + 6, ty + 78, chx + 18, ty + 100], fill=(150, 122, 78))
    d.rectangle([chx + 72, ty + 78, chx + 84, ty + 100], fill=(150, 122, 78))
d.rectangle([ix0, iy0, ix1, iy1], outline=INK, width=3)
d.text((ix0 + 16, iy1 - 40),
       "The summit hall, empty: COP31 ended on Sunday with no agreement.",
       font=SANS(26), fill=(235, 230, 215))
y = iy1 + 24

# lead body, three columns (measured heights)
col_w, gap = 690, 45
bodies = [
    ("ANTALYA — Two weeks of talks, the longest climate summit in history, "
     "ended on Sunday without an agreement. The European Union, Panama and "
     "small Pacific states refused a draft deal — the Antalya Pact — that "
     "contained no mention of a transition away from fossil fuels."),
    ("Russia, Saudi Arabia and others insisted the final text stay silent "
     "on oil, gas and coal, while backing carbon capture instead. "
     "“A climate deal that leaves out fossil fuels is like a plan to quit "
     "smoking that never mentions cigarettes,” said climate scientist "
     "Katharine Hayhoe."),
    ("It is the first major breakdown since Copenhagen in 2009, and it "
     "comes as October 2026 ran 1.8°C above pre-industrial levels. "
     "Delegates put some decisions off to next year; activists in the hall "
     "held up a banner reading simply: “FAILURE”."),
]
y_body = y
for i, txt in enumerate(bodies):
    y_body = max(y_body, para(txt, SERIF(36), 90 + i * (col_w + gap),
                              y, col_w, 46))
y = y_body + 16
y = rule(y, 2)

# ---------- second row: two stories ----------
y += 20
half_w = 1050
lx = 90
yy = kicker(lx, y, "DISASTER  —  BANTEN, INDONESIA", 32)
yy = story_head(lx, yy, "24 DEAD IN FACTORY FIRE; 30 STILL MISSING", half_w, 48)
yy = para("A blaze tore through the PT Fonusa Agung Mulia confectionery "
          "factory in Cikande on Saturday night. Rescuers picked through "
          "unstable wreckage on Monday as the toll reached 24, with about "
          "30 people unaccounted for. Early reports point to an "
          "air-conditioner short circuit; the labour adviser to the "
          "president has summoned the factory's chief executive.",
          SERIF(35), lx, yy, half_w, 46)
rx = 90 + half_w + 60
d.line([(rx - 30, y), (rx - 30, y + 480)], fill=GREY, width=2)
yy2 = kicker(rx, y, "WAR  —  UKRAINE", 32)
yy2 = story_head(rx, yy2, "KYIV REGION HIT; DRONES STRIKE SHIP OFF LIBYA", half_w, 48)
yy2 = para("Ukraine reported a Russian attack in the Kyiv region that "
           "killed several people and left others missing, as a new analysis "
           "put Russian military deaths in the war above 700,000. Kyiv said "
           "its naval drones hit a Russian warship off the coast of Libya — "
           "a strike that shows how far the war at sea now reaches.",
           SERIF(35), rx, yy2, half_w, 46)
y = max(yy, yy2) + 22
y = rule(y, 2)

# ---------- third row: three columns ----------
y += 20
third_w = 690
tx = 90
yy = kicker(tx, y, "MARKETS", 32)
yy = story_head(tx, yy, "TRUMP BLAMES DEMOCRATS FOR $1TN SELL-OFF", third_w, 44)
yy = para("Wall Street fell after the midterm results; the president said "
          "the rout was the Democrats' doing. In Mumbai the Sensex slid "
          "1,484 points to 82,435.", SERIF(34), tx, yy, third_w, 45)
tx += third_w + gap
d.line([(tx - 22, y), (tx - 22, y + 380)], fill=GREY, width=2)
yy2 = kicker(tx, y, "TECH", 32)
yy2 = story_head(tx, yy2, "HUANG IS BACK AT NVIDIA", third_w, 44)
yy2 = para("Jensen Huang returns as chief executive after a pressure "
           "campaign backed by President Trump, ending the chipmaker's "
           "leadership crisis.", SERIF(34), tx, yy2, third_w, 45)
tx += third_w + gap
d.line([(tx - 22, y), (tx - 22, y + 380)], fill=GREY, width=2)
yy3 = kicker(tx, y, "SOUTH ASIA", 32)
yy3 = story_head(tx, yy3, "MODI, SHAH SEAL 8 DEALS; DHAKA WARNS HASINA", third_w, 44)
yy3 = para("India and Nepal signed eight pacts and a Rs 15,000-crore "
           "package. Bangladesh vowed to arrest ex-premier Sheikh Hasina "
           "if she returns from India.", SERIF(34), tx, yy3, third_w, 45)
y = max(yy, yy2, yy3) + 22
y = rule(y, 2)

# ---------- in brief strip ----------
y += 18
d.text((90, y), "IN BRIEF", font=SANS_B(32), fill=RED)
y += 44
briefs = [
    "SPORT — India v New Zealand, 1st Test ends in a draw; WTC final hopes dented.",
    "CHINA — Beijing sets 2030 targets for elderly care and childcare support.",
    "SEOUL — President nominates a new foreign minister and intelligence chief.",
    "YEREVAN — Armenia proposes a new constitution to advance peace with Azerbaijan.",
    "DUSHANBE — Tajikistan moves to quit the ICC on the day of Putin's visit.",
]
for b in briefs:
    d.text((130, y), "•", font=SANS_B(32), fill=RED)
    y = para(b, SERIF(33), 170, y, 2140, 40)
    y += 2
y += 8
y = rule(y, 8)
y = rule(y + 6, 2)
y += 14
d.text((90, y), "Sources: Reuters · AP · The Guardian · CNN · Bloomberg — "
       "all stories as reported on 24 November 2026.", font=SANS(26), fill=GREY)
d.text((2310, y), "THE WORLD TODAY", font=SANS_B(26), fill=GREY, anchor="ra")

img.save("entry.png")
print("saved entry.png", img.size, "final y:", y)
