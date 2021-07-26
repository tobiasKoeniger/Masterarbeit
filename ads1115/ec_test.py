
import board
import busio

import time
import math

from gpiozero import LED
#import RPi.GPIO as GPIO

#GPIO.setmode(GPIO.BCM)


from waterTemperatureSensor import WaterTemperatureSensor


i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS

from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)

# differential
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

ads.gain = 2/3


#GPIO.setup(16, GPIO.OUT)
#GPIO.setup(26, GPIO.OUT)
#GPIO.setup(5, GPIO.OUT)
transistor5V = LED(16)
transistor3V3 = LED(26)
transistorEC = LED(5)
transistorAntiEC = LED(11)

transistor5V.off()
#GPIO.output(16, GPIO.LOW)
print("5 V circuit powered on")

transistor3V3.off()
#GPIO.output(26, GPIO.LOW)
print("3.3 V circuit powered on")

transistorEC.off()
#GPIO.output(5, GPIO.LOW)
print("EC meter powered off")

transistorAntiEC.off()

print()

time.sleep(1)


print("Water temperature sensor init.. ", end = '')
waterTemperatureSensor = WaterTemperatureSensor()
print("successful \n")



while True:
	
	waterTemperature = waterTemperatureSensor.getTemperature()
	print ("Water temperature: {:.1f} °C".format(waterTemperature) )
	
	
	transistorEC.on()
	#GPIO.output(5, GPIO.HIGH)
	
	time.sleep(0.03)

	chan = AnalogIn(ads, ADS.P1)
	
	time.sleep(0.03)
	
	u = chan.voltage
	
	transistorEC.off()
	
	print("voltage: {:.2f} V".format(u))
	
	
	transistorAntiEC.on()
	
	time.sleep(0.06)
	
	transistorAntiEC.off()
	

	#print(chan.value, chan.voltage)
	
	#transistorEC.off()
	#GPIO.output(5, GPIO.LOW)
	
	u_power = 2.81
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
	ec = 0.32 + ( (2.4 - 0.32) / (0.655 - 0.549) ) * (ec25 - 0.549)
	print("ec: {:.2f} mS/cm".format(ec))

	print()
	
	#transistorEC.off()
	#GPIO.output(5, GPIO.LOW)

	time.sleep(0)
