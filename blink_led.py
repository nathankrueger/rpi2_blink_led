#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import argparse

RED_LED_PIN = 20
GREEN_LED_PIN = 26
BLUE_LED_PIN = 21
INPUT_PIN = 19

# Setup and teardown
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RED_LED_PIN, GPIO.OUT)
	GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
	GPIO.setup(BLUE_LED_PIN, GPIO.OUT)
	GPIO.setup(INPUT_PIN, GPIO.IN)

def cleanup():
	GPIO.cleanup()

# Red LED
def redLED(val):
	GPIO.output(RED_LED_PIN, val)

def redOn():
	redLED(1)

def redOff():
	redLED(0)

# Green LED
def greenLED(val):
	GPIO.output(GREEN_LED_PIN, val)

def greenOn():
	greenLED(1)

def greenOff():
	greenLED(0)

# Blue LED
def blueLED(val):
	GPIO.output(BLUE_LED_PIN, val)

def blueOn():
	blueLED(1)

def blueOff():
	blueLED(0)

# Inputs
def getInputPinVal(pin):
	ret_val = None
	pin_int = int(pin)
	try:
		ret_val = GPIO.input(pin_int)
	except Exception as err:
		print err
		ret_val = 'X'

	return ret_val

def getInputPinValOnce(pin):
	ret_val = None
	pin_int = int(pin)
	try:
		GPIO.setup(pin_int, GPIO.IN)
		ret_val = getInputPinVal(pin_int)
		GPIO.cleanup(pin_int)
	except Exception as err:
		print err
		ret_val = 'X'

	return ret_val

# Multiple LEDs
def allOff():
	redOff()
	greenOff()
	blueOff()

def cycleRGB(rate):
	redOn()
	time.sleep(rate)
	redOff()
	greenOn()
	time.sleep(rate)
	greenOff()
	blueOn()
	time.sleep(rate)
	blueOff()

# Command-line arguments
def getArgs():
	parser = argparse.ArgumentParser(description='Control an RGB LED via GPIO on a Raspberry Pi 2.')
	parser.add_argument('--cycle_rgb', type=int, help='Cycle through Red, Green, and Blue at a specified rate.')
	parser.add_argument('--red', type=str, choices=['0','1'], help='Turn on / off the red LED.')
	parser.add_argument('--green', type=str, choices=['0','1'], help='Turn on / off the green LED.')
	parser.add_argument('--blue', type=str, choices=['0','1'], help='Turn on / off the blue LED.')
	parser.add_argument('--off', action='store_true', help='Turn all LEDs off.')
	parser.add_argument('--cleanup', action='store_true', help='Cleanup LED pin state upon exiting.')
	parser.add_argument('--read_input', type=str, help='Read from an input pin.')

	return parser.parse_args()

def main():
	setup()
	args = getArgs()

	if args.cycle_rgb:
		rate = 2
		if args.cycle_rgb > 0:
			rate = args.cycle_rgb
		cycleRGB(rate)

	# Control Red
	if args.red:
		if args.red == '0':
			redOff()
		elif args.red == '1':
			redOn()

	# Control Green
	if args.green:
		if args.green == '0':
			greenOff()
		elif args.green == '1':
			greenOn()

	# Control Blue
	if args.blue:
		if args.blue == '0':
			blueOff()
		elif args.blue == '1':
			blueOn()

	if args.off:
		allOff()

	# Read an input pin
	if args.read_input:
		print getInputPinValOnce(args.read_input)

	if args.cleanup:
		cleanup()

if __name__ == '__main__':
	main()
