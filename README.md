# ArduinoTog → Betty-Wandler

Arduino Nano adapter board for fitting a **2000s VAG/Audi instrument cluster into an older car** (here: an Audi A6 C5 cluster in a VW T3 Syncro with a 1.9 TDI).

One Nano does three jobs:

| Function | What it does |
|---|---|
| **TOG / oil temperature** | Emulates the pulse-coded oil temperature sender (TOG) the cluster expects, based on a standard VW oil temp sensor (A1). No warnings, working gauge. |
| **Fuel gauge** | Reads the original (old) tank sender (A2) and drives the cluster's fuel input through a switchable resistor network (PhotoMOS relays). The curve is calibrated over USB and stored in EEPROM. |
| **Warning lamp output** | Open-drain output (D5, MOSFET) that can pull a cluster warning lamp line (e.g. ABS) to ground. |

> ⚠️ **Status: design, not yet built or road-tested** (v1, Nov 2026). Use at your own risk – this is connected to a car's wiring.

## Repository layout

```
firmware/betty_wandler/    Arduino sketch (Nano, ATmega328P)
hardware/pcb/              KiCad 9 board, generator script, JLCPCB fab files (gerber zip, BOM, CPL)
hardware/enclosure/        OpenSCAD enclosure + STLs (base with M5 mounting tabs, vented lid)
docs/                      schematic, wiring plan (PDF), build & calibration notes (German: LIESMICH.txt)
legacy/                    the original ArduinoTog sketches
```

## Quick start

1. Order the PCB (2 layers, 2.0 mm, assembled) with the files in `hardware/pcb/fertigung/` – see `docs/LIESMICH.txt`.
2. Flash `firmware/betty_wandler/betty_wandler.ino` to an Arduino Nano.
3. Wire it as shown in `docs/anschlussplan.pdf`.
4. Calibrate over USB serial (115200 baud): `ohm <value>`, `hier <i> <ohm>`, `tabelle`, `speichern`, `auto`.

## Credits

- [BlackBrix/TinyTOG](https://github.com/BlackBrix/TinyTOG) for the initial TOG research and logic.
- gnif (hostfission) for correcting and explaining the original code.

License: GPL-3.0 (see `LICENSE`).
