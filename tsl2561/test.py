import smbus
import time
 
# Get I2C bus
bus = smbus.SMBus(1)

bus.write_byte_data(0x39, 0x00 | 0x80, 0x03)
bus.write_byte_data(0x39, 0x01 | 0x80, 0x02)


while True:

	time.sleep(1)

	data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2)
	data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2)
	 
	# Convert the data
	ch0 = data[1] * 256 + data[0]
	ch1 = data1[1] * 256 + data1[0]
	 
	# Output data to screen
	print ("Full Spectrum(IR + Visible) : {} lux".format(ch0))
	print ("Infrared Value : {} lux".format(ch1))
	print ("Visible Value : {} lux".format(ch0 - ch1))
	print ("")

