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
    
    level = 13.3 - measurement
    
    level = level + 4.85
    
    print("Distance from bottom: {:.1f}cm".format(level))
    
    volume = 7 * 12.5 * (level)
    
    weights = [0, 263, 539, 846, 1010]
    volumes = [0, 320, 740, 1070, 1281]
    
    print("Volume: {:.1f}ml".format(volume))
    
    for i in range(3):
        
        if (volume > volumes[i]) and (volume < volumes[i+1]):
            
            weight = weights[i] + ( (weights[i+1] - weights[i]) / (volumes[i+1] - volumes[i]) ) * (volume - volumes[i])
            
            print("Weight: {:.1f}g".format(weight))
            
            
    print()
            
    
    # print("Volume: {:.1f}ml".format(volume))
    
    time.sleep(1.0)
