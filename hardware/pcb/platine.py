"""Betty-Wandler: Platine per pcbnew-Skript (Platzierung + Leiterbahnen von Hand), KiCad 9.  → betty-wandler.kicad_pcb
Netze/Belegung (22.11.2026):
  Tank:  Geber → R1 150Ω Pull-up (+5V), R2 10k + C4 100n → A2; D3 TVS.   Kette K1..K8 (PhotoMOS) über RC1..RC8 → X2 A/B
  Öl:    Fühler → R3 1k Pull-up, R4 10k + C5 100n → A1 (wie ArduinoTog); D4 TVS
  TOG:   D6 → R5 1k → X2/3 (wie ArduinoTog direkt, Strom begrenzt)
  ABS:   D5 → R6 100Ω → Q1 2N7002 (Drain → X2/4, zieht Leitung nach Masse; Code: D5 HIGH = Warnung unterdrückt)
  Versorgung: X1 +12V → F1 PTC → D1 SS34 → D2 TVS, C1 → U1 L78M05 → +5V (C2, C3) → Nano 5V
Relais-Steuerung: D2,D3,D4,D7,D8,D9,D10,D11 (D5/D6 frei für ArduinoTog).
"""
import pcbnew
from pcbnew import VECTOR2I, FromMM as MM, ToMM

B = pcbnew.BOARD()
FP = "/usr/share/kicad/footprints/%s.pretty"
NETS = {}


def net(n):
    if n not in NETS:
        ni = pcbnew.NETINFO_ITEM(B, n); B.Add(ni); NETS[n] = ni
    return NETS[n]


def place(ref, lib, name, x, y, rot=0, value="", side="F"):
    f = pcbnew.FootprintLoad(FP % lib, name)
    f.SetReference(ref); f.SetValue(value or name)
    f.SetPosition(VECTOR2I(MM(x), MM(y))); f.SetOrientationDegrees(rot)
    B.Add(f)
    return f


def pad(f, num):
    for p in f.Pads():
        if p.GetNumber() == str(num):
            return p
    raise KeyError((f.GetReference(), num))


def P(f, num):
    p = pad(f, num).GetPosition(); return (ToMM(p.x), ToMM(p.y))


def setnet(f, num, n):
    pad(f, num).SetNet(net(n))


def track(n, pts, w=0.4, layer=pcbnew.F_Cu):
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        t = pcbnew.PCB_TRACK(B); t.SetStart(VECTOR2I(MM(x1), MM(y1))); t.SetEnd(VECTOR2I(MM(x2), MM(y2)))
        t.SetWidth(MM(w)); t.SetLayer(layer); t.SetNet(net(n)); B.Add(t)


def via(n, x, y):
    v = pcbnew.PCB_VIA(B); v.SetPosition(VECTOR2I(MM(x), MM(y))); v.SetDrill(MM(0.4)); v.SetWidth(MM(0.8))
    v.SetNet(net(n)); B.Add(v)


def gndvia(f, num, dx=0, dy=0):
    x, y = P(f, num); vx, vy = x + dx, y + dy
    if dx or dy:
        track("GND", [(x, y), (vx, vy)], 0.5)
    via("GND", vx, vy)


# ---------------- Platine ----------------
X0, Y0, X1E, Y1E = 5, 0, 81, 92
r = pcbnew.PCB_SHAPE(B); r.SetShape(pcbnew.SHAPE_T_RECT); r.SetLayer(pcbnew.Edge_Cuts); r.SetWidth(MM(0.1))
r.SetStart(VECTOR2I(MM(X0), MM(Y0))); r.SetEnd(VECTOR2I(MM(X1E), MM(Y1E))); B.Add(r)
for i, (hx, hy) in enumerate([(40.0, 71.0), (X1E - 3.5, 88.5), (X1E - 3.5, 3.5), (X1E - 4.0, 50.0)]):
    place(f"H{i+1}", "MountingHole", "MountingHole_3.2mm_M3", hx, hy)

