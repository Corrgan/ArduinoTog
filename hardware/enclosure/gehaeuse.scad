// Gehäuse Betty-Wandler v1 (Platine 76 × 92 mm) – Unterteil + Deckel mit Lüftungsschlitzen. 22.11.2026
// teil = "unterteil" | "deckel" | "alles"
teil = "alles";
$fn = 40;

pcb_w = 76; pcb_h = 92; pcb_t = 1.6;
spalt = 1.0; wand = 2.2; boden = 2.0;
in_w = pcb_w + 2*spalt; in_h = pcb_h + 2*spalt;
aus_w = in_w + 2*wand; aus_h = in_h + 2*wand;
abst_h = 5;                       // Abstandshalter unter der Platine
pcb_z = boden + abst_h;           // Unterkante Platine
innen_hoehe = 27;                 // Nano auf Sockel + Klemmen + Luft
gesamt_h = boden + innen_hoehe;

// Platinen-Koordinaten (KiCad: x 5..81, y 0..92, y nach unten) → Gehäuse
function P(x, y) = [wand + spalt + (x - 5), wand + spalt + (pcb_h - y)];
loecher = [[40, 71], [77.5, 88.5], [77.5, 3.5], [77, 50]];

module schlitze_x(x0, y0, z0, n, l, b, abst, tiefe) {   // Schlitze in einer Wand (senkrecht)
    for (i = [0:n-1]) translate([x0 + i*abst, y0, z0]) cube([b, tiefe, l]);
}

module unterteil() {
    difference() {
        cube([aus_w, aus_h, gesamt_h]);
        translate([wand, wand, boden]) cube([in_w, in_h, gesamt_h]);
        // USB (linke Wand), Nano-Mitte y=49.6, Höhe ~ Platine + 8.5 Sockel + 1.6 + 1.5
        usb = P(5, 49.6);
        translate([-1, usb[1] - 6.5, pcb_z + pcb_t + 8.5 - 1]) cube([wand + 2, 13, 9]);
        // Klemme X2 oben (Kombi), Drahteinführung zur oberen Wand (Platinen-y=0)
        x2a = P(8, 0); x2b = P(27.5, 0);
        translate([x2a[0], aus_h - wand - 1, pcb_z + pcb_t + 0.5]) cube([x2b[0] - x2a[0], wand + 2, 9]);
        // Klemme X1 unten (Versorgung/Geber/Öl), Drahteinführung zur unteren Wand (Platinen-y=92)
        x1a = P(12, 92); x1b = P(31.5, 92);
        translate([x1a[0], -1, pcb_z + pcb_t + 0.5]) cube([x1b[0] - x1a[0], wand + 2, 9]);
        // Lüftungsschlitze rechte Wand (bei Spannungsregler) und linke Wand unten
        for (j = [0:6]) translate([aus_w - wand - 1, 12 + j*8, pcb_z + 4]) cube([wand + 2, 3, 14]);
        for (j = [0:3]) translate([-1, 6 + j*7, pcb_z + 4]) cube([wand + 2, 3, 12]);
        // Beschriftung der Klemmen außen, senkrecht über jeder Klemme (1 mm tief graviert)
        for (i = [0:3]) {
            p_ = P(10 + i*5.08, 0); p2 = P(14 + i*5.08, 92);
            translate([p_[0], aus_h - 0.8, pcb_z + pcb_t + 10.0]) rotate([90, 0, 180]) rotate([0, 0, 90]) linear_extrude(1)
                text(["A", "B", "TOG", "ABS"][i], size = 2.2, valign = "center", font = "DejaVu Sans:style=Bold");
            translate([p2[0], 0.8, pcb_z + pcb_t + 10.0]) rotate([90, 0, 0]) rotate([0, 0, 90]) linear_extrude(1)
                text(["ÖL", "GEBER", "GND", "+12V"][i], size = 2.2, valign = "center", font = "DejaVu Sans:style=Bold");
        }
        // „TANK“ waagerecht unter den Klemmen A/B
        tk = P(12.54, 0);
        translate([tk[0], aus_h - 0.8, boden + 2.2]) rotate([90, 0, 180]) linear_extrude(1)
            text("TANK", size = 2.4, halign = "center", font = "DejaVu Sans:style=Bold");
        usbp = P(5, 49.6);
        translate([0.8, usbp[1], pcb_z + pcb_t + 8.5 + 10]) rotate([90, 0, -90]) linear_extrude(1)
            text("USB", size = 3, halign = "center", font = "DejaVu Sans:style=Bold");
        // Kabelbinder-/Befestigungslaschen-Löcher im Boden
        for (p = [[aus_w/2 - 20, aus_h/2], [aus_w/2 + 20, aus_h/2]]) translate([p[0], p[1], -1]) cylinder(d = 4.2, h = boden + 2);
    }
    // Befestigungslaschen links und rechts (je 2 Langlöcher für M5)
    for (seite = [0, 1]) {
        x = seite == 0 ? -14 : aus_w;
        translate([x, 0, 0]) difference() {
            cube([14, aus_h, 4]);
            for (y = [14, aus_h - 14]) hull() for (dy = [-2, 2]) translate([7, y + dy, -1]) cylinder(d = 5.5, h = 6);
        }
        // Versteifung zwischen Lasche und Wand
        for (y = [aus_h/2 - 1.5]) translate([seite == 0 ? -10 : aus_w, y, 0])
            hull() { cube([10, 3, 0.1]); translate([seite == 0 ? 10 : 0, 0, 0]) cube([0.1, 3, 14]); }
    }
    // Abstandshalter mit Loch für M3-Blechschraube (2,5 mm) bzw. Einschmelzmutter (4 mm Loch → Variable)
    for (l = loecher) {
        p = P(l[0], l[1]);
        translate([p[0], p[1], boden - 0.01]) difference() {
            cylinder(d = 6.5, h = abst_h);
            translate([0, 0, 0.8]) cylinder(d = 2.6, h = abst_h);
        }
    }
    // kleine Rastnasen innen oben für den Deckel
    for (x = [aus_w/2]) for (y = [wand - 0.01, aus_h - wand - 0.6]) translate([x - 8, y, gesamt_h - 3.2]) cube([16, 0.6, 1.2]);
}

