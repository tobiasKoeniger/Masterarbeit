#! /usr/bin/python3

print("\n")
print("Libraries loading")

# Loading libraries
import time
import datetime 
import sys

# Raspberry GPIO libraries
# import RPi.GPIO as GPIO
from gpiozero import LED

# MySQL library
import mysql.connector


# Load sensor classes
from dht22 import DHT22
from lightSensor import LightSensor
from waterTemperatureSensor import WaterTemperatureSensor
from distanceSensor import DistanceSensor
from pHsensor import PHsensor

# Load expander class
from gpioExpander import GPIOExpander

# # Load userInput class
# from userInput import UserInput

# Load gpio class
from gpio import GPIO

# Load database class
from database import Database


# Begin of main program
def main():

    # Show welcome header
    print("--------------------------")
    print("Hydroponics Software Start")
    print()


    # Database routines
    
    # Initialize the database class
    print("Database init.. ", end = '\n\n')
    database = Database()
    print("\nsuccessful")    
    
    
    print()
    
    
    # Initialize classes
    
    # Initialize the GPIO class
    print("GPIO init.. ", end = '\n\n')
    gpio = GPIO()
    print("\nsuccessful")
    
    time.sleep(1)
    
    print()
    
    # Now, initialize all sensor classes
    
    # DHT22: temperature and humidity
    print("Temperature and humidity sensor init.. ", end = '')
    dht22 = DHT22()
    print("successful")
    
    # Light sensor
    print("Light sensor init.. ", end = '')
    lightSensor = LightSensor()
    print("successful")
    
    # Water sensor
    print("Water temperature sensor init.. ", end = '')
    waterTemperatureSensor = WaterTemperatureSensor()
    print("successful")
    
    # Distance sensor
    print("Distance sensor init.. ", end = '')
    distanceSensor1 = DistanceSensor()
    print("successful")
    
    # PH sensor
    print("PH sensor init.. ", end = '')
    pHsensor = PHsensor()
    print("successful")

    # GPIO expander
    # The expander is not needed, but can be used to add more 
    # components to the system.
    # print("GPIO expander init.. ", end = '')
    # gpioExpander = GPIOExpander() 
    # print("successful")
    
    # # userInput class to store user input data 
    # userInput = UserInput()
    
    print()
    print()
    

    # If one manually closes the program with Ctrl+c:
    def cleanAndExit():
        
        print("Cleaning...")
        
        # Closing the database connection
        mycursor.close()
        mydb.close()

        # GPIO.cleanup()
            
        print("Bye!")
        print("\n")
        
        # Close the program
        sys.exit()


    # Main loop
    while True:
        
        # Try to run the loop
        try:    
            
            # Check userInput data
            
            userInput = database.getUserInput()            
            
            
            # userInput.time = result[0]
            # userInput.systemState = result[1]
            # userInput.pHmeasureState = result[2]
            # userInput.ledState = result[3]
            # userInput.autoLedState = result[4]
            # userInput.sunrise = result[5]
            # userInput.sunset = result[6]
            # userInput.autoHeightAdaptionState = result[7]
            # userInput.plantingDate = result[8]
            # userInput.ledUp = result[9]
            # userInput.ledDown = result[10]
            
            print()
            
            
            # Check, if system is switched on
            if (userInput.systemState == True):
                
            
            # Read sensors
            
            # Read the humidity and temperature values from the DHT22
            print("Reading sensors")
            [humidity, temperature] = dht22.getValues()
            # [humidity, temperature] = [0, 0]
            print ("Humidity: {:.1f} %".format(humidity) )
            print ("Temperature: {:.1f} °C".format(temperature) )
            
            
            # Read the light sensor values
            [full_spectrum, infrared] = lightSensor.getValues()
            
            # Calculate the share of visible light
            visibleLight = full_spectrum - infrared
            
            print ("Full Spectrum(IR + Visible) : {} lux".format(full_spectrum) )
            print ("Infrared Value : {} lux".format(infrared) )
            print ("Visible Value : {} lux".format(visibleLight) )
            
            
            # Read the water temperature sensor
            waterTemperature = waterTemperatureSensor.getTemperature()
            print ("Water temperature: {:.1f} °C".format(waterTemperature) )
            
            
            # Read the distance sensor
            distance1 = distanceSensor1.getDistance()
            print ("Distance 1: {0} mm".format(distance1) )            
            
            
            # Read the pH sensor
            pH = pHsensor.getPH()
            print ("PH: {:.3f}".format(pH))    
              
              
            # Update the sensor data in the database table 'sensors'
            
            database.updateSensors(temperature, humidity, visibleLight, waterTemperature, 0, pH, distance1)                                                 

            
            print()
            
            # Do not sleep
            time.sleep(0)

        # Catch an error message and display the message
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


# This is the main program
if __name__ == "__main__":
    main()
