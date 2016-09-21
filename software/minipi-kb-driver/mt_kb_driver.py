from Adafruit_MCP230xx import Adafruit_MCP230XX as mcp
from time import sleep
import sys
import locale
from uinput import *

class MiniKb:

	REPEAT = 20

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

	# [Y][X] -> [NORMAL, SHIFT+KEY, CTRL+KEY]
	KEYMAP = [
		[
			[KEY_SPACE, None, None],
			None,
			None,
			None,
			None,
			None,
			None,
			None
		],
		[
			None ,
			[KEY_3, None, None],
			[KEY_6, None, None],
			[KEY_QUESTION, KEY_SLASH, None],
			[KEY_I, None, KEY_TAB],
			[KEY_O, None, None],
			[KEY_9, KEY_RIGHTBRACE, None],
			[KEY_X, None, None]
		],
		[
			[KEY_0, KEY_UP, None],
			[KEY_2, None, None],
			[KEY_5, None, None],
			[KEY_M, None, None],
			[KEY_U, None, None],
			[KEY_P, None, None],
			[KEY_8, None, None],
			[KEY_C, None, None]
		],
		[
			None,
			[KEY_1, None, None],
			[KEY_4, None, None],
			[KEY_MINUS, None, None],
			[KEY_Y, None, None],
			[KEY_SEMICOLON, None, None],
			[KEY_7, None, None],
			[KEY_V, None, None],
		],
		[
			[KEY_ENTER, None, None],
			None,
			None,
			[KEY_M, None, None],
			[KEY_T, None, None],
			[KEY_K, None, None],
			[KEY_L, None, None],
			[KEY_RIGHTSHIFT, None, None]
		],
		[
			[KEY_RIGHT, None, None],
			None,
			None,
			[KEY_APOSTROPHE, None, None],
			[KEY_R, None, None],
			[KEY_H, None, None],
			[KEY_J, None, None],
			[KEY_N, None, None],
		],
		[
			[KEY_LEFT, None, None],
			None,
			[KEY_BACKSPACE, None, None],
			[KEY_DOT, None, None],
			[KEY_E, None, None],
			[KEY_F, None, None],
			[KEY_G, None, None],
			[KEY_B, None, None],
		],
		[
			[KEY_DOWN, None, None],
			[KEY_HOME, None, None],
			None,
			[KEY_COMMA, None, None],
			[KEY_W, None, None],
			[KEY_S, None, None],
			[KEY_D, None, None],
			[KEY_Z, None, None],
		],
		[
			[KEY_UP, None, None],
			None,
			None,
			[KEY_ESC, None, None],
			[KEY_Q, None, None],
			[KEY_LEFTCTRL, None, None],
			[KEY_A, None, None],
			[KEY_LEFTSHIFT, None, None],
		],
	]

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

		self.device = None
		"""
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
		"""
		self.init_device()

	def init_device(self):
		"""
		Parse keymap and declare our uinput device.
		"""
		events = []
		for row in self.KEYMAP:
			for key in row:
				if key is not None:
					for event in key:
						if event not in events and event is not None:
							events.append(event)
		self.device = Device(events)



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


	def echo(self, k):
		sys.stdout.write(k)
		sys.stdout.flush()

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

		#self.joystick.emit(ABS_X, 128, syn=False)
		#self.joystick.emit(ABS_Y, 128, syn=False)

		repeat_keys = {}
		while True:
			pressed_keys = []
			released_keys = []
			# Determine pressed keys
			for i in range(9):
				self._set_Y(i)
				# read X
				X = self._read_X()
				for j in range(8):
					if X[j] == 0:
						# handle our joystick
						#if self.KEYMAP[i][j] is not None:
						#	self.device.emit(self.KEYMAP[i][j][0], 1)
						pressed_keys.append((i,j))
						if (i,j) not in repeat_keys:
							#self.process_joystick_btn(i,j,1)
							repeat_keys[(i,j)] = 1
						else:
							repeat_keys[(i,j)] += 1
					else:
						if (i,j) in repeat_keys:
							#self.process_joystick_btn(i,j,0)
							del repeat_keys[(i,j)]
							released_keys.append((i,j))
							#if self.KEYMAP[i][j] is not None:
							#	self.device.emit(self.KEYMAP[i][j][0], 0)

			#self.process_joystick_xy(pressed_keys)
			# If shift is pressed
			if (self.LSHIFT in pressed_keys) or (self.RSHIFT in pressed_keys):
				shifted = []
				for keycode in pressed_keys:
					if keycode!=self.LSHIFT and keycode!=self.RSHIFT:
						x,y = keycode
						if self.KEYMAP[x][y] is not None:
							if self.KEYMAP[x][y][1] is not None:
								if (x,y) in repeat_keys and ((repeat_keys[(x,y)] > self.REPEAT) or (repeat_keys[(x,y)] == 1)):
									self.device.emit_click(self.KEYMAP[x][y][1])
									break
							elif (x,y) in repeat_keys and ((repeat_keys[(x,y)] > self.REPEAT) or (repeat_keys[(x,y)] == 1)):
								shifted.append(self.KEYMAP[x][y][0])
				if len(shifted) > 0:
					shifted.insert(0, KEY_LEFTSHIFT)
					self.device.emit_combo(shifted)
			# If control pressed
			elif (self.CTRL in pressed_keys):
				ctrled = []
				# if a control key is defined
				for keycode in pressed_keys:
					x,y = keycode
					c = self.KEYMAP[x][y]
					if c is not None and c[2] is not None:
						if (x,y) in repeat_keys and ((repeat_keys[(x,y)] > self.REPEAT) or (repeat_keys[(x,y)] == 1)):
							self.device.emit_click(c[2])
							break
					elif c is not None and c[0] is not None:
						if (x,y) in repeat_keys and ((repeat_keys[(x,y)] > self.REPEAT) or (repeat_keys[(x,y)] == 1)):
							ctrled.append(c[0])
				if len(ctrled)>0:
					ctrled.insert(0, KEY_LEFTCTRL)
					self.device.emit_combo(ctrled)
			elif len(pressed_keys)>0:
				# Only handle normal keys
				translated_keys = []
				for x,y in pressed_keys:
					c = self.KEYMAP[x][y]
					if c is not None and (repeat_keys[(x,y)] > self.REPEAT or repeat_keys[(x,y)] == 1):
						self.device.emit_click(self.KEYMAP[x][y][0])


if __name__ == '__main__':
	print '[+] Minitel Keyboard I2C driver'
	locale.setlocale(locale.LC_ALL, 'en_GB.utf8')
	kb = MiniKb()
	kb.process()

