# Raspberry Pi + Muons

This code was supposed to power a Raspberry Pi controlled muon detector using leftover plastic scintillator bars from an old T2K experiment ([*The Electromagnetic Calorimeter for the T2K Near Detector*](https://arxiv.org/abs/1308.3445) page 11).

However, the project came to a halt as we discovered that would could not measure light pulses small enough to detect muon interactions in the scintillator in a way that would scale to the number of bars we wanted to use (and be within budget).

My original plan was to have the Raspberry Pi running a web server on the local network that would provide controls for the detector, and store, analyse and present the collected data. I completed most of this before we hit the light detection problem, so it is close to being in a working condition. In its current state, it has been converted to run as a light pulse detector instead, with the Raspberry Pi connected to a potential divider circuit using a phototransistor left over from our first failed attempt at low level light detection.

The entry point for the web interface code is muons.py.

### pi_code

All the code I wrote on the Pi was moved into this folder and committed at the end of the project. The primary use was flashing an LED to test how our photodiode/amplifier circuit behaved with changing rate/brightness of the LED pulses.

The Pi specific code used in the light pulse detector web interface is in detector/rpi.py.

![](https://raw.githubusercontent.com/H4rtland/rpi_muons/master/pi_setup.jpg)
We also had a huge excess of 10kΩ resistors. The variable resistor was used to change the brightness of the LED for use with our other light detection circuit.
