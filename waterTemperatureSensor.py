import board
import busio

from math import log

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class WaterTemperatureSensor:
	
	def __init__(self):
	
		self.i2c = busio.I2C(board.SCL, board.SDA)

		self.ads = ADS.ADS1115(self.i2c)
		self.ads.gain = 2/3
		

	def getTemperature(self):
		
		chan = AnalogIn(self.ads, ADS.P0)
		
		# print("Voltage Water sensor: {}".format(chan.voltage))
		
		# resistance in kohm
		supplyVoltage = 3.3
		
		resistance = (chan.voltage * 10) / (supplyVoltage - chan.voltage)
		
		# print("Voltage Water sensor: {}".format(chan.voltage))
		# print("Resistance: {} kOhm".format(resistance))
		
		# temperature
		waterTemperature = self.steinhart_temperature_C(resistance*1000)
		
		return waterTemperature
		
		
	def steinhart_temperature_C(self, resistance, Ro=10000.0, To=25.0, beta=3950.0):

		if ((resistance / Ro) <= 0):
			
			print("Warning: Temperature sensor out of range")
			
			return 0

		steinhart = (log(resistance / Ro)) / beta      # log(R/Ro) / beta		
		steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
		steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C

		return steinhart
		
		
		
