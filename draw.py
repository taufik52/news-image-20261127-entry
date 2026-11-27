"""Draw the front page of THE WORLD TODAY for Friday 27 November 2026.

A single-page newspaper image (1024x1024) summing up the day's world news.
Everything here is drawn from scratch with Pillow: masthead, hero story with
a schematic illustration, four secondary stories, a numbers strip and a
ticker. No network, no photos, no downloaded assets -- the output is
deterministic. Sections flow from the one above: each drawing function
returns the y coordinate where it ended, so nothing ever overlaps.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (246, 241, 229)
INK = (20, 20, 20)
RED = (155, 28, 28)
GREY = (96, 94, 88)
SKY = (198, 214, 228)
SUN = (232, 196, 110)
SAND = (216, 198, 162)
RIDGE = (96, 84, 70)
SMOKE = (226, 224, 218)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

MARGIN = 36
RIGHT = W - MARGIN

_fonts = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit_font(draw, text, path, size, max_w):
    """Largest size at or below `size` that fits `text` in `max_w`."""
    while size > 8 and text_w(draw, text, font(path, size)) > max_w:
        size -= 2
    return font(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if text_w(draw, trial, fnt) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - text_w(draw, text, fnt) / 2, y), text, font=fnt, fill=fill)


def spaced(draw, x, y, text, fnt, fill=INK, step=2):
    """Draw text with extra space between letters (for kickers)."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=fnt, fill=fill)
        cx += text_w(draw, ch, fnt) + step
    return cx


def spaced_width(draw, text, fnt, step=2):
    return sum(text_w(draw, ch, fnt) + step for ch in text) - step


