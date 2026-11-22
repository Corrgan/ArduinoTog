"""Schaltplan-Übersicht Betty-Wandler (Tank + TOG/Öltemperatur) als SVG → schaltplan.png (22.11.2026, Entwurf 1)."""
W, H = 1500, 1000
TXT, MUT, LINE, ACC = "#1a1a19", "#6b6a64", "#1a1a19", "#2a78d6"
o = [f'<rect width="{W}" height="{H}" fill="#fcfcfb"/>',
     f'<text x="30" y="42" font-size="28" font-weight="700" fill="{TXT}">Betty-Wandler – Schaltplan Entwurf 1 (Tankgeber + Öltemperatur/TOG)</text>',
     f'<text x="30" y="70" font-size="16" fill="{MUT}">Arduino Nano gesteckt · JLCPCB bestückt · Werte/Teile vorläufig, Pinbelegung D5/D6/A1 wie ArduinoTog</text>']


def box(x, y, w, h, title, lines, col=LINE):
    o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#ffffff" stroke="{col}" stroke-width="2"/>')
    o.append(f'<text x="{x+12}" y="{y+26}" font-size="18" font-weight="600" fill="{TXT}">{title}</text>')
    for i, l in enumerate(lines):
        o.append(f'<text x="{x+12}" y="{y+52+i*22}" font-size="15" fill="{TXT}">{l}</text>')


def wire(pts, label=None, col=LINE, at=0.5):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    o.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="2"/>')
    if label:
        (x1, y1), (x2, y2) = pts[0], pts[1]
        o.append(f'<text x="{x1+(x2-x1)*at+4}" y="{y1+(y2-y1)*at-6}" font-size="14" fill="{MUT}">{label}</text>')


# Klemmen
box(30, 110, 230, 200, "X1 Klemme Eingang", ["1  +12 V (Zündung, Kl. 15)", "2  Masse (Kl. 31)", "3  Tankgeber T3", "4  Öltemperatur-Fühler"])
box(30, 700, 230, 200, "X2 Klemme Ausgang", ["1  Kombi Tank A", "2  Kombi Tank B", "3  TOG-Signal → Kombi", "4  D5 (IMMER, LOW)"])

# Versorgung
box(330, 110, 360, 210, "Versorgung", ["F1  PTC 500 mA (1812)", "D1  SS34 Verpolschutz", "D2  SMBJ24A TVS (Lastabwurf)", "C1  10 µF/50 V", "U1  L78M05 (TO-252) → +5 V", "C2/C3  10 µF + 100 nF"])
wire([(260, 165), (330, 165)], "+12V")

# Nano
box(760, 300, 300, 400, "Arduino Nano (Sockel)", ["+5V  ← U1 (Pin 27)", "GND  (Pin 4, 29)", "A0   ← Tankgeber", "A1   ← Öltemperatur", "D2–D4, D7–D11 → 8 Relais", "D6   → TOG-Ausgang", "D5   → IMMER (LOW)", "USB  zum Programmieren", "      und Kalibrieren"], ACC)
wire([(690, 215), (910, 215), (910, 300)], "+5V")

# Eingänge
box(330, 380, 360, 150, "Eingang Tankgeber", ["R1 150 Ω nach +5 V (Geber nach Masse)", "R2 10 kΩ + C4 100 nF → A0", "D3 SMAJ5.0CA Schutz"])
wire([(260, 205), (300, 205), (300, 450), (330, 450)], "Geber")
wire([(690, 450), (760, 450)], "A0")
box(330, 560, 360, 120, "Eingang Öltemperatur", ["R3 1 kΩ nach +5 V (wie ArduinoTog)", "R4 10 kΩ + C5 100 nF → A1", "D4 SMAJ5.0CA Schutz"])
wire([(260, 225), (285, 225), (285, 620), (330, 620)], "Öl")
wire([(690, 620), (760, 620)], "A1")

# Relais-Kette
box(1130, 110, 340, 560, "Widerstands-Kette Tank", ["8 Widerstände in Reihe:", "2,0 · 3,9 · 8,2 · 16 Ω", "33 · 62 · 130 · 270 Ω", "= 0 … ~525 Ω einstellbar", "", "jeder überbrückt von einem", "PhotoMOS-Relais K1–K8", "(AQY212GS, SOP-4, Ron ≈ 1 Ω)", "", "Relais-LED: Arduino-Pin", "→ 470 Ω → LED → Masse", "", "Kombi sieht zwischen A und B", "genau den gewählten Widerstand,", "galvanisch getrennt vom Arduino"], ACC)
wire([(1060, 400), (1130, 400)], "8× Steuer")
wire([(1300, 670), (1300, 760), (260, 760)], "Tank A/B")

# TOG
box(330, 720, 360, 150, "TOG-Ausgang (ArduinoTog)", ["D6 → R5 220 Ω → X2/3", "(optional Transistor-Bestückung,", " je nach Kombi-Eingang – offen)", "D5 → R6 220 Ω → X2/4"])
wire([(760, 650), (720, 650), (720, 790), (690, 790)], "D5/D6")
wire([(330, 800), (260, 800)])

o.append(f'<text x="30" y="960" font-size="15" fill="{MUT}">Offen: Funktion D5, TOG direkt oder über Transistor, Typ/Widerstand Ölfühler, Widerstandsbereiche Tankgeber/Kombi (per Kalibrier-Modus einmessbar).</text>')
open(__import__("os").path.join(__import__("os").path.dirname(__file__), "schaltplan.svg"), "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="DejaVu Sans, sans-serif">' + "\n".join(o) + "</svg>")
