"""
Alcovia Ad Creatives Generator
24 creatives @ 1080x1350 (4:5) as PNG
Brand: Emerald #234944 | Yellow #EABF36 | Maroon #912F3C | Navy #012C46 | Beige #E5D1BE
"""
from PIL import Image, ImageDraw, ImageFont
import math, os, textwrap

OUT = "/home/user/CV/creatives/pngs"
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350

# BRAND PALETTE
G  = (35, 73, 68)       # emerald
Y  = (234, 191, 54)     # gold/yellow
M  = (145, 47, 60)      # maroon
N  = (1, 44, 70)        # navy
B  = (229, 209, 190)    # beige
W_ = (255, 255, 255)
DK = (18, 18, 26)       # near black
LG = (245, 242, 238)    # light cream

# FONTS
F = "/usr/share/fonts/truetype/open-sans"
R = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF"

def fnt(size, weight="bold"):
    if weight == "black":
        return ImageFont.truetype(R + "/Roboto-Black.ttf", size)
    if weight == "bold":
        return ImageFont.truetype(F + "/OpenSans-Bold.ttf", size)
    if weight == "extrabold":
        return ImageFont.truetype(F + "/OpenSans-ExtraBold.ttf", size)
    if weight == "semibold":
        return ImageFont.truetype(F + "/OpenSans-Semibold.ttf", size)
    if weight == "medium":
        return ImageFont.truetype(R + "/Roboto-Medium.ttf", size)
    return ImageFont.truetype(F + "/OpenSans-Regular.ttf", size)

def new_img(bg):
    return Image.new("RGB", (W, H), bg)

def draw_text_block(d, text, x, y, max_w, font, color, align="left", line_spacing=1.25):
    char_w = max(1, font.getlength("M"))
    chars = max(1, int(max_w / char_w))
    lines = textwrap.wrap(text, width=chars) if "\n" not in text else text.split("\n")
    cy = y
    for line in lines:
        bb = font.getbbox(line)
        lw = bb[2] - bb[0]
        lh = bb[3] - bb[1]
        if align == "center":
            lx = x - lw // 2
        elif align == "right":
            lx = x - lw
        else:
            lx = x
        d.text((lx, cy), line, font=font, fill=color)
        cy += int(lh * line_spacing) + 4
    return cy

def draw_rect(d, x1, y1, x2, y2, fill, radius=0):
    if radius:
        d.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill)
    else:
        d.rectangle([x1, y1, x2, y2], fill=fill)

def draw_circle(d, cx, cy, r, fill):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)

def draw_logo(d, x, y, name_col, tag_col):
    d.text((x, y),      "alcovia",                        font=fnt(40, "black"),  fill=name_col)
    d.text((x, y + 50), "A H E A D  O F  T H E  C U R V E", font=fnt(17, "medium"), fill=tag_col)

