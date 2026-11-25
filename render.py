#!/usr/bin/env python3
"""Render the news-image-20261125 entry: a one-page newspaper front page.

Draws a 1024x1024 front page, "THE WORLD - WEDNESDAY 25 NOVEMBER 2026",
summing up the world news of Wednesday 25 November 2026 as reported that
day, and writes entry.png beside this script. Pillow is build-time only;
the graded program main.py only copies the finished PNG.

Stories (all reported 24-25 Nov 2026, from Reuters and other wires):
- Lead: Zelenskiy confirms Ukraine struck a Russian cargo ship in the
  Gulf of Finland and a warship off Benghazi, Libya; Norway urges caution.
- Houthi drone strike wounds 11 at Riyadh's PIF Tower, second hit in a week.
- Iran says three oil tankers hit by naval mines in the Strait of Hormuz.
- Sarkozy and wife Carla Bruni ordered to trial over the Libya case.
- NATO to deploy early-warning aircraft in Poland after missiles landed there.
- EU announces further sanctions on Russia; Kyiv and Moscow trade UN charges.
- Sport: England level the T20 series vs Australia; Real Madrid rout PSV 5-1.
- Also today: Trump pardons turkeys Freedom and Feathers; Giuliani gets the
  Medal of Freedom; Nvidia's Huang returns as CEO, shares jump 31%;
  Iraq moves on Kurdish oilfields; Colombia car bomb injures 23;
  Senegal regain the AFCON title after a CAS ruling; FBI crime database
  hit by a suspected breach.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# --- palette ---------------------------------------------------------------
PAPER_BG = (246, 241, 227)   # newsprint cream
PANEL_BG = (255, 253, 246)   # panel paper
NAVY = (22, 35, 63)          # masthead
NAVY2 = (38, 56, 92)
CRIMSON = (176, 42, 48)      # kicker red
GOLD = (201, 162, 39)        # masthead rule
INK = (24, 24, 24)
BODY_GREY = (60, 60, 58)
MUTED = (96, 96, 88)
BORDER = (185, 174, 148)
SKY = (216, 231, 244)
SEA = (198, 224, 238)

W, H = 1024, 1024

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap_text(draw, text, fnt, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, path, size, max_w, max_lines):
    """Largest font size (stepping down) whose wrap fits in max_lines."""
    while size > 13:
        fnt = load_font(path, size)
        lines = wrap_text(draw, text, fnt, max_w)
        if len(lines) <= max_lines:
            return fnt, lines
        size -= 1
    fnt = load_font(path, 13)
    return fnt, wrap_text(draw, text, fnt, max_w)


def centred(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def tracked(draw, cx, y, text, fnt, fill, gap=4):
    """Centred text with extra letter spacing."""
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + gap * (len(text) - 1)
    x = cx - total / 2
    for ch, wch in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += wch + gap


# --- illustrations: each draws inside its own box --------------------------

def illu_ship(d, x0, y0, x1, y1):
    """Cargo ship at sea under a drone strike, Gulf of Finland."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    mid = y0 + h * 0.62
    # explosion starburst above the bow: jagged orange star, yellow core
    ex, ey = x0 + w * 0.28, y0 + h * 0.22
    er = h * 0.14
    pts = []
    for i in range(16):
        ang = math.radians(i * 22.5)
        rr = er if i % 2 == 0 else er * 0.45
        pts.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
    d.polygon(pts, fill=(232, 120, 30))
    d.ellipse([ex - er * 0.45, ey - er * 0.45, ex + er * 0.45, ey + er * 0.45],
              fill=(255, 210, 80))
    # small drone silhouette diving in from upper right
    dx0, dy0 = x1 - w * 0.14, y0 + h * 0.12
    d.ellipse([dx0 - 14, dy0 - 5, dx0 + 14, dy0 + 5], fill=INK)
    d.line([(dx0 - 20, dy0 - 9), (dx0 + 20, dy0 - 9)], fill=INK, width=3)
    d.line([(dx0 - 20, dy0 + 9), (dx0 + 20, dy0 + 9)], fill=INK, width=3)
    d.line([(dx0 - 6, dy0 + 2), (ex + er * 0.5, ey - er * 0.3)],
           fill=INK, width=2)
    # cargo hull with stacked containers
    d.polygon([(x0 + w * 0.08, mid), (x1 - w * 0.06, mid),
               (x1 - w * 0.16, mid + h * 0.18), (x0 + w * 0.16, mid + h * 0.18)],
              fill=(64, 72, 86), outline=NAVY, width=2)
    for i, col in enumerate(((176, 42, 48), (201, 162, 39), (38, 56, 92))):
        cx0 = x0 + w * (0.22 + i * 0.16)
        d.rectangle([cx0, mid - h * 0.16, cx0 + w * 0.13, mid - 1],
                    fill=col, outline=NAVY, width=2)
    # bridge tower at the stern
    d.rectangle([x1 - w * 0.20, mid - h * 0.34, x1 - w * 0.11, mid - 1],
                fill=(240, 240, 238), outline=NAVY, width=2)
    # waves
    for wy in (y0 + h * 0.88, y0 + h * 0.96):
        for wx in range(int(x0 + 4), int(x1 - 20), 34):
            d.arc([wx, wy, wx + 30, wy + 9], 180, 360, fill=NAVY2, width=2)


