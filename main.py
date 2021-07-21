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
    
    # Turn the circuits on for initialization
    gpio.transistor5V.off()
    gpio.transistor3V3.off()
    gpio.transistorPH.off()
    print("All power circuits turned on")
    
    print("\nsuccessful")
    
    time.sleep(0.1)
    
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
    
    
    # Turn the circuits off again
    gpio.transistor5V.on()
    gpio.transistor3V3.on()
    gpio.transistorPH.on()
    print("All power circuits turned off")
    
    
    print()
    print()
    
    # time.sleep(10)
    

    # If one manually closes the program with Ctrl+c:
    def cleanAndExit():
        
        print("Cleaning...")
        
        # Closing the database connection
        # mycursor.close()
        # mydb.close()

        # GPIO.cleanup()
        
        database.closeConnection()
            
        print("Bye!")
        print("\n")
        
        # Close the program
        sys.exit()


    # Main loop
    while True:
        
        # Try to run the loop
        try:                            
            
            # Check userInput data
            # print(database.getUserInput().systemState)
            userInput = database.getUserInput()            
            
            
            # userInput.time = x[0]
            # userInput.systemState = x[1]
            # userInput.pHmeasureState = x[2]
            # userInput.ledState = x[3]
            # userInput.autoLedState = x[4]
            # userInput.sunrise = x[5]
            # userInput.sunset = x[6]
            # userInput.autoHeightAdaptionState = x[7]
            # userInput.plantingDate = x[8]
            # userInput.ledUp = x[9]
            # userInput.ledDown = x[10]
            
            print()
            
            
            # Check, if system is switched on
            if (userInput.systemState == True):
                
                # Turn the circuits on 
                gpio.transistor5V.off()
                gpio.transistor3V3.off()                
                print("3.3 V and 5 V circuits turned on")
                
                time.sleep(0.1)
                
                # Turn the circulation pump on
                gpio.pumpCirculation.value = 0.5
                print("Turning the circulation pump on")
            
                # Read sensors
                
                # Read the humidity and temperature values from the DHT22
                print("Reading sensors")
                [humidity, temperature] = dht22.getValues()
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
                
                # Update database
                database.updateSensors(temperature, humidity, visibleLight, waterTemperature, 0, distance1)        
                         
                
                # Check, if pH sensing is switched on 
                if(userInput.pHmeasureState == True):
                    
                    # Turn pH sensor circuit on
                    gpio.transistorPH.off()
                    
                    time.sleep(0.1)
                    
                    # Read the pH sensor
                    pH = pHsensor.getPH()
                    print ("PH: {:.3f}".format(pH))    
                    
                    # Update database
                    database.updatePH(pH)
                    
                # PH sensing is switched off
                else:
                    # Turn pH sensor circuit off
                    gpio.transistorPH.on()                                                            
                

            # System is switched off
            else:                
                # Turn the circuits off
                gpio.transistor5V.on()
                gpio.transistor3V3.on()
                
                print("All power circuits turned off")
                
                time.sleep(0.1)
                
            
            print()
                        

        # Catch an error message and display the message
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


# This is the main program
if __name__ == "__main__":
    main()
