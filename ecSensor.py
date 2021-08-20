
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
		# self.ads.mode = Mode.CONTINUOUS
		
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
		
		
		#GPIO.output(5, GPIO.HIGH)
		
		T = 0.001
		
		
		# chan = AnalogIn(self.ads, ADS.P1)
		
		# time.sleep(0.03)
		
		timeEnd = round(time.time() * 1000 * 1000) + T*1000*1000
		
		self.transistorEC.on()
		beginTime = round(time.time() * 1000 * 1000) 
		
		while (round(time.time() * 1000 * 1000) < timeEnd):			
		
			chan = AnalogIn(self.ads, ADS.P1)		
			u = chan.voltage	
			
			mil = abs( beginTime - round(time.time() * 1000 * 1000) )
			print("voltage: {0:.2f} V after {1} mus".format(u, mil))
		
		# time.sleep(T)

		u = chan.voltage
		
		self.transistorEC.off()
		
		
		
		
		
		timeEnd = round(time.time() * 1000 * 1000) + T*1000*1000
		
		self.transistorAntiEC.on()
		beginTime = round(time.time() * 1000 * 1000) 
		
		while (round(time.time() * 1000 * 1000) < timeEnd):			
		
			chan = AnalogIn(self.ads, ADS.P1)		
			k = chan.voltage	
			
			mil = abs( beginTime - round(time.time() * 1000 * 1000) )
			print("voltage: {0:.2f} V after {1} mus".format(k, mil))
		
		# time.sleep(T)
		
		self.transistorAntiEC.off()
		

		#print(chan.value, chan.voltage)
		
		#transistorEC.off()
		#GPIO.output(5, GPIO.LOW)
		
		u_power = 3.314
		resistance_R1 = 470

		# resistance in ohm
		r = ( (u * resistance_R1) / (u_power - u) ) - 1000
		kohm = r/1000
		print("resistance: {:.3f} kOhm".format(kohm))

		#print("resistance: {} Ohm".format(r))
		# mS/cm
		# cell_constant = 25/18
		cell_constant_calculated = 0.7 / ((1/r) * 1000)
		print("cell constant: {:.4f}".format(cell_constant_calculated))
		
		# cell_constant = 1.389
		
		# cell_constant = 0.206
		
		cell_constant = 0.7213
		
		# cell_constant = 0.1584
		
		# cell_constant = 0.0671
		
		# cell_constant = 3.4937
		ec_raw = (cell_constant) * (1/r) * 1000

		print("ec raw: {:.4f} mS/cm".format(ec_raw))


		# temperature compensation
		T = waterTemperature
		ec25 = ec_raw / (1 + 0.019*(T-25))
		print("ec 25: {:.4f} mS/cm".format(ec25))
		
		
		# linear correction
		# ec = 0.642 + ( (1.59 - 0.642) / (1.36 - 0.93) ) * (ec25 - 0.93)
		
		# ec = 0.32 + ( (2.4 - 0.32) / (0.7746 - 0.6714) ) * (ec25 - 0.6714)
		
		ec = 2.20408 * ec25 - 0.90306

		print("final ec: {:.2f} mS/cm".format(ec))

		print()
		
		#transistorEC.off()
		#GPIO.output(5, GPIO.LOW)

		time.sleep(0)


		return ec
		
	
		
		
		