module deckel() {
    lippe = 4; tol = 0.35;
    nano_a = P(9.44 - 3.8, 42 - 1.4); nano_b = P(45 + 3.8, 57.24 + 1.4);
    nano_oben = pcb_z + pcb_t + 8.5 + 1.6 + 2.5;      // Oberkante Nano-Bauteile (USB-Buchse ~2,5 mm)
    difference() {
        union() {
            cube([aus_w, aus_h, 2]);
            // Niederhalter: zwei Stege über den Nano-Längskanten, enden 2 mm über dem Nano → 2-3 mm Schaumstoff dazwischen
            for (y = [nano_b[1] + 1.5, nano_a[1] - 4.5]) translate([nano_a[0] + 6, y, 2]) cube([nano_b[0] - nano_a[0] - 8, 3, gesamt_h - nano_oben - 2]);
            translate([wand + tol, wand + tol, 2]) difference() {
                cube([in_w - 2*tol, in_h - 2*tol, lippe]);
                translate([1.6, 1.6, -1]) cube([in_w - 2*tol - 3.2, in_h - 2*tol - 3.2, lippe + 2]);
            }
        }
        // Lüftungsschlitze im Deckel (über Relais-Reihe und Spannungsregler)
        for (i = [0:10]) translate([10 + i*6, aus_h - 38, -1]) cube([2.5, 22, 4]);
        for (i = [0:4]) translate([aus_w - 32 + i*5.5, 16, -1]) cube([2.5, 22, 4]);
        // Aussparung Schraubenzugang über den Klemmen
        x2a = P(8, 0); x2b = P(27.5, 0); x1a = P(12, 92); x1b = P(31.5, 92);
        translate([x2a[0], aus_h - wand - 9, -1]) cube([x2b[0] - x2a[0], 6, 4]);
        translate([x1a[0], wand + 3, -1]) cube([x1b[0] - x1a[0], 6, 4]);
        // Rastnuten passend zu den Nasen
        for (y = [wand + tol - 0.01, aus_h - wand - tol - 0.7]) translate([aus_w/2 - 8.5, y, 2 + lippe - 2.6]) cube([17, 0.71, 1.6]);
        // Beschriftung
        // Außenseite des Deckels ist z = 0 (Lippe zeigt nach innen) → dort 0,6 mm tief, gespiegelt, damit es von außen lesbar ist
        translate([aus_w/2, aus_h/2 - 4, -1]) mirror([1, 0, 0]) linear_extrude(1.6) text("BETTY", size = 7, halign = "center", font = "DejaVu Sans:style=Bold");
        translate([aus_w/2, aus_h/2 - 14, -1]) mirror([1, 0, 0]) linear_extrude(1.6) text("Tank + Öl/TOG", size = 4.5, halign = "center", font = "DejaVu Sans");
    }
}

if (teil == "unterteil") unterteil();
else if (teil == "deckel") deckel();
else { unterteil(); translate([aus_w + 10, 0, 0]) deckel(); }
