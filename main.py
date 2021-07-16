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
    try:
        with open('credentials.txt', 'r') as reader:
            credentials = reader.readlines()
        print("Reading credentials successful")
        
    except Error as err:
        print(f"Error: '{err}'")
    
    host = credentials[2].rstrip()    
    user = credentials[5].rstrip()
    password = credentials[8].rstrip()
    
    print(host + ", " + user + ", " + password)
    
    
    try:
        mydb = mysql.connector.connect(
        
            host=host,
            user=user,
            password=password
        )
        print("MySQL Database connection successful")
        
    except Error as err:
        print(f"The error '{e}' occurred")
        
    
    mycursor = mydb.cursor()
    
    mycursor.execute("SHOW DATABASES")
    databaseNames = mycursor.fetchall()
    
    if not 'hydroponics' in str(databaseNames):
                
        mycursor.execute("CREATE DATABASE hydroponics")
        print("Database hydroponics created")            

    mycursor.close()
    mydb.close()
    
    
    try:
        mydb = mysql.connector.connect(
        
            host="localhost",
            user=user,
            password=password,
            database="hydroponics"
        )
        print("Connection to MySQL Database hydroponics successful")
        
    except Error as err:
        print(f"The error '{e}' occurred")
        
    mycursor = mydb.cursor()
    
    mycursor.execute("SHOW TABLES")
    tableNames = mycursor.fetchall()
    
    # if 'sensors' in str(tableNames):

        # mycursor.execute("DROP TABLE sensors")
        
        # mycursor.execute("SHOW TABLES")
        # tableNames = mycursor.fetchall()
        
        
    # if 'userInput' in str(tableNames):

        # mycursor.execute("DROP TABLE userInput")
        
        # mycursor.execute("SHOW TABLES")
        # tableNames = mycursor.fetchall()
    
    
    if not 'sensors' in str(tableNames):
        
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
        
        # Insert one row
        sql = "INSERT INTO sensors VALUES (NOW(), 0, 0, 0, 0, 0, 0, 0)"
        mycursor.execute(sql)

        mydb.commit()
        
        
    if not 'userInput' in str(tableNames):
        
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
        
        # Insert one row
        # sql = "INSERT INTO userInput VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # data = ("NOW()", "FALSE", "FALSE", "FALSE", "TRUE", "08:00:00", "20:00:00", "TRUE", "CURDATE()", "FALSE", "FALSE")
        # mycursor.execute(sql, data)
        
        sql = "INSERT INTO userInput VALUES (NOW(), FALSE, FALSE, FALSE, TRUE, '08:00:00', '20:00:00', TRUE, CURDATE(), FALSE, FALSE)"
        mycursor.execute(sql)

        mydb.commit()

    
    print()
    
    transistor5V = LED(16)
    transistor3V3 = LED(26)
    transistorPH = LED(6)
    
    transistor5V.off()
    print("5 V circuit powered on")
    
    transistor3V3.off()
    print("3.3 V circuit powered on")
    
    transistorPH.off()
    print("PH sensor powered on")
    
    time.sleep(1)
    
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
        
        print("Cleaning...")
        
        mycursor.close()
        mydb.close()

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
            visibleLight = full_spectrum - infrared
            print ("Full Spectrum(IR + Visible) : {} lux".format(full_spectrum) )
            print ("Infrared Value : {} lux".format(infrared) )
            print ("Visible Value : {} lux".format(visibleLight) )
            
            
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
            
            
            # variables to dict
            # dictionary = {}
            
            
            # for variable in ["humidity", "temperature", "height"]:
              #   dictionary[variable] = eval(variable)
              
              
            # save data to mysql database table hydroponics
                        
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
            
            
            # print database
            mycursor.execute("SELECT * FROM userInput")

            myresult = mycursor.fetchall()

            for x in myresult:
                print(x)
            
            
            print()
            
            
            time.sleep(0)

        except (KeyboardInterrupt, SystemExit):
            cleanAndExit()


if __name__ == "__main__":
    main()
