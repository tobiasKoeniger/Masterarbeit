#! /usr/bin/python3

print("\n")
print("Libraries loading")

# Loading libraries
import time
from datetime import datetime 
from datetime import timedelta
import sys

# Raspberry GPIO libraries
# import RPi.GPIO as GPIO
from gpiozero import LED

# MySQL library
import mysql.connector

# Threading
# from threading import *

# Load sensor classes
from dht22 import DHT22
from lightSensor import LightSensor
from waterTemperatureSensor import WaterTemperatureSensor
from distanceSensor import DistanceSensor
from pHsensor import PHsensor
# from ecSensor import EcSensor


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
    mainTankLevelSensor = DistanceSensor()
    print("successful")
    
    # PH sensor
    print("PH sensor init.. ", end = '')
    pHsensor = PHsensor()
    print("successful")
    
    # EC sensor
    # print("EC sensor init.. ", end = '')
    # ecsensor = EcSensor()
    # print("successful")
    
    
    # Initialize main tank's water level buffer
    # Array of ten 
    waterLevelMainTankBuffer = [80] * 10
    
    # Number of tank level updates
    waterLevelMainTankUpdates = 0
    
    # EC level buffer
    ecLevelBuffer = [1.2] * 10
    
    # Number of EC level updates
    ecLevelUpdates = 0
    
    # Initialize nutrient matrix
    nutrientTable = [[1, 1, 1, 1.5, 1.5, 1, 0.5, 0.5, 0.5],     # FloraGro
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],               # FloraMicro
                     [1, 1, 1, 0.5, 0.5, 1, 1.5, 1.5, 1.5],     # FloraBloom
                     [0.7, 0.8, 0.8, 0.9, 1, 1, 1, 1, 1]]
    
    # GPIO expander
    # The expander is not needed, but can be used to add more 
    # components to the system.
    # print("GPIO expander init.. ", end = '')
    # gpioExpander = GPIOExpander() 
    # print("successful")
    
    # # userInput class to store user input data 
    # userInput = UserInput()
    
    
    # Turn the 3.3 V circuit and pH meter off again
    # gpio.transistor5V.on()
    gpio.transistor3V3.on()
    gpio.transistorPH.on()
    print("3.3 V circuit and pH meter turned off")
    
    
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


    userInput = database.getUserInput()  
    
    # # Check, if system is switched on
    # if (userInput.systemState == True):

        # T = Thread(target=dht22reading(dht22))
        # T.setDaemon(True)
        # T.start()
    

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
                
                # Turn the 3.3 V and 5 V circuits on 
                gpio.transistor5V.off()
                gpio.transistor3V3.off()                
                print("5 V circuit turned on")
                
                time.sleep(0.1)
                # time.sleep(100)
                
                # Turn the circulation pump on
                gpio.pumpCirculation.value = 0.5
                print("Turning the circulation pump on to {} %".format(gpio.pumpCirculation.value*100))
            
            
                # Read sensors
                                
                # Read the humidity and temperature values from the DHT22
                
                # threading.Thread(target=dht22reading(dht22)).start()
                
                print("Reading sensors")
                # [humidity, temperature] = dht22.getValues()
                # print ("Humidity: {:.1f} %".format(humidity) )
                # print ("Temperature: {:.1f} °C".format(temperature) )
                
                
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
                
                
                # Read the main water level sensor
                distance = mainTankLevelSensor.getDistance()
                waterLevelMainTank = 250 - distance
                print ("Distance of main tank level sensor: {0} mm".format(distance) ) 
                print ("Water level main tank: {0} mm".format(waterLevelMainTank) )   
                
                
                # EC level
                
                # Read EC level
                # ecLevel = ecsensor.getEC()
                ecLevel = database.getEC()
                print("EC level: {}".format(ecLevel))
                # ecLevel = 1.2
                
                if (ecLevelBuffer[-1] != ecLevel):
                    
                    # Set first value of buffer                
                    ecLevelBuffer[0] = ecLevel
                    ecLevelUpdates += 1
                    
                    # Rotate buffer
                    ecLevelBuffer = ecLevelBuffer[-1:] + ecLevelBuffer[:-1]
                    
                    print(ecLevelBuffer)
                    
                # Calculate mean EC level
                meanECLevel = sum(ecLevelBuffer) / len(ecLevelBuffer)   
                
                print("Mean EC level: {:.0f}".format(meanECLevel))                                                                                                                                  
                
                # Water level main tank
                
                # Set first value of buffer                
                waterLevelMainTankBuffer[0] = waterLevelMainTank
                waterLevelMainTankUpdates += 1
                
                # Rotate buffer
                waterLevelMainTankBuffer = waterLevelMainTankBuffer[-1:] + waterLevelMainTankBuffer[:-1]
                
                print(waterLevelMainTankBuffer)
                
                # Calculate mean water level
                meanWaterLevelMainTank = sum(waterLevelMainTankBuffer) / len(waterLevelMainTankBuffer)
                
                print("Current water tank level mean: {:.0f}".format(meanWaterLevelMainTank))
                
                
                # Update database
                database.updateSensors(visibleLight, waterTemperature, meanWaterLevelMainTank)  
                
                
                # Get current time
                now = datetime.now()
                
                # Extract 
                # sunrise_hour = int(userInput.sunrise.seconds / (60*60))
                # sunset_hour = int(userInput.sunset.seconds / (60*60))
                
                # Transform current time into timedelta (of that day)
                now = timedelta(hours = now.hour, minutes = now.minute)

                # Check, if the main tank's water level is too low 
                # and there have been at least 10 water level main tank sensor readings
                # and the current time is within the sunrise sunset hours
                if( (meanWaterLevelMainTank < 60) and (waterLevelMainTankUpdates > 10) and (now > userInput.sunrise) and (now < userInput.sunset)):
                    
                    # Turn water refill pump on
                    gpio.pumpWater.value = 0.2
                    
                    print("Water refill pump turned on")
                    
                    time.sleep(0.5)
                    
                    waterLevelMainTankUpdates = 0
                    
                # Turn water refill pump off
                else:
                    gpio.pumpWater.off()
                    
                
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
                
                # Check, if LEDs are switched on
                if (userInput.ledState == True):
                    
                    # Get current time
                    now = datetime.now()
                    
                    
                    # Transform current time into timedelta (of that day)
                    now = timedelta(hours = now.hour, minutes = now.minute)
                    print(now)
                    
                    # If current time is between sunrise and sunset
                    if( (now > userInput.sunrise) and (now < userInput.sunset) ):    
                        
                        print("Current time is between sunrise and sunset")                                        
                    
                        # If LEDs are set to auto adjust
                        if (userInput.autoLedState == True):
                            
                            # Calculate LED intensity from visibleLight value
                            ledIntensity = 1 - (visibleLight / 1000 / 15)
                            
                            # Set LED intensity
                            gpio.leds13.value = ledIntensity
                            gpio.leds15.value = ledIntensity
                            
                            print("Turned 1:3 LEDs to {0:.0f} % and 1:5 LEDs to {1:.0f} %".format(gpio.leds13.value*100, gpio.leds15.value*100))                            
                        
                        # No auto adjust
                        else:
                            # Turn LEDs on
                            gpio.leds13.value = 0.5
                            gpio.leds15.value = 0.5
                            
                            print("Turned 1:3 LEDs to {0} % and 1:5 LEDs to {1} %".format(gpio.leds13.value*100, gpio.leds15.value*100))
                            
                    # Current time not between sunrise and sunset
                    else:
                        # Turn LEDs off
                        gpio.leds13.off()
                        gpio.leds15.off()
                        
                        print("LEDs switched off")
                    
                # LEDs not switched on
                else: 
                    # Turn LEDs off
                    gpio.leds13.off()
                    gpio.leds15.off()
                    
                    print("LEDs switched off")
                    
                                        
                # Check, if the LED Up button is being pressed
                while (userInput.ledUp == True):
                    
                    gpio.ledUp.value = 0.1
                    print("Moving the LEDs up with {} % power".format(gpio.ledUp.value*100))
                    
                    time.sleep(0.1)
                    
                    # Check userInput data
                    userInput = database.getUserInput()                                          
                    
                # Button not pressed
                else:                    
                    gpio.ledUp.off()
                    print("LED upward movement stopped")
                    
                
                # Check, if the LED Down button is being pressed    
                while (userInput.ledDown == True):
                    
                    gpio.ledDown.value = 0.1                
                    print("Moving the LEDs up with {} % power".format(gpio.ledDown.value*100))
                    
                    time.sleep(0.1)
                    
                    # Check userInput data
                    userInput = database.getUserInput()                                    
                    
                # Button not pressed
                else:
                    gpio.ledDown.off()
                    print("LED downward movement stopped")
                    
                    
                # EC level adaption     
                # if( (meanECLevel < 60) and (waterLevelMainTankUpdates > 10) and (now.hour > userInput.sunrise.hour + 1) and (now.hour < userInput.sunset.hour + 1)):
                
                # Get current time as date object
                now = datetime.now().date()
                
                # Calculate current week number
                elapsed = now - userInput.plantingDate
                elapsed_weeks = int(elapsed.days / 7)
                
                print("Elapsed days since planting: {}".format(elapsed.days))
                print("Elapsed weeks since planting: {}".format(elapsed_weeks))
                
                # Get the current time                
                now = datetime.now()
                    
                # Time inside nutrient table
                if (elapsed_weeks < 9):
                    
                    print("EC level desired: {}".format(nutrientTable[3][elapsed_weeks]))
                    
                    # Transform current time into timedelta (of that day)
                    now = timedelta(hours = now.hour, minutes = now.minute)

                    # Is mean EC level below nutrient table entry and within sunrise/ sunset and the EC level has been updated at least 10 times?
                    if( (meanECLevel < nutrientTable[3][elapsed_weeks]) and (now > userInput.sunrise) and (now < userInput.sunset) and (ecLevelUpdates > 10) ):

                        # Adjust nutrient level            
                        # Turn each pump on for a short moment according to the nutrient table                                  
                        gpio.pumpFloraGro.value = 0.2
                        time.sleep(nutrientTable[1][elapsed_weeks]) 
                        gpio.pumpFloraGro.off()
                        
                        gpio.pumpFloraMicro.value = 0.2
                        time.sleep(nutrientTable[2][elapsed_weeks]) 
                        gpio.pumpFloraMicro.off()
                        
                        gpio.pumpFloraBloom.value = 0.2                                                
                        time.sleep(nutrientTable[3][elapsed_weeks]) 
                        gpio.pumpFloraBloom.off()   
                        
                        ecLevelUpdates = 0                     
                        
                        print("Nutrients refilled")
                                                                  
                        
                # Time outside nutrient table
                else:
                    # Is mean EC level below last nutrient table entry and within sunrise/ sunset and the EC level has been updated at least 10 times?
                    if( (meanECLevel < nutrientTable[3][8]) and (now > userInput.sunrise) and (now < userInput.sunset) and (ecLevelUpdates > 10) ):                    
                        
                        # Adjust nutrient level  
                        # Turn each pump on for a short moment according to the nutrient table              
                        gpio.pumpFloraGro.value = 0.2
                        time.sleep(nutrientTable[1][8]) 
                        gpio.pumpFloraGro.off()
                        
                        gpio.pumpFloraMicro.value = 0.2
                        time.sleep(nutrientTable[2][8]) 
                        gpio.pumpFloraMicro.off()
                        
                        gpio.pumpFloraBloom.value = 0.2                                                
                        time.sleep(nutrientTable[3][8]) 
                        gpio.pumpFloraBloom.off()  
                        
                        ecLevelUpdates = 0
                        
                        print("Nutrients refilled")
    

            # System is switched off
            else:                
                # Turn pH sensor circuit off
                gpio.transistorPH.on()  
                    
                # Turn the LEDs off
                gpio.leds13.off()
                gpio.leds15.off()
                
                print("LEDs switched off")
                
                # Turn the circulation pump off
                gpio.pumpCirculation.off()
                
                print("Turning the circulation pump off")
                
                # Turn the circuits off
                gpio.transistor5V.on()
                gpio.transistor3V3.on()
                
                print("3.3 V and 5 V power circuits turned off")
                
                time.sleep(0.1)
                
            
            print()
                        

        # Catch an error message and display the message
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


# This is the main program
if __name__ == "__main__":
    main()

