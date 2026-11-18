#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news broadsheet poster (1024x1024 PNG).

All artwork is drawn with PIL shapes; no photos or downloaded images.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
NAVY = (16, 38, 63)
GOLD = (214, 164, 60)
INK = (24, 24, 24)
GREY = (90, 90, 90)
PANEL_BG = (255, 255, 255)
PANEL_BORDER = (170, 170, 165)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def bold(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)


def regular(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap measured in pixels."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_icon(draw, kind, x, y, s, color):
    """Small pictogram drawn with PIL shapes inside a box of side s at (x, y)."""
    if kind == "drone":
        # quadcopter: central body, four arms, four rotors
        cx, cy = x + s // 2, y + s // 2
        arm = s // 3
        for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
            draw.line([(cx, cy), (cx + dx * arm, cy + dy * arm)],
                      fill=color, width=4)
            rx, ry = cx + dx * arm, cy + dy * arm
            draw.ellipse([rx - 9, ry - 4, rx + 9, ry + 4], fill=color)
        draw.rounded_rectangle([cx - 13, cy - 8, cx + 13, cy + 8],
                               radius=6, fill=color)
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=PAPER)
    elif kind == "bridge":
        # arch bridge with a broken deck in the middle
        deck_y = y + s - 24
        # the arch (top half of an ellipse)
        draw.arc([x + 6, y + 12, x + s - 6, y + s - 4], 180, 360,
                 fill=color, width=5)
        # deck: solid left half, dropped right half (the broken span)
        draw.line([(x + 4, deck_y), (x + s // 2 - 6, deck_y)],
                  fill=color, width=5)
        draw.line([(x + s // 2 + 8, deck_y + 9), (x + s - 4, deck_y)],
                  fill=color, width=5)
        # two short posts joining arch to deck
        for px in (x + 16, x + s - 20):
            draw.line([(px, y + 26), (px, deck_y)], fill=color, width=3)
    elif kind == "plane":
        # simple airliner flying right: fuselage, tail fin, swept wing
        cx, cy = x + s // 2, y + s // 2
        # swept rear wing, below the fuselage toward the tail
        draw.polygon([(cx - 26, cy + 11), (cx - 4, cy + 32),
                      (cx + 6, cy + 11)], fill=color)
        # fuselage
        draw.rounded_rectangle([x + 6, cy - 9, x + s - 6, cy + 9],
                               radius=9, fill=color)
        # tail fin
        draw.polygon([(x + 8, cy - 6), (x + 16, cy - 28),
                      (x + 26, cy - 6)], fill=color)
    elif kind == "shield":
        # shield with an exclamation mark
        pts = [(x + s // 2, y + 2), (x + s - 4, y + 12), (x + s - 4, y + s // 2),
               (x + s // 2, y + s - 4), (x + 4, y + s // 2), (x + 4, y + 12)]
        draw.polygon(pts, outline=color, width=4)
        cx = x + s // 2
        draw.rectangle([cx - 3, y + 16, cx + 3, y + s - 26], fill=color)
        draw.ellipse([cx - 4, y + s - 20, cx + 4, y + s - 12], fill=color)
    elif kind == "rocket":
        # rocket with flame
        cx = x + s // 2
        draw.polygon([(cx, y + 2), (cx + 13, y + 30), (cx - 13, y + 30)],
                     fill=color)
        draw.rectangle([cx - 13, y + 30, cx + 13, y + s - 24], fill=color)
        draw.polygon([(cx - 13, y + s - 24), (cx - 24, y + s - 8),
                      (cx - 13, y + s - 14)], fill=color)
        draw.polygon([(cx + 13, y + s - 24), (cx + 24, y + s - 8),
                      (cx + 13, y + s - 14)], fill=color)
        draw.ellipse([cx - 5, y + 14, cx + 5, y + 24], fill=PAPER)
        draw.polygon([(cx - 7, y + s - 22), (cx + 7, y + s - 22),
                      (cx, y + s - 2)], fill=(230, 90, 40))
    elif kind == "chip":
        # microchip with pins
        draw.rounded_rectangle([x + 12, y + 12, x + s - 12, y + s - 12],
                               radius=6, outline=color, width=5)
        draw.rectangle([x + s // 2 - 10, y + s // 2 - 10,
                        x + s // 2 + 10, y + s // 2 + 10], fill=color)
        for i in range(3):
            off = 18 + i * 14
            draw.line([(x + off, y + 2), (x + off, y + 12)], fill=color, width=4)
            draw.line([(x + off, y + s - 12), (x + off, y + s - 2)],
                      fill=color, width=4)
            draw.line([(x + 2, y + off), (x + 12, y + off)], fill=color, width=4)
            draw.line([(x + s - 12, y + off), (x + s - 2, y + off)],
                      fill=color, width=4)


STORIES = [
    ("MIDDLE EAST", (178, 34, 34), "drone",
     "Iran fires drones at US radar base in Bahrain",
     "Iran's Revolutionary Guards said they struck the US radar at "
     "Sheikh Isa base; Bahrain said it intercepted the drones, with "
     "no casualties reported."),
    ("UKRAINE WAR", (24, 78, 150), "bridge",
     "Crimea bridge span collapses after Ukrainian strike",
     "Ukraine hit the bridge linking Russia to Crimea; Russian "
     "missiles hit two bridges in Kyiv overnight."),
    ("ASIA", (24, 120, 70), "plane",
     "Trump lands in Manila for ASEAN summit",
     "A Trump-Xi-Putin trilateral summit is confirmed for "
     "19 November in Shenzhen."),
    ("CYBER", (110, 60, 170), "shield",
     "Hackers hit BBC, CNN and 178 sites",
     "Malicious code spread via Optimizely tried to steal crypto "
     "and card data from visitors."),
    ("SPACE", (210, 110, 20), "rocket",
     "Vulcan rocket fails, 40 Amazon satellites lost",
     "ULA's Vulcan suffered an anomaly about 10 minutes after "
     "launch from Cape Canaveral."),
    ("TRADE", (14, 130, 130), "chip",
     "US tightens AI chip export rules",
     "China called the curbs economic coercion; Singapore seeks "
     "\"trusted access\" for legitimate business."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer frame
    d.rectangle([6, 6, W - 7, H - 7], outline=NAVY, width=4)

    # ---- Masthead ----
    d.rectangle([10, 10, W - 11, 158], fill=NAVY)
    title_font = bold(62)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=title_font)
    d.text(((W - tw) / 2, 26), title, font=title_font, fill=(255, 255, 255))
    date_font = bold(30)
    date = "TUESDAY, 17 NOVEMBER 2026"
    dw = d.textlength(date, font=date_font)
    d.text(((W - dw) / 2, 106), date, font=date_font, fill=GOLD)
    d.rectangle([10, 158, W - 11, 163], fill=GOLD)

    # ---- Story grid: 2 columns x 3 rows ----
    margin, gap = 18, 14
    grid_top, grid_bottom = 178, 972
    col_w = (W - 2 * margin - gap) // 2
    row_h = (grid_bottom - grid_top - 2 * gap) // 3

    for idx, (kicker, color, icon, headline, summary) in enumerate(STORIES):
        row, col = divmod(idx, 2)
        x0 = margin + col * (col_w + gap)
        y0 = grid_top + row * (row_h + gap)
        x1, y1 = x0 + col_w, y0 + row_h

        d.rounded_rectangle([x0, y0, x1, y1], radius=8,
                            fill=PANEL_BG, outline=PANEL_BORDER, width=2)
        # colour bar on the left edge
        d.rectangle([x0 + 2, y0 + 8, x0 + 8, y1 - 8], fill=color)

        pad = 20
        tx = x0 + pad + 6
        ty = y0 + 14
        # kicker
        kicker_font = bold(17)
        d.text((tx, ty), kicker, font=kicker_font, fill=color)
        # icon top-right
        draw_icon(d, icon, x1 - 78, y0 + 8, 64, color)
        # gold rule under kicker
        d.line([(tx, ty + 26), (x1 - 88, ty + 26)], fill=GOLD, width=2)

        # headline: wrap narrow so every line clears the top-right icon
        head_font = bold(25)
        head_w = col_w - pad * 2 - 6 - 88
        lines = wrap_text(d, headline, head_font, head_w)
        hy = ty + 38
        for line in lines:
            d.text((tx, hy), line, font=head_font, fill=INK)
            hy += 31

        # summary
        sum_font = regular(18)
        sum_w = col_w - pad * 2 - 6
        slines = wrap_text(d, summary, sum_font, sum_w)
        sy = hy + 6
        for line in slines:
            d.text((tx, sy), line, font=sum_font, fill=(50, 50, 50))
            sy += 24

    # ---- Footer ----
    d.rectangle([10, 976, W - 11, H - 11], fill=NAVY)
    foot_font = bold(21)
    foot = "Six stories that defined Tuesday, 17 November 2026."
    fw = d.textlength(foot, font=foot_font)
    d.text(((W - fw) / 2, 985), foot, font=foot_font, fill=(255, 255, 255))

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
