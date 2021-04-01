#! /usr/bin/python3

print("\n")
print("Libraries loading")

import time
import sys

import RPi.GPIO as GPIO

# sys.path.append('hx711')

# from weightSensor import WeightSensor
from dht22 import DHT22
from lightSensor import LightSensor
from waterTemperatureSensor import WaterTemperatureSensor
from distanceSensor import DistanceSensor
from pHsensor import PHsensor

from gpioExpander import GPIOExpander


def main():
    
    print("--------------------------")
    print("Hydroponics Software Start")
    print()
    
    # weightsensor1 = WeightSensor()
    # print("Weight sensor init successful")
    
    dht22 = DHT22()
    print("Temperature and humidity sensor init successful")
    
    lightSensor = LightSensor()
    print("Light sensor init successful")
    
    waterTemperatureSensor = WaterTemperatureSensor()
    print("Water temperature sensor init successful")
    
    distanceSensor1 = DistanceSensor()
    print("Distance sensor init successful")
    
    pHsensor = PHsensor()
    print("PH sensor init successful")
    
    gpioExpander = GPIOExpander 
    
    print()
    print()
    

    def cleanAndExit():
        
        print("Cleaning...")

        GPIO.cleanup()
            
        print("Bye!")
        print("\n")
        
        sys.exit()


    while True:
        try:            
            
            [humidity, temperature] = dht22.getValues()
            
            print ("Humidity: {:.1f} %".format(humidity) )
            print ("Temperature: {:.1f} °C".format(temperature) )
            
            
            [full_spectrum, infrared] = lightSensor.getValues()
            print ("Full Spectrum(IR + Visible) : {} lux".format(full_spectrum) )
            print ("Infrared Value : {} lux".format(infrared) )
            print ("Visible Value : {} lux".format(full_spectrum - infrared) )
            
            
            waterTemperature = waterTemperatureSensor.getTemperature()
            print ("Water temperature: {:.1f} °C".format(waterTemperature) )
            
            
            distance1 = distanceSensor1.getDistance()
            print ("Distance 1: {0} mm".format(distance1) )
            
            
            # weight = weightsensor1.getLoad()
            
            # adjusted_weight = weightsensor1.temperatureCompensation(weight, temperature)

            # print ("Weight: {} g".format(weight))
            # print ("Temperature adjusted weight: {:.0f} g".format(adjusted_weight))
            
            
            pH = pHsensor.getPH()
            print ("PH: {:.3f}".format(pH))
            
            

            print()

            time.sleep(0)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


if __name__ == "__main__":
    main()