def draw_cta(d, label, cx, y, bg, fg, radius=12):
    f = fnt(30, "bold")
    tw = int(f.getlength(label)) + 64
    th = 74
    x1 = cx - tw // 2
    d.rounded_rectangle([x1, y, x1 + tw, y + th], radius=radius, fill=bg)
    d.text((cx - int(f.getlength(label)) // 2, y + 20), label, font=f, fill=fg)
    return y + th


# ============================================================
# 6 LAYOUT FUNCTIONS
# ============================================================

def layout_diagonal(img, d, headline, subhead, cta,
                    bg, accent, text_c, sub_c, btn_bg, btn_fg):
    # diagonal accent block top-right
    d.polygon([(W // 2, 0), (W, 0), (W, H * 2 // 3)], fill=accent)
    for i in range(4):
        alpha_col = tuple(min(255, c + 30) for c in accent)
        d.line([(W // 2 - 60 + i * 40, 0), (W, H * 2 // 3 - i * 100)],
               fill=alpha_col, width=2)
    # concentric circles top-right corner
    draw_circle(d, W - 100, 100, 160, bg)
    draw_circle(d, W - 100, 100, 110, accent)
    draw_circle(d, W - 100, 100, 60,  bg)
    draw_circle(d, W - 100, 100, 20,  W_)
    # accent bar left
    draw_rect(d, 0, 0, 12, H, accent)
    # content — vertically centred in lower 60% of canvas
    y = draw_text_block(d, headline, 60, 320, 700, fnt(74, "extrabold"), text_c, line_spacing=1.18)
    y += 24
    y = draw_text_block(d, subhead,  60, y,   700, fnt(34, "regular"),   sub_c,  line_spacing=1.42)
    y += 40
    draw_cta(d, cta, 320, y, btn_bg, btn_fg)
    draw_logo(d, 60, H - 118, text_c, accent)


def layout_splitv(img, d, headline, subhead, cta,
                  bg, accent, text_c, sub_c, btn_bg, btn_fg):
    # left colour strip
    draw_rect(d, 0, 0, 14, H, accent)
    draw_rect(d, 14, 0, 200, H, tuple(max(0, c - 20) for c in accent))
    # target/bullseye top right
    for r in [220, 170, 120, 70, 25]:
        fill = accent if (r // 50) % 2 == 0 else bg
        draw_circle(d, W - 140, 220, r, fill)
    # content — start higher, push CTA and logo proportionally
    y = draw_text_block(d, headline, 220, 80, 740, fnt(76, "extrabold"), text_c, line_spacing=1.15)
    y += 28
    y = draw_text_block(d, subhead,  220, y,   740, fnt(34, "regular"),   sub_c,  line_spacing=1.43)
    y += 40
    draw_cta(d, cta, W // 2 + 80, y, btn_bg, btn_fg)
    draw_logo(d, 220, H - 118, text_c, accent)


def layout_hero(img, d, headline, subhead, cta,
                bg, accent, text_c, sub_c, btn_bg, btn_fg):
    # radiating lines from top-center
    cx, cy = W // 2, 240
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        x2 = cx + int(600 * math.cos(rad))
        y2 = cy + int(600 * math.sin(rad))
        lc = tuple(min(255, c + 20) for c in bg)
        d.line([(cx, cy), (x2, y2)], fill=lc, width=3)
    # concentric
    for r, col in [(240, accent), (180, bg), (110, accent), (50, bg), (18, W_)]:
        draw_circle(d, cx, cy, r, col)
    # centered content
    y = draw_text_block(d, headline, W // 2, 480, 920, fnt(78, "extrabold"), text_c, align="center", line_spacing=1.16)
    y += 28
    y = draw_text_block(d, subhead,  W // 2, y,   880, fnt(33, "regular"),   sub_c,  align="center", line_spacing=1.42)
    y += 44
    draw_cta(d, cta, W // 2, y, btn_bg, btn_fg)
    draw_logo(d, W // 2 - 130, H - 118, text_c, accent)


def layout_bold_quote(img, d, headline, subhead, cta,
                      bg, accent, text_c, sub_c, btn_bg, btn_fg):
    # top colour band
    draw_rect(d, 0, 0, W, 360, accent)
    # polka-dot pattern in band
    for row in range(0, 360, 70):
        for col in range(0, W, 70):
            draw_circle(d, col + 35, row + 35, 5, tuple(max(0, c - 40) for c in accent))
    # overlapping circle at bottom of band
    draw_circle(d, 160, 360, 150, bg)
    draw_circle(d, 160, 360, 110, accent)
    # decorative icon
    d.text((108, 288), "+", font=fnt(100, "black"), fill=bg)
    # content below band
    y = draw_text_block(d, headline, 60, 390, 920, fnt(72, "extrabold"), text_c, line_spacing=1.15)
    y += 26
    y = draw_text_block(d, subhead,  60, y,   920, fnt(33, "regular"),   sub_c,  line_spacing=1.42)
    y += 40
    draw_cta(d, cta, W // 2, y, btn_bg, btn_fg)
    draw_logo(d, 60, H - 118, text_c, accent if bg != accent else sub_c)


def layout_comparison(img, d, headline, subhead, cta,
                      bg, accent, text_c, sub_c, btn_bg, btn_fg):
    # top third: split left navy / right accent, VS hero
    TOP = 420
    draw_rect(d, 0, 0, W // 2, TOP, N)
    draw_rect(d, W // 2, 0, W, TOP, accent if accent != N else G)
    # diagonal divider
    d.polygon([(W // 2 - 24, 0), (W // 2 + 24, 0),
               (W // 2 + 24, TOP), (W // 2 - 24, TOP)], fill=W_)
    # VS label centered in top band
    vs_font = fnt(160, "black")
    vs_w = int(vs_font.getlength("VS"))
    d.text((W // 2 - vs_w // 2, 120), "VS", font=vs_font, fill=W_)
    # left label
    d.text((80, 50), "BOOK\nSMART", font=fnt(44, "extrabold"), fill=Y)
    # right label
    d.text((W // 2 + 40, 50), "REAL\nWORLD", font=fnt(44, "extrabold"), fill=N)
    # content below split
    y = TOP + 40
    y = draw_text_block(d, subhead, W // 2, y, 900, fnt(36, "regular"), (60, 60, 60), align="center", line_spacing=1.42)
    y += 44
    draw_cta(d, cta, W // 2, y, N, W_)
    y += 100
    draw_text_block(d, headline, W // 2, y, 900, fnt(56, "extrabold"), N, align="center", line_spacing=1.18)
    draw_logo(d, W // 2 - 130, H - 118, N, accent if accent != N else G)


def layout_stat(img, d, headline, subhead, cta,
                bg, accent, text_c, sub_c, btn_bg, btn_fg):
    # top accent band
    draw_rect(d, 0, 0, W, 320, accent)
    # giant faded "1%" in background of band
    d.text((40, -20), "1%", font=fnt(260, "black"),
           fill=tuple(max(0, c - 60) for c in accent))
    # subtle grid over band
    for col in range(0, W, 90):
        d.line([(col, 0), (col, 320)], fill=tuple(max(0, c - 30) for c in accent), width=1)
    # small accent circle bottom-right
    draw_circle(d, W - 80, 320, 100, accent)
    draw_circle(d, W - 80, 320, 70,  bg)
    # content
    y = draw_text_block(d, headline, 60, 350, 920, fnt(74, "extrabold"), text_c, line_spacing=1.15)
    y += 26
    y = draw_text_block(d, subhead,  60, y,   920, fnt(33, "regular"),   sub_c,  line_spacing=1.42)
    y += 40
    draw_cta(d, cta, W // 2, y, btn_bg, btn_fg)
    draw_logo(d, 60, H - 118, text_c, accent)


# ============================================================
# CREATIVE DATA
# ============================================================

CREATIVES = [
    ("Is your teenager too\n'soft' for the real world?",
     "Good grades won't save them when real-world friction hits.",
     "Book a quick call"),
    ("Raise a teen who\nfinishes what they start.",
     "We turn ideas teenagers talk about into projects they actually build.",
     "Book a quick 15 min call"),
    ("Bright teenagers are not\nautomatically\nreal-world ready.",
     "What sets exceptional teenagers apart is not intelligence but how early they build real-world readiness.",
     "Book a quick 15 min call"),
    ("Being 'book smart'\nisn't enough anymore.",
     "'Book smart' means nothing if they quit when things get hard. Build actual resilience through real-world projects.",
     "Book a discovery call"),
    ("Book-Smart\nvs.\nReal-World Ready.",
     "Average students memorize and quit. Alcovians build actual grit by finishing the projects they talk about.",
     "Book a quick call"),
    ("Why is your teen going\nthrough 'elite' career\ncounselling for a career\nthat won't exist in 5 years?",
     "Old-school career counselling can't keep up with a world changing everyday.",
     "Book a discovery call"),
    ("True career\nclarity\nstarts here.",
     "Give them the ultimate gift: total clarity. Let them shadow real professionals to build a future they believe in.",
     "Get to know who they are"),
    ("Preparing for top\nuniversities is NOT\npreparing for the future.",
     "At Alcovia, your teenager will explore real work with real professionals.",
     "Get to know who they are"),
    ("Marks measure\nmemory.\nThe real world\nmeasures initiatives.",
     "Why plan for 2035 using outdated advice? Swap the anxiety for real-world industry exposure.",
     "Book a discovery call"),
    ("Stop Preparing\nTeens For\nYesterday's Careers.",
     "Old-school prep breeds imposter syndrome. Alcovia builds unshakeable clarity through direct access to real professionals.",
     "Get to know who they are"),
    ("What if your teenager\nis working hard but in\nall the wrong directions?",
     "Fake 'study calls' and endless tuitions are destroying their focus.",
     "Book a quick call"),
    ("Time Is Your\nTeenager's\nBiggest Asset.",
     "The Right Environment Can Multiply It. Imagine your teen managing their time like a CXO.",
     "Book a quick call"),
    ("CXO-level time\nmanagement\nfor teenagers",
     "We train teens using the exact productivity frameworks taught to top business owners.",
     "Book a quick call"),
    ("'Busy' doesn't\nmean productive.",
     "Juggling 4 hobbies isn't productive - it's burnout. Learn intentional time management from real experts.",
     "Get to know who they are"),
    ("Average teens waste\nhours scrolling.",
     "Alcovians master their schedules using CXO-level time management systems.",
     "Book a quick call"),
    ("Your teenager's peer group\nmay be deciding\nmore than you are.",
     "An average peer group creates an average teenager. Your child deserves more.",
     "Book a quick 15 min call"),
    ("Ambitious Teens\nNeed\nAmbitious Friends.",
     "How about those friends being the top 1% of Gurgaon?",
     "Book a quick 15 min call"),
    ("Welcome to the\n1% Club\nfor teens.",
     "National robotics winners, India's top gymnasts, golfers & equestrians are already onboard.",
     "Book a discovery call"),
    ("Myth: School success\nis a reliable sign of\nfuture success.",
     "Exceptional teenagers are shaped by stronger environments, sharper peers & real-world exposure.",
     "Book a discovery call"),
    ("Average Teen\nvs.\nAlcovian.",
     "While others gossip online, Alcovians are launching startups, leading projects & networking with experts.",
     "Get to know who they are"),
    ("Potential alone does not\nput a teenager\nin the top 1%.",
     "Global competition is ruthless. If your teen isn't building an unfair advantage today, they'll be left behind.",
     "Book a discovery call"),
    ("You Built A Top 1% Life.\nNow Build It\nFor Your Teenager.",
     "Give them the ultimate unfair advantage. Join an elite cohort of driven teens building real companies today.",
     "Book a quick call"),
    ("Myth: Cracking a top\nuniversity means your\nteenager is set.",
     "Get your teen into the rooms where real startups and leaders are made.",
     "Book a quick call"),
    ("The 99% wait.\nThe 1% build.",
     "The 99% wait for graduation. The 1% are already building companies and learning from McKinsey mentors at age 14.",
     "Get to know who they are"),
]

# layout, theme: (bg, accent, text_c, sub_c, btn_bg, btn_fg)
PLANS = [
    (layout_diagonal,   (LG, G, N,  (80,80,80),    G, W_)),   # 01
    (layout_splitv,     (N,  Y, W_, (200,200,200),  Y, N )),   # 02
    (layout_hero,       (DK, G, W_, (180,180,180),  G, W_)),   # 03
    (layout_bold_quote, (LG, M, N,  (80,80,80),     M, W_)),   # 04
    (layout_comparison, (LG, Y, N,  (60,60,60),     Y, N )),   # 05
    (layout_diagonal,   (N,  M, W_, (210,190,180),  M, W_)),   # 06
    (layout_hero,       (DK, Y, W_, (200,200,200),  Y, DK)),   # 07
    (layout_bold_quote, (DK, G, W_, (180,180,180),  G, W_)),   # 08
    (layout_splitv,     (LG, M, N,  (80,80,80),     M, W_)),   # 09
    (layout_stat,       (N,  Y, W_, (200,200,200),  Y, N )),   # 10
    (layout_diagonal,   (N,  M, W_, (210,190,180),  M, W_)),   # 11
    (layout_hero,       (DK, Y, W_, (200,200,200),  Y, DK)),   # 12
    (layout_splitv,     (DK, G, W_, (180,180,180),  G, W_)),   # 13
    (layout_bold_quote, (N,  Y, W_, (200,200,200),  Y, N )),   # 14
    (layout_stat,       (LG, G, N,  (70,70,70),     G, W_)),   # 15
    (layout_diagonal,   (B,  N, N,  (60,60,60),     N, W_)),   # 16
    (layout_hero,       (M,  N, W_, (230,210,190),  Y, N )),   # 17
    (layout_stat,       (LG, M, N,  (70,70,70),     M, W_)),   # 18
    (layout_bold_quote, (N,  Y, W_, (200,200,200),  Y, N )),   # 19
    (layout_comparison, (DK, G, W_, (180,180,180),  G, W_)),   # 20
    (layout_splitv,     (DK, Y, W_, (200,200,200),  Y, DK)),   # 21
    (layout_hero,       (LG, G, N,  (70,70,70),     G, W_)),   # 22
    (layout_bold_quote, (M,  N, W_, (230,210,190),  Y, N )),   # 23
    (layout_stat,       (N,  Y, W_, (200,200,200),  Y, N )),   # 24
]

SLUGS = [
    "soft-for-real-world", "finishes-what-they-start", "not-automatically-ready",
    "book-smart-not-enough", "book-smart-vs-real-world", "career-counselling-5-years",
    "true-career-clarity", "top-uni-not-equal-future", "marks-measure-memory",
    "stop-yesterdays-careers", "working-hard-wrong-direction", "time-biggest-asset",
    "cxo-time-management", "busy-not-productive", "average-teens-scroll",
    "peer-group-deciding", "ambitious-friends", "1pct-club",
    "myth-school-success", "average-vs-alcovian", "potential-alone",
    "top1pct-life-for-teen", "myth-top-university", "99pct-wait-1pct-build",
]

# ============================================================
# GENERATE ALL 24
# ============================================================
print("Generating 24 Alcovia ad creatives (1080x1350)...\n")
for i, ((headline, subhead, cta), (layout_fn, theme), slug) in enumerate(
        zip(CREATIVES, PLANS, SLUGS), 1):
    bg, accent, text_c, sub_c, btn_bg, btn_fg = theme
    img = new_img(bg)
    d   = ImageDraw.Draw(img)
    layout_fn(img, d, headline, subhead, cta, bg, accent, text_c, sub_c, btn_bg, btn_fg)
    path = f"{OUT}/{i:02d}_{slug}.png"
    img.save(path, "PNG", optimize=True)
    print(f"  [{i:02d}/24] {slug}.png")

print(f"\nDone - 24 PNGs saved to {OUT}/")
