from RPi import GPIO
from time import sleep
import subprocess
import ZeroSeg.led as led
import time

clk = 5
dt = 6
btn = 13

# vals from output of amixer cget numid=1
min = 0
max = 207

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_UP)

isMuted = False
preVolume = volume = 100  # Default volume
clkLastState = GPIO.input(clk)
btnLastState = GPIO.input(btn)

subprocess.call(['amixer','q', '-c', '1', 'cset', 'numid=4', str(volume)])

try:
    while True:
        btnPushed = GPIO.input(btn)
        if ((not btnLastState) and btnPushed):
            if isMuted:
                volume = preVolume
                isMuted = False
                print "Unmute"
            else:
                preVolume = volume
                volume = 0
                isMuted = True
                print "Muted"
		device.write_text(1,"OFF")
            subprocess.call(['amixer', '-q', '-c', '1', 'cset', 'numid=4', str(volume)])
            sleep(0.05)
        else:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            if clkState != clkLastState:
                if isMuted:
                    isMuted = False
                    volume = 0
                if dtState != clkState:
                    volume += 5
                    if volume > max:
                        volume = max
                else:
                    volume -= 5
                    if volume < min:
                        volume = min
                print "{:d} ({:.0%})".format(volume, float(volume)/float(max))
                vol = "{:d} {:.0%}".format(volume,float(volume)/float(max))
                device = led.sevensegment(cascaded=2)
                getvol = len(vol)
                #Update display
		if getvol == 4:
		    device.write_text(1,vol[2:3])
		elif getvol == 5:
		    device.write_text(1,vol[3:4])
		elif getvol==6:
		   device.write_text(1,vol[3:5])
		elif getvol==7:
		   device.write_text(1,vol[4:6])
		elif getvol==8:
		    device.write_text(1,vol[4:7])
		else:
		   print "Error while setting volume levels"

                subprocess.call(['amixer', '-q', '-c', '1', 'cset', 'numid=4', str(volume)])
            clkLastState = clkState
        btnLastState = btnPushed
finally:
    GPIO.cleanup()

