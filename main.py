#! /usr/bin/python3

print("\n")
print("Libraries loading")

# Loading libraries
import time 
import sys

# Raspberry GPIO libraries
import RPi.GPIO as GPIO
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


# Begin of main program
def main():

    # Show welcome header
    print("--------------------------")
    print("Hydroponics Software Start")
    print()

    
    # Read database credentials from .txt file
    try:
        # Open file
        with open('credentials.txt', 'r') as reader:
            credentials = reader.readlines()
        print("Reading credentials successful")
        
    # Show error message
    except Error as err:
        print(f"Error: '{err}'")
    
    # Remove trailing spaces from read strings
    host = credentials[2].rstrip()    
    user = credentials[5].rstrip()
    password = credentials[8].rstrip()
    
    print(host + ", " + user + ", " + password)
    
    
    # Connect to the MySQL database
    try:
        mydb = mysql.connector.connect(
        
            host=host,
            user=user,
            password=password
        )
        print("MySQL Database connection successful")
        
    # Show error message
    except Error as err:
        print(f"The error '{e}' occurred")
        
    
    mycursor = mydb.cursor()
    
    # Fetch all database names
    mycursor.execute("SHOW DATABASES")
    databaseNames = mycursor.fetchall()
    
    # Check if database 'hydroponics' is available
    if not 'hydroponics' in str(databaseNames):
                
        # If not, create new database
        mycursor.execute("CREATE DATABASE hydroponics")
        print("Database hydroponics created")            

    # Close connection
    mycursor.close()
    mydb.close()
    
    
    # Now, try to directly connect to the 'hydroponics' database
    try:
        mydb = mysql.connector.connect(
        
            host="localhost",
            user=user,
            password=password,
            database="hydroponics"
        )
        print("Connection to MySQL Database hydroponics successful")
        
    # Show error
    except Error as err:
        print(f"The error '{e}' occurred")
        
    mycursor = mydb.cursor()
    
    # Fetch all table names
    mycursor.execute("SHOW TABLES")
    tableNames = mycursor.fetchall()
    
    
    # Check, if table 'sensors' is available
    if not 'sensors' in str(tableNames):
        
        # If not, create table 'sensors'
        query = """ CREATE TABLE sensors (
            time DATETIME,
            temperature DOUBLE(8, 3),
            humidity DOUBLE(8, 3),
            lightIntensity DOUBLE(8, 3),
            waterTemperature DOUBLE(8, 3),
            ecLevel DOUBLE(8, 3),
            phLevel DOUBLE(8, 3),
            waterLevel DOUBLE(8, 3)  
        ); """
        
        mycursor.execute(query)
        print("Table sensors created")
        
        # Insert one data row with zeroes
        sql = "INSERT INTO sensors VALUES (NOW(), 0, 0, 0, 0, 0, 0, 0)"
        mycursor.execute(sql)

        mydb.commit()
        
    
    # Check, if table 'userInput' is available
    if not 'userInput' in str(tableNames):
        
        # If not, create table 'userInput'
        query = """ CREATE TABLE userInput (
            time DATETIME,
            systemState BOOLEAN,
            pHmeasureState BOOLEAN,
            ledState BOOLEAN,
            autoLedState BOOLEAN,
            sunrise TIME,
            sunset TIME,
            autoHeightAdaptionState BOOLEAN,
            plantingDate DATE, 
            ledUp BOOLEAN,
            ledDown BOOLEAN
        ); """

        
        mycursor.execute(query)
        print("Table userInput created")    
        
        # Insert one data row with default values
        sql = "INSERT INTO userInput VALUES (NOW(), FALSE, FALSE, FALSE, TRUE, '08:00:00', '20:00:00', TRUE, CURDATE(), FALSE, FALSE)"
        mycursor.execute(sql)

        mydb.commit()

    
    print()
    
    # Now, start the program:
    
    # Initialize the power control transistors
    transistor5V = LED(16)
    transistor3V3 = LED(26)
    transistorPH = LED(6)
    
    # Power 5 V on
    transistor5V.off()
    print("5 V circuit powered on")
    
    # Power 3.3 V on 
    transistor3V3.off()
    print("3.3 V circuit powered on")
    
    # Power the pH sensor on 
    transistorPH.off()
    print("PH sensor powered on")
    
    # time.sleep(1)
    
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
    print("GPIO expander init.. ", end = '')
    gpioExpander = GPIOExpander() 
    print("successful")
    
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
            
            # Read the humidity and temperature values from the DHT22
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
            
            
            # Read the pH sensor
            pH = pHsensor.getPH()
            print ("PH: {:.3f}".format(pH))    
              
              
            # Update the sensor data in the database table 'hydroponics'
                        
            sql = """UPDATE sensors SET 
                        time = NOW(), 
                        temperature = %s, 
                        humidity = %s, 
                        lightIntensity = %s, 
                        waterTemperature = %s,
                        ecLevel = %s,
                        phLevel = %s,
                        waterLevel = %s"""
            
            data = (temperature, humidity, visibleLight, waterTemperature, 0, pH, distance1)            
            
            mycursor.execute(sql, data)

            mydb.commit()
            
            
            # Print the database tabel 'userInput'
            mycursor.execute("SELECT * FROM userInput")

            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)
            
            
            print()
            
            # Do not sleep
            time.sleep(0)

        # Catch an error message and display the message
        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


# This is the main program
if __name__ == "__main__":
    main()
