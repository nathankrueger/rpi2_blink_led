#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import argparse

RED_LED_PIN = 20
GREEN_LED_PIN = 26
BLUE_LED_PIN = 21

# Setup and teardown
def setup():
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

	return parser.parse_args()

def main():
	setup()
	args = getArgs()

	if args.cycle_rgb:
		rate = 2
		if args.cycle_rgb > 0:
			rate = args.cycle_rgb
		cycleRGB(rate)

	cleanup()

if __name__ == '__main__':
	main()
