#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import argparse

RED_LED_PIN = 20
GREEN_LED_PIN = 26
BLUE_LED_PIN = 21
DEFAULT_INPUT_PIN = 19

# Setup and teardown
def setup():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(RED_LED_PIN, GPIO.OUT)
	GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
	GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

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

# Outputs
def setOutput(val, pin):
	# This may be dangerous, if for example the pin is configured as an input...
	if GPIO.gpio_function(pin) != GPIO.OUT:
		GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, val)

def highOutputPulse(pin, period_ms):
	pin_i = int(pin)
	period_ms_f = float(period_ms)

	# This may be dangerous, if for example the pin is configured as an input...
	GPIO.setup(pin_i, GPIO.OUT)
	GPIO.output(pin_i, 1)
	time.sleep(period_ms_f)
	GPIO.output(pin_i, 0)

def handlePulse(pulse_args):
	arg_list = pulse_args.split(',')
	pin = arg_list[0]
	period_ms = arg_list[1]
	highOutputPulse(pin, period_ms)
	
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
def setRGB(red, green, blue):
	redLED(red)
	greenLED(green)
	blueLED(blue)

def purpleOn():
	setRGB(1,0,1)

def blueGreenOn():
	setRGB(0,1,1)

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
	parser.add_argument('--blue_green', action='store_true', help='Turn on the blue and green LEDs.')
	parser.add_argument('--purple', action='store_true', help='Turn on the red and blue LEDs.')
	parser.add_argument('--off', action='store_true', help='Turn all LEDs off.')
	parser.add_argument('--cleanup', action='store_true', help='Cleanup LED pin state upon exiting.')
	parser.add_argument('--read_input', type=str, help='Read from an input pin.')
	parser.add_argument('--pulse_output', type=str, help='Send a high output pulse to an input pin.')

	return parser.parse_args()

def main():
	setup()
	args = getArgs()

	if args.pulse_output:
		handlePulse(args.pulse_output)

	if args.cycle_rgb:
		rate = 2 # The default pin cycling rate.
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
	
	# Multiple LEDs at once
	if args.blue_green:
		blueGreenOn()

	if args.purple:
		purpleOn()

	if args.off:
		allOff()

	# Read an input pin
	if args.read_input:
		print getInputPinValOnce(args.read_input)

	if args.cleanup:
		cleanup()

if __name__ == '__main__':
	main()
