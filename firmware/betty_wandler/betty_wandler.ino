/*
  Betty-Wandler v1 – ein Arduino Nano für Tankanzeige + Öltemperatur/TOG (ArduinoTog) im VW T3 Syncro
  mit Audi-A6-C5-Kombi. Platine „Betty-Wandler v1“ (22.11.2026).

  Tank:  T3-Tankgeber an Klemme GEBER (gegen Masse, 150 Ω Pull-up auf der Platine) → A2.
         Ausgang: 8 Widerstände in Reihe (2,0 … 270 Ω), je per PhotoMOS-Relais überbrückt → Kombi sieht 0 … ~525 Ω.
         Umrechnung Geber-Ω → Kombi-Ω über eine Kalibriertabelle im EEPROM (per USB einmessen, s. u.).
  Öl:    Fühler an Klemme OEL (1 kΩ Pull-up) → A1, Schwellen + Pulsmuster unverändert aus ArduinoTog
         (arduino_tog_new.ino), aber ohne delay(): läuft nicht blockierend neben der Tankanzeige.
  TOG:   D6 → 1 kΩ → Klemme TOG (direkt wie bisher).
  ABS:   D5 → MOSFET → Klemme ABS. Der MOSFET zieht die Leitung nach Masse, wenn D5 HIGH ist
         (bisher war D5 selbst LOW = Leitung an Masse; gleiche Wirkung, aber das Kombi kann den Pin nicht mehr beschädigen).

  USB-Befehle (Serieller Monitor, 115200 Baud, Zeilenende „Neue Zeile“):
    hilfe            Übersicht
    status           Geber-Ω, Kombi-Ω, Öl-Rohwert/Stufe
    ohm <wert>       Kombi-Ausgang fest auf <wert> Ω (Kalibrieren: welcher Wert zeigt leer/¼/½/¾/voll?)
    auto             zurück in den Normalbetrieb (Tabelle)
    punkt <i> <geber> <kombi>   Tabellenpunkt i (0–7) setzen: Geber-Ω → Kombi-Ω, aufsteigend nach Geber-Ω
    tabelle          Tabelle anzeigen     speichern   Tabelle ins EEPROM
    hier <i> <kombi> Tabellenpunkt i mit dem AKTUELL gemessenen Geber-Ω und <kombi> setzen (bequem beim Tanken)
*/
#include <EEPROM.h>

// ---------------- Pins ----------------
const uint8_t PIN_TOG = 6, PIN_ABS = 5;
const uint8_t PIN_OEL = A1, PIN_GEBER = A2;
const uint8_t RELAIS[8] = {2, 3, 4, 7, 8, 9, 10, 11};                 // überbrücken RC8..RC1
const float   R_KETTE[8] = {2.0, 3.9, 8.2, 16.0, 33.0, 62.0, 130.0, 270.0}; // Ω, zu RELAIS[i]
const float   R_ON = 1.0;            // PhotoMOS-Durchlasswiderstand (Datenblatt typ. ~0,8–2 Ω)
const float   R_PULLUP_GEBER = 150.0;

// ---------------- Öl / TOG (aus ArduinoTog, unverändert) ----------------
const int ANALOG_VALUES[] = {983, 939, 915, 889, 863, 839, 815, 782, 755, 726, 700, 663, 645, 621, 583, 502, 473, 449, 414, 384, 359, 332, 0};
const unsigned int LOW_US[]  = {23000, 26250, 27000, 28000, 28500, 29250, 30250, 31000, 31750, 32500, 33250, 34000, 35000, 35750, 36750, 37500, 38250, 39250, 40000, 41000, 41750, 42750, 44500};
const unsigned int HIGH_US[] = {24000, 27000, 27750, 28250, 29250, 30000, 30750, 31500, 32500, 33250, 34000, 35000, 35750, 36750, 37500, 38250, 39250, 40000, 40750, 41750, 42750, 43500, 45250};
const uint8_t NUM_LEVELS = sizeof(ANALOG_VALUES) / sizeof(ANALOG_VALUES[0]);

// ---------------- Kalibriertabelle (EEPROM) ----------------
struct Tabelle { uint16_t magic; uint8_t n; float geber[8]; float kombi[8]; };
const uint16_t MAGIC = 0xB377;
Tabelle tab;
// Platzhalter bis zum Einmessen: T2-Richtwert (10 Ω voll … 73 Ω leer) → A5-Richtwert (65 Ω voll … 280 Ω leer)
void tabelleStandard() {
  tab.magic = MAGIC; tab.n = 2;
  tab.geber[0] = 10;  tab.kombi[0] = 65;
  tab.geber[1] = 73;  tab.kombi[1] = 280;
}

