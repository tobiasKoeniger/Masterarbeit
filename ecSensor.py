
import board
import busio

import time
import math

from gpiozero import LED

from waterTemperatureSensor import WaterTemperatureSensor

import adafruit_ads1x15.ads1115 as ADS

from adafruit_ads1x15.analog_in import AnalogIn


class EcSensor:
	
	def __init__(self):
	
		self.i2c = busio.I2C(board.SCL, board.SDA)

		self.ads = ADS.ADS1115(self.i2c)
		
		# Full range measurement
		self.ads.gain = 4  # 8  # 4  # 2 	# 1   # 2/3
		
		# BCM numbering: initialize EC transistors
		self.transistorEC = LED(21)
		self.transistorAntiEC = LED(20)
		
		# Initialize water temperature sensor
		print("Water temperature sensor init.. ", end = '')
		self.waterTemperatureSensor = WaterTemperatureSensor()
		print("successful \n")
		
		# Disable EC circuits
		self.transistorEC.off()
		self.transistorAntiEC.off()
		print("EC meter powered off")		
				

	def getEC(self, waterTemperature):
		
		mil1 = 0
		
		# while (mil1 < 1400 or mil1 > 1700):
		
		# Let the voltage settle
		time.sleep(0.3)
		
		# Get the water temperature
		# The water temperature reading "prepares" the I2C bus for the EC reading
		# The reading helps to get a replicable EC reading time thereby increasing 
		# the sensor's accuracy.
		measured = self.waterTemperatureSensor.getTemperature()
		# print ("Water temperature: {:.1f} °C".format(waterTemperature) )
		
		# EC reading time: 1 ms
		T = 0.001
		
		# Save begin time
		beginTime = round(time.time() * 1000 * 1000) 
		
		# Turn EC circuit on 
		self.transistorEC.on()						
		
		# Read voltage
		chan = AnalogIn(self.ads, ADS.P1)		
		u = chan.voltage	
		
		# Turn circuit off
		self.transistorEC.off()
		
		# Measure passed time
		mil1 = abs( beginTime - round(time.time() * 1000 * 1000) )			
		
		
		# Save begin time
		beginTime = round(time.time() * 1000 * 1000) 		
		
		# Turn opposed EC circuit on 
		self.transistorAntiEC.on()	
		
		# Read voltage
		chan = AnalogIn(self.ads, ADS.P1)		
		k = chan.voltage	
		
		# Turn circuit off
		self.transistorAntiEC.off()
		
		# Measure passed time
		mil2 = abs( beginTime - round(time.time() * 1000 * 1000) )
			
			
			# if(mil1 < 1400 or mil1 > 1700):
				# print("--- Skipping ---")
			
		
		print("voltage: {0:.3f} V after {1} mus".format(u, mil1))
		print("voltage: {0:.2f} V after {1} mus".format(k, mil2))
		
		# Supplied voltage
		u_power = 3.283 
		
		# Resistance R1
		# resistance_R1 = 470 
		# resistance_R1 = 3615
		resistance_R1 = 9940 + 217
		# resistance_R1 = 32810

		# resistance in ohm
		r = ( (u * resistance_R1) / (u_power - u) ) - 1000
		kohm = r/1000
		print("resistance: {:.3f} kOhm".format(kohm))

		# Calculate cell constant for calibration (ec level assumed 0.7)
		cell_constant_calculated = 0.640 / ((1/r) * 1000)
		print("cell constant: {:.4f}".format(cell_constant_calculated))
		
		# Set cell constant
		cell_constant = 2.0862

		# Calculate raw ec level
		ec_raw = (cell_constant) * (1/r) * 1000
		print("ec raw: {:.4f} mS/cm".format(ec_raw))


		# Temperature compensation
		# T = waterTemperature
		# ec25 = ec_raw / (1 + 0.019*(T-25))
		# print("ec 25: {:.4f} mS/cm".format(ec25))
		
		
		# linear correction
		# ec = 0.642 + ( (1.59 - 0.642) / (1.36 - 0.93) ) * (ec25 - 0.93)
		# ec = 2.20408 * ec25 - 0.90306
		
		# if (ec_raw < 0.931):
			# ec = 2.34657*ec25 - 0.894657
			
		# else:
			# ec = 3.3787466*ec25 - 1.855613
			
		# ec = 2.34657*ec25 - 0.894657
		# ec = 3.3787466*ec25 - 1.855613
		
		x = ec_raw
		ec = 1.9386155088348*(x**3) - 4.7035379960156*(x**2) + 5.4271925803641*x - 1.3903934826734

		print("EC after interpolation: {:.2f} mS/cm \n".format(ec))


		return ec
		
	
		
		
		

