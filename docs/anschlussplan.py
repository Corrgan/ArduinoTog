"""Anschlussplan Betty-Wandler für die Werkstatt (einfach, druckbar) → anschlussplan.svg/.png/.pdf"""
W, H = 1240, 1754   # A4 hoch @150 dpi
TXT, MUT, LINE = "#1a1a19", "#5f5e58", "#1a1a19"
C = {"rot": "#d0342c", "schwarz": "#222222", "blau": "#2a78d6", "gruen": "#1baf7a", "orange": "#eb6834", "lila": "#8e5bd0", "gelb": "#c99a00", "grau": "#7a7a74"}
o = [f'<rect width="{W}" height="{H}" fill="#ffffff"/>']


def t(x, y, s, size=26, w="400", fill=TXT, anchor="start"):
    o.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}">{s}</text>')


def box(x, y, w, h, title, sub="", fill="#f4f3ef", stroke=LINE):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="3"/>')
    t(x + w / 2, y + 42, title, 30, "700", anchor="middle")
    if sub:
        t(x + w / 2, y + 76, sub, 20, "400", MUT, "middle")


def kabel(pts, farbe, label=None, lx=None, ly=None, dash=""):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    o.append(f'<path d="{d}" fill="none" stroke="{farbe}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"{da}/>')
    if label:
        o.append(f'<rect x="{lx-6}" y="{ly-24}" width="{len(label)*12+12}" height="32" rx="6" fill="#ffffff" opacity="0.9"/>')
        t(lx, ly, label, 21, "600", farbe)


def klemme(x, y, namen, farben, titel):
    t(x + 2 * 70, y - 16, titel, 22, "700", anchor="middle")
    for i, (n, f) in enumerate(zip(namen, farben)):
        o.append(f'<rect x="{x + i*70}" y="{y}" width="62" height="62" rx="8" fill="#ffffff" stroke="{f}" stroke-width="5"/>')
        o.append(f'<circle cx="{x + i*70 + 31}" cy="{y + 31}" r="12" fill="#cfcfc8" stroke="{LINE}" stroke-width="2"/>')
        t(x + i * 70 + 31, y + 92, n, 20, "700", f, "middle")


t(60, 80, "Betty-Wandler – Anschlussplan", 46, "700")
t(60, 122, "Tankanzeige + Öltemperatur/TOG + ABS-Leuchte · VW T3 Syncro mit Audi-A6-Kombi", 24, "400", MUT)

# Wandler in der Mitte
box(420, 620, 400, 520, "", "", "#eef4fc", C["blau"])
t(620, 880, "BETTY-WANDLER", 34, "700", anchor="middle")
t(620, 915, "Arduino Nano · USB nach links", 20, "400", MUT, "middle")
klemme(450, 1030, ["ÖL", "GEBER", "GND", "+12V"], [C["gelb"], C["gruen"], C["schwarz"], C["rot"]], "")
t(620, 1006, "Klemme UNTEN", 22, "700", anchor="middle")
klemme(450, 680, ["A", "B", "TOG", "ABS"], [C["orange"], C["grau"], C["lila"], C["blau"]], "")
t(620, 668, "Klemme OBEN", 20, "700", C["blau"], "middle")
t(519, 790, "└── TANK ──┘", 20, "600", C["orange"], "middle")

# Auto-Seite unten
box(60, 1330, 300, 150, "Öltemperatur-Fühler", "am Ölfilterflansch")
box(400, 1330, 280, 150, "Tankgeber T3", "im Tank (alter Geber)")
box(720, 1330, 220, 150, "Masse", "Karosserie / Kl. 31")
box(980, 1330, 200, 150, "+12 V", "Zündungsplus Kl. 15")
# Kabel unten
kabel([(481, 1092), (481, 1180), (210, 1180), (210, 1330)], C["gelb"], "ÖL", 230, 1172)
kabel([(551, 1092), (551, 1330)], C["gruen"], "GEBER", 560, 1250)
kabel([(621, 1092), (621, 1230), (830, 1230), (830, 1330)], C["schwarz"], "GND", 700, 1222)
kabel([(691, 1092), (691, 1200), (1080, 1200), (1080, 1330)], C["rot"], "+12 V (Sicherung 1 A)", 860, 1192)

# Kombi oben
box(260, 190, 720, 300, "Kombiinstrument Audi A6 (C5)", "Stecker hinten am Kombi")
for i, (n, f, lbl) in enumerate([(0, C["orange"], "Tankgeber Eingang"), (1, C["grau"], "Masse (Kl. 31)"),
                                  (2, C["lila"], "Öltemp. (TOG)"), (3, C["blau"], "ABS Warnlampe")]):
    x = 300 + i * 170
    o.append(f'<rect x="{x}" y="300" width="150" height="150" rx="10" fill="#ffffff" stroke="{f}" stroke-width="4"/>')
    for j, ln in enumerate(lbl.split(" ")):
        t(x + 75, 360 + j * 30, ln, 20, "600", f, "middle")
kabel([(481, 680), (481, 560), (375, 560), (375, 450)], C["orange"], "A", 392, 552)
kabel([(551, 680), (551, 580), (545, 580), (545, 450)], C["grau"], "B", 560, 572)
kabel([(621, 680), (621, 560), (715, 560), (715, 450)], C["lila"], "TOG", 640, 552)
kabel([(691, 680), (691, 600), (885, 600), (885, 450)], C["blau"], "ABS", 900, 592)

# Schritte
y = 1540
t(60, y, "So geht's – Schritt für Schritt", 30, "700"); y += 40
schritte = [
    "1. Batterie abklemmen.",
    "2. Das EINE Geberkabel auftrennen: Kombi-Seite → A, Geber-Seite → GEBER. B → Masse.",
    "   Alten ArduinoTog-Nano ausbauen; seine Leitungen → ÖL, TOG, ABS.",
    "3. +12 V (Zündungsplus, mit 1-A-Sicherung) und GND (Masse) anklemmen. Aderendhülsen verwenden!",
    "4. Batterie dran, Zündung an. Per USB am Laptop einmessen (LIESMICH: ohm / hier / speichern).",
    "Geber-Masse bleibt wie sie ist an der Karosserie. B: an Masse (oder an einen Masse-Pin des Kombis).",
]
for s in schritte:
    t(60, y, s, 21, "400", TXT if not s.startswith("Tipp") else MUT); y += 32

open(__import__("os").path.join(__import__("os").path.dirname(__file__), "anschlussplan.svg"), "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="DejaVu Sans, sans-serif">' + "\n".join(o) + "</svg>")
