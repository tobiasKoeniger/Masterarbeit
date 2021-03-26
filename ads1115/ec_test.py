
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


while True:

	chan = AnalogIn(ads, ADS.P1)

	# print(chan.value, chan.voltage)

	u = chan.voltage
	u = round(u, 2)
	print("voltage: {} V".format(u))


	# resistance in ohm
	r = (chan.voltage * 470) / (3.3 - chan.voltage)
	kohm = r/1000
	kohm = round(kohm, 1)
	print("resistance: {} kOhm".format(kohm))


	# mS/cm
	ec = (25/18) * (1/r) * 1000

	ec = round(ec, 1)
	print("ec: {} mS/cm".format(ec))


	# temperature compensation
	T = 21
	ec25 = ec / (1 + 0.019*(T-25))
	ec25 = round(ec25, 1)
	print("ec 25: {} mS/cm".format(ec25))

	print()

	time.sleep(0.5)
