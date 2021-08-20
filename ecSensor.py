
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
		
		# self.transistor5V = LED(16)
		# self.transistor3V3 = LED(26)
		
		# BCM numbering		
		self.transistorEC = LED(21)
		self.transistorAntiEC = LED(20)
		
		print("Water temperature sensor init.. ", end = '')
		self.waterTemperatureSensor = WaterTemperatureSensor()
		print("successful \n")
		
		# self.transistor5V.off()
		# print("5 V circuit powered on")

		# self.transistor3V3.off()
		# print("3.3 V circuit powered on")
		
		self.transistorEC.off()
		self.transistorAntiEC.off()
		#GPIO.output(5, GPIO.LOW)
		print("EC meter powered off")		
				

	def getEC(self):
		
		waterTemperature = self.waterTemperatureSensor.getTemperature()
		print ("Water temperature: {:.1f} °C".format(waterTemperature) )
		
		self.transistorEC.on()
		#GPIO.output(5, GPIO.HIGH)
		
		time.sleep(0.03)

		chan = AnalogIn(self.ads, ADS.P1)
		
		time.sleep(0.03)
		
		u = chan.voltage
		
		self.transistorEC.off()
		
		print("voltage: {:.2f} V".format(u))
		
		
		self.transistorAntiEC.on()
		
		time.sleep(0.06)
		
		self.transistorAntiEC.off()
		

		#print(chan.value, chan.voltage)
		
		#transistorEC.off()
		#GPIO.output(5, GPIO.LOW)
		
		u_power = 3.157
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

		print("ec raw: {:.4f} mS/cm".format(ec_raw))


		# temperature compensation
		T = waterTemperature
		ec25 = ec_raw / (1 + 0.019*(T-25))
		print("ec 25: {:.4f} mS/cm".format(ec25))
		
		
		# linear correction
		# ec = 0.642 + ( (1.59 - 0.642) / (1.36 - 0.93) ) * (ec25 - 0.93)
		
		# ec = 0.32 + ( (2.4 - 0.32) / (0.7746 - 0.6714) ) * (ec25 - 0.6714)
		
		ec = 13.3559 * ec25 - 9.62

		print("final ec: {:.2f} mS/cm".format(ec))

		print()
		
		#transistorEC.off()
		#GPIO.output(5, GPIO.LOW)

		time.sleep(0)


		return ec
		
	
		
		
		

