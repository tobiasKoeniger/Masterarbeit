
import board
import busio
import digitalio

from adafruit_mcp230xx.mcp23017 import MCP23017


class GPIOExpander:
	
	# weightSensors = [ [0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1] ];
	weightSensors = [ [False, False, False], [False, False, True], [False, True, False], [False, True, True], [True, False, False], [True, False, True] ]
	
	def __init__(self):
		
		# Initialize the I2C bus:
		self.i2c = busio.I2C(board.SCL, board.SDA)
		
		self.mcp = MCP23017(i2c, address=0x27)  # MCP23017
		
		# Initialize Pins
		# 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4).
		self.pin[3] = self.mcp.get_pin(3) # enable pin
		
		self.pin[0] = self.mcp.get_pin(0)
		self.pin[1] = self.mcp.get_pin(1)
		self.pin[2] = self.mcp.get_pin(2)
		
		# Initialize all Pins as Outputs and False 
		self.pin[3].switch_to_output(value = False) # False = enable enable pin
		
		self.pin[0].switch_to_output(value = weightSensors[0][0])
		self.pin[1].switch_to_output(value = weightSensors[0][1])
		self.pin[2].switch_to_output(value = weightSensors[0][2])
		
		
	def setOutput(self, output_pin_number, pin_state):
		
		self.pin[output_pin_number].value = pin_state
		
		
	def enableWeightSensor(self, weightSensorNumber):
		
		pass
		
	
		
