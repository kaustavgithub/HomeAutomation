#!/usr/bin/python
import RPi.GPIO as GPIO

def setup():
	GPIO.cleanup()
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

class GPIOSwitch():
	def __init__(self, pin_no):
		self.pin_no = pin_no
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin_no, GPIO.OUT)

	def on(self):
		GPIO.output(self.pin_no, GPIO.HIGH)

	def off(self):
		GPIO.output(self.pin_no, GPIO.LOW)

	def getState(self):
		return GPIO.input(self.pin_no)
		
	def __str__(self):
		status = "on" if self.getState() else "off"
		return "pin: %s, status: %s" % (str(self.pin_no), status)


