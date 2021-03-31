
from hx711 import HX711

import board
import busio
import digitalio


class WeightSensor:	
	
	def __init__(self):
		
		self.hx = HX711(5, 6)
		
		self.hx.set_reading_format("MSB", "MSB")
		# self.hx.set_reference_unit(-21.28)		
		# self.hx.set_offset_A(-25724.888)
		self.hx.set_reference_unit(-21.25)		
		self.hx.set_offset_A(-25627)
		
		self.hx.reset()
		
		
	def getLoad(self):
		
		val = max(0, int(self.hx.get_weight(5)))
		
		self.hx.reset()
		
		return val
		
		
	def temperatureCompensation(self, weight, temperature):
		
		temperature_weight_constant = 50
			
		adjusted_weight = weight - (temperature - 22) * temperature_weight_constant
		
		return adjusted_weight