# ---------------- Nano-Sockel ----------------
YA, YB = 42.0, 42.0 + 15.24
JA = place("J3", "Connector_PinSocket_2.54mm", "PinSocket_1x15_P2.54mm_Vertical", 45.0, YA, 270, "Nano 1-15")
JB = place("J4", "Connector_PinSocket_2.54mm", "PinSocket_1x15_P2.54mm_Vertical", 45.0 - 14 * 2.54, YB, 90, "Nano 16-30")
nano = lambda n: (JA, n) if n <= 15 else (JB, n - 15)
for n, netn in {4: "GND", 29: "GND", 27: "+5V", 20: "A1", 21: "A2", 8: "D5", 9: "D6",
                5: "D2", 6: "D3", 7: "D4", 10: "D7", 11: "D8", 12: "D9", 13: "D10", 14: "D11"}.items():
    f, k = nano(n); setnet(f, k, netn)
NP = lambda n: P(*nano(n))

# ---------------- Relais-Kette ----------------
REL_X = [10, 19, 28, 37, 46, 55, 64, 73]
DRV = ["D11", "D10", "D9", "D8", "D7", "D4", "D3", "D2"]          # links → rechts
DRV_PIN = {"D2": 5, "D3": 6, "D4": 7, "D7": 10, "D8": 11, "D9": 12, "D10": 13, "D11": 14}
RVAL = {"D2": "2R0", "D3": "3R9", "D4": "8R2", "D7": "16R", "D8": "33R", "D9": "62R", "D10": "130R", "D11": "270R"}
YC, YK = 17.0, 22.4
YR = YK + 3.19 + 3.0
LEVEL = {"D2": 1, "D3": 2, "D4": 3, "D7": 4, "D8": 5, "D9": 6, "D10": 7, "D11": 1}
Ly = lambda k: YA - 2.6 - (k - 1) * 1.4
chain = []
for i, (x, d) in enumerate(zip(REL_X, DRV)):
    K = place(f"K{i+1}", "Package_SO", "SOP-4_4.4x2.6mm_P1.27mm", x, YK, 90, "AQY212GS")
    RC = place(f"RC{i+1}", "Resistor_SMD", "R_1206_3216Metric", x, YC, 0, RVAL[d])
    RL = place(f"RL{i+1}", "Resistor_SMD", "R_0805_2012Metric", x - 0.64, YR, 90, "470R")
    a, b = f"KETTE{i}", f"KETTE{i+1}"
    setnet(RC, 1, a); setnet(RC, 2, b); setnet(K, 4, a); setnet(K, 3, b)
    rl_top = 1 if P(RL, 1)[1] < P(RL, 2)[1] else 2
    setnet(K, 1, f"LED_{d}"); setnet(K, 2, "GND"); setnet(RL, rl_top, f"LED_{d}"); setnet(RL, 3 - rl_top, d)
    track(a, [P(K, 4), (P(K, 4)[0], P(K, 4)[1] - 0.9), P(RC, 1)])
    track(b, [P(K, 3), (P(K, 3)[0], P(K, 3)[1] - 0.9), P(RC, 2)])
    pl = P(RL, 1) if P(RL, 1)[1] < P(RL, 2)[1] else P(RL, 2)          # oberes RL-Pad → Relais-Pin 1
    track(f"LED_{d}", [P(K, 1), pl])
    gndvia(K, 2, 1.4, 1.2)
    # Ansteuerung vom Nano-Pin über Ebene
    px, py = NP(DRV_PIN[d]); lx = P(RL, 2)[0]; low = P(RL, 2) if P(RL, 2)[1] > P(RL, 1)[1] else P(RL, 1)
    track(d, [(px, py), (px, Ly(LEVEL[d])), (lx, Ly(LEVEL[d])), low])
    chain.append(RC)
# Ketten-Verbindungen
for i in range(7):
    track(f"KETTE{i+1}", [P(chain[i], 2), P(chain[i + 1], 1)])

# ---------------- Klemme X2 oben: Kombi A, Kombi B, TOG, ABS ----------------
TB4 = "TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal"
X2 = place("X2", "TerminalBlock_Phoenix", TB4, 10 + 3 * 5.08, 6.5, 180, "Kombi A|B|TOG|ABS")
# bei 180° läuft die Klemme nach links → Pin-Positionen aus dem Footprint lesen
x2 = {n: P(X2, n) for n in (1, 2, 3, 4)}
order = sorted(x2, key=lambda n: x2[n][0])          # links → rechts
KA, KB, TOG, ABS = order
setnet(X2, KA, "KETTE0"); setnet(X2, KB, "KETTE8"); setnet(X2, TOG, "TOG"); setnet(X2, ABS, "ABS")
ka, kb, tg, ab = x2[KA], x2[KB], x2[TOG], x2[ABS]
c0 = P(chain[0], 1); c8 = P(chain[7], 2)
track("KETTE0", [c0, (c0[0] - 1.4, c0[1]), (c0[0] - 1.4, ka[1] + 3.5), (ka[0], ka[1] + 3.5), ka], 0.5)
yb = 14.6
track("KETTE8", [c8, (c8[0] + 3.5, c8[1]), (c8[0] + 3.5, yb), (kb[0], yb), kb], 0.5)

