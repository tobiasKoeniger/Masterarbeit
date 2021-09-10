
import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017


class GPIOExpander:	
	
	def __init__(self):
		
		# Initialize the I2C bus:
		self.i2c = busio.I2C(board.SCL, board.SDA)
		
		self.mcp = MCP23017(self.i2c, address=0x27)  # MCP23017
		
		# Initialize list of pins
		# 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4).
		self.pin = []
		
		
		# Append pins to list
		self.pin.append(self.mcp.get_pin(0))
		self.pin.append(self.mcp.get_pin(1))
		self.pin.append(self.mcp.get_pin(2))
		self.pin.append(self.mcp.get_pin(3))
		self.pin.append(self.mcp.get_pin(4))
		self.pin.append(self.mcp.get_pin(5))
		self.pin.append(self.mcp.get_pin(6))
		self.pin.append(self.mcp.get_pin(7))
		self.pin.append(self.mcp.get_pin(8))
		self.pin.append(self.mcp.get_pin(9))
		
		
		# Switch pins to output and set value to False
		self.pin[0].switch_to_output(value = False) 
		self.pin[1].switch_to_output(value = False) 
		self.pin[2].switch_to_output(value = False) 
		self.pin[3].switch_to_output(value = False) 
		self.pin[4].switch_to_output(value = False) 
		self.pin[5].switch_to_output(value = False) 
		self.pin[6].switch_to_output(value = False) 
		self.pin[7].switch_to_output(value = False) 
		self.pin[8].switch_to_output(value = False) 
		self.pin[9].switch_to_output(value = False) 
		
		
	# Enable sensor
	def setSensor(self, sensor_number):
		
		# Disable all sensors
		for sensor in self.pin:
			sensor.value = False
			
		# Enable the given sensor
		self.pin[sensor_number].value = True
		
	
	# Disable all sensors
	def cleanClose(self):
		
		for sensor in self.pin:
			sensor.value = False

