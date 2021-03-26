import board
import busio
import adafruit_vl53l0x

class DistanceSensor:
	
	def __init__(self):
	
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.sensor = adafruit_vl53l0x.VL53L0X(self.i2c)

		self.sensor.measurement_timing_budget = 200000
		

	def getDistance(self):
		
		distance = self.sensor.range
		
		return distance
		
		
		
