# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
#
# SPDX-License-Identifier: MIT
 
# Simple demo of reading and writing the digital I/O of the MCP2300xx as if
# they were native CircuitPython digital inputs/outputs.
# Author: Tony DiCola
import time
 
import board
import busio
import digitalio

import sys
 
# from adafruit_mcp230xx.mcp23008 import MCP23008
 
from adafruit_mcp230xx.mcp23017 import MCP23017
 
 
# Initialize the I2C bus:
i2c = busio.I2C(board.SCL, board.SDA)
 
# Create an instance of either the MCP23008 or MCP23017 class depending on
# which chip you're using:
# mcp = MCP23008(i2c)  # MCP23008
mcp = MCP23017(i2c, address=0x27)  # MCP23017
 
# Optionally change the address of the device if you set any of the A0, A1, A2
# pins.  Specify the new address with a keyword parameter:
# mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set


def cleanAndExit():
	
	print("Resetting to default...")

	# Exit
	pinA0.value = False
	pinA1.value = False
	pinA2.value = False
	pinA3.value = False
	
	print("Bye!")
	print("\n")
	
	sys.exit()
	
 
# Now call the get_pin function to get an instance of a pin on the chip.
# This instance will act just like a digitalio.DigitalInOut class instance
# and has all the same properties and methods (except you can't set pull-down
# resistors, only pull-up!).  For the MCP23008 you specify a pin number from 0
# to 7 for the GP0...GP7 pins.  For the MCP23017 you specify a pin number from
# 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4).
pinA0 = mcp.get_pin(0)
pinA1 = mcp.get_pin(1)
pinA2 = mcp.get_pin(2)
pinA3 = mcp.get_pin(3)

pinValue = False

# Setup pin0 as an output that's at a high logic level.
pinA0.switch_to_output(value=pinValue)
pinA1.switch_to_output(value=pinValue)
pinA2.switch_to_output(value=pinValue)
pinA3.switch_to_output(value=pinValue)
	
	

while True:
	try: 
		print("Running")
		time.sleep(1)
		
	except (KeyboardInterrupt, SystemExit):
		cleanAndExit()
	 
