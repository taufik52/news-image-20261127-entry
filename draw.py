#!/usr/bin/env python3
"""Draw the news-image-20261127 front page with Pillow.

One 1024x1024 newspaper page summing up Friday 27 November 2026,
built from the day's reported news:

- Main story: Saudi Arabia says it destroyed 50 Houthi military
  targets in Yemen (Sanaa, Al Hudaydah, Saada) — weapons depots,
  ballistic-missile and drone launch sites and command centres — in
  airstrikes after Houthis hit an Aramco facility.
- Two Italian Rheinmetall technicians killed, two hurt, in a drone
  strike in Kuwait; Iran blamed, denies responsibility.
- Pablo Hernandez de Cos elected ECB president, succeeding Christine
  Lagarde after her resignation.
- Zelenskyy warns Russia is preparing a large-scale attack on
  Ukraine within days; Washington approves $621.9m in new aid.
- Trump declares "victory at hand" on Iran and urges its leaders to
  negotiate; China and Brazil lead the pushback on his new tariffs.
- Numbers: 50 targets, $621.9m aid, 30 killed by gunmen in Nigeria,
  12,000+ Ebola cases in DR Congo.
- Ticker: Bangkok oil-depot blast hurts 9; two tankers hit by mines
  off Oman; UK migration at a near 30-year low; Alcaraz wins the ATP
  Finals; Huang reinstated as Nvidia chief; Serbia sets a vote for
  27 December.

Everything is drawn from shapes and text — no photographs, no
network, no randomness — so every run produces the same bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (163, 18, 18)
NAVY = (28, 53, 94)
SAND = (194, 158, 104)
GREY = (90, 90, 86)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_IT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines fitting `width`."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill=INK, leading=None):
    lines = wrap(draw, text, fnt, width)
    step = leading or int(fnt.size * 1.25)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def rule(draw, x0, y, x1, weight=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


def hero_art(draw, x0, y0, x1, y1):
    """Flat dusk scene over Yemen: sky bands, low sun, mountains,
    two jets, and explosions on the ground targets below."""
    bands = [(44, 52, 80), (92, 76, 92), (158, 88, 62),
             (204, 122, 54), (234, 168, 78)]
    horizon = y0 + int((y1 - y0) * 0.55)
    band_h = (horizon - y0) // len(bands)
    for i, colour in enumerate(bands):
        draw.rectangle([x0, y0 + i * band_h, x1, y0 + (i + 1) * band_h],
                       fill=colour)
    draw.rectangle([x0, y0 + len(bands) * band_h, x1, horizon],
                   fill=bands[-1])
    # Low sun.
    cx, cy = x0 + int((x1 - x0) * 0.80), horizon - 16
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(250, 226, 160))
    # Mountain ridges.
    draw.polygon([(x0, horizon), (x0 + 150, horizon - 42),
                  (x0 + 300, horizon - 12), (x0 + 470, horizon - 52),
                  (x0 + 640, horizon - 18), (x0 + 800, horizon - 40),
                  (x1, horizon - 8), (x1, horizon)],
                 fill=(52, 44, 52))
    # Desert floor.
    draw.rectangle([x0, horizon, x1, y1], fill=(122, 94, 58))
    for wy in range(horizon + 12, y1 - 6, 16):
        draw.line([(x0 + 14, wy), (x0 + 110, wy)], fill=(150, 122, 82),
                  width=2)
        draw.line([(x1 - 200, wy + 8), (x1 - 50, wy + 8)],
                  fill=(150, 122, 82), width=2)
    # Two jets in the sky, banking away.
    for jx, jy, s in ((x0 + 150, y0 + 42, 1.0), (x0 + 330, y0 + 74, 0.8)):
        draw.polygon([(jx - 34 * s, jy), (jx + 30 * s, jy - 6 * s),
                      (jx + 46 * s, jy), (jx + 30 * s, jy + 6 * s)],
                     fill=(20, 20, 22))
        draw.polygon([(jx - 6 * s, jy - 4 * s), (jx + 6 * s, jy - 4 * s),
                      (jx + 2 * s, jy - 18 * s)],
                     fill=(20, 20, 22))
        draw.polygon([(jx - 6 * s, jy + 4 * s), (jx + 6 * s, jy + 4 * s),
                      (jx + 2 * s, jy + 14 * s)],
                     fill=(20, 20, 22))
    # Explosions on three ground targets, smoke kept inside the box.
    for ex, ey, r in ((x0 + 220, y1 - 34, 26), (x0 + 480, y1 - 26, 30),
                      (x0 + 700, y1 - 38, 22)):
        draw.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(232, 120, 30))
        draw.ellipse([ex - r // 2, ey - r // 2, ex + r // 2, ey + r // 2],
                     fill=(250, 200, 90))
        for i, sr in enumerate((9, 12, 15)):
            cy2 = ey - r - 8 - i * 16
            draw.ellipse([ex + i * 4 - sr, cy2 - sr,
                          ex + i * 4 + sr, cy2 + sr],
                         fill=(70, 70, 74))
    # A small compound on the left horizon, for scale.
    draw.rectangle([x0 + 60, horizon - 14, x0 + 110, horizon],
                   fill=(40, 34, 38))
    draw.polygon([(x0 + 60, horizon - 14), (x0 + 85, horizon - 26),
                  (x0 + 110, horizon - 14)], fill=(40, 34, 38))
    lab = "SANAA, YEMEN"
    lf = font(SANS_BOLD, 11)
    draw.text((x1 - draw.textlength(lab, font=lf) - 10, y1 - 22), lab,
              font=lf, fill=(235, 230, 215))


def icon(draw, kind, x, y, colour):
    """Small flat pictogram (26x26 box at x, y) for a story cell."""
    if kind == "blast":  # explosion burst
        import math
        for k in range(8):
            a = 2 * math.pi * k / 8
            x2 = x + 13 + 12 * math.cos(a)
            y2 = y + 13 + 12 * math.sin(a)
            draw.line([(x + 13, y + 13), (x2, y2)], fill=colour, width=3)
        draw.ellipse([x + 7, y + 7, x + 19, y + 19], fill=colour)
    elif kind == "bank":  # bank / central bank building
        draw.rectangle([x + 2, y + 4, x + 24, y + 7], fill=colour)
        draw.rectangle([x + 2, y + 21, x + 24, y + 24], fill=colour)
        for px in (x + 4, x + 11, x + 18):
            draw.rectangle([px, y + 8, px + 3, y + 20], fill=colour)
    elif kind == "shield":  # shield
        draw.polygon([(x + 13, y + 1), (x + 25, y + 6), (x + 25, y + 14),
                      (x + 13, y + 25), (x + 1, y + 14), (x + 1, y + 6)],
                     fill=colour)
        draw.line([(x + 8, y + 13), (x + 12, y + 17), (x + 19, y + 8)],
                  fill=PAPER, width=2)
    elif kind == "flag":  # white-flag truce / negotiation
        draw.line([(x + 6, y + 2), (x + 6, y + 24)], fill=colour, width=2)
        draw.polygon([(x + 6, y + 2), (x + 24, y + 6), (x + 6, y + 11)],
                     fill=colour)


def story_cell(draw, x, y, w, head, body, accent, kind):
    icon(draw, kind, x, y, accent)
    draw.rectangle([x + 34, y + 10, x + w, y + 15], fill=accent)
    y = draw_wrapped(draw, x, y + 32, head, font(SERIF_BOLD, 21), w,
                     leading=24)
    y = draw_wrapped(draw, x, y + 4, body, font(SERIF, 15), w, leading=18)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 34  # side margin
    rx = W - mx

    # ---- Masthead ----
    title = font(SERIF_BOLD, 64)
    d.text(((W - d.textlength("THE WORLD TODAY", font=title)) / 2, 22),
           "THE WORLD TODAY", font=title, fill=INK)
    rule(d, mx, 100, rx, 3)
    rule(d, mx, 105, rx, 1)
    meta = font(SANS_BOLD, 15)
    d.text((mx, 114), "FRIDAY, 27 NOVEMBER 2026", font=meta, fill=INK)
    right = "ONE DAY  •  ONE PAGE"
    d.text((rx - d.textlength(right, font=meta), 114), right, font=meta,
           fill=INK)
    rule(d, mx, 140, rx, 2)

    # ---- Main headline ----
    kick = "RIYADH HITS BACK AFTER ATTACK ON ARAMCO"
    kf = font(SANS_BOLD, 12)
    d.text(((W - d.textlength(kick, font=kf)) / 2, 144), kick, font=kf,
           fill=RED)
    head = font(SERIF_BOLD, 45)
    lines = ["SAUDI JETS POUND 50", "HOUTHI TARGETS IN YEMEN"]
    y = 160
    for ln in lines:
        d.text(((W - d.textlength(ln, font=head)) / 2, y), ln, font=head,
               fill=INK)
        y += 50
    stand = ("Riyadh says strikes on Sanaa, Al Hudaydah and Saada destroyed "
             "weapons depots, missile and drone launch sites and command "
             "centres, after Houthis hit an Aramco facility.")
    y = draw_wrapped(d, mx + 60, y + 2, stand, font(SERIF_IT, 18), rx - mx - 120,
                     fill=(40, 40, 40), leading=22)

    # ---- Hero art + caption ----
    art_y0, art_y1 = 308, 464
    hero_art(d, mx, art_y0, rx, art_y1)
    d.rectangle([mx, art_y0, rx, art_y1], outline=INK, width=2)
    cap = ("Saudi jets strike Houthi targets in Yemen, Riyadh said, after "
           "a Houthi attack on an Aramco facility. — Illustration")
    draw_wrapped(d, mx, art_y1 + 8, cap, font(SERIF_IT, 13), rx - mx,
                 fill=GREY, leading=16)

    # ---- Dateline: where the day happened ----
    tf = font(SANS_BOLD, 10)
    y_line = 508
    d.text((mx, y_line - 14), "WHERE THE DAY HAPPENED", font=tf, fill=GREY)
    d.line([(mx, y_line), (rx, y_line)], fill=GREY, width=1)
    cities = [("SANAA", -44, False), ("KUWAIT", 48, False),
              ("KHASAB", 56, True), ("KYIV", 30, False),
              ("BANGKOK", 100, True)]
    for name, lon, above in cities:
        cx = mx + int((lon + 50) / 160 * (rx - mx))
        d.ellipse([cx - 4, y_line - 4, cx + 4, y_line + 4], fill=RED)
        w = d.textlength(name, font=tf)
        lx = min(max(cx - w / 2, mx), rx - w)
        ly = y_line - 13 if above else y_line + 6
        d.text((lx, ly), name, font=tf, fill=INK)

    # ---- Four stories, two by two ----
    rule(d, mx, 534, rx, 2)
    col_w = (rx - mx - 24) // 2
    story_cell(
        d, mx, 546, col_w,
        "TWO ITALIANS KILLED IN DRONE STRIKE IN KUWAIT",
        "Two Rheinmetall technicians are killed and two people hurt in a "
        "drone strike in Kuwait. Iran is blamed for the attack and denies "
        "responsibility.",
        RED, "blast")
    story_cell(
        d, mx + col_w + 24, 546, col_w,
        "ECB PICKS DE COS TO SUCCEED LAGARDE",
        "Spanish economist Pablo Hernandez de Cos is elected the new "
        "president of the European Central Bank, after Christine Lagarde's "
        "resignation.",
        NAVY, "bank")
    rule(d, mx, 686, rx, 1, fill=GREY)
    story_cell(
        d, mx, 696, col_w,
        "ZELENSKYY WARNS OF BIG RUSSIAN ATTACK WITHIN DAYS",
        "Kyiv warns Moscow is preparing a large-scale attack on Ukraine "
        "within days. Washington approves $621.9m in new military aid for "
        "Ukraine.",
        RED, "shield")
    story_cell(
        d, mx + col_w + 24, 696, col_w,
        "TRUMP DECLARES “VICTORY AT HAND” ON IRAN",
        "Trump urges Iran's leaders to negotiate a settlement. China and "
        "Brazil lead the pushback against his new tariff threats.",
        NAVY, "flag")

    # ---- The day in numbers ----
    rule(d, mx, 834, rx, 2)
    d.text((mx, 846), "THE DAY IN NUMBERS", font=font(SANS_BOLD, 13),
           fill=GREY)
    stats = [("50", "Houthi targets hit in Yemen"),
             ("$621.9m", "new US military aid to Ukraine"),
             ("30", "killed by gunmen in Nigeria"),
             ("12,000+", "Ebola cases in DR Congo")]
    col = (rx - mx) // 4
    for i, (num, lab) in enumerate(stats):
        x = mx + i * col
        d.text((x, 866), num, font=font(SANS_BOLD, 22), fill=RED)
        draw_wrapped(d, x, 894, lab, font(SANS, 11), col - 12,
                     fill=INK, leading=14)

    # ---- Ticker ----
    d.rectangle([mx, 920, rx, 962], fill=NAVY)
    ticker = ("BANGKOK OIL DEPOT BLAST HURTS 9  •  TWO TANKERS HIT BY "
              "MINES OFF OMAN  •  UK MIGRATION AT NEAR 30-YEAR LOW  •  "
              "ALCARAZ WINS ATP FINALS  •  HUANG REINSTATED AS NVIDIA "
              "CHIEF  •  SERBIA SETS VOTE FOR 27 DECEMBER")
    tf = font(SANS_BOLD, 13)
    tlines = wrap(d, ticker, tf, rx - mx - 16)
    ty = 928
    for ln in tlines:
        d.text((mx + 8, ty), ln, font=tf, fill=(255, 255, 255))
        ty += 18

    # ---- Footer ----
    foot = ("The World Today — one page summing up Friday 27 November 2026  •  "
            "Drawn by an AI agent for make.fun")
    ff = font(SANS, 12)
    d.text(((W - d.textlength(foot, font=ff)) / 2, 972), foot, font=ff,
           fill=GREY)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
