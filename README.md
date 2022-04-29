# ArduinoTog
Emulation of Oil Temp Sensor signal with an arduiono

VAG Engines from 2000 onwards have a oil temp sensor that does not give a simple voltage but pulse in a certain pwm pattern which makes for inconvenient beeps, errors and/or broken dials in the dashboard if you install the engines or dashboards into other cars not equipped with that setup.

Based on the work of the TinyTOG by BlackBrix here on github i wrote a -atm somewhat hacky- solution to silence the alarms and give out a real reading based on a standard oil temp sensor.

# WHAT WORKS
Right now it pulses according to a certain threshold. if no sensor is connected it defaults to 170°C Oil Temp. No warning lights, just for the dash dial. Theoretical it should work if you connect a oil temp sensor to the analog input A1, though it might need a reference voltage output by the arduino. I will test this as soon as i have it installed.

# TODO
Rework the whole code. I want to have a logic with an array and a if loop, not that atrocious thing I wrote.
Also i'm trying to get some sort of layout graphics created on how its supposed to work and connect. Bear with me ;-)

# Credits
BlackBrix/TinyTOG here on github for the initial research and logic.
gnif from hostfission for correcting and explaining my code and what i could do better.
ITS A WORK IN PROGRESS.
