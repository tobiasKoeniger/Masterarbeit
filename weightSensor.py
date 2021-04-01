
from hx711 import HX711

import board
import busio
import digitalio

from gpioExpander import GPIOExpander


class WeightSensor:	
	
	references = [-21.25, 20.51, 21.56, 22, 21.5, 20.9]
	offsets = [-25627, -184933.66, -377104.22, 79333, 125073.33, 32014]
	
	def __init__(self):
		
		gpioExpander = GPIOExpander				
		
		self.hx = HX711(5, 6)
		
		self.hx.set_reading_format("MSB", "MSB")
		# self.hx.set_reference_unit(-21.28)		
		# self.hx.set_offset_A(-25724.888)
		
		self.hx.set_reference_unit(-21.25)		
		self.hx.set_offset_A(-25627)
		
		self.hx.reset()
		
		
	def getLoad(self):
		
		self.hx.set_reference_unit(self.references[0])		
		self.hx.set_offset_A(self.offsets[0])
			
		self.hx.reset()
		
		# 5 = median of 5 measurements 
		load = max(0, int(self.hx.get_weight(5)))
		
		self.hx.reset()
		
		return load
		
		
	def getLoads(self):
		
		# iterate through all sensors 0 to 5
		for i in range(6):
			
			self.hx.set_reference_unit(self.references[i])		
			self.hx.set_offset_A(self.offsets[i])
			
			self.hx.reset()
			
			# 5 = median of 5 measurements 
			loads[i] = max(0, int(self.hx.get_weight(5)))				
			
			self.hx.reset()
			
		return loads
		
		
	def temperatureCompensation(self, weight, temperature):
		
		temperature_weight_constant = 50
			
		adjusted_weight = weight - (temperature - 22) * temperature_weight_constant
		
		return adjusted_weight