// ---------------- Zustand ----------------
float geberOhm = 0, kombiSoll = 0, kombiIst = 0;
int oelRoh = 0; uint8_t oelStufe = NUM_LEVELS - 1;
bool festModus = false; float festOhm = 0;
uint8_t aktiveMaske = 0xFF;

// ---------------- Hilfen ----------------
float leseGeberOhm() {
  long s = 0;
  for (uint8_t i = 0; i < 16; i++) s += analogRead(PIN_GEBER);
  float u = s / 16.0;                                   // 0 … 1023
  if (u >= 1022) return 9999;                           // Geber offen
  return R_PULLUP_GEBER * u / (1023.0 - u);
}

float interpol(float g) {
  if (tab.n == 0) return g;
  if (g <= tab.geber[0]) return tab.kombi[0];
  for (uint8_t i = 1; i < tab.n; i++)
    if (g <= tab.geber[i])
      return tab.kombi[i-1] + (tab.kombi[i] - tab.kombi[i-1]) * (g - tab.geber[i-1]) / (tab.geber[i] - tab.geber[i-1]);
  return tab.kombi[tab.n - 1];
}

// Beste Relais-Kombination für den Zielwiderstand (Bit gesetzt = Relais zu = Widerstand überbrückt)
float ohmVonMaske(uint8_t m) {
  float r = 0;
  for (uint8_t i = 0; i < 8; i++) r += (m & (1 << i)) ? R_ON : R_KETTE[i];
  return r;
}
void setzeAusgang(float ziel) {
  uint8_t best = 0; float bestFehler = 1e9;
  for (uint16_t m = 0; m < 256; m++) {
    float f = fabs(ohmVonMaske(m) - ziel);
    if (f < bestFehler) { bestFehler = f; best = m; }
  }
  if (best != aktiveMaske) {
    // erst schließen, dann öffnen → kein kurzer „offener“ Zustand (= Tank leer-Sprung) beim Umschalten
    for (uint8_t i = 0; i < 8; i++) if (best & (1 << i)) digitalWrite(RELAIS[i], HIGH);
    for (uint8_t i = 0; i < 8; i++) if (!(best & (1 << i))) digitalWrite(RELAIS[i], LOW);
    aktiveMaske = best;
  }
  kombiIst = ohmVonMaske(best);
}

// ---------------- TOG nicht blockierend ----------------
// Phasen: 20 ms HIGH, LOW_US LOW, HIGH_US HIGH, dann 250 ms Pause (wie im Original)
uint8_t togPhase = 0; unsigned long togStart = 0, togDauer = 0;
void togSchritt() {
  unsigned long jetzt = micros();
  if (jetzt - togStart < togDauer) return;
  togStart = jetzt;
  switch (togPhase) {
    case 0: digitalWrite(PIN_TOG, HIGH); togDauer = 20000UL;                 togPhase = 1; break;
    case 1: digitalWrite(PIN_TOG, LOW);  togDauer = LOW_US[oelStufe];        togPhase = 2; break;
    case 2: digitalWrite(PIN_TOG, HIGH); togDauer = HIGH_US[oelStufe];       togPhase = 3; break;
    default: digitalWrite(PIN_TOG, LOW); togDauer = 250000UL;                togPhase = 0; break;
  }
}

void leseOel() {
  long s = 0;
  for (uint8_t i = 0; i < 8; i++) s += analogRead(PIN_OEL);
  oelRoh = s / 8;
  uint8_t st = NUM_LEVELS - 1;
  for (uint8_t i = 0; i < NUM_LEVELS; i++) if (oelRoh >= ANALOG_VALUES[i]) { st = i; break; }
  if (togPhase == 0) oelStufe = st;   // Stufe nur zwischen zwei Pulsfolgen wechseln
}

