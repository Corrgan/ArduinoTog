# Betty-Wandler (vormals ArduinoTog)

Arduino-Nano-Platine, um ein **VAG/Audi-Kombiinstrument ab ca. 2000 in ein älteres Auto** einzubauen (hier: Audi-A6-C5-Kombi in einem VW T3 Syncro mit 1.9 TDI).

Ein Nano erledigt drei Aufgaben:

| Funktion | Was sie macht |
|---|---|
| **TOG / Öltemperatur** | Emuliert den pulscodierten Öltemperaturgeber (TOG), den das Kombi erwartet – auf Basis eines normalen VW-Öltemperaturfühlers (A1). Keine Warnungen, Anzeige funktioniert. |
| **Tankanzeige** | Liest den originalen (alten) Tankgeber (A2) und steuert den Tankeingang des Kombis über ein schaltbares Widerstandsnetz (PhotoMOS-Relais). Die Kennlinie wird per USB eingemessen und im EEPROM gespeichert. |
| **Warnleuchten-Ausgang** | Open-Drain-Ausgang (D5, MOSFET), der eine Warnleuchten-Leitung des Kombis (z. B. ABS) nach Masse ziehen kann. |

> ⚠️ **Stand: Entwurf, noch nicht gebaut oder im Fahrzeug getestet** (v1, Nov. 2026). Nutzung auf eigene Gefahr – das Ding hängt an der Fahrzeugelektrik.

## Aufbau des Repos

```
firmware/betty_wandler/    Arduino-Sketch (Nano, ATmega328P)
hardware/pcb/              KiCad-9-Platine, Generator-Skript, JLCPCB-Fertigungsdaten (Gerber-ZIP, BOM, CPL)
hardware/enclosure/        OpenSCAD-Gehäuse + STLs (Unterteil mit M5-Laschen, Deckel mit Lüftungsschlitzen)
docs/                      Schaltplan, Anschlussplan (PDF), Bau- und Einmess-Anleitung (LIESMICH.txt)
legacy/                    die ursprünglichen ArduinoTog-Sketches
```

## Schnellstart

1. Platine bestellen (2 Lagen, 2,0 mm, bestückt) mit den Dateien aus `hardware/pcb/fertigung/` – Details in `docs/LIESMICH.txt`.
2. `firmware/betty_wandler/betty_wandler.ino` auf einen Arduino Nano flashen.
3. Anschließen wie in `docs/anschlussplan.pdf`.
4. Per USB einmessen (Serieller Monitor, 115200 Baud): `ohm <wert>`, `hier <i> <ohm>`, `tabelle`, `speichern`, `auto`.

## Danke

- [BlackBrix/TinyTOG](https://github.com/BlackBrix/TinyTOG) für die ursprüngliche TOG-Recherche und -Logik.
- gnif (hostfission) fürs Korrigieren und Erklären des ersten Codes.

Lizenz: GPL-3.0 (siehe `LICENSE`).