# TOG / ABS
R5 = place("R5", "Resistor_SMD", "R_0805_2012Metric", 40, 3.0, 0, "1k")
setnet(R5, 1, "TOG"); setnet(R5, 2, "D6")
track("TOG", [P(R5, 1), (tg[0], P(R5, 1)[1]), tg])
Q1 = place("Q1", "Package_TO_SOT_SMD", "SOT-23", 47, 9.0, 180, "2N7002")
R6 = place("R6", "Resistor_SMD", "R_0805_2012Metric", 43, 12.3, 0, "100R")
R7 = place("R7", "Resistor_SMD", "R_0805_2012Metric", 49.5, 12.3, 0, "100k")
# SOT-23: 1=G 2=S 3=D
setnet(Q1, 1, "GATE"); setnet(Q1, 2, "GND"); setnet(Q1, 3, "ABS")
setnet(R6, 2, "GATE"); setnet(R6, 1, "D5"); setnet(R7, 1, "GATE"); setnet(R7, 2, "GND")
g = P(Q1, 1); d_ = P(Q1, 3); s = P(Q1, 2)
track("GATE", [g, (g[0], P(R6, 2)[1]), P(R6, 2)])
track("GATE", [(g[0], P(R7, 1)[1]), P(R7, 1)])
gndvia(R7, 2, 1.3, 0); gndvia(Q1, 2, 1.4, 0)
track("ABS", [d_, (d_[0], ab[1]), ab])
# D5/D6 von den Nano-Pins auf der Unterseite nach oben
for n, nn, tx in ((9, "D6", P(R5, 2)), (8, "D5", P(R6, 1))):
    px, py = NP(n); vx, vy = (tx[0] + 1.6, tx[1]) if nn == "D6" else (tx[0] - 1.6, tx[1])
    track(nn, [tx, (vx, vy)])
    via(nn, vx, vy)
    if nn == "D6":   # D6 läuft oberhalb des D5-Vias nach rechts → keine Kreuzung
        track(nn, [(px, py), (px, 10.0), (vx, 10.0), (vx, vy)], 0.4, pcbnew.B_Cu)
    else:
        track(nn, [(px, py), (px, 14.0), (vx, 14.0), (vx, vy)], 0.4, pcbnew.B_Cu)

# ---------------- Versorgung (rechts unten) ----------------
TB4b = "TerminalBlock_Phoenix_MKDS-1,5-4-5.08_1x04_P5.08mm_Horizontal"
X1 = place("X1", "TerminalBlock_Phoenix", TB4b, 14, 85.5, 0, "Oel|Geber|GND|+12V")
x1 = {n: P(X1, n) for n in (1, 2, 3, 4)}
o1 = sorted(x1, key=lambda n: x1[n][0])
OEL_T, GEB_T, GND_T, V12_T = o1
setnet(X1, OEL_T, "OEL"); setnet(X1, GEB_T, "GEBER"); setnet(X1, GND_T, "GND"); setnet(X1, V12_T, "+12V")
F1 = place("F1", "Fuse", "Fuse_1812_4532Metric", 37, 81, 0, "PTC 0.5A")
D1 = place("D1", "Diode_SMD", "D_SMA", 44.5, 81, 180, "SS34")
D2 = place("D2", "Diode_SMD", "D_SMB", 50.5, 80, 90, "SMBJ24A")
C1 = place("C1", "Capacitor_SMD", "C_1206_3216Metric", 55, 80, 90, "10u 50V")
U1 = place("U1", "Package_TO_SOT_SMD", "TO-252-2", 60, 70, 180, "L78M05")
C2 = place("C2", "Capacitor_SMD", "C_1206_3216Metric", 70, 66, 90, "10u 25V")
C3 = place("C3", "Capacitor_SMD", "C_0805_2012Metric", 74, 66, 90, "100n")
setnet(F1, 1, "+12V"); setnet(F1, 2, "12V_F")
setnet(D1, 2, "12V_F"); setnet(D1, 1, "12V_P")           # Pad 2 = Anode
setnet(D2, 1, "12V_P"); setnet(D2, 2, "GND")
for c, top in ((C1, "12V_P"), (C2, "+5V"), (C3, "+5V")):
    pa, pb = P(c, 1), P(c, 2)
    hi, lo = (1, 2) if pa[1] > pb[1] else (2, 1)         # hi = unteres Pad
    setnet(c, hi, top); setnet(c, lo, "GND")
