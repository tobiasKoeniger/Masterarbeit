import Adafruit_DHT

class DHT22:
	
	def __init__(self):
	
		self.DHT_SENSOR = Adafruit_DHT.DHT22
		self.DHT_PIN = 22

	def getValues(self):
		self.humidity, self.temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
		
		return [self.humidity, self.temperature]
		
		
		