def illu_tower(d, x0, y0, x1, y1):
    """Riyadh's PIF Tower, smoke and fire near its crown."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(228, 234, 240))
    cx = x0 + w * 0.42
    top, base = y0 + h * 0.06, y1 - h * 0.04
    # tapered tower
    d.polygon([(cx - w * 0.11, base), (cx - w * 0.06, top),
               (cx + w * 0.06, top), (cx + w * 0.11, base)],
              fill=(150, 164, 182), outline=NAVY, width=2)
    for fy in range(5):
        yy = top + h * 0.14 + fy * h * 0.14
        d.line([(cx - w * 0.085, yy), (cx + w * 0.085, yy)],
               fill=(110, 126, 148), width=2)
    # fire licking from the damaged floors
    fx, fy = cx + w * 0.04, top + h * 0.26
    d.polygon([(fx - h * 0.12, fy), (fx, fy - h * 0.30),
               (fx + h * 0.12, fy)], fill=(232, 120, 30))
    d.polygon([(fx - h * 0.06, fy), (fx, fy - h * 0.17),
               (fx + h * 0.06, fy)], fill=(245, 200, 60))
    # smoke puffs drifting right
    for bx, by, r in ((cx + w * 0.22, top + h * 0.10, h * 0.09),
                      (cx + w * 0.30, top + h * 0.04, h * 0.11)):
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(110, 110, 108))
    # smaller neighbour towers
    for tx0, th in ((x0 + w * 0.68, h * 0.52), (x0 + w * 0.84, h * 0.38)):
        d.rectangle([tx0, base - th, tx0 + w * 0.10, base],
                    fill=(170, 182, 196), outline=NAVY, width=2)
    # ground line
    d.line([(x0, base), (x1, base)], fill=NAVY, width=2)


def illu_tanker(d, x0, y0, x1, y1):
    """Oil tanker on fire in the Strait of Hormuz, mine in the water."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    mid = y0 + h * 0.60
    # flames on deck
    for fx in (x0 + w * 0.30, x0 + w * 0.50, x0 + w * 0.70):
        d.polygon([(fx - h * 0.11, mid - 2), (fx, mid - h * 0.38),
                   (fx + h * 0.11, mid - 2)], fill=(232, 120, 30))
        d.polygon([(fx - h * 0.05, mid - 2), (fx, mid - h * 0.22),
                   (fx + h * 0.05, mid - 2)], fill=(245, 200, 60))
    # long hull
    d.rectangle([x0 + w * 0.07, mid - 2, x1 - w * 0.07, mid + h * 0.20],
                fill=(122, 52, 44), outline=NAVY, width=2)
    d.rectangle([x0 + w * 0.07, mid + h * 0.12, x1 - w * 0.07, mid + h * 0.20],
                fill=(70, 40, 36))
    # deck tanks
    for tx in (x0 + w * 0.18, x0 + w * 0.38, x0 + w * 0.58):
        d.ellipse([tx, mid - h * 0.20, tx + w * 0.14, mid - 2],
                  fill=(226, 226, 220), outline=NAVY, width=2)
    # bridge tower
    d.rectangle([x1 - w * 0.19, mid - h * 0.40, x1 - w * 0.09, mid - 2],
                fill=(240, 240, 238), outline=NAVY, width=2)
    # smoke
    for bx, by, r in ((x0 + w * 0.30, y0 + h * 0.05, h * 0.09),
                      (x0 + w * 0.42, y0 + h * 0.01, h * 0.10)):
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(110, 110, 108))
    # naval mine, lower right
    mx, my = x1 - w * 0.28, y0 + h * 0.90
    d.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=(40, 40, 40))
    for dx, dy in ((-11, 0), (11, 0), (0, -11), (0, 11),
                   (-8, -8), (8, -8), (-8, 8), (8, 8)):
        d.line([(mx, my), (mx + dx, my + dy)], fill=(40, 40, 40), width=2)
    for wy in (y0 + h * 0.86,):
        for wx in range(int(x0 + 4), int(x1 - 20), 34):
            d.arc([wx, wy, wx + 30, wy + 9], 180, 360, fill=NAVY2, width=2)