setnet(U1, 1, "12V_P"); setnet(U1, 3, "+5V"); setnet(U1, 2, "GND")
v = x1[V12_T]
track("+12V", [v, (v[0], P(F1, 1)[1]), P(F1, 1)], 0.8)
track("12V_F", [P(F1, 2), P(D1, 2)], 0.8)
d1k = P(D1, 1)
d2k = P(D2, 1)
track("12V_P", [d1k, (d2k[0], d1k[1]), d2k], 0.8)
c1p = [P(C1, n) for n in (1, 2) if pad(C1, n).GetNetname() == "12V_P"][0]
c1g = [n for n in (1, 2) if pad(C1, n).GetNetname() == "GND"][0]
track("12V_P", [(d2k[0], d1k[1]), (c1p[0], d1k[1]), c1p], 0.8)
uin = P(U1, 1); uout = P(U1, 3)
track("12V_P", [(c1p[0], d1k[1]), (uin[0] + 2.5, d1k[1]), (uin[0] + 2.5, uin[1]), uin], 0.8)
gndvia(D2, 2, 0, -1.4); gndvia(C1, c1g, 0, -1.3)
tab = P(U1, 2); via("GND", tab[0] - 1.5, tab[1] - 1.5); via("GND", tab[0] - 1.5, tab[1] + 1.5); via("GND", tab[0] + 1.0, tab[1])
for c in (C2, C3):
    pp = [P(c, n) for n in (1, 2) if pad(c, n).GetNetname() == "+5V"][0]
    gn = [n for n in (1, 2) if pad(c, n).GetNetname() == "GND"][0]
    track("+5V", [uout, (pp[0], uout[1]), pp], 0.8)
    gndvia(c, gn, 0, -1.3)
y5 = 61.0
track("+5V", [uout, (uout[0], y5), (NP(27)[0], y5), NP(27)], 0.8)
y5b = 62.6
track("+5V", [(NP(27)[0], y5), (30.0, y5), (30.0, y5b)], 0.6)
via("+5V", 30.0, y5b)
track("+5V", [(30.0, y5b), (8.0, y5b)], 0.6, pcbnew.B_Cu)
via("+5V", 8.0, y5b)