// ---------------- Seriell ----------------
char zeile[48]; uint8_t zl = 0;
void hilfe() {
  Serial.println(F("Befehle: status | ohm <w> | auto | punkt <i> <geber> <kombi> | hier <i> <kombi> | tabelle | speichern"));
}
void zeigeTabelle() {
  Serial.print(F("Tabelle (")); Serial.print(tab.n); Serial.println(F(" Punkte): Geber-Ohm -> Kombi-Ohm"));
  for (uint8_t i = 0; i < tab.n; i++) { Serial.print(i); Serial.print(F(": ")); Serial.print(tab.geber[i]); Serial.print(F(" -> ")); Serial.println(tab.kombi[i]); }
}
void sortiere() {
  for (uint8_t a = 0; a < tab.n; a++) for (uint8_t b = a + 1; b < tab.n; b++)
    if (tab.geber[b] < tab.geber[a]) { float t = tab.geber[a]; tab.geber[a] = tab.geber[b]; tab.geber[b] = t;
                                       t = tab.kombi[a]; tab.kombi[a] = tab.kombi[b]; tab.kombi[b] = t; }
}
void setzePunkt(int i, float g, float k) {
  if (i < 0 || i > 7) { Serial.println(F("i muss 0..7 sein")); return; }
  tab.geber[i] = g; tab.kombi[i] = k; if (i >= tab.n) tab.n = i + 1;
  sortiere(); zeigeTabelle();
}
void befehl(char *c) {
  char *cmd = strtok(c, " ");
  if (!cmd) return;
  if (!strcmp(cmd, "status")) {
    Serial.print(F("Geber ")); Serial.print(geberOhm); Serial.print(F(" Ohm -> Kombi soll ")); Serial.print(kombiSoll);
    Serial.print(F(" / ist ")); Serial.print(kombiIst); Serial.print(F(" Ohm (Maske 0x")); Serial.print(aktiveMaske, HEX);
    Serial.print(F(")  Oel roh ")); Serial.print(oelRoh); Serial.print(F(" Stufe ")); Serial.print(oelStufe);
    Serial.println(festModus ? F("  [FEST]") : F(""));
  } else if (!strcmp(cmd, "ohm")) {
    char *w = strtok(NULL, " "); if (w) { festOhm = atof(w); festModus = true; Serial.print(F("fest auf ")); Serial.println(festOhm); }
  } else if (!strcmp(cmd, "auto")) { festModus = false; Serial.println(F("Normalbetrieb"));
  } else if (!strcmp(cmd, "punkt")) {
    char *a = strtok(NULL, " "), *b = strtok(NULL, " "), *d = strtok(NULL, " ");
    if (a && b && d) setzePunkt(atoi(a), atof(b), atof(d));
  } else if (!strcmp(cmd, "hier")) {
    char *a = strtok(NULL, " "), *d = strtok(NULL, " ");
    if (a && d) setzePunkt(atoi(a), geberOhm, atof(d));
  } else if (!strcmp(cmd, "tabelle")) { zeigeTabelle();
  } else if (!strcmp(cmd, "speichern")) { EEPROM.put(0, tab); Serial.println(F("gespeichert"));
  } else hilfe();
}
void leseSeriell() {
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n' || ch == '\r') { if (zl) { zeile[zl] = 0; befehl(zeile); zl = 0; } }
    else if (zl < sizeof(zeile) - 1) zeile[zl++] = ch;
  }
}

// ---------------- Setup / Loop ----------------
void setup() {
  pinMode(PIN_TOG, OUTPUT); digitalWrite(PIN_TOG, LOW);
  pinMode(PIN_ABS, OUTPUT); digitalWrite(PIN_ABS, HIGH);       // MOSFET an → ABS-Leitung an Masse (wie bisher D5 LOW)
  for (uint8_t i = 0; i < 8; i++) { pinMode(RELAIS[i], OUTPUT); digitalWrite(RELAIS[i], LOW); }
  Serial.begin(115200);
  EEPROM.get(0, tab);
  if (tab.magic != MAGIC || tab.n > 8) tabelleStandard();
  Serial.println(F("Betty-Wandler v1"));
  hilfe();
}

unsigned long tLetzt = 0;
float geberGlatt = -1;
// Messen/Rechnen nur in der 250-ms-Pause zwischen zwei TOG-Pulsfolgen (togPhase 0 = Pause läuft) und nur,
// wenn noch genug Pause übrig ist – sonst würden analogRead und die Relais-Suche die µs-genauen Pulse verzögern.
bool pauseFrei() { return togPhase == 0 && (micros() - togStart) < togDauer - 30000UL; }
void loop() {
  togSchritt();
  if (!pauseFrei()) return;
  leseSeriell();
  if (millis() - tLetzt >= 200) {           // 5× pro Sekunde messen
    tLetzt = millis();
    leseOel();
    float g = leseGeberOhm();
    // Gleitender Mittelwert (~10 s) gegen Schwappen im Tank
    geberGlatt = (geberGlatt < 0) ? g : geberGlatt + (g - geberGlatt) * 0.02;
    geberOhm = geberGlatt;
    kombiSoll = festModus ? festOhm : interpol(geberOhm);
    setzeAusgang(kombiSoll);
  }
}
