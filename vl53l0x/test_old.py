import board
import busio
import adafruit_vl53l0x
import time

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

sensor.measurement_timing_budget = 200000

while True:
    
    measurement = sensor.range
    
    # mm to cm 
    measurement = measurement / 10 
    
    print("Range: {0}cm".format(measurement))
    
    time.sleep(1.0)
