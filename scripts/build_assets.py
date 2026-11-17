#!/usr/bin/env python3
"""Training ground: draws the animated SVGs in assets/.

Run: python3 scripts/build_assets.py
Change the club colors in PALETTE and every image follows.
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 840

PALETTE = {
    "club": "#f4b52e",   # gold
    "club2": "#d8392c",  # red
    "navy": "#14213d",
    "cream": "#f6eed9",
    "pitch": "#1f8a4c",
    "pitch2": "#1a7a43",
    "board": "#070b12",
    "led": "#ffcf4d",
}
P = PALETTE

DISPLAY = "Impact, Haettenschweiler, 'Arial Narrow Bold', 'Franklin Gothic Bold', sans-serif"
BODY = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

BASE_CSS = (
    ":root{--bg:#f7f0dd;--bg2:#e6dab6;--ink:#14213d;--muted:#55657d;"
    "--sky1:#7cc4ee;--sky2:#e6f4fd;--stars:0;--beam:.10}"
    "@media (prefers-color-scheme:dark){:root{--bg:#0c1a2e;--bg2:#1b3050;--ink:#f6eed9;"
    "--muted:#a6b7cb;--sky1:#040914;--sky2:#17305a;--stars:1;--beam:.17}}"
    ".d{font-family:" + DISPLAY + "}"
    ".b{font-family:" + BODY + "}"
    ".m{font-family:" + MONO + "}"
    ".fb{transform-box:fill-box;transform-origin:center}"
)
REDUCE = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def svg(h, css, body, label):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
        f'role="img" aria-label="{label}">'
        f"<title>{label}</title><style>{BASE_CSS}{css}{REDUCE}</style>{body}</svg>\n"
    )


def ball(r):
    pts = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        pts.append((math.cos(a), math.sin(a)))
    pent = " ".join(f"{x * r * .42:.1f},{y * r * .42:.1f}" for x, y in pts)
    spokes = "".join(
        f'<line x1="{x * r * .42:.1f}" y1="{y * r * .42:.1f}" x2="{x * r * .95:.1f}" y2="{y * r * .95:.1f}" '
        f'stroke="#111" stroke-width="{r * .12:.1f}"/>'
        for x, y in pts
    )
    return (
        f'<circle r="{r}" fill="#fff" stroke="#111" stroke-width="{r * .13:.1f}"/>'
        f'<polygon points="{pent}" fill="#111"/>{spokes}'
    )


def crest():
    return (
        f'<path d="M-46,-56 H46 V8 C46,42 20,60 0,68 C-20,60 -46,42 -46,8 Z" fill="{P["club"]}" '
        f'stroke="{P["navy"]}" stroke-width="6" stroke-linejoin="round"/>'
        f'<path d="M-43,-53 H43 V-26 H-43 Z" fill="{P["navy"]}"/>'
        f'<text class="d" x="0" y="-32" font-size="22" text-anchor="middle" fill="{P["cream"]}" '
        f'letter-spacing="3">HFC</text>'
        f'<g transform="translate(0,14)">{ball(24)}</g>'
        f'<path d="M-30,-18 L30,-18" stroke="{P["club2"]}" stroke-width="5"/>'
    )


_clip = [0]


def rolling(text, x, baseline, size, fill, anim):
    """Digits that roll up to their value. Base state is the final value."""
    adv = size * 0.6
    step = size * 1.2
    out = []
    for i, ch in enumerate(text):
        cx = x + i * adv
        if ch.isdigit():
            _clip[0] += 1
            cid = f"c{_clip[0]}"
            col = "".join(
                f'<text class="m" x="{cx:.1f}" y="{baseline + n * step:.1f}" font-size="{size}" '
                f'font-weight="700" fill="{fill}">{n}</text>'
                for n in range(10)
            )
            t = -int(ch) * step
            out.append(
                f'<clipPath id="{cid}"><rect x="{cx - 2:.1f}" y="{baseline - size * .86:.1f}" '
                f'width="{adv + 4:.1f}" height="{size * 1.06:.1f}"/></clipPath>'
                f'<g clip-path="url(#{cid})"><g style="--t:{t:.1f}px;transform:translateY(var(--t));'
                f'animation:{anim};animation-delay:{i * .12:.2f}s">{col}</g></g>'
            )
        else:
            out.append(
                f'<text class="m" x="{cx:.1f}" y="{baseline}" font-size="{size}" font-weight="700" '
                f'fill="{fill}">{ch}</text>'
            )
    return "".join(out)


# ---------------------------------------------------------------- banner
def banner():
    rnd = random.Random(7)
    H = 300
    css = (
        ".star{animation:tw 3s ease-in-out infinite alternate}"
        "@keyframes tw{from{opacity:.15}to{opacity:1}}"
        ".lamp{animation:flick .9s linear backwards,glow 2.6s ease-in-out infinite alternate}"
        "@keyframes flick{0%{opacity:.05}20%{opacity:1}32%{opacity:.15}50%{opacity:1}62%{opacity:.3}100%{opacity:1}}"
        "@keyframes glow{from{opacity:1}to{opacity:.72}}"
        ".beam{opacity:var(--beam);animation:beam 5s ease-in-out infinite alternate}"
        "@keyframes beam{from{opacity:calc(var(--beam)*.55)}to{opacity:var(--beam)}}"
        ".L{animation:drop .75s cubic-bezier(.3,1.5,.5,1) backwards,hop 7s ease-in-out infinite}"
        "@keyframes drop{from{transform:translateY(-230px);opacity:0}}"
        "@keyframes hop{0%,9%,100%{transform:none}4.5%{transform:translateY(-13px)}}"
        ".crest{animation:spin 1.4s cubic-bezier(.2,.9,.3,1.2) backwards,sway 5s ease-in-out 1.4s infinite alternate}"
        "@keyframes spin{from{transform:rotate(-540deg) scale(0)}}"
        "@keyframes sway{from{transform:rotate(-4deg)}to{transform:rotate(4deg)}}"
        ".sub{animation:fade 1s ease-out 1.6s backwards}"
        "@keyframes fade{from{opacity:0;transform:translateY(8px)}}"
        ".fan{animation:bob .9s ease-in-out infinite alternate}"
        "@keyframes bob{to{transform:translateY(-5px)}}"
        ".scarf{animation:wave 1.1s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:left center}"
        "@keyframes wave{from{transform:rotate(-16deg)}to{transform:rotate(14deg)}}"
        ".run{animation:run 9s ease-in-out infinite alternate}"
        "@keyframes run{from{transform:translateX(-385px)}to{transform:translateX(385px)}}"
        ".rot{animation:rot 9s ease-in-out infinite alternate}"
        "@keyframes rot{from{transform:rotate(-1440deg)}to{transform:rotate(1440deg)}}"
    )
    b = ['<defs><clipPath id="r"><rect width="840" height="300" rx="18"/></clipPath>'
         '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" style="stop-color:var(--sky1)"/><stop offset="1" style="stop-color:var(--sky2)"/>'
         '</linearGradient></defs><g clip-path="url(#r)">'
         '<rect width="840" height="300" fill="url(#sky)"/>']
    # stars (night only)
    b.append('<g style="opacity:var(--stars)">')
    for _ in range(34):
        b.append(
            f'<circle class="star" cx="{rnd.randint(8, 832)}" cy="{rnd.randint(6, 150)}" '
            f'r="{rnd.choice([1, 1.3, 1.8])}" fill="#fff" style="animation-delay:{rnd.uniform(0, 3):.2f}s"/>'
        )
    b.append("</g>")
    # floodlights
    for side, x in ((1, 52), (-1, 788)):
        far = x + side * 330
        b.append(
            f'<polygon class="beam" points="{x},34 {far},250 {x + side * 60},250" fill="#fff6c9"/>'
            f'<rect x="{x - 4}" y="50" width="8" height="170" fill="#3b4a63"/>'
            f'<rect x="{x - 34}" y="14" width="68" height="42" rx="5" fill="#26334a" stroke="#3b4a63" stroke-width="3"/>'
        )
        k = 0
        for row in range(2):
            for col in range(3):
                d = 0.25 + k * 0.22 + (0 if side == 1 else 0.11)
                b.append(
                    f'<circle class="lamp" cx="{x - 20 + col * 20}" cy="{26 + row * 18}" r="6.5" fill="#fff3b0" '
                    f'style="animation-delay:{d:.2f}s,{d + 1:.2f}s"/>'
                )
                k += 1
    # crest
    b.append(f'<g transform="translate(182,112)"><g class="crest fb">{crest()}</g></g>')
    # title letters
    widths = {"H": .61, "U": .59, "I": .30, "Z": .47, "N": .60, "G": .59, "A": .57, " ": .26, "F": .50,
              ".": .22, "C": .58}
    size, gap, x = 76, 3, 262
    for i, ch in enumerate("HUIZINGA F.C."):
        w = widths[ch] * size
        if ch != " ":
            d = 0.5 + i * 0.07
            b.append(
                f'<text class="d L" x="{x + w / 2:.1f}" y="138" font-size="{size}" text-anchor="middle" '
                f'style="fill:var(--ink);animation-delay:{d:.2f}s,{3 + i * .09:.2f}s">{ch}</text>'
            )
        x += w + gap
    b.append(
        '<g class="sub"><text class="b" x="262" y="172" font-size="17" font-weight="700" letter-spacing="3.2" '
        'style="fill:var(--ink)">OFFICIAL MATCHDAY PROGRAMME</text>'
        '<text class="b" x="262" y="195" font-size="14" font-weight="600" letter-spacing="2.4" '
        'style="fill:var(--muted)">EST. INDIANAPOLIS · MANAGER: G. HUIZINGA</text></g>'
    )
    # stand and crowd
    b.append(f'<rect y="206" width="840" height="50" fill="#1a2740"/>')
    cols = [P["club"], P["club2"], P["cream"], "#8fb7e8"]
    for row, y in enumerate((222, 240)):
        for i in range(47):
            cx = 9 + i * 18 + (9 if row else 0)
            b.append(
                f'<circle class="fan" cx="{cx}" cy="{y}" r="6.5" fill="{rnd.choice(cols)}" '
                f'style="animation-delay:{rnd.uniform(0, .9):.2f}s;animation-duration:{rnd.uniform(.6, 1.2):.2f}s"/>'
            )
    for i in range(9):
        sx = 40 + i * 95 + rnd.randint(-12, 12)
        b.append(
            f'<rect class="scarf" x="{sx}" y="210" width="30" height="6" rx="2" '
            f'fill="{P["club"] if i % 2 else P["club2"]}" style="animation-delay:{rnd.uniform(0, 1):.2f}s"/>'
        )
    # pitch strip and ball
    for i in range(12):
        b.append(f'<rect x="{i * 70}" y="254" width="70" height="46" fill="{P["pitch"] if i % 2 else P["pitch2"]}"/>')
    b.append('<rect y="254" width="840" height="3" fill="#fff" opacity=".9"/>')
    b.append(f'<g transform="translate(420,279)"><g class="run"><g class="rot fb">{ball(13)}</g></g></g>')
    b.append("</g>")
    return svg(H, css, "".join(b), "Huizinga F.C. official matchday programme. Manager: Gerrit Huizinga, Indianapolis.")


# ---------------------------------------------------------------- lineup
PLAYERS = [
    (1, "Send Gate", 420, 880, False),
    (2, "DNC Check", 120, 715, False),
    (5, "Hours 8–8", 322, 760, False),
    (4, "No Prices", 518, 760, False),
    (3, "Watchdog", 720, 715, False),
    (8, "Zinga's OS", 175, 545, False),
    (10, "Val", 420, 590, True),
    (6, "Salesforce", 665, 545, False),
    (7, "Daily Briefs", 165, 345, False),
    (9, "Follow-ups", 420, 270, False),
    (11, "Estimator", 675, 345, False),
]


def lineup():
    rnd = random.Random(3)
    H = 1130
    # the passing move: keeper -> defence -> Val -> Zinga's OS -> wing -> striker -> net
    stops = [(432, 868), (530, 748), (432, 578), (187, 533), (177, 333), (432, 258), (420, 106)]
    def tr(p):
        return f"transform:translate({p[0]}px,{p[1]}px)"
    kf = [
        f"0%{{{tr(stops[0])};opacity:0}}", f"3%,6%{{{tr(stops[0])};opacity:1}}",
        f"14%,18%{{{tr(stops[1])}}}", f"28%,32%{{{tr(stops[2])}}}", f"40%,44%{{{tr(stops[3])}}}",
        f"54%,58%{{{tr(stops[4])}}}", f"66%,70%{{{tr(stops[5])}}}",
        f"75%,90%{{{tr(stops[6])};opacity:1}}", f"94%,100%{{{tr(stops[6])};opacity:0}}",
    ]
    css = (
        ".in{animation:runin 1.1s cubic-bezier(.2,.8,.2,1) backwards}"
        "@keyframes runin{from{transform:translate(var(--dx),var(--dy));opacity:0}}"
        ".bob{animation:bob 1.3s ease-in-out infinite alternate}"
        "@keyframes bob{to{transform:translateY(-4px)}}"
        ".ball{animation:play 12s ease-in-out 2.8s infinite backwards}"
        "@keyframes play{" + "".join(kf) + "}"
        ".net{transform-box:fill-box;transform-origin:center bottom;animation:net 12s ease-out 2.8s infinite}"
        "@keyframes net{0%,75%,87%,100%{transform:none}77%{transform:scaleY(1.45)}80%{transform:scaleY(.9)}83%{transform:scaleY(1.2)}}"
        ".goal{opacity:0;animation:goal 12s ease-out 2.8s infinite}"
        "@keyframes goal{0%,75.5%{opacity:0;transform:scale(.4)}78%{opacity:1;transform:scale(1.18)}80%,88%{opacity:1;transform:scale(1)}92%,100%{opacity:0;transform:scale(1)}}"
        ".ants{animation:ants 1.2s linear infinite}"
        "@keyframes ants{to{stroke-dashoffset:-28}}"
        ".ref{animation:ref 9s ease-in-out infinite alternate}"
        "@keyframes ref{from{transform:translate(-120px,10px)}to{transform:translate(110px,-24px)}}"
        ".var{animation:blink 1.2s steps(2,start) infinite}"
        "@keyframes blink{to{opacity:.25}}"
        ".sub{animation:shuf 1.6s ease-in-out infinite alternate}"
        "@keyframes shuf{to{transform:translateX(5px)}}"
    )
    b = ['<rect width="840" height="1130" rx="18" style="fill:var(--bg)"/>',
         '<text class="d" x="40" y="50" font-size="44" letter-spacing="1.5" style="fill:var(--ink)">STARTING XI</text>',
         '<text class="b" x="800" y="46" font-size="18" font-weight="700" text-anchor="end" letter-spacing="1.5" '
         'style="fill:var(--muted)">4-3-3 · MANAGER: G. HUIZINGA</text>',
         '<text class="b" x="40" y="80" font-size="18" style="fill:var(--muted)">'
         "Build from the back: nothing leaves without the keeper's say-so.</text>"]
    # pitch
    b.append('<clipPath id="p"><rect x="40" y="120" width="760" height="820" rx="6"/></clipPath><g clip-path="url(#p)">')
    for i in range(10):
        b.append(f'<rect x="40" y="{120 + i * 82}" width="760" height="82" fill="{P["pitch"] if i % 2 else P["pitch2"]}"/>')
    b.append("</g>")
    line = 'fill="none" stroke="#fff" stroke-opacity=".85" stroke-width="3"'
    b.append(
        f'<rect x="40" y="120" width="760" height="820" rx="6" {line}/>'
        f'<line x1="40" y1="530" x2="800" y2="530" stroke="#fff" stroke-opacity=".85" stroke-width="3"/>'
        f'<circle cx="420" cy="530" r="82" {line}/><circle cx="420" cy="530" r="5" fill="#fff"/>'
        f'<rect x="220" y="120" width="400" height="130" {line}/><rect x="330" y="120" width="180" height="50" {line}/>'
        f'<rect x="220" y="810" width="400" height="130" {line}/><rect x="330" y="890" width="180" height="50" {line}/>'
    )
    # goals
    def goal(y):
        g = f'<rect x="360" y="{y}" width="120" height="24" fill="#fff" fill-opacity=".14" stroke="#fff" stroke-width="3"/>'
        for i in range(1, 8):
            g += f'<line x1="{360 + i * 15}" y1="{y}" x2="{360 + i * 15}" y2="{y + 24}" stroke="#fff" stroke-opacity=".6"/>'
        g += f'<line x1="360" y1="{y + 12}" x2="480" y2="{y + 12}" stroke="#fff" stroke-opacity=".6"/>'
        return g
    b.append(f'<g class="net">{goal(96)}</g>{goal(940)}')
    # passing lanes
    pts = " ".join(f"{x - 12},{y + 12}" for x, y in stops[:-1]) + " 420,120"
    b.append(f'<polyline class="ants" points="{pts}" fill="none" stroke="#fff" stroke-opacity=".5" '
             f'stroke-width="3" stroke-dasharray="4 10" stroke-linecap="round"/>')
    # referee
    b.append(f'<g transform="translate(560,440)"><g class="ref"><circle r="12" fill="#111" stroke="{P["club"]}" stroke-width="3"/></g></g>')
    # players
    for i, (num, name, x, y, cap) in enumerate(PLAYERS):
        tw = len(name) * 11.4 + 22
        badge = (f'<circle cx="21" cy="-21" r="11" fill="{P["club2"]}" stroke="#fff" stroke-width="2"/>'
                 f'<text class="b" x="21" y="-15.500" font-size="15" font-weight="800" text-anchor="middle" fill="#fff">C</text>'
                 if cap else "")
        b.append(
            f'<g transform="translate({x},{y})"><g class="in" style="--dx:{820 - x}px;--dy:{530 - y}px;'
            f'animation-delay:{0.2 + i * .16:.2f}s"><g class="bob" style="animation-delay:{rnd.uniform(0, 1.3):.2f}s">'
            f'<ellipse cx="0" cy="24" rx="20" ry="5" fill="#000" opacity=".22"/>'
            f'<circle r="24" fill="{P["club"]}" stroke="{P["navy"]}" stroke-width="3.5"/>'
            f'<text class="d" y="9" font-size="25" text-anchor="middle" fill="{P["navy"]}">{num}</text>{badge}</g>'
            f'<rect x="{-tw / 2:.1f}" y="33" width="{tw:.1f}" height="30" rx="8" fill="{P["navy"]}" fill-opacity=".92"/>'
            f'<text class="b" y="54.500" font-size="19" font-weight="700" text-anchor="middle" fill="{P["cream"]}">{name}</text>'
            f"</g></g>"
        )
    # goal shout and ball
    b.append(f'<text class="d goal fb" x="420" y="205" font-size="70" text-anchor="middle" fill="{P["club"]}" '
             f'stroke="{P["navy"]}" stroke-width="3" paint-order="stroke" letter-spacing="3">GOAL!</text>')
    b.append(f'<g class="ball" transform="translate({stops[5][0]},{stops[5][1]})">{ball(11)}</g>')
    # legend
    rows = [
        ("REFEREE", "Scoring agent · 80+ to play on, 90+ if it's public"),
        ("VAR", "Security and bug review before any push"),
        ("BENCH", "The rest of the squad of about 25 agents"),
    ]
    for i, (t, d) in enumerate(rows):
        y = 996 + i * 46
        if i == 0:
            icon = f'<circle cx="62" cy="{y - 7}" r="12" fill="#111" stroke="{P["club"]}" stroke-width="3"/>'
        elif i == 1:
            icon = (f'<rect x="46" y="{y - 21}" width="34" height="24" rx="4" fill="#111" stroke="{P["club"]}" stroke-width="3"/>'
                    f'<circle class="var" cx="63" cy="{y - 9}" r="5" fill="{P["club2"]}"/>')
        else:
            icon = "".join(
                f'<circle class="sub" cx="{48 + k * 14}" cy="{y - 7}" r="5.5" fill="{P["club"]}" stroke="{P["navy"]}" '
                f'stroke-width="1.5" style="animation-delay:{k * .25:.2f}s"/>' for k in range(3))
        b.append(
            f'{icon}<text class="d" x="100" y="{y}" font-size="23" letter-spacing="1.2" style="fill:var(--ink)">{t}</text>'
            f'<text class="b" x="212" y="{y - 1}" font-size="19" style="fill:var(--muted)">{d}</text>'
        )
    return svg(H, css, "".join(b),
               "Starting eleven: Send Gate in goal; DNC Check, Hours 8 to 8, No Prices and Watchdog in defence; "
               "Zinga's OS, Val (captain) and Salesforce in midfield; Daily Briefs, Follow-ups and Estimator up front. "
               "Referee: scoring agent. VAR: security and bug review.")


# ---------------------------------------------------------------- scoreboard
def scoreboard():
    H = 290
    led, cream = P["led"], P["cream"]
    css = (
        ".sA{animation:sA 16s linear infinite}.sB{opacity:0;animation:sB 16s linear infinite}"
        "@keyframes sA{0%,46%{opacity:1}49%,97%{opacity:0}100%{opacity:1}}"
        "@keyframes sB{0%,47%{opacity:0}50%,96%{opacity:1}99%,100%{opacity:0}}"
        "@keyframes rA{0%{transform:translateY(0)}9%,100%{transform:translateY(var(--t))}}"
        "@keyframes rB{0%,50%{transform:translateY(0)}59%,100%{transform:translateY(var(--t))}}"
        ".live{animation:live 1s steps(2,start) infinite}"
        "@keyframes live{to{opacity:.2}}"
        ".scan{animation:scan 4s linear infinite}"
        "@keyframes scan{from{transform:translateX(-200px)}to{transform:translateX(900px)}}"
    )
    b = ['<rect width="840" height="290" rx="18" style="fill:var(--bg)"/>',
         '<defs><pattern id="dots" width="5" height="5" patternUnits="userSpaceOnUse">'
         '<rect width="5" height="5" fill="none"/><rect x="4" width="1" height="5" fill="#000" opacity=".35"/>'
         '<rect y="4" width="5" height="1" fill="#000" opacity=".35"/></pattern>'
         '<clipPath id="bd"><rect x="26" y="22" width="788" height="246" rx="14"/></clipPath></defs>',
         f'<rect x="26" y="22" width="788" height="246" rx="14" fill="{P["board"]}" stroke="#33445f" stroke-width="5"/>',
         f'<circle class="live" cx="62" cy="60" r="8" fill="{P["club2"]}"/>'
         f'<text class="m" x="78" y="67" font-size="19" font-weight="700" fill="{P["club2"]}">LIVE</text>']
    a = [f'<text class="m" x="420" y="67" font-size="21" font-weight="700" text-anchor="middle" fill="{cream}" '
         f'letter-spacing="1">RECONCILIATION CUP · FULL TIME</text>',
         f'<text class="m" x="291" y="108" font-size="18" text-anchor="middle" fill="#8ea3bd">ZINGA\'S OS DASHBOARD</text>',
         f'<text class="m" x="655" y="108" font-size="18" text-anchor="middle" fill="#8ea3bd">MISMATCHES</text>',
         rolling("11,761", 140, 194, 84, led, "rA 16s ease-out infinite backwards"),
         f'<text class="m" x="530" y="186" font-size="70" font-weight="700" text-anchor="middle" fill="{cream}">–</text>',
         rolling("0", 630, 194, 84, led, "rA 16s ease-out infinite backwards"),
         f'<text class="m" x="420" y="243" font-size="16.500" text-anchor="middle" fill="#8ea3bd">'
         f'11,761 of 11,761 checks vs Salesforce · 5 regions · 15 reps · 13 months</text>']
    s = [f'<text class="m" x="420" y="67" font-size="21" font-weight="700" text-anchor="middle" fill="{cream}" '
         f'letter-spacing="1">VAL · FIRST WEEK LIVE · OCT 22–29</text>']
    for val, lab, cx in (("24", "TEXTS SENT", 180), ("18", "SENT UNEDITED", 420), ("12", "CUSTOMER REPLIES", 660)):
        s.append(rolling(val, cx - 50, 188, 84, led, "rB 16s ease-out infinite backwards"))
        s.append(f'<text class="m" x="{cx}" y="238" font-size="18" text-anchor="middle" fill="#8ea3bd">{lab}</text>')
    b.append(f'<g class="sA">{"".join(a)}</g><g class="sB">{"".join(s)}</g>')
    b.append('<g clip-path="url(#bd)"><rect x="26" y="22" width="788" height="246" fill="url(#dots)"/>'
             '<rect class="scan" x="0" y="22" width="120" height="246" fill="#fff" opacity=".045" transform="skewX(-18)"/></g>')
    return svg(H, css, "".join(b),
               "Scoreboard. Reconciliation Cup, full time: Zinga's OS dashboard 11,761, mismatches 0. "
               "Val's first week live: 24 texts sent, 18 sent unedited, 12 customer replies.")


# ---------------------------------------------------------------- stats
def stats():
    H = 330
    rows = [("Automated tests", 867), ("Commits to Zinga's OS", 266), ("Meetings remembered", 170),
            ("Work-log entries", 131)]
    css = (
        ".bar{transform-box:fill-box;transform-origin:left center;animation:grow 12s cubic-bezier(.2,.8,.2,1) infinite}"
        "@keyframes grow{0%{transform:scaleX(0)}14%,100%{transform:scaleX(1)}}"
        "@keyframes rS{0%{transform:translateY(0)}14%,100%{transform:translateY(var(--t))}}"
        ".tip{animation:tip 12s cubic-bezier(.2,.8,.2,1) infinite}"
        "@keyframes tip{0%{transform:translateX(calc(var(--w)*-1))}14%,100%{transform:none}}"
        ".rot{animation:rot 2.4s linear infinite}@keyframes rot{to{transform:rotate(360deg)}}"
    )
    b = ['<rect width="840" height="330" rx="18" style="fill:var(--bg)"/>',
         '<text class="d" x="40" y="58" font-size="40" letter-spacing="1.5" style="fill:var(--ink)">SEASON STATS</text>',
         '<text class="b" x="800" y="54" font-size="18" font-weight="700" text-anchor="end" letter-spacing="1.5" '
         'style="fill:var(--muted)">2026 CAMPAIGN</text>']
    for i, (lab, n) in enumerate(rows):
        y = 112 + i * 56
        w = max(40, 380 * n / 867)
        d = f"animation-delay:{i * .25:.2f}s"
        b.append(
            f'<text class="b" x="40" y="{y + 7}" font-size="20" font-weight="600" style="fill:var(--ink)">{lab}</text>'
            f'<rect x="280" y="{y - 13}" width="380" height="26" rx="13" style="fill:var(--bg2)"/>'
            f'<rect class="bar" x="280" y="{y - 13}" width="{w:.0f}" height="26" rx="13" fill="{P["club"]}" style="{d}"/>'
            f'<g transform="translate({280 + w:.0f},{y})"><g class="tip" style="--w:{w:.0f}px;{d}">'
            f'<g class="rot fb">{ball(15)}</g></g></g>'
        )
        b.append(f'<g style="color:inherit">{rolling(str(n), 700, y + 12, 34, "currentColor", "rS 12s ease-out infinite backwards")}</g>')
    body = "".join(b).replace('fill="currentColor"', 'style="fill:var(--ink)"')
    return svg(H, css, body,
               "Season stats: 867 automated tests, 266 commits to Zinga's OS, 170 meetings remembered, 131 work-log entries.")


# ---------------------------------------------------------------- ticker
def ticker():
    H = 56
    items = [
        "INJURY REPORT: 26-hour outage traced to a memory leak, squad back to full fitness",
        "TRANSFER NEWS: manager open to offers in AI solutions and deployment",
        "TEAM NEWS: 867 automated tests named in the squad",
        "TRAINING GROUND: 131 work-log entries and counting",
        "DISCIPLINE: no prices, complaints or cancellations ever sent on auto",
    ]
    text = "  ●  ".join(items) + "  ●"
    width = len(text) * 11.5
    css = (
        f".t{{animation:tick 48s linear infinite}}"
        f"@keyframes tick{{from{{transform:translateX(700px)}}to{{transform:translateX(-{width:.0f}px)}}}}"
        ".live{animation:live 1s steps(2,start) infinite}@keyframes live{to{opacity:.3}}"
    )
    b = (
        f'<defs><clipPath id="k"><rect x="128" y="0" width="712" height="56"/></clipPath>'
        f'<clipPath id="r"><rect width="840" height="56" rx="12"/></clipPath></defs>'
        f'<g clip-path="url(#r)"><rect width="840" height="56" fill="{P["board"]}"/>'
        f'<g clip-path="url(#k)"><text class="m t" x="140" y="35" font-size="19" font-weight="700" '
        f'fill="{P["led"]}" xml:space="preserve">{text}</text></g>'
        f'<rect width="128" height="56" fill="{P["club2"]}"/>'
        f'<circle class="live" cx="22" cy="28" r="6" fill="#fff"/>'
        f'<text class="d" x="38" y="37" font-size="24" fill="#fff" letter-spacing="1.5">LATEST</text></g>'
    )
    return svg(H, css, b, "Club news: " + ". ".join(items) + ".")


# ---------------------------------------------------------------- divider
def divider():
    H = 44
    css = (
        ".go{animation:go 8s linear infinite}@keyframes go{from{transform:translateX(-460px)}to{transform:translateX(460px)}}"
        ".hop{animation:hop .45s ease-out infinite alternate}@keyframes hop{to{transform:translateY(-9px)}}"
        ".rot{animation:rot 1s linear infinite}@keyframes rot{to{transform:rotate(360deg)}}"
        ".step{animation:hop .3s ease-out infinite alternate}"
    )
    b = (
        '<line x1="0" y1="36" x2="840" y2="36" stroke-width="3" stroke-dasharray="14 8" style="stroke:var(--muted)" opacity=".6"/>'
        f'<g transform="translate(420,26)"><g class="go">'
        f'<g class="step"><circle cx="-30" cy="-2" r="9" fill="{P["club"]}" stroke="{P["navy"]}" stroke-width="2.5"/></g>'
        f'<g class="hop"><g class="rot fb">{ball(8)}</g></g></g></g>'
    )
    return svg(H, css, b, "A player dribbling a ball along the touchline")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name, fn in (("banner", banner), ("lineup", lineup), ("scoreboard", scoreboard), ("stats", stats),
                     ("ticker", ticker), ("divider", divider)):
        data = fn()
        (OUT / f"{name}.svg").write_text(data, encoding="utf-8")
        print(f"{name}.svg  {len(data) / 1024:.1f} KB")
