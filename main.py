#! /usr/bin/python3

print("\n")
print("Libraries loading")

# Loading libraries
import time
from datetime import datetime 
from datetime import timedelta
import sys

from statistics import median

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
from ecSensor import EcSensor


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
    # gpio.transistorPH.off()
    print("All power circuits turned on")
    
    print("\nsuccessful")
    
    time.sleep(0.1)
    
    print()
    
    # Now, initialize all sensor classes
    
    # GPIO expander    
    print("GPIO expander init.. ", end = '')
    gpioExpander = GPIOExpander() 
    gpioExpander.setSensor(0)
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
    mainTankLevelSensor = DistanceSensor()
    print("successful")
    
    # PH sensor
    print("PH sensor init.. ", end = '')
    pHsensor = PHsensor()
    print("successful")
    
    # DHT22: temperature and humidity
    print("*Temperature and humidity sensor init.. ", end = '')
    dht22 = DHT22()
    print("*successful")
    
    # EC sensor
    print("EC sensor init.. ", end = '')
    ecsensor = EcSensor()
    print("successful")
    
    
    # EC level detection repetitions and buffer
    ecLevelRepetitions = 10
    ecLevelBuffer = [2] * ecLevelRepetitions
    ecLevelDetectionInterval = 60*60 
    
    
    # Initialize main tank's water level buffer
    waterLevelMainTankBuffer = [80] * 10
    
    tankLevelDetectionInterval = 60 * 60
    
    waitingOnTankLevelDetection = False
    
    # DHT22 interval
    dhtDetectionInterval = 60
    
    # Number of tank level updates
    waterLevelMainTankUpdates = 0
    
    # Skip the sensor if an error is reported
    skipLevelSensor = False
    
    
    # Initialize nutrient matrix
    nutrientTable = [[1, 1, 1, 1.5, 1.5, 1, 0.5, 0.5, 0.5],     # FloraGro
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],               # FloraMicro
                     [1, 1, 1, 0.5, 0.5, 1, 1.5, 1.5, 1.5],     # FloraBloom
                     [0.7, 0.8, 0.8, 0.9, 1, 1, 1, 1, 1]]
        
    
    # Turn PH sensor off
    gpio.transistorPH.on()
    print("PH meter circuit turned off")
    
    
    print()
    print()
    

    # If one manually closes the program with Ctrl+c:
    def cleanAndExit():
        
        print("Cleaning...")
        
        # Closing the database connection
        # mycursor.close()
        # mydb.close()

        # GPIO.cleanup()
        
        database.closeConnection()
        
        gpioExpander.cleanClose()
            
        print("Bye!")
        print("\n")
        
        # Close the program
        sys.exit()


    # Get current user input from the database
    userInput = database.getUserInput()  
    
    # Starting system
    start_up = True
    
    # Remember last system state user input
    last_systemState = False
    

    # Main loop
    while True:
        
        # Try to run the loop
        try:                            
            
            # Check userInput data            
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
                                                
                # Switch transistors on if system state was just enabled
                if(last_systemState == False):
                    
                    # Turn the 3.3 V and 5 V circuits on 
                    gpio.transistor5V.off()
                    gpio.transistor3V3.off()                
                    print("3.3 V and 5 V circuits turned on")
                    
                    time.sleep(0.1)
                    
                # System state has been enabled
                last_systemState = True


                # Reading sensors
                print("Reading sensors")                            
                
                # Read the light sensor values
                [full_spectrum, infrared] = lightSensor.getValues()
                
                # Calculate the share of visible light
                visibleLight = full_spectrum - infrared
                
                print ("Full Spectrum(IR + Visible) : {} lux".format(full_spectrum) )
                print ("Infrared Value : {} lux".format(infrared) )
                print ("Visible Value : {} lux".format(visibleLight) )                
                
                # Read the water temperature sensor
                try: 
                    waterTemperature = waterTemperatureSensor.getTemperature()
                    print ("Water temperature: {:.1f} °C".format(waterTemperature) )
                    
                except (KeyboardInterrupt, SystemExit, OSError):                    
                    waterTemperature = 20
                    print ("Skipping water temperature sensor. Setting water temperature to: {:.1f} °C".format(waterTemperature) )
                                    
                
                # Check, if the LEDs are switched on
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
                            
                            if(abs(gpio.leds13.value - ledIntensity) > 0.05):
                            
                                while ((ledIntensity - gpio.leds13.value) > 0.005):                            
                                
                                    gpio.leds13.value += 0.001
                                    gpio.leds15.value += 0.001
                                    
                                    time.sleep(0.001)
                                    
                                while ((gpio.leds13.value - ledIntensity) > 0.005):                            
                                
                                    gpio.leds13.value -= 0.001
                                    gpio.leds15.value -= 0.001
                                    
                                    time.sleep(0.001)
                                
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


                
                # Detect plant height and tank levels
                
                current_time = datetime.now()
                # print(current_time)
                
                if(start_up == True):
                                        
                    last_plantHeight_detection = datetime.now()
                    
                    last_tankLevel_detection = datetime.now() 
                    
                    last_ecLevel_detection = datetime.now() 
                    
                    last_dth22_detection = datetime.now() 
                    
                    ecReadingNumber = 0 
                    
                    start_up = False                
                    
                    plant_heights = [0, 0, 0]  
                    
                    tank_levels = [0, 0, 0, 0, 0, 0]         
                    
                    meanECLevel = 100       
                    
                    ec_start_up = True                                        
                    
                    dth_start_up = True
                    
                    
                time_delta_plantHeight = current_time - last_plantHeight_detection
            
                print(time_delta_plantHeight.seconds)
                
                
                
                if(time_delta_plantHeight.seconds == 86399):
                    
                    print("\nInitial sensor init")
                    print("-------------------")   
                
                
                # Detect tank levels
                time_delta_tankLevel = current_time - last_tankLevel_detection
                
                if(time_delta_tankLevel.seconds > tankLevelDetectionInterval): # 60*60
                    
                    tankLevelDetectionInterval = 60 * 60
                    
                    for i in range(1, 7):
                        
                        # Detect plant height
                        gpioExpander.setSensor(i)
                        time.sleep(0.01)
                        
                        # Reinitialize sensor
                        distance_sensor = DistanceSensor()
                        
                        distance = distance_sensor.getDistance()                                                
                        
                        tank_levels[i - 1] = distance
                        
                        print ("Tank level sensor {0}: {1} mm".format((i), tank_levels[i - 1]) ) 
                                        
                                        
                    last_tankLevel_detection = datetime.now()
                    
                    start_up = False
                    
                    
                    # Set main tank level sensor
                    gpioExpander.setSensor(0)
                    
                    time.sleep(0.01)
                    
                    # Reinitialize sensor
                    mainTankLevelSensor = DistanceSensor()
                    print("Main tank sensor reinitialized")
                    
                    
                    sensorRepetitions = 0
                    
                    while(sensorRepetitions < 10):
                    
                        # Read the main water level sensor
                        try:
                            distance = mainTankLevelSensor.getDistance()
                            waterLevelMainTank = 247 - distance
                            
                            # print ("Distance of main tank level sensor: {0} mm".format(distance) )                                                         
                            print ("Water level main tank: {0} mm".format(waterLevelMainTank) )   
                            
                            # time.sleep(0.5)
                            
                            skipLevelSensor = False
                                                                                    
                            
                        # Catch an error message and display the message
                        except (KeyboardInterrupt, SystemExit, OSError):
                            print("Skipping main tank level sensor")
                            print("X"*90)
                            skipLevelSensor = True
                                                        
                            
                        if (skipLevelSensor == False):
                        
                            # Set first value of buffer                
                            waterLevelMainTankBuffer[0] = waterLevelMainTank
                            waterLevelMainTankUpdates += 1
                            
                            # Rotate buffer
                            waterLevelMainTankBuffer = waterLevelMainTankBuffer[-1:] + waterLevelMainTankBuffer[:-1]     
                            
                            sensorRepetitions += 1    
                        
                        
                    print(waterLevelMainTankBuffer)
                    
                    # Calculate mean water level
                    # meanWaterLevelMainTank = sum(waterLevelMainTankBuffer) / len(waterLevelMainTankBuffer)
                    
                    meanWaterLevelMainTank = median(waterLevelMainTankBuffer) 
            
                    print("Current water tank level median: {:.0f}".format(meanWaterLevelMainTank))
                                        
                    waitingOnTankLevelDetection = False
                    
                
                # Update database
                database.updateSensors(visibleLight, waterTemperature, meanWaterLevelMainTank)  
                
                
                    
                # Get current time
                now = datetime.now()
                
                # Transform current time into timedelta (of that day)
                now = timedelta(hours = now.hour, minutes = now.minute)

                # Check, if the main tank's water level is too low 
                # and there have been at least 10 water level main tank sensor readings
                # and the current time is within the sunrise sunset hours
                if( (meanWaterLevelMainTank < 60) and (now > userInput.sunrise) and (now < userInput.sunset) and (waitingOnTankLevelDetection == False)):
                    
                    # Turn water refill pump on
                    gpio.pumpWaterSupply.value = 1 # 0.4
                    
                    print("Water refill pump turned on")
                    
                    time.sleep(3)
                    
                    gpio.pumpWaterSupply.off()
                    
                    tankLevelDetectionInterval = 60
                    
                    waitingOnTankLevelDetection = True                                                            
                    
                    
                # Turn water refill pump off
                else:
                    gpio.pumpWaterSupply.off()
                    
                    
                    
                # Turn the circulation pump on
                gpio.pumpCirculation.value = 0.3
                print("Turning the circulation pump on to {} %".format(gpio.pumpCirculation.value*100))
                
                    
                    
                # DHT22
                # current_time = datetime.now()
                time_delta_dht22 = current_time - last_dth22_detection
            
                print("time_delta_dht22.seconds: {}".format(time_delta_dht22.seconds))
                                            
                    
                if( (dth_start_up == True) or (time_delta_dht22.seconds > dhtDetectionInterval ) ):
                    
                    [humidity, temperature] = dht22.getValues()
                    
                    print("D"*80)
                    print ("Humidity: {:.1f} %".format(humidity) )
                    print ("Temperature: {:.1f} °C".format(temperature) )
                    
                    database.updateDHT22(humidity, temperature)
                    
                    last_dth22_detection = datetime.now()
                   
                    dth_start_up = False
                
                
                
                # Detect plant height
                if(time_delta_plantHeight.seconds > 60*60): # 60*60
                    
                    for i in range(7, 10):
                        
                        # Detect plant height
                        gpioExpander.setSensor(i)
                        time.sleep(0.01)
                        

                        distance_sensor = DistanceSensor()                        
                        
                        distance = distance_sensor.getDistance()
                        
                        plant_heights[i - 7] = distance
                        
                        print ("Distance plant height sensor {0}: {1} mm".format((i-6), plant_heights[i - 7]) ) 
                    
                    
                    last_plantHeight_detection = datetime.now()
                    
                    start_up = False
                    
                    
                    # Set main tank level sensor
                    gpioExpander.setSensor(0)
                    
                    time.sleep(0.01)
                    
                    # Reinitialize sensor
                    mainTankLevelSensor = DistanceSensor()
                    print("Main tank sensor reinitialized")
                

                   
                if(time_delta_plantHeight.seconds == 86399):
                    
                    print("Sensor init finished")
                    print("--------------------\n")
                    
                            
               
                
                # EC level
                
                # Read EC level
                
                current_time = datetime.now()
                
                # Detect tank levels
                time_delta_ecLevel = current_time - last_ecLevel_detection
                
                
                print("time_delta_ecLevel.seconds: {}".format(time_delta_ecLevel.seconds))
                
                # timeBetweenECMeasurements = 15 # 30                    
                # nextECReading = timeBetweenECMeasurements * ecReadingNumber + 6
                
                # print("nextECReading: {}".format(nextECReading))
                
                # if((ecReadingNumber < ecLevelRepetitions) and (time_delta_ecLevel.seconds > nextECReading)): # 10

                    # # Try to make a measurement
                    # try:
                        
                        # print(str(ecReadingNumber + 1)*90)
                        # print("\n\nEC Reading No. {}".format(ecReadingNumber + 1))
                        
                        # time.sleep(0.2)
                        # ecLevel = ecsensor.getEC()                
                        
                        # # Set first value of buffer                
                        # ecLevelBuffer[0] = ecLevel                
                        
                        # # Rotate buffer
                        # ecLevelBuffer = ecLevelBuffer[-1:] + ecLevelBuffer[:-1]         
                        
                        # print("ecLevelBuffer: {}".format(ecLevelBuffer))                                                                                                                                               

                        # ecReadingNumber += 1
                                                    
                        
                    # # Catch an error message and display the message
                    # except (KeyboardInterrupt, SystemExit):
                        # cleanAndExit()
                
                # # T = 7
                # # time.sleep(T)
                
                # if(ecReadingNumber >= ecLevelRepetitions):
                                    
                    # # print(ecLevelBuffer)                              
                    
                    # print(ecLevelBuffer[1:ecLevelRepetitions])
                    # print((len(ecLevelBuffer) - 1))
                    
                    # # Calculate mean water level
                    # # meanECLevel = sum(ecLevelBuffer[1:ecLevelRepetitions]) / (len(ecLevelBuffer) - 1)
                    # # meanECLevel = sum(ecLevelBuffer) / len(ecLevelBuffer)
                    
                    # meanECLevel = median(ecLevelBuffer)
                    
                    # database.updateEC(meanECLevel)                                                                            
                                            
                    # ecReadingNumber = 0                
                    
                    # last_ecLevel_detection = datetime.now()   
                    
                    # print("===================================================================================") 
            
                    # print("Current EC level median: {:.3f}".format(meanECLevel))    
                    
                    # ec_start_up = False      
                
                
                
                print("time_delta_ecLevel.seconds: {}".format(time_delta_ecLevel.seconds))
                
                if((time_delta_ecLevel.seconds > ecLevelDetectionInterval) or (ec_start_up == True)): # 60*60  
                    
                    ecLevelDetectionInterval = 60*60 
                    
                    time.sleep(3)                                                      
                
                    readingNumber = 0
                    
                    while(readingNumber < 13): # 10
            
                        # Try to run the loop
                        try:
                            
                            print("\n\nEC Reading No. {}".format(readingNumber + 1))
                            
                            ecLevel = ecsensor.getEC()                
                            
                            # Set first value of buffer                
                            ecLevelBuffer[0] = ecLevel                
                            
                            # Rotate buffer
                            ecLevelBuffer = ecLevelBuffer[-1:] + ecLevelBuffer[:-1]                                                                                                                                                         

                            readingNumber += 1
                                                        
                            
                        # Catch an error message and display the message
                        except (KeyboardInterrupt, SystemExit):
                            cleanAndExit()
                        
                        T = 1
                        time.sleep(T)                        
                    
                    
                    print(ecLevelBuffer)    
                    
                    # Calculate mean water level
                    # meanECLevel = sum(ecLevelBuffer) / len(ecLevelBuffer)
                    
                    meanECLevel = median(ecLevelBuffer)
            
                    print("Current EC level median: {:.3f}".format(meanECLevel))
                    
                    # Update database
                    database.updateEC(meanECLevel)  
                    
                    
                    ec_start_up = False
                    
                    last_ecLevel_detection = datetime.now()
                                                                                                                                     

                

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
                
                
                
                # Auto Adjust LED height 
                
                # Get current time
                now = datetime.now()
                
                # Transform current time into timedelta (of that day)
                now = timedelta(hours = now.hour, minutes = now.minute)
                
                if ((now > userInput.sunrise) and (now < userInput.sunset) and (userInput.autoHeightAdaptionState == True)):
                    
                    while ((plant_heights[0] < 500) or (plant_heights[1] < 500) or (plant_heights[2] < 500)):
                        
                        # Adjust LED height
                        gpio.ledUp.value = 0.15
                        print("Moving the LEDs up with {} % power".format(gpio.ledUp.value*100))
                        
                        time.sleep(0.1)
                        
                        # Check sensors again
                        for i in range(7, 10):
                        
                            # Detect plant height
                            gpioExpander.setSensor(i)
                            time.sleep(0.1)
                            
                            # Reinitialize sensor
                            distance_sensor = DistanceSensor()                        
                            
                            distance = distance_sensor.getDistance()
                            
                            plant_heights[i - 7] = distance
                            
                            print ("Distance plant height sensor {0}: {1} mm".format((i-6), plant_heights[i - 7]) ) 
                        
                        # time.sleep(0.1)
                        
                    gpio.ledUp.off()
                    print("LED upward movement stopped")                
                    
                    
                led_movement_was_on = False
                                        
                # Check, if the LED Up button is being pressed
                while (userInput.ledUp == True):
                    
                    gpio.ledUp.value = 1
                    print("Moving the LEDs up with {} % power".format(gpio.ledUp.value*100))
                    
                    time.sleep(0.5)
                    
                    # Check userInput data
                    userInput = database.getUserInput()     
                    
                    led_movement_was_on = True                                     
                    
                # Button not pressed
                else:                    
                    gpio.ledUp.off()
                    print("LED upward movement stopped")
                    
                    if (led_movement_was_on == True):
                        
                        time.sleep(0.5)
                        
                        # Reinitialize sensor
                        mainTankLevelSensor = DistanceSensor()
                        print("Main tank sensor reinitialized")
                        
                        led_movement_was_on = False
                    
                
                # Check, if the LED Down button is being pressed    
                while (userInput.ledDown == True):
                    
                    gpio.ledDown.value = 1                
                    print("Moving the LEDs up with {} % power".format(gpio.ledDown.value*100))
                    
                    time.sleep(0.5)
                    
                    # Check userInput data
                    userInput = database.getUserInput()                
                    
                    led_movement_was_on = True                    
                    
                # Button not pressed
                else:
                    gpio.ledDown.off()
                    print("LED downward movement stopped")
                    
                    if (led_movement_was_on == True):
                        
                        time.sleep(0.5)
                        
                        # Reinitialize sensor
                        mainTankLevelSensor = DistanceSensor()
                        print("Main tank sensor reinitialized")
                        
                        led_movement_was_on = False
                    
                    
                    
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
                    if( (meanECLevel < nutrientTable[3][elapsed_weeks]) and (now > userInput.sunrise) and (now < userInput.sunset) and False):

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
                        
                        # Next EC level detection in 10 min                        
                        ecLevelDetectionInterval = 60*5                        
                                                                  
                        
                # Time outside nutrient table
                else:
                    # Is mean EC level below last nutrient table entry and within sunrise/ sunset and the EC level has been updated at least 10 times?
                    if( (meanECLevel < nutrientTable[3][8]) and (now > userInput.sunrise) and (now < userInput.sunset) and False):                    
                        
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
                        
                        print("Nutrients refilled")
                        
                        # Next EC level detection in 10 min                        
                        ecLevelDetectionInterval = 60*5  
    

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
                
                last_systemState = False
                
                time.sleep(0.1)
                
            
            print()
                        

        # Catch an error message and display the message
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


# This is the main program
if __name__ == "__main__":
    main()

