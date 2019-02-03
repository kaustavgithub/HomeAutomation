#!/usr/bin/python

def setup():
	print("GPIO Setup Done...")

class GPIOPIN(object):
	def __init__(self, pin):
		self.pin_no = pin
		self.pin_state = False

	def on(self):
		self.pin_state = True
		print("Made %s pin -> HIGH" % self.pin_no)

	def off(self):
		self.pin_state = False
		print("Made %s pin -> LOW" % self.pin_no)

	def getState(self):
		return self.pin_state

class GPIOSwitch(object):
	_instance = None  # Keep instance reference
	_pins = {}
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = object.__new__(cls)
			cls.pins = {}
			for i in range(1,41):
				cls._pins[i] = GPIOPIN(i)
		return cls._pins[args[0]]

if __name__ == "__main__":
	pin17 = GPIOSwitch(17)
	pin_17 = GPIOSwitch(17)
	pin18 = GPIOSwitch(18)
	pin_18 = GPIOSwitch(18)

	print(pin_17.getState())
	pin17.on()
	print(pin_17.getState())
	#pin_17.off()
	#print(pin17.getState())

	print(pin_18.getState())
	pin18.on()
	print(pin_18.getState())
	pin_18.off()
	print(pin18.getState())

