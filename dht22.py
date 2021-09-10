import Adafruit_DHT

class DHT22:
	
	# Init
	def __init__(self):
	
		self.DHT_SENSOR = Adafruit_DHT.DHT22
		
		# Set pin number
		self.DHT_PIN = 22

	# Read sensor
	def getValues(self):
		
		# Read sensor
		self.humidity, self.temperature = Adafruit_DHT.read_retry(self.DHT_SENSOR, self.DHT_PIN)
		
		return [self.humidity, self.temperature]
		
		
		
