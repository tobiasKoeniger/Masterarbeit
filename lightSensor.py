import smbus

class LightSensor:
	
	# Init
	def __init__(self):
	
		# Get I2C bus
		self.bus = smbus.SMBus(1)

		self.bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
		self.bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)

	# Read sensor
	def getValues(self):
		
		# Read bus
		data = self.bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
		data1 = self.bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
		 
		# Convert the data
		full_spectrum = data[1] * 256 + data[0]
		infrared = data1[1] * 256 + data1[0]
		
		return [full_spectrum, infrared]
		
		
		
