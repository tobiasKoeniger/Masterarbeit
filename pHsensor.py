import board
import busio

from math import log

import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn


class PHsensor:
	
	def __init__(self):
	
		self.i2c = busio.I2C(board.SCL, board.SDA)

		self.ads = ADS.ADS1115(self.i2c)
		
		# Enable the full range measurement (measure more than 5 V)
		self.ads.gain = 2/3
		

	# Read pH level
	def getPH(self):
		
		# Read channel
		chan2 = AnalogIn(self.ads, ADS.P2)
		
		# PH linear interpolation
		pH = 7.65 + ( (7.65 - 3.64) / (3.85 - 4.236) ) * (chan2.voltage - 3.85)
		
		# Out of range
		if (pH > 14):
			pH = 0
			print("pH level out of range")
		
		return pH
		
	
		
		
		

