#! /usr/bin/python3

print("\n")
print("Libraries loading")

# Raspberry GPIO libraries
# import RPi.GPIO as GPIO
from gpiozero import LED

# MySQL library
import mysql.connector

# Load sensor classes
from dht22 import DHT22

# Load database class
from database import Database

# Load gpio class
# from gpio import GPIO

import time


# Begin of main program
def main():

	# Show welcome header
	print("--------------------------")
	print("DHT22 Sensor Reading Start")
	print()


	# Database routines

	# Initialize the database class
	print("*Database init.. ", end = '\n\n')
	database = Database()
	print("\nsuccessful")    
	
	
	# Initialize the GPIO class
	print("*GPIO init.. ", end = '\n\n')
	# gpio = GPIO()
	# transistor3V3 = LED(26)

	# Turn the circuits on for initialization
	# transistor3V3.off()
	# print("*3 V circuit turned on")

	# time.sleep(0.1)

	# DHT22: temperature and humidity
	print("*Temperature and humidity sensor init.. ", end = '')
	dht22 = DHT22()
	print("*successful")


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

				print("*Reading DHT22")
				[humidity, temperature] = dht22.getValues()
				print("********************************************************************************************")
				print("*success*")
				
				try:
					print ("*Humidity: {:.1f} %".format(humidity) )    # :.1f
					print ("*Temperature: {:.1f} °C".format(temperature) )
				
					# Update database
					database.updateDHT22(temperature, humidity)  

				except (TypeError):
					print("Skipping DHT22 sensor")
								
			# Catch an error message and display the message
			except (KeyboardInterrupt, SystemExit):
				cleanAndExit()
			
		# System is switched off
		else:  
			time.sleep(0.5)

# This is the main program
if __name__ == "__main__":
	main()

