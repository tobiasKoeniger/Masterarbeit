#! /usr/bin/python3

print("\n")
print("Libraries loading")

# Load expander class
from gpioExpander import GPIOExpander

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
    print("Plant Height Detection Start")
    print()
    
    
    # Database routines

    # Initialize the database class
    print("*Database init.. ", end = '\n\n')
    database = Database()
    print("\nsuccessful")    


    # GPIO expander    
    print("GPIO expander init.. ", end = '')
    gpioExpander = GPIOExpander() 
    print("successful")
    
    
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
        
            # Try to run the loop
            try:

                # Read EC level
                print("*Reading EC level")
                                
                ecLevel = ecsensor.getEC()
                print("-----------------------------------------------------------------------------------")
                print("*success*")
                
                # Update database
                database.updateEC(ecLevel)  

                
            # Catch an error message and display the message
            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()
                
            time.sleep(60)
            
        # System is switched off
        else:  
            time.sleep(0.5)

# This is the main program
if __name__ == "__main__":
    main()


