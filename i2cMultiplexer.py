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
tca_tank_levels = adafruit_tca9548a.TCA9548A(i2c)

tank_sensors = [0, 0]

# sensors = [adafruit_vl53l0x.VL53L0X(tca[6]), adafruit_vl53l0x.VL53L0X(tca[7])]

# For each sensor, create it using the TCA9548A channel instead of the I2C object
tank_sensors[0] = adafruit_vl53l0x.VL53L0X(tca_tank_levels[6])
tank_sensors[0].measurement_timing_budget = 200000

tank_sensors[1] = adafruit_vl53l0x.VL53L0X(tca_tank_levels[7])
tank_sensors[1].measurement_timing_budget = 200000


plant_sensors = [0, 0]

# Create the TCA9548A object and give it the I2C bus
tca_plant_heights = adafruit_tca9548a.TCA9548A(i2c, address=0x74)

plant_sensors[0] = adafruit_vl53l0x.VL53L0X(tca_plant_heights[6])
plant_sensors[0].measurement_timing_budget = 200000

plant_sensors[1] = adafruit_vl53l0x.VL53L0X(tca_plant_heights[7])
plant_sensors[1].measurement_timing_budget = 200000


def cleanAndExit():
    
    # print("Cleaning...")
        
    print("Bye!")
    print("\n")
    
    sys.exit()
        

# Loop and profit!
while True:
    try: 
        print("Range 0: {0}mm".format(tank_sensors[0].range))
        print("Range 1: {0}mm".format(tank_sensors[1].range))
        
        print("Range 2: {0}mm".format(plant_sensors[0].range))
        print("Range 3: {0}mm".format(plant_sensors[1].range))
        
        print()
        
        time.sleep(1.0)
        
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


