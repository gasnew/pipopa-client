# PiPoPa: Hello, I wish to register a complaint

This is the client. Install, point to a bud, check your inbox, transmit private, unencrypted bits.

## Requirements
Check out the [BOM](https://docs.google.com/spreadsheets/d/1JkMSPfeMcv-XkWP2sKz12ZnJmRpIdHP3svDDLYOQGbs/edit#gid=0).

## Setup
1. [Install Raspbian Stretch Lite on Micro SD card](https://www.raspberrypi.org/downloads/raspbian/).
2. Set up wifi on Raspberry Pi via [this guide](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md).
3. Configure your circuits according to the photos [here](https://photos.app.goo.gl/LztuDxjtWD6dfXhNA). If necessary, consult [this diagram of a Pi](https://www.jameco.com/Jameco/workshop/circuitnotes/raspberry_pi_circuit_note_fig2.jpg) and/or ask Garrett.

## Installation
1. Install Python packages and git
```bash
sudo apt-get install python-pygame
sudo apt-get install python-requests
sudo apt-get install python-dev
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install git
```
2. Install pyaudio
```bash
git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
cd pyaudio
python setup.py install --user
```
3. Download PiPoPa, and checkout your branch
```bash
cd ~
git clone http://github.com/gasnew/pipopa-client
cd pipopa-client
git checkout dad
```

## Running your PiPoPa!
From inside the `pipopa-client` directory:
```bash
python main.py
```
**NOTE:** If you want it to run at startup, then try following [this guide](https://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html). You may find `start.sh` in `scripts/` helpful.