def illu_court(d, x0, y0, x1, y1):
    """A courthouse facade with columns and a gavel."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(238, 234, 222))
    cx = x0 + w * 0.38
    base = y0 + h * 0.92
    # pediment
    d.polygon([(cx - w * 0.26, y0 + h * 0.30), (cx, y0 + h * 0.06),
               (cx + w * 0.26, y0 + h * 0.30)], fill=(210, 202, 180),
              outline=NAVY, width=2)
    d.ellipse([cx - 7, y0 + h * 0.16, cx + 7, y0 + h * 0.30], fill=NAVY)
    # columns
    for colx in (cx - w * 0.20, cx - w * 0.07, cx + w * 0.07, cx + w * 0.20):
        d.rectangle([colx - 6, y0 + h * 0.32, colx + 6, base - h * 0.06],
                    fill=(240, 236, 224), outline=NAVY, width=2)
    # steps
    d.rectangle([cx - w * 0.30, base - h * 0.06, cx + w * 0.30, base],
                fill=(200, 192, 170), outline=NAVY, width=2)
    # scales of justice, right side
    gx, gy = x1 - w * 0.16, y0 + h * 0.50
    d.line([(gx, y0 + h * 0.14), (gx, gy + h * 0.30)], fill=NAVY, width=3)
    d.line([(gx - w * 0.11, y0 + h * 0.20), (gx + w * 0.11, y0 + h * 0.20)],
           fill=NAVY, width=3)
    for side in (-1, 1):
        px = gx + side * w * 0.11
        d.line([(px, y0 + h * 0.20), (px - 8, gy + h * 0.08)], fill=NAVY,
               width=2)
        d.line([(px, y0 + h * 0.20), (px + 8, gy + h * 0.08)], fill=NAVY,
               width=2)
        d.arc([px - 12, gy + h * 0.02, px + 12, gy + h * 0.16], 0, 180,
              fill=(201, 162, 39), width=3)
    d.ellipse([gx - 4, y0 + h * 0.10, gx + 4, y0 + h * 0.18], fill=GOLD)


def illu_radar_plane(d, x0, y0, x1, y1):
    """NATO early-warning aircraft with its radar dome (fits a 70px band)."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    cx, cy = x0 + w * 0.50, y0 + h * 0.52
    # clouds
    for bx, by in ((x0 + w * 0.04, y0 + h * 0.12), (x1 - w * 0.30, y1 - h * 0.16)):
        d.ellipse([bx, by, bx + 56, by + 16], fill=(255, 255, 255))
        d.ellipse([bx + 14, by - 8, bx + 62, by + 8], fill=(255, 255, 255))
    # fuselage
    d.polygon([(cx - 95, cy + 5), (cx - 45, cy - 10), (cx + 70, cy - 10),
               (cx + 112, cy + 2), (cx + 70, cy + 10), (cx - 45, cy + 10)],
              fill=(240, 240, 238), outline=NAVY, width=2)
    # wings
    d.polygon([(cx - 14, cy - 9), (cx + 6, cy - 30), (cx + 32, cy - 30),
               (cx + 22, cy - 9)], fill=(200, 208, 220), outline=NAVY, width=2)
    d.polygon([(cx - 14, cy + 9), (cx + 6, cy + 28), (cx + 32, cy + 28),
               (cx + 22, cy + 9)], fill=(200, 208, 220), outline=NAVY, width=2)
    # tail fin
    d.polygon([(cx + 72, cy - 9), (cx + 100, cy - 26), (cx + 106, cy - 9)],
              fill=(200, 208, 220), outline=NAVY, width=2)
    # radar dome on a short strut (kept inside the band)
    d.line([(cx - 3, cy - 10), (cx - 3, cy - 22)], fill=NAVY, width=3)
    d.ellipse([cx - 19, cy - 34, cx + 13, cy - 20], fill=(226, 232, 240),
              outline=NAVY, width=2)
    # radar sweep arcs above the dome
    d.arc([cx - 28, cy - 40, cx + 22, cy - 10], 200, 340, fill=NAVY2, width=2)
    # cockpit window
    d.ellipse([cx + 70, cy - 6, cx + 86, cy + 6], fill=(120, 130, 145),
              outline=NAVY, width=2)


