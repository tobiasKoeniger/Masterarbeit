
from gpiozero import LED
from gpiozero import PWMLED

import time


# pumpWaterSupply = PWMLED(10)

# pumpWaterSupply.on()

# pumpCirculation = PWMLED(8)

# pumpCirculation.value = 0.6
# pumpCirculation.value = 0.3

transistor5V = LED(16)
transistor3V3 = LED(26)

# Power 5 V off
transistor5V.off()
print("5 V circuit powered on")

# Power 3.3 V off 
transistor3V3.off()
print("3.3 V circuit powered on")


pumpCirculation = PWMLED(24)

pumpCirculation.value = 0.5

time.sleep(10000)

