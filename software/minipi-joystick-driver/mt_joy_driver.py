from Adafruit_MCP230xx import Adafruit_MCP230XX as mcp
from time import sleep
import sys
import locale
from uinput import *

class MiniKb:

	REPEAT = 10

	LSHIFT, RSHIFT, CTRL = (8, 7), (4, 7), (8,5)

	BTN1, BTN2, BTN3, BTN4, BTN5, BTN6 = (8,6), (7,5), (7,7), (1,7), (7,6), (2,7)
	START, SELECT = (8,4), (7,4)
	LEFT, RIGHT, UP, DOWN = (5,6), (4,6), (1,4), (4,5)

	JOYSTICK = {
		BTN1: BTN_1,
		BTN2: BTN_2,
		BTN3: BTN_3,
		BTN4: BTN_4,
		BTN5: BTN_5,
		BTN6: BTN_6,
		START: BTN_START,
		SELECT: BTN_SELECT,
	}


	def __init__(self):
		# get mcp23017
		self.mcp17 = mcp(address = 0x20, num_gpios = 16)
		self.mcp08 = mcp(address = 0x21, num_gpios = 8)
		self.keypress = None

		# set PORTA and PORTB of mcp23017 as OUTPUT
		for i in range(16):
			self.mcp17.config(i, mcp.OUTPUT)

		# set PORTA of mcp23008 as INPUT
		for i in range(8):
			self.mcp08.config(i, mcp.INPUT)
			self.mcp08.pullup(i, 1)

		self.joystick = Device([
			BTN_1,
			BTN_2,
			BTN_3,
			BTN_4,
			BTN_5,
			BTN_6,
			BTN_SELECT,
			BTN_START,
			ABS_X + (0,255,0,0),
			ABS_Y + (0,255,0,0),
		])

	def _set_Y(self, y):
		"""
		Optimized write of 16 bits MCP23017
		"""
		self.mcp17.i2c.write8(0x12, 0xff)
		self.mcp17.i2c.write8(0x13, 0xff)
		# set bit
		if y<10:
			self.mcp17.output(y, 0)

	def _read_X(self):
		"""
		Optimized read of MCP23008 IO port
		"""
		bits = [int(c) for c in bin(self.mcp08.i2c.readU8(0x09))[2:].rjust(8,'0')][::-1]
		return bits

	def process_joystick_btn(self, i, j, state):
		if (i,j) in self.JOYSTICK:
			self.joystick.emit(self.JOYSTICK[(i,j)], state)

	def process_joystick_xy(self, pressed):
		if self.LEFT in pressed:
			self.joystick.emit(ABS_X, 0)
		elif self.RIGHT in pressed:
			self.joystick.emit(ABS_X, 255)
		else:
			self.joystick.emit(ABS_X, 128)
		if self.UP in pressed:
			self.joystick.emit(ABS_Y, 0)
		elif self.DOWN in pressed:
			self.joystick.emit(ABS_Y, 255)
		else:
			self.joystick.emit(ABS_Y, 128)

	def process(self):

		self.joystick.emit(ABS_X, 128, syn=False)
		self.joystick.emit(ABS_Y, 128, syn=False)

		KEYS = self.JOYSTICK.keys() + [self.UP,self.DOWN,self.LEFT,self.RIGHT]
		repeat_keys = {}
		while True:
			pressed_keys = []
			released_keys = []
			# DEtermine pressed keys
			for x,y in KEYS:
				self._set_Y(x)
				# read X
				X = self._read_X()
				if X[y] == 0:
					pressed_keys.append((x,y))
					if (x,y) not in repeat_keys:
						self.process_joystick_btn(x,y,1)
						repeat_keys[(x,y)] = 1
					else:
						repeat_keys[(x,y)] += 1
				else:
					if (x,y) in repeat_keys:
						self.process_joystick_btn(x,y,0)
						del repeat_keys[(x,y)]
						released_keys.append((x,y))
			print pressed_keys
			self.process_joystick_xy(pressed_keys)
			sleep(0.05)


if __name__ == '__main__':
	print '[+] Minitel Keyboard I2C driver'
	locale.setlocale(locale.LC_ALL, 'en_GB.utf8')
	kb = MiniKb()
	kb.process()

