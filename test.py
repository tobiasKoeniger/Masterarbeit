
from gpiozero import LED
from gpiozero import PWMLED

import time


# pumpWaterSupply = PWMLED(10)

# pumpWaterSupply.on()

# pumpCirculation = PWMLED(8)

# pumpCirculation.value = 0.6
# pumpCirculation.value = 0.3

pumpCirculation = PWMLED(12)

pumpCirculation.value = 1

time.sleep(10000)

