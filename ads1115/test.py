
import board
import busio

import time
import math

i2c = busio.I2C(board.SCL, board.SDA)

import adafruit_ads1x15.ads1115 as ADS

from adafruit_ads1x15.analog_in import AnalogIn

ads = ADS.ADS1115(i2c)

# differential
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

ads.gain = 2/3


def steinhart_temperature_C(resistance, Ro=10000.0, To=25.0, beta=3950.0):

    steinhart = math.log(resistance / Ro) / beta      # log(R/Ro) / beta
    steinhart += 1.0 / (To + 273.15)         # log(R/Ro) / beta + 1/To
    steinhart = (1.0 / steinhart) - 273.15   # Invert, convert to C

    return steinhart


while True:
	
	chan0 = AnalogIn(ads, ADS.P0)
	chan1 = AnalogIn(ads, ADS.P1)
	chan2 = AnalogIn(ads, ADS.P2)
	chan3 = AnalogIn(ads, ADS.P3)

	# print("Voltage 0: {:.1f} V".format(chan0.voltage))
	# print("Voltage 1: {:.1f} V".format(chan1.voltage))
	print("Voltage 2: {:.3f} V".format(chan2.voltage))
	# print("Voltage 3: {:.1f} V".format(chan3.voltage))

	pH = 7.65 + ( (7.65 - 3.64) / (3.85 - 4.236) ) * (chan2.voltage - 3.85)
	
	print("PH {:.3f}".format(pH))
	
	print()


	# resistance in kohm
	r = (chan0.voltage * 10) / (3.3 - chan0.voltage)
	# print(r)

	# temperate
	t = steinhart_temperature_C(r*1000)
	# print(t)

	# print()

	time.sleep(1)
