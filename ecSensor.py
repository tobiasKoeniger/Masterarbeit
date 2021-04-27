
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
		self.ads.gain = 2/3
		
		self.transistor5V = LED(16)
		self.transistor3V3 = LED(26)
		self.transistorEC = LED(5)
		self.transistorAntiEC = LED(11)
		
		print("Water temperature sensor init.. ", end = '')
		self.waterTemperatureSensor = WaterTemperatureSensor()
		print("successful \n")
		
		self.transistor5V.off()
		print("5 V circuit powered on")

		self.transistor3V3.off()
		print("3.3 V circuit powered on")

		self.transistorEC.off()
		print("EC meter powered off")

		self.transistorAntiEC.off()
		

	def getEC(self):
		
		waterTemperature = self.waterTemperatureSensor.getTemperature()
		print ("Water temperature: {:.1f} °C".format(waterTemperature) )
		
		
		self.transistorEC.on()
		
		time.sleep(0.03)

		chan = AnalogIn(self.ads, ADS.P1)
		
		u = chan.voltage
		
		time.sleep(0.03)
		
		transistorEC.off()
		
		
		transistorAntiEC.on()
		
		time.sleep(0.06)
		
		transistorAntiEC.off()

		
		print("voltage: {:.2f} V".format(u))
		
		u_power = 3.265
		resistance_R1 = 470

		# resistance in ohm
		r = (u * resistance_R1) / (u_power - u)
		kohm = r/1000
		print("resistance: {:.1f} kOhm".format(kohm))

		#print("resistance: {} Ohm".format(r))
		# mS/cm
		# cell_constant = 25/18
		cell_constant = 1.356
		ec_raw = (cell_constant) * (1/r) * 1000

		print("ec raw: {:.2f} mS/cm".format(ec_raw))


		# temperature compensation
		T = waterTemperature
		ec25 = ec_raw / (1 + 0.019*(T-25))
		print("ec 25: {:.2f} mS/cm".format(ec25))
		
		
		# linear correction
		ec = 0.642 + ( (1.59 - 0.642) / (1.36 - 0.93) ) * (ec25 - 0.93)
		print("ec: {:.2f} mS/cm".format(ec))


		return ec25
		
	
		
		
		
