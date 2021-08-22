#! /usr/bin/python3

print("\n")
print("Libraries loading")

from ecSensor import EcSensor

# Raspberry GPIO libraries
# import RPi.GPIO as GPIO
from gpiozero import LED

# MySQL library
import mysql.connector

# Load database class
from database import Database

# Load gpio class
# from gpio import GPIO

import time



# Begin of main program
def main():
    
    # Show welcome header
    print("--------------------------")
    print("EC Level Sensor Reading Start")
    print()
    
    
    # Database routines

    # Initialize the database class
    print("*Database init.. ", end = '\n\n')
    database = Database()
    print("\nsuccessful")    
    
    
    # Write default number to database
    database.updateEC(100)  


    # Initialize the GPIO class
    print("*GPIO init.. ", end = '\n\n')    
    transistor5V = LED(16)
    transistor3V3 = LED(26)


    # Turn the circuits on for initialization
    transistor3V3.off()
    transistor5V.off()
    print("*3.3 V amd 5 V circuit turned on")

    time.sleep(0.1)


    # EC sensor
    print("EC sensor init.. ", end = '')
    ecsensor = EcSensor()
    print("successful")
    
    
    # Array of ten 
    ecLevelBuffer = [2] * 10
    
    readingNumber = 0 
            

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


    while True:
        
        userInput = database.getUserInput()  
        
        # Check, if system is switched on
        if (userInput.systemState == True):
        
            # Read EC level
            print("*Reading EC level")
            
            while(readingNumber < 10): # 10
            
                # Try to run the loop
                try:

                    ecLevel = ecsensor.getEC()                
                    
                    # Set first value of buffer                
                    ecLevelBuffer[0] = ecLevel                
                    
                    # Rotate buffer
                    ecLevelBuffer = ecLevelBuffer[-1:] + ecLevelBuffer[:-1]                                                                                                                                                         

                    readingNumber += 1
                    
                    print("ooooooooooooooooooooooooooooooooooooooooooooooooooooo")
                    
                # Catch an error message and display the message
                except (KeyboardInterrupt, SystemExit):
                    cleanAndExit()
                
                time.sleep(1)
                
                
            print(ecLevelBuffer)    
            
            # Calculate mean water level
            meanECLevel = sum(ecLevelBuffer) / len(ecLevelBuffer)
    
            print("Current EC level mean: {:.2f}".format(meanECLevel))
            
            
            # Update database
            database.updateEC(meanECLevel)  
            
            
            print("-----------------------------------------------------------------------------------")
            print("*success*")
            
            
            readingNumber = 0
            
                
            time.sleep(0)
            
        # System is switched off
        else:  
            time.sleep(0.5)

# This is the main program
if __name__ == "__main__":
    main()

