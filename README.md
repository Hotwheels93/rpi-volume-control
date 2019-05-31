# rpi-volume-control
Raspberry Pi volume control using rotary encoder KY040 and ZeroSeg 7 segment display

### Hardware: ###

- ZeroSeg  8 character 7 segment display
- KY040 rotary encoder with push button function

# Installation

### 1. Update dependencies ###

Open terminal

> sudo apt-get update && apt-get upgrade 

### 2. Setup ZeroSeg as descriped in the manual: ###

https://cdn.shopify.com/s/files/1/0176/3274/files/ZeroSeg_User_Guide_1.2.pdf

### 3. Preparing GPIO connection ###

To use the left GPIO pins which are unfortunately not accessible because ZeroSeg covers all 40 pins you have to different options.


### 3.1 Connect the used GPIO pins manually using the official pinout from ZeroSeg manual ###

| Name | Description | Physical Pin | RPi Function |
| --- | --- | --- | --- |
|DIN| Data In 19 | GPIO 10 (MOSI)|
|CS| Chip Select | 24 GPIO 8 (SPI CE0)|
|CLK| Clock | 23 GPIO | 11 (SPI CLK)|
|SW1| Left Switch/Button | 11 | GPIO 17|
|SW2| Right Switch/Button |37 | GPIO 26|


### Power supply: ###

The manual of ZeroSeg gives the following hint:

> Power and GND lines have not been documented, however it's worth mentioning that the MAX7219CNG chip uses the 5V line, whilst the switches use 3.3V

For this I connected all of the 40 GPIO pins with male-female wires and simply did some trial and error to check which pins are used for power supply. The result is the following:

First 2 pins of the ZeroSeg are 3V and 5V

GND pin is the pin under the the second 5V pin

**Schematic:**

| Pin | Pin | Description | 
| --- | --- | --- |
|3V| 5V | <== VCC|
|IO2| 5V ||
|IO3| GND | <== GND (choose any if already in use) |
|IO4| IO14 | |
|...| ... | |



| Pin | Pin |  Description |
| --- | --- | --- | 
|3V| 5V|     <== VCC |
|IO2| 5V   ||             
|IO3| GND  | <== GND (choose any if already in use) |
|IO4| IO14 ||
|...|...|| 

### Attention ###

**You have to be careful when you connect the pins to the RPi. Do not miscalculate while counting the pins. Do not connect wrong pins, this could damage your RPi seriously. I am not responsible for any damage caused by wrong wiring or use of this tutorial.**


### OR ###

### 3.2 Easy but needs additional hardware: ###

Get a GPIO exander or multiplexer, google search delivers lots of results.

### 4. Check audio card ###

If you use want to use onboard audio enter:

> amixer -c 0 controls

If you want to use an external usb sound card enter:

> amixer -c 1 controls

Should output results like this:

> numid=3,iface=MIXER,name='PCM Playback Switch'
numid=4,iface=MIXER,name='PCM Playback Volume'      <== Script default, change if necessary
numid=2,iface=PCM,name='Capture Channel Map'
numid=1,iface=PCM,name='Playback Channel Map'

**Note the device descriped with "Playback Volume", here numid = 4**


### 5. Clone and config ###

 > git clone https://github.com/Hotwheels93/rpi-volume-control
 > cd rpi-volume-control
 
 **Edit volumectl.py:** 

To set the right sound card change the lines ***25, 41 and 76*** to with your card number and id:

> sudo nano volumectl.py

Example: ['amixer','q', '-c', '1', 'cset', 'numid=4', str(volume)] (default)
 
 **Run:**
 > python volumectl.py


### 5 Autostart (Additional) ###

To enable autostart open terminal and type

> **crontab -e**

> @reboot sudo python /home/pi/rpi-volume-control/volumectl.py