def illu_eu_stars(d, x0, y0, x1, y1):
    """Ring of gold stars on blue: the European Union."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(20, 40, 90))
    cx, cy = x0 + w * 0.50, y0 + h * 0.50
    r = h * 0.40
    for i in range(12):
        ang = math.radians(i * 30 - 90)
        sx, sy = cx + r * math.cos(ang), cy + r * math.sin(ang)
        star(d, sx, sy, 6, (255, 210, 60))
    etxt = "EU"
    ew = d.textlength(etxt, font=load_font(SANS_B, 20))
    d.text((cx - ew / 2, cy - 11), etxt, font=load_font(SANS_B, 20),
           fill=(255, 255, 255))


def star(d, cx, cy, r, fill):
    """Five-pointed star centred at (cx, cy)."""
    pts = []
    for i in range(10):
        ang = math.radians(i * 36 - 90)
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


def illu_cricket(d, x0, y0, x1, y1):
    """Cricket bat and red ball on the outfield."""
    w, h = x1 - x0, y1 - y0
    d.rectangle([x0, y0, x1, y1], fill=(214, 232, 196))
    # stumps
    sx = x0 + w * 0.72
    for i in range(3):
        d.rectangle([sx + i * 9, y0 + h * 0.22, sx + i * 9 + 5, y0 + h * 0.78],
                    fill=(245, 220, 130), outline=NAVY, width=1)
    d.rectangle([sx - 2, y0 + h * 0.18, sx + 28, y0 + h * 0.22],
                fill=(245, 220, 130), outline=NAVY, width=1)
    # bat, leaning at a slight angle: blade + handle
    bx, by = x0 + w * 0.28, y0 + h * 0.12
    d.polygon([(bx - 13, by + 4), (bx + 13, by - 4), (bx + 24, by + h * 0.46),
               (bx - 2, by + h * 0.54)], fill=(222, 196, 140),
              outline=NAVY, width=2)
    d.line([(bx + 11, by + h * 0.50), (bx + 22, by + h * 0.76)],
           fill=(120, 82, 40), width=6)
    # red ball with seam
    cx, cy = x0 + w * 0.52, y0 + h * 0.72
    r = h * 0.13
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(176, 42, 48),
              outline=NAVY, width=2)
    d.arc([cx - r, cy - r, cx + r, cy + r], 300, 60, fill=(255, 255, 255),
          width=2)
    # motion lines behind the ball
    for oy in (-8, 0, 8):
        d.line([(cx - r - 34, cy + oy), (cx - r - 8, cy + oy)],
               fill=NAVY, width=2)


# --- page ------------------------------------------------------------------

def story_panel(img, draw, x, y, w, h, kicker, headline, body, illu):
    """One grid panel: illustration band on top, kicker, headline, body."""
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=BORDER, width=2)
    band = 70
    layer = Image.new("RGB", (w - 4, band), PANEL_BG)
    illu(ImageDraw.Draw(layer), 0, 0, w - 4, band)
    img.paste(layer, (x + 2, y + 2))
    draw.line([(x, y + band), (x + w, y + band)], fill=BORDER, width=2)
    ty = y + band + 8
    draw.text((x + 14, ty), kicker, font=load_font(SANS_B, 17), fill=CRIMSON)
    ty += 24
    hfnt, hlines = fit_text(draw, headline, SERIF_B, 25, w - 28, 2)
    for line in hlines:
        draw.text((x + 14, ty), line, font=hfnt, fill=INK)
        ty += 30
    ty += 4
    bfnt, blines = fit_text(draw, body, SANS, 18, w - 28, 2)
    for line in blines:
        draw.text((x + 14, ty), line, font=bfnt, fill=BODY_GREY)
        ty += 22


def main():
    img = Image.new("RGB", (W, H), PAPER_BG)
    draw = ImageDraw.Draw(img)

    # --- masthead ---
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    centred(draw, W // 2, 12, "THE WORLD", load_font(SERIF_B, 92),
            (250, 246, 232))
    tracked(draw, W // 2, 116, "WEDNESDAY 25 NOVEMBER 2026",
            load_font(SANS_B, 27), GOLD, gap=5)
    draw.rectangle([0, 148, W, 153], fill=GOLD)
    centred(draw, W // 2, 162, "THE DAY'S WORLD NEWS — IN ONE PAGE",
            load_font(SANS_B, 19), MUTED)

    # --- lead story: Ukraine confirms the ship strikes ---
    lx, ly, lw, lh = 36, 192, 952, 236
    draw.rectangle([lx, ly, lx + lw, ly + lh], fill=PANEL_BG, outline=NAVY,
                   width=3)
    ix0, iy0, ix1, iy1 = lx + lw - 330, ly + 2, lx + lw - 2, ly + lh - 2
    layer = Image.new("RGB", (ix1 - ix0, iy1 - iy0), SEA)
    illu_ship(ImageDraw.Draw(layer), 0, 0, ix1 - ix0, iy1 - iy0)
    img.paste(layer, (ix0, iy0))
    draw.line([(ix0, ly), (ix0, ly + lh)], fill=BORDER, width=2)
    tx = lx + 24
    draw.text((tx, ly + 16), "UKRAINE  •  BALTIC & LIBYA",
              font=load_font(SANS_B, 22), fill=CRIMSON)
    hy = ly + 48
    for line in ("KYIV CONFIRMS", "STRIKES ON SHIPS"):
        draw.text((tx, hy), line, font=load_font(SERIF_B, 58), fill=INK)
        hy += 64
    bfnt, blines = fit_text(
        draw,
        "Zelenskiy says Ukraine hit a Russian cargo ship in the Gulf of "
        "Finland and a warship off Benghazi. Norway urges caution.",
        SANS, 20, ix0 - tx - 16, 2)
    by = ly + 182
    for line in blines:
        draw.text((tx, by), line, font=bfnt, fill=BODY_GREY)
        by += 25

    # --- story grid: 3 columns x 2 rows ---
    panels = [
        ("RIYADH", "HOUTHIS HIT TALLEST TOWER AGAIN",
         "Drone strike wounds 11 at the PIF Tower — second hit in a week.",
         illu_tower),
        ("STRAIT OF HORMUZ", "TANKERS HIT BY MINES",
         "Iran says three tankers struck by naval mines; shipping on alert.",
         illu_tanker),
        ("FRANCE", "SARKOZY ORDERED TO TRIAL",
         "Ex-president and wife Carla Bruni face the Libya corruption trial.",
         illu_court),
        ("POLAND", "NATO SENDS SPY PLANES",
         "Early-warning aircraft to deploy after missiles landed in Poland.",
         illu_radar_plane),
        ("EUROPE", "EU ADDS RUSSIA SANCTIONS",
         "New measures as Kyiv and Moscow trade accusations at the UN.",
         illu_eu_stars),
        ("SPORT", "ENGLAND LEVEL T20 SERIES",
         "Eight-wicket win over Australia; Real Madrid rout PSV 5–1.",
         illu_cricket),
    ]
    pw, ph, gap = 306, 224, 17
    gx, gy = 36, 440
    for i, (kicker, headline, body, illu) in enumerate(panels):
        px = gx + (i % 3) * (pw + gap)
        py = gy + (i // 3) * (ph + 12)
        story_panel(img, draw, px, py, pw, ph, kicker, headline, body, illu)

    # --- ALSO TODAY strip ---
    sx, sy, sw, sh = 36, 912, 952, 100
    draw.rectangle([sx, sy, sx + sw, sy + sh], fill=PANEL_BG, outline=NAVY,
                   width=2)
    draw.text((sx + 16, sy + 9), "ALSO TODAY", font=load_font(SANS_B, 19),
              fill=CRIMSON)
    items = ("Trump pardons turkeys Freedom and Feathers  •  Giuliani awarded "
             "the Medal of Freedom  •  Nvidia's Huang back as CEO, shares jump "
             "31%  •  Iraq moves to seize Kurdish oilfields  •  Colombia car "
             "bomb injures 23  •  Senegal regain AFCON title after CAS ruling  "
             "•  FBI crime database hit by suspected breach")
    sfnt, slines = fit_text(draw, items, SANS, 19, sw - 32, 3)
    ly = sy + 36
    for line in slines:
        draw.text((sx + 16, ly), line, font=sfnt, fill=INK)
        ly += 21

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