def rule(draw, y, width=2, x0=MARGIN, x1=RIGHT, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_top_strip(draw):
    fnt = font(SANS_BOLD, 16)
    draw.text((MARGIN, 28), "FRIDAY, 27 NOVEMBER 2026", font=fnt, fill=INK)
    centered(draw, W // 2, 28, "WORLD EDITION", fnt)
    right = "PAGE 1"
    draw.text((RIGHT - text_w(draw, right, fnt), 28), right, font=fnt, fill=INK)
    rule(draw, 54, 2)


def draw_masthead(draw):
    title = "THE WORLD TODAY"
    fnt = fit_font(draw, title, SERIF_BOLD, 92, RIGHT - MARGIN)
    centered(draw, W // 2, 60, title, fnt)
    rule(draw, 152, 5)
    rule(draw, 158, 1)
    stand = "Fifty targets hit in Yemen  \u2022  $621.9m US aid for Kyiv  \u2022  ECB names De Cos"
    fnt2 = fit_font(draw, stand, SANS, 20, RIGHT - MARGIN)
    centered(draw, W // 2, 166, stand, fnt2)
    rule(draw, 194, 1)


def draw_hero(draw):
    kicker = "MIDDLE EAST \u2014 AIR STRIKES"
    kf = font(SANS_BOLD, 22)
    kw = spaced_width(draw, kicker, kf, 2)
    spaced(draw, (W - kw) / 2, 204, kicker, kf, fill=RED, step=2)

    lines = ["SAUDI JETS POUND", "50 HOUTHI TARGETS", "IN YEMEN"]
    y = 232
    for line in lines:
        fnt = fit_font(draw, line, SERIF_BOLD, 60, RIGHT - MARGIN)
        centered(draw, W // 2, y, line, fnt)
        y += 62

    deck = ("Riyadh says the raids destroyed weapons depots and missile and "
            "drone launch sites \u2014 days after Houthi fire hit an Aramco "
            "facility.")
    df = font(SERIF, 24)
    dl = wrap(draw, deck, df, 880)
    y = 426
    for line in dl:
        centered(draw, W // 2, y, line, df)
        y += 28
    return y


def draw_hero_lower(draw, top):
    mid_x = 560
    draw.line([(mid_x, top), (mid_x, top + 190)], fill=GREY, width=1)

    label = "THE STORY SO FAR"
    lf = font(SANS_BOLD, 14)
    draw.text((MARGIN, top + 2), label, font=lf, fill=RED)

    body = [
        "Saudi warplanes struck 50 targets across Sanaa, Al Hudaydah and "
        "Saada overnight, the kingdom said.",
        "The targets included weapons depots, missile and drone launch sites "
        "and command centres.",
        "The raids followed a Houthi attack on an Aramco oil facility.",
    ]
    bf = font(SERIF, 19)
    y = top + 26
    for para in body:
        for line in wrap(draw, para, bf, mid_x - MARGIN - 24):
            draw.text((MARGIN, y), line, font=bf, fill=INK)
            y += 25
        y += 8
    left_bottom = y

    px0, py0, px1, py1 = 580, top, 988, top + 140
    draw_illustration(draw, px0, py0, px1, py1)
    draw.rectangle([px0, py0, px1, py1], outline=INK, width=2)
    cap = ("Saudi jets over Yemen: depots and launch sites were among the "
           "targets, Riyadh said.")
    cf = font(SANS, 14)
    y = py1 + 6
    for line in wrap(draw, cap, cf, px1 - px0):
        draw.text((px0, y), line, font=cf, fill=GREY)
        y += 18
    return max(left_bottom, y)


def draw_illustration(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    draw.ellipse([x1 - 78, y0 + 14, x1 - 38, y0 + 54], fill=SUN)
    draw.ellipse([x1 - 72, y0 + 20, x1 - 44, y0 + 48], fill=(240, 210, 140))
    # Desert floor and ridge.
    draw.polygon([(x0, y1), (x0, y1 - 34), (x0 + 90, y1 - 58),
                  (x0 + 190, y1 - 40), (x0 + 290, y1 - 66),
                  (x0 + 408, y1 - 44), (x1, y1 - 30), (x1, y1)],
                 fill=RIDGE)
    draw.polygon([(x0, y1), (x0, y1 - 22), (x1, y1 - 14), (x1, y1)],
                 fill=SAND)
    # Smoke columns rising from three struck points.
    for sx in (x0 + 70, x0 + 210, x0 + 330):
        base = y1 - 40
        for i, r in enumerate((13, 10, 8)):
            cy = base - 18 - i * 16
            draw.ellipse([sx - r, cy - r, sx + r, cy + r], fill=SMOKE)
        draw.ellipse([sx - 5, base - 6, sx + 5, base + 4], fill=RED)
        draw.ellipse([sx - 9, base - 10, sx + 9, base + 8], outline=RED, width=2)
    # Three jets with short contrails.
    for jx, jy in ((x0 + 90, y0 + 34), (x0 + 200, y0 + 52), (x0 + 300, y0 + 26)):
        draw.line([(jx - 58, jy + 10), (jx - 26, jy + 3)], fill=(255, 255, 255),
                  width=2)
        draw.polygon([(jx + 14, jy), (jx - 16, jy - 9), (jx - 8, jy),
                      (jx - 16, jy + 9)], fill=INK)


def card_height(draw, head, body, col_w):
    hf = font(SERIF_BOLD, 20)
    bf = font(SERIF, 16)
    head_lines = wrap(draw, head, hf, col_w)
    body_lines = wrap(draw, body, bf, col_w)[:2]
    return 18 + len(head_lines) * 24 + 2 + len(body_lines) * 20


def draw_card(draw, x, y, kicker, head, body, col_w):
    kf = font(SANS_BOLD, 14)
    draw.text((x, y), kicker, font=kf, fill=RED)
    hf = font(SERIF_BOLD, 20)
    hy = y + 18
    for line in wrap(draw, head, hf, col_w):
        draw.text((x, hy), line, font=hf, fill=INK)
        hy += 24
    bf = font(SERIF, 16)
    by = hy + 2
    for line in wrap(draw, body, bf, col_w)[:2]:
        draw.text((x, by), line, font=bf, fill=INK)
        by += 20
    return by


def draw_stories(draw, top):
    col_w = 464
    cols = [MARGIN, 524]
    cards = [
        ("KUWAIT \u2014 DRONE STRIKE",
         "Two Italians killed in Kuwait attack",
         "Two Italian nationals were killed in a drone strike in Kuwait. "
         "Officials blamed Iran."),
        ("EUROPE \u2014 CENTRAL BANK",
         "ECB picks De Cos to succeed Lagarde",
         "The European Central Bank chose Pablo Hern\u00e1ndez de Cos to take "
         "over from Christine Lagarde."),
        ("UKRAINE \u2014 WAR WARNING",
         "Zelenskyy warns of major Russian attack",
         "Volodymyr Zelenskyy warned a major attack could come within days, "
         "as the US approved $621.9m in aid."),
        ("UNITED STATES \u2014 IRAN",
         "Trump declares \u2018victory at hand\u2019 on Iran",
         "Donald Trump declared \u2018victory at hand\u2019 over Iran, saying "
         "his pressure campaign had brought Tehran to heel."),
    ]
    y = top
    for row in range(2):
        pair = cards[row * 2:(row + 1) * 2]
        heights = [card_height(draw, c[1], c[2], col_w) for c in pair]
        row_h = max(heights)
        for i, (kicker, head, body) in enumerate(pair):
            draw_card(draw, cols[i], y, kicker, head, body, col_w)
        y += row_h
        if row == 0:
            rule(draw, y + 4, 1, x0=MARGIN, x1=RIGHT, fill=GREY)
            y += 8
    draw.line([(512, top), (512, y)], fill=GREY, width=1)
    return y


def draw_numbers(draw, top):
    label = "THE DAY IN NUMBERS"
    lf = font(SANS_BOLD, 14)
    draw.text((MARGIN, top), label, font=lf, fill=RED)
    band_y0 = top + 18
    band_y1 = band_y0 + 62
    draw.rectangle([MARGIN, band_y0, RIGHT, band_y1], fill=INK)
    stats = [
        ("50", "targets struck in Yemen"),
        ("$621.9M", "US aid approved for Ukraine"),
        ("30", "killed in attacks in Nigeria"),
        ("12,000+", "Ebola cases in DR Congo"),
    ]
    col_w = (RIGHT - MARGIN) / 4
    for i, (num, lab) in enumerate(stats):
        cx = MARGIN + col_w * (i + 0.5)
        nf = fit_font(draw, num, SERIF_BOLD, 28, col_w - 16)
        centered(draw, cx, band_y0 + 6, num, nf, fill=(255, 255, 255))
        lf2 = font(SANS, 13)
        for line in wrap(draw, lab, lf2, col_w - 20)[:1]:
            centered(draw, cx, band_y0 + 38, line, lf2, fill=(220, 220, 220))
    return band_y1


def draw_ticker(draw, y):
    tick = ("Bangkok blast hurts 9  \u2022  Tankers mined off Oman  \u2022  UK "
            "migration near 30-year low  \u2022  Alcaraz wins ATP Finals  "
            "\u2022  Huang back at Nvidia  \u2022  Serbia vote: 27 Dec")
    fnt = fit_font(draw, tick, SANS, 14, RIGHT - MARGIN)
    centered(draw, W // 2, y, tick, fnt, fill=GREY)


def render():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([14, 14, W - 15, H - 15], outline=INK, width=3)
    draw.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)
    draw_top_strip(draw)
    draw_masthead(draw)
    deck_bottom = draw_hero(draw)
    hero_bottom = draw_hero_lower(draw, deck_bottom + 10)
    rule(draw, hero_bottom + 8, 2)
    stories_bottom = draw_stories(draw, hero_bottom + 18)
    band_bottom = draw_numbers(draw, stories_bottom + 10)
    draw_ticker(draw, band_bottom + 8)
    return img