# ---------------- Eingänge (links unten) ----------------
# Öl: A1 (Pin 20) → R4 → OEL;  Tank: A2 (Pin 21) → R2 → GEBER
a1, a2 = NP(20), NP(21)
R4 = place("R4", "Resistor_SMD", "R_0805_2012Metric", a1[0], 64.0, 90, "10k")
R2 = place("R2", "Resistor_SMD", "R_0805_2012Metric", a2[0], 64.0, 90, "10k")
top_ = lambda f: 1 if P(f, 1)[1] < P(f, 2)[1] else 2
bot_ = lambda f: 2 if top_(f) == 1 else 1
setnet(R4, top_(R4), "A1"); setnet(R4, bot_(R4), "OEL")
setnet(R2, top_(R2), "A2"); setnet(R2, bot_(R2), "GEBER")
track("A1", [a1, P(R4, top_(R4))]); track("A2", [a2, P(R2, top_(R2))])
C5 = place("C5", "Capacitor_SMD", "C_0805_2012Metric", a1[0] - 3.2, 60.2, 0, "100n")
C4 = place("C4", "Capacitor_SMD", "C_0805_2012Metric", a2[0] + 3.2, 60.2, 0, "100n")
setnet(C5, 2, "A1"); setnet(C5, 1, "GND"); setnet(C4, 1, "A2"); setnet(C4, 2, "GND")
track("A1", [P(C5, 2), (a1[0], P(C5, 2)[1])]); track("A2", [P(C4, 1), (a2[0], P(C4, 1)[1])])
gndvia(C5, 1, -1.2, 0); gndvia(C4, 2, 1.2, 0)
# Pull-ups
R3 = place("R3", "Resistor_SMD", "R_0805_2012Metric", 8.0, 65.6, 90, "1k")
setnet(R3, top_(R3), "+5V"); setnet(R3, bot_(R3), "OEL")
track("+5V", [(8.0, y5b), P(R3, top_(R3))], 0.5)
oel = P(R4, bot_(R4)); yo = oel[1] + 1.6
track("OEL", [oel, (oel[0], yo), (11.0, yo), (11.0, 79.0), (x1[OEL_T][0], 81.0), x1[OEL_T]])
track("OEL", [P(R3, bot_(R3)), (8.0, yo), (11.0, yo)])
R1 = place("R1", "Resistor_SMD", "R_1206_3216Metric", 27.0, 70.0, 0, "150R")
setnet(R1, 1, "GEBER"); setnet(R1, 2, "+5V")
geb = P(R2, bot_(R2))
track("GEBER", [geb, (geb[0], P(R1, 1)[1]), P(R1, 1)])
track("GEBER", [(geb[0], P(R1, 1)[1]), (geb[0], 76.0), (x1[GEB_T][0], 79.0), x1[GEB_T]])
track("+5V", [P(R1, 2), (30.0, P(R1, 2)[1]), (30.0, y5b)], 0.5)
D3 = place("D3", "Diode_SMD", "D_SMA", 18.6, 74.0, 90, "SMAJ5.0A")
D4 = place("D4", "Diode_SMD", "D_SMA", 7.6, 73.0, 90, "SMAJ5.0A")
for D, n_, lx in ((D3, "GEBER", geb[0]), (D4, "OEL", 11.0)):
    k1, k2 = P(D, 1), P(D, 2)
    kpad = 1
    setnet(D, kpad, n_); setnet(D, 2, "GND")
    track(n_, [P(D, kpad), (lx, P(D, kpad)[1])])
    gndvia(D, 2, 0, -1.4 if P(D, 2)[1] < P(D, 1)[1] else 1.4)

# ---------------- Masseflächen ----------------
for layer in (pcbnew.B_Cu, pcbnew.F_Cu):
    z = pcbnew.ZONE(B); z.SetLayer(layer); z.SetNet(net("GND")); z.SetIsFilled(False)
    z.SetLocalClearance(MM(0.3)); z.SetMinThickness(MM(0.25))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
    ol = z.Outline(); ol.NewOutline()
    for px_, py_ in ((X0 + 0.5, Y0 + 0.5), (X1E - 0.5, Y0 + 0.5), (X1E - 0.5, Y1E - 0.5), (X0 + 0.5, Y1E - 0.5)):
        ol.Append(MM(px_), MM(py_))
    B.Add(z)

# Beschriftung
def text(s, x, y, size=1.2, layer=pcbnew.F_SilkS):
    t = pcbnew.PCB_TEXT(B); t.SetText(s); t.SetPosition(VECTOR2I(MM(x), MM(y))); t.SetLayer(layer)
    t.SetTextSize(VECTOR2I(MM(size), MM(size))); t.SetTextThickness(MM(size * 0.15)); B.Add(t)
text("BETTY-WANDLER v1  Tank + Oel/TOG", 43, 90.3, 1.0)
for n_, lbl in zip(o1, ("OEL", "GEBER", "GND", "+12V")):
    text(lbl, x1[n_][0], 79.6, 1.0)
for n_, lbl in zip(order, ("TANK-A", "TANK-B", "TOG", "ABS")):
    text(lbl, x2[n_][0], 13.2, 0.9)
text("<- USB  Nano: Bauteile oben", 26, 49.6, 1.2)
text("D12 ... D2 GND RST RX TX", 27, 44.6, 0.8)
text("D13 3V3 REF A0..A7 5V RST GND VIN", 27, 54.8, 0.8)

ds = B.GetDesignSettings(); ds.SetCopperLayerCount(2)
# Zonen füllt kicad-cli drc --refill-zones --save-board (Fill im Skript stürzt ab)
B.Save(__import__("os").path.join(__import__("os").path.dirname(__file__), "betty-wandler.kicad_pcb"))
print("gespeichert")
