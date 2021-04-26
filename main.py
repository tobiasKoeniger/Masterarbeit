#! /usr/bin/python3

print("\n")
print("Libraries loading")

import time
import sys

import RPi.GPIO as GPIO
from gpiozero import LED

import mysql.connector

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
    
    # database credentials
    with open('credentials.txt', 'r') as reader:
        credentials = reader.readlines()
        
    user = credentials[2]
    password = credentials[5]
    
    mydb = mysql.connector.connect(
      host="localhost",
      user=user,
      password=password
    )
    
    mycursor = mydb.cursor()

    # mycursor.execute("CREATE DATABASE mydatabase")
    
    mycursor.execute("SHOW DATABASES")

    for x in mycursor:
      print(x)
    
    
    transistor5V = LED(16)
    transistor3V3 = LED(26)
    transistorPH = LED(6)
    
    transistor5V.off()
    print("5 V circuit powered on")
    
    transistor3V3.off()
    print("3.3 V circuit powered on")
    
    transistorPH.off()
    print("PH sensor powered on")
    
    print()
        
    
    print("Temperature and humidity sensor init.. ", end = '')
    dht22 = DHT22()
    print("successful")
    
    print("Light sensor init.. ", end = '')
    lightSensor = LightSensor()
    print("successful")
    
    print("Water temperature sensor init.. ", end = '')
    waterTemperatureSensor = WaterTemperatureSensor()
    print("successful")
    
    print("Distance sensor init.. ", end = '')
    distanceSensor1 = DistanceSensor()
    print("successful")
    
    print("PH sensor init.. ", end = '')
    pHsensor = PHsensor()
    print("successful")

    
    gpioExpander = GPIOExpander 
    
    print()
    print()
    

    def cleanAndExit():
        
        # print("Cleaning...")

        # GPIO.cleanup()
            
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
            
            
            # variables to dict
            # dictionary = {}
            
            
            # for variable in ["humidity", "temperature", "height"]:
              #   dictionary[variable] = eval(variable)
            

            time.sleep(0)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


if __name__ == "__main__":
    main()
