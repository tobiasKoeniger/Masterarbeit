#! /usr/bin/python3

# Loading message
print("\n")
print("Libraries loading")

# Loading libraries
import time
from datetime import datetime 
from datetime import timedelta
import sys

from statistics import median

# MySQL library
import mysql.connector


# Load sensor classes
from dht22 import DHT22
from lightSensor import LightSensor
from waterTemperatureSensor import WaterTemperatureSensor
from distanceSensor import DistanceSensor
from pHsensor import PHsensor
from ecSensor import EcSensor


# Load GPIO expander class
from gpioExpander import GPIOExpander

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


    # Initialize classes

    # Database class initialization    
    print("Database init.. ", end = '\n\n')
    database = Database()
    print("\nsuccessful\n")    
        
    
    # Initialize the GPIO class
    print("GPIO init.. ", end = '\n\n')
    gpio = GPIO()
    print("\nsuccessful\n")    
    
    
    # Turn the circuits on for initialization
    gpio.transistor5V.off()
    gpio.transistor3V3.off()
    # gpio.transistorPH.off()
    print("All power circuits turned successfully on\n")    
    
    # Wait for the power supply 
    time.sleep(0.1)
        
    
    # Now, initialize all sensor classes
    
    # GPIO expander    
    print("GPIO expander init.. ", end = '')
    gpioExpander = GPIOExpander() 
    
    # Set the main tank sensor as default
    gpioExpander.setSensor(0)
    print("successful")
    time.sleep(0.1)
    
    # Debug point for distance sensors
    # time.sleep(100000000)
    
    # Light sensor
    print("Light sensor init.. ", end = '')
    lightSensor = LightSensor()
    print("successful")
    
    try: 
        # Water sensor      
        print("Water temperature sensor init.. ", end = '')
        waterTemperatureSensor = WaterTemperatureSensor()
        print("successful")
        
    except (KeyboardInterrupt, SystemExit, OSError):      
        print("Skipping main tank sensor")
        
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
    
    # Number of sensor reading repetetitions to determine the median
    ecLevelRepetitions = 7
    
    # Buffer to save the readings
    ecLevelBuffer = [2] * ecLevelRepetitions
    
    # Interval between ec level detections is set later to 1h = 60 * 60 s
    ecLevelDetectionInterval = 0
    
    ecReadingNumber = 0     
    
    # Default EC level
    ecLevel = 100       
    
    
    # Buffer for main tank's water level sensor: 10 repetitions
    waterLevelMainTankBuffer = [80] * 10
    
    # Interval between tank level detections
    tankLevelDetectionInterval = 60 * 60
    
    # Variable for tank level control
    waitingOnTankLevelDetection = False
    
    # Skip the tank sensor if an error is reported
    skipLevelSensor = False
    
    
    # DHT22 humidty and temperature reading interval = 1 min
    dhtDetectionInterval = 60
    
    
    # Initialize nutrient table matrix
    nutrientTable = [[1, 1, 1, 1.5, 1.5, 1, 0.5, 0.5, 0.5],     # FloraGro
                     [1, 1, 1, 1, 1, 1, 1, 1, 1],               # FloraMicro
                     [1, 1, 1, 0.5, 0.5, 1, 1.5, 1.5, 1.5],     # FloraBloom
                     [0.7, 0.8, 0.8, 0.9, 1, 1, 1, 1, 1]]       # EC level
                     
                     
    # Variables for last sensor readings                    
    last_plantHeight_detection = datetime.now()
    
    last_tankLevel_detection = datetime.now() 
    
    last_ecLevel_detection = datetime.now() 
    
    last_dth22_detection = datetime.now()     
                        
    
    # List to save plant height sensors' reading
    plant_heights = [0, 0, 0]  
    
    # List to save tank levels of each tank
    tank_levels = [0, 0, 0, 0, 0, 0]
                     
    

    # If one manually closes the program with Ctrl+c:
    def cleanAndExit():
        
        print("Cleaning...")
        
        # Closing the database connection
        database.closeConnection()
        
        # Setting all GPIO pins low
        gpioExpander.cleanClose()
            
        print("Bye!")
        print("\n")
        
        # Close the program
        sys.exit()

    
    # Starting system
    start_up = True
    
    # Variable to remember the last system state user input
    last_systemState = False
    

    # Main loop
    # runs forever except if a user exception (ctrl-c) occurs
    while True:
        
        # Try to run the loop
        try:                            
            
            # Check userInput data from database           
            userInput = database.getUserInput()            
        
            # The tables includes: 
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
                        
                        
            # Check, if the system is switched on
            if (userInput.systemState == True):
                                                
                # Switch transistors on if the system state was just enabled
                if(last_systemState == False):
                    
                    # Turn the 3.3 V and 5 V circuits on 
                    gpio.transistor5V.off()
                    gpio.transistor3V3.off()                
                    print("\n3.3 V and 5 V circuits turned on")
                    
                    # Wait for the power
                    time.sleep(0.1)
                    
                # System state has been enabled
                last_systemState = True


                # Reading sensors
                print("\nReading sensors")                            
                
                
                # Read the light sensor values
                [full_spectrum, infrared] = lightSensor.getValues()
                
                # Calculate the share of visible light
                visibleLight = full_spectrum - infrared
                
                # Print the values
                print ("Full Spectrum(IR + Visible) : {} lux".format(full_spectrum) )
                print ("Infrared Value : {} lux".format(infrared) )
                print ("Visible Value : {} lux".format(visibleLight) )                
                
                
                # Read the water temperature sensor
                try: 
                    waterTemperature = waterTemperatureSensor.getTemperature()
                    print ("Water temperature: {:.1f} °C".format(waterTemperature) )
                    
                except (KeyboardInterrupt, SystemExit, OSError):       
                    
                    # Setting water temperature default
                    waterTemperature = 20
                    print ("Skipping water temperature sensor. Setting water temperature to: {:.1f} °C".format(waterTemperature) )
                                    
                
                # Check, if the user switched the LEDs on
                if (userInput.ledState == True):
                    
                    # Get current time
                    now = datetime.now()
                    
                    # Transform current time into timedelta (of that day)
                    now = timedelta(hours = now.hour, minutes = now.minute)
                    # print(now)
                    
                    # If current time is between sunrise and sunset
                    if( (now > userInput.sunrise) and (now < userInput.sunset) ):    
                        
                        print("Current time is between sunrise and sunset")                                        
                    
                        # If LEDs are set by the user to auto adjust
                        if (userInput.autoLedState == True):
                            
                            # Calculate LEDs' target intensity (between 0 and 1) 
                            # from the measured visible light value.
                            # Light target intensity collectively: 150 lux
                            ledIntensity = 1 - (visibleLight / 150 / 100)
                            
                            # If there is more than a 5 % difference between the measured light intensity and the target value
                            if(abs(gpio.leds13.value - ledIntensity) > 0.05):

                                # Adjust the LEDs' intensity upwards by 0.1 %
                                # as long as there is a 0.5 % deviation.
                                # Thereby a smooth intensity transition is achieved.
                                while ((ledIntensity - gpio.leds13.value) > 0.005):                            
                                
                                    gpio.leds13.value += 0.001
                                    gpio.leds15.value += 0.001
                                    
                                    time.sleep(0.001)
                                
                                # Adjust the LEDs' intensity downwards    
                                while ((gpio.leds13.value - ledIntensity) > 0.005):                            
                                
                                    gpio.leds13.value -= 0.001
                                    gpio.leds15.value -= 0.001
                                    
                                    time.sleep(0.001)
                                
                                print("Turned 1:3 LEDs to {0:.0f} % and 1:5 LEDs to {1:.0f} %".format(gpio.leds13.value*100, gpio.leds15.value*100))                            
                        
                        # LEDs are not set to auto adjust
                        else:
                            # Set the LED levels both to 50 %
                            gpio.leds13.value = 0.5
                            gpio.leds15.value = 0.5
                            
                            print("Turned 1:3 LEDs to {0} % and 1:5 LEDs to {1} %".format(gpio.leds13.value*100, gpio.leds15.value*100))
                            
                    # The current time not between sunrise and sunset
                    else:
                        # Turn the LEDs off
                        gpio.leds13.off()
                        gpio.leds15.off()
                        
                        print("LEDs switched off")
                    
                # The LEDs are not switched on by the user
                else: 
                    # Turn LEDs off
                    gpio.leds13.off()
                    gpio.leds15.off()
                    
                    print("LEDs switched off")


                # Initialize control variables at system start up
                if(start_up == True):                                                                            
                    
                    # Print banner
                    print("\nInitial sensor init")
                    print("-------------------")                
                    
                
                # Get current time
                current_time = datetime.now()
                # print(current_time)
                

                # Detect tank levels
                
                # Time since last detection
                time_delta_tankLevel = current_time - last_tankLevel_detection
                
                # If the last tank level detection is more than 1 h ago
                if( (time_delta_tankLevel.seconds > tankLevelDetectionInterval) or (start_up == True) ):  # 60*60
                    
                    # Reset detection interval
                    tankLevelDetectionInterval = 60 * 60
                    
                    # Loop through the sensors
                    for i in range(1, 7):
                        
                        # Turn sensor with gpio expander on
                        gpioExpander.setSensor(i)
                        time.sleep(0.01)
                        
                        # Initialize the sensor
                        distance_sensor = DistanceSensor()
                        
                        # Measure the distance
                        distance = distance_sensor.getDistance()                                                
                        
                        # Save distance in list
                        tank_levels[i - 1] = distance
                        
                        print ("Tank level sensor {0}: {1} mm".format((i), tank_levels[i - 1]) ) 
                                                            
                    # Save current time
                    last_tankLevel_detection = datetime.now()                                        
                    
                    
                    # Set default sensor to main tank level sensor
                    gpioExpander.setSensor(0)
                    
                    time.sleep(0.01)
                    
                    # Initialize sensor
                    mainTankLevelSensor = DistanceSensor()
                    print("Main tank sensor reinitialized")
                    
                    
                    # Read the main tank water level sensor
                    sensorRepetitions = 0
                    
                    # 10 Repetitions
                    while(sensorRepetitions < 10):
                                        
                        try:
                            # Read the sensor's distance
                            distance = mainTankLevelSensor.getDistance()
                            
                            # Calculate the level from the sensor height
                            waterLevelMainTankReading = 247 - distance
                            
                            # Print the reading
                            # print ("Distance of main tank level sensor: {0} mm".format(distance) )                                                         
                            print ("Water level main tank: {0} mm".format(waterLevelMainTankReading) )                                                           
                            
                            # Did not skip
                            skipLevelSensor = False                                                                                    
                            
                        # Catch an error message and display the message
                        except (KeyboardInterrupt, SystemExit, OSError):
                            
                            print("Skipping main tank level sensor")
                            print("X"*90)
                            
                            # Skip
                            skipLevelSensor = True
                                                       
                                                        
                        # If the reading was successful
                        if (skipLevelSensor == False):
                        
                            # Set first value of buffer                
                            waterLevelMainTankBuffer[0] = waterLevelMainTankReading                    
                            
                            # Rotate buffer
                            waterLevelMainTankBuffer = waterLevelMainTankBuffer[-1:] + waterLevelMainTankBuffer[:-1]     
                            
                            # Adjust sensor reading number
                            sensorRepetitions += 1    
                            
                                            
                    # print(waterLevelMainTankBuffer)
                    
                    # Calculate mean water level
                    # waterLevelMainTank = sum(waterLevelMainTankBuffer) / len(waterLevelMainTankBuffer)
                    
                    # Calculate median of buffer
                    waterLevelMainTank = median(waterLevelMainTankBuffer) 
            
                    print("Current water tank level median: {:.0f}".format(waterLevelMainTank))
                                        
                    # Tank level detection succesfull
                    waitingOnTankLevelDetection = False
                    
                
                # Update database
                database.updateSensors(visibleLight, waterTemperature, waterLevelMainTank)  
                
                
                    
                # Get current time
                now = datetime.now()
                
                # Transform current time into timedelta (of that day)
                now = timedelta(hours = now.hour, minutes = now.minute)

                # Check, if the main tank's water level is too low 
                # and there have been at least 10 water level main tank sensor readings
                # and the current time is within the sunrise sunset hours
                if( (waterLevelMainTank < 60) and (now > userInput.sunrise) and (now < userInput.sunset) and (waitingOnTankLevelDetection == False)):
                    
                    # Turn water refill pump on for 3 s
                    gpio.pumpWaterSupply.value = 1      # 0.4                    
                    print("Water refill pump turned on")
                    
                    time.sleep(3)
                    
                    # Turn pump off
                    gpio.pumpWaterSupply.off()
                    
                    # Refresh the main tank's level in 60 seconds
                    tankLevelDetectionInterval = 60
                    
                    # Wait for the main tank level reading before the pump is switched on again
                    waitingOnTankLevelDetection = True                                                                            
                    
                                        
                # Turn the circulation pump on to 30 % (most silent)
                gpio.pumpCirculation.value = 0.0 # 0.3
                print("Turning the circulation pump on to {} %".format(gpio.pumpCirculation.value*100))
                
                                                        
                # DHT22 
                # Air temperature and humidity reading
                # current_time = datetime.now()
                
                # Time since last reading
                time_delta_dht22 = current_time - last_dth22_detection
            
                print("time_delta_dht22.seconds: {}".format(time_delta_dht22.seconds))
                                            
                # On start up or if the detection interval is over
                if( (start_up == True) or (time_delta_dht22.seconds > dhtDetectionInterval ) ):
                    
                    # Read sensor
                    [humidity, temperature] = dht22.getValues()
                    
                    # Print sensor values
                    print("D"*80)
                    print ("Humidity: {:.1f} %".format(humidity) )
                    print ("Temperature: {:.1f} °C".format(temperature) )
                    
                    # Write to database
                    database.updateDHT22(temperature, humidity)
                    
                    # Save time
                    last_dth22_detection = datetime.now()                                    
                
                
                # Calculate time since last plant height detection
                time_delta_plantHeight = current_time - last_plantHeight_detection    
                                                
                # Detect plant height if the detection interval is up
                # The time since the last detection was already calculated above
                if( (start_up == True) or (time_delta_plantHeight.seconds > 60 * 60) ): # 60*60
                    
                    # Loop through the sensors
                    for i in range(7, 10):
                        
                        # Enable sensor
                        gpioExpander.setSensor(i)
                        time.sleep(0.01)
                        
                        # Initialize sensor
                        distance_sensor = DistanceSensor()                        
                        
                        # Measure 
                        distance = distance_sensor.getDistance()
                        
                        # Save
                        plant_heights[i - 7] = distance
                        
                        # Print value
                        print ("Distance plant height sensor {0}: {1} mm".format((i-6), plant_heights[i - 7]) ) 
                    
                    # Save time
                    last_plantHeight_detection = datetime.now()                                    
                    
                    
                    # Set main tank level sensor
                    gpioExpander.setSensor(0)
                    
                    time.sleep(0.01)
                    
                    # Reinitialize default sensor
                    mainTankLevelSensor = DistanceSensor()
                    print("Main tank sensor reinitialized")                       
               
                
                # EC level
                
                # Get current time                
                current_time = datetime.now()
                
                # Time since last detection
                time_delta_ecLevel = current_time - last_ecLevel_detection                
                
                print("time_delta_ecLevel.seconds: {}".format(time_delta_ecLevel.seconds))
                
                
                #################################
                # EC level detection not in a row
                
                # # Waiting time between individual measurements
                # timeBetweenECMeasurements = 15 # 30                    
                
                # # Time of next reading
                # nextECReading = timeBetweenECMeasurements * ecReadingNumber + 6 + ecLevelDetectionInterval
                       
                # print("nextECReading: {}".format(nextECReading))
                
                # # If one reading sequence has not been completed and the interval between readings is up:
                # if((ecReadingNumber < ecLevelRepetitions) and (time_delta_ecLevel.seconds > nextECReading)): 

                    # # Try to make a measurement
                    # try:
                        
                        # # Print reading number
                        # print(str(ecReadingNumber + 1)*90)
                        # print("\n\nEC Reading No. {}".format(ecReadingNumber + 1))
                        
                        # # Wait for voltage stabilization
                        # time.sleep(0.2)
                        
                        # # Read the sensor
                        # ecLevelReading = ecsensor.getEC()                
                        
                        # # Set first value of buffer                
                        # ecLevelBuffer[0] = ecLevelReading                
                        
                        # # Rotate buffer
                        # ecLevelBuffer = ecLevelBuffer[-1:] + ecLevelBuffer[:-1]         
                        
                        # print("ecLevelBuffer: {}".format(ecLevelBuffer))                                                                                                                                               

                        # # Reading number up
                        # ecReadingNumber += 1
                                                                            
                    # # Catch an error message and display the message
                    # except (KeyboardInterrupt, SystemExit):
                        # cleanAndExit()
                                        
                # # If all readings of one detection cycle were concluded 
                # if(ecReadingNumber >= ecLevelRepetitions):
                                    
                    # # print(ecLevelBuffer)                              
                    
                    # # print(ecLevelBuffer[1:ecLevelRepetitions])
                    # # print((len(ecLevelBuffer) - 1))
                    
                    # # Calculate mean water level
                    # # ecLevel = sum(ecLevelBuffer[1:ecLevelRepetitions]) / (len(ecLevelBuffer) - 1)
                    # # ecLevel = sum(ecLevelBuffer) / len(ecLevelBuffer)
                    
                    # # Calculate median
                    # ecLevel = median(ecLevelBuffer)
                    
                    # # Update database
                    # database.updateEC(ecLevel)    
                    
                    # # Set detection interval
                    # ecLevelDetectionInterval = 60 * 60                                                                        
                                    
                    # # Restart counting
                    # ecReadingNumber = 0                
                    
                    # # Save time
                    # last_ecLevel_detection = datetime.now()                       
                    
                    # print("===================================================================================") 
            
                    # print("Current EC level median: {:.3f}".format(ecLevel))    
                
                
                #############################
                # EC level detection in a row
                
                # If the interval is up or start up true
                if((time_delta_ecLevel.seconds > ecLevelDetectionInterval) or (start_up == True)): # 60*60  
                    
                    # Reset detection interval
                    ecLevelDetectionInterval = 60*60 
                    
                    # Let the voltage settle
                    time.sleep(3)                                                      
                
                    # Set reading number
                    readingNumber = 0
                    
                    # Drop the first three readings
                    while(readingNumber < ecLevelRepetitions + 3): 
            
                        # Try to run the loop
                        try:
                            
                            print("\n\nEC Reading No. {}".format(readingNumber + 1))
                            
                            # Read sensor
                            ecLevelReading = ecsensor.getEC()                
                            
                            # Set first value of buffer                
                            ecLevelBuffer[0] = ecLevelReading                
                            
                            # Rotate buffer
                            ecLevelBuffer = ecLevelBuffer[-1:] + ecLevelBuffer[:-1]                                                                                                                                                         

                            # Adjust reading number
                            readingNumber += 1
                                                        
                            
                        # Catch an error message and display the message
                        except (KeyboardInterrupt, SystemExit):
                            cleanAndExit()
                        
                        
                        # Sleep for the ions to settle
                        T = 1
                        time.sleep(T)                        
                    
                    
                    # Print buffer
                    print(ecLevelBuffer)    
                    
                    # Calculate mean water level
                    # ecLevel = sum(ecLevelBuffer) / len(ecLevelBuffer)
                    
                    # Calculate median
                    ecLevel = median(ecLevelBuffer)
            
                    print("Current EC level median: {:.3f}".format(ecLevel))
                    
                    # Update database
                    database.updateEC(ecLevel)  
                    
                    # Save time
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
                
                # If the current time is within the active hours
                # and the user turned auto adaption on
                if ((now > userInput.sunrise) and (now < userInput.sunset) and (userInput.autoHeightAdaptionState == True)):
                    
                    # As long as one sensor senses a plant
                    while ((plant_heights[0] < 500) or (plant_heights[1] < 500) or (plant_heights[2] < 500)):
                        
                        # Adjust LED height
                        # Enable actuator
                        gpio.ledUp.value = 0.15
                        print("Moving the LEDs up with {} % power".format(gpio.ledUp.value*100))
                                                
                        time.sleep(0.1)
                        
                        # Check sensors again
                        for i in range(7, 10):
                        
                            # Set sensor
                            gpioExpander.setSensor(i)
                            time.sleep(0.1)
                            
                            # Initialize sensor
                            distance_sensor = DistanceSensor()                        
                           
                            # Read sensor
                            distance = distance_sensor.getDistance()
                            
                            # Save value
                            plant_heights[i - 7] = distance
                            
                            print ("Distance plant height sensor {0}: {1} mm".format((i-6), plant_heights[i - 7]) )                         
                    
                    # Disable actuator
                    gpio.ledUp.off()
                    print("LED upward movement stopped")                
                    
                
                # Manual LED height adjustment
                led_movement_was_on = False
                                        
                # Check, if the LED Up button is being pressed
                while (userInput.ledUp == True):
                    
                    # Move LEDs up with full speed
                    gpio.ledUp.value = 1
                    print("Moving the LEDs up with {} % power".format(gpio.ledUp.value*100))
                                        
                    time.sleep(0.5)
                    
                    # Check userInput data again
                    userInput = database.getUserInput()                                                     
                    
                # Button not pressed
                else: 
                    # Disable motor                   
                    gpio.ledUp.off()
                    print("LED upward movement stopped")
                                                            
                
                # Check, if the LED Down button is being pressed    
                while (userInput.ledDown == True):
                    
                    gpio.ledDown.value = 1                
                    print("Moving the LEDs up with {} % power".format(gpio.ledDown.value*100))
                    
                    time.sleep(0.5)
                    
                    # Check userInput data
                    userInput = database.getUserInput()                                
                    
                # Button not pressed
                else:
                    gpio.ledDown.off()
                    print("LED downward movement stopped")
                                                                
                
                # Get current time as date object
                now = datetime.now().date()
                
                # Calculate current week number
                elapsed = now - userInput.plantingDate
                elapsed_weeks = int(elapsed.days / 7)
                
                print("Elapsed days since planting: {}".format(elapsed.days))
                print("Elapsed weeks since planting: {}".format(elapsed_weeks))
                
                # Get the current time                
                now = datetime.now()
                    
                # Current week number within nutrient table?
                if (elapsed_weeks < 9):
                    
                    print("EC level desired: {}".format(nutrientTable[3][elapsed_weeks]))
                    
                    # Transform current time into timedelta (of that day)
                    now = timedelta(hours = now.hour, minutes = now.minute)

                    # Is mean EC level below nutrient table entry and within sunrise/ sunset and the EC level has been updated at least 10 times?
                    if( (ecLevel < nutrientTable[3][elapsed_weeks]) and (now > userInput.sunrise) and (now < userInput.sunset) and False):

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
                        
                        print("Nutrients refilled")
                        
                        # Next EC level detection in 10 min                        
                        ecLevelDetectionInterval = 60*5                        
                                                                  
                        
                # Time outside nutrient table
                else:
                    # Is mean EC level below last nutrient table entry and within sunrise/ sunset and the EC level has been updated at least 10 times?
                    if( (ecLevel < nutrientTable[3][8]) and (now > userInput.sunrise) and (now < userInput.sunset) and False):                    
                        
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
                        
                        
                # Start up over
                start_up = False
    

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
                
                # Safe system state
                last_systemState = False
                
                # Wait 0.1 for new user input
                time.sleep(0.1)
                
            
            print("\n")
                        

        # Catch an error message and display the message
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


# This is the main program
if __name__ == "__main__":
    main()

