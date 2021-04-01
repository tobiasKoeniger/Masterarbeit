# This example shows using two TSL2491 light sensors attached to TCA9548A channels 0 and 1.
# Use with other I2C sensors would be similar.
import time
import board
import busio
import adafruit_vl53l0x
import adafruit_tca9548a

import sys


# Create I2C bus as normal
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

# For each sensor, create it using the TCA9548A channel instead of the I2C object
sensor[0] = adafruit_vl53l0x.VL53L0X(tca[7])
sensor[0].measurement_timing_budget = 200000

# sensor[1] = adafruit_vl53l0x.VL53L0X(tca[7])
# sensor[1].measurement_timing_budget = 200000


def cleanAndExit():
    
    # print("Cleaning...")
        
    print("Bye!")
    print("\n")
    
    sys.exit()
        

# Loop and profit!
while True:
    try: 
        print("Range: {0}mm".format(sensor[0].range))
        # print("Range: {0}mm".format(sensor[1].range))
        
        time.sleep(1.0)
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()
