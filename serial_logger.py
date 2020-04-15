#!/usr/bin/env python
# Log data from serial port
import os.path
from os import path

import RPi.GPIO as GPIO
import argparse
import serial
import datetime
import time
import os

no_msg = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)
##GPIO.output(23, 0)
def gpreset():

	GPIO.setup(23, GPIO.OUT)
	GPIO.output(23, 1)
	time.sleep(1)

##GPIO.output(23, GPIO.LOW)
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--device", help="device to read from", default="/dev/serial0")
parser.add_argument("-s", "--speed", help="speed in bps", default=115200, type=int)
args = parser.parse_args()


outputFilePath = os.path.join(os.path.dirname(__file__),
                 datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S") + ".log")
with serial.Serial(args.device, args.speed, timeout=100) as ser, open(outputFilePath, mode='a') as outputFile:
    print("Logging started. Ctrl-C to stop.")
    try:
        while True:
		print no_msg
		time.sleep(0.1)
		lin = ser.read(ser.inWaiting())
		if not lin:
			print "not"
			no_msg = no_msg + 1
		else:
			no_msg = 0
		if (no_msg > 10):
			no_msg = 0
			print "triggered!!!"
			lin = "!!!!!!! RESET RELAY TRIGGERED!!!!!!"
			gpreset()
		GPIO.setup(23, GPIO.IN)
		print lin
		outputFile.write(lin)
		outputFile.flush()
    except KeyboardInterrupt:
        print("Logging stopped")
	GPIO.cleanup()
