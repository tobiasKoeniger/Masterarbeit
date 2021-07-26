# MySQL library
import mysql.connector

# Load userInput class
from userInput import UserInput


class Database: 

	
	def __init__(self):
		
		# userInput class to store user input data 
		self.userInput = UserInput()
		
		
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
		self.host = credentials[2].rstrip()    
		self.user = credentials[5].rstrip()
		self.password = credentials[8].rstrip()
		
		print(self.host + ", " + self.user + ", " + self.password)
		
		
		# Connect to the MySQL database
		try:
			self.mydb = mysql.connector.connect(
			
				host=self.host,
				user=self.user,
				password=self.password
			)
			print("MySQL Database connection successful")
			
		# Show error message
		except Error as err:
			print(f"The error '{e}' occurred")


		self.mycursor = self.mydb.cursor()
    
		# Fetch all database names
		self.mycursor.execute("SHOW DATABASES")
		databaseNames = self.mycursor.fetchall()
		
		# Check if database 'hydroponics' is available
		if not 'hydroponics' in str(databaseNames):
					
			# If not, create new database
			self.mycursor.execute("CREATE DATABASE hydroponics")
			print("Database hydroponics created")            

		# Close connection
		self.mycursor.close()
		self.mydb.close()
		
		
		# Now, try to directly connect to the 'hydroponics' database
		try:
			self.mydb = mysql.connector.connect(
			
				host="localhost",
				user=self.user,
				password=self.password,
				database="hydroponics"
			)
			print("Connection to MySQL Database hydroponics successful")
			
		# Show error
		except Error as err:
			print(f"The error '{e}' occurred")
			
		self.mycursor = self.mydb.cursor()
		
		# Fetch all table names
		self.mycursor.execute("SHOW TABLES")
		tableNames = self.mycursor.fetchall()
		
		
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
			
			self.mycursor.execute(query)
			print("Table sensors created")
			
			# Insert one data row with zeroes
			sql = "INSERT INTO sensors VALUES (NOW(), 0, 0, 0, 0, 0, 0, 0)"
			self.mycursor.execute(sql)

			self.mydb.commit()
			
		
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

			
			self.mycursor.execute(query)
			print("Table userInput created")    
			
			# Insert one data row with default values
			sql = "INSERT INTO userInput VALUES (NOW(), FALSE, FALSE, FALSE, TRUE, '08:00:00', '20:00:00', TRUE, CURDATE(), FALSE, FALSE)"
			self.mycursor.execute(sql)

			self.mydb.commit()
			
		self.closeConnection()
		
			
	def connectToDatabase(self):
		
		# Now, try to directly connect to the 'hydroponics' database
		try:
			self.mydb = mysql.connector.connect(
			
				host="localhost",
				user=self.user,
				password=self.password,
				database="hydroponics"
			)
			# print("Connection to MySQL Database hydroponics successful")
			
		# Show error
		except Error as err:
			print(f"The error '{e}' occurred")
			
		self.mycursor = self.mydb.cursor()
			
			
	def updateSensors(self, visibleLight, waterTemperature, distance1):
		
		self.connectToDatabase()
		
		# Update the sensor data in the database table 'sensors'
					
		sql = """UPDATE sensors SET 
					time = NOW(), 
					lightIntensity = %s, 
					waterTemperature = %s,					
					waterLevel = %s"""

		data = (visibleLight, waterTemperature, distance1)            

		self.mycursor.execute(sql, data)

		self.mydb.commit()   
		
		self.closeConnection()
		
		
	def updateEC(self, ec):
		
		self.connectToDatabase()
		
		# Update the sensor data in the database table 'sensors'
					
		sql = """UPDATE sensors SET 
					time = NOW(), 
					ecLevel = """ + str(ec)		

		self.mycursor.execute(sql)

		self.mydb.commit()   
		
		self.closeConnection()	
		
	
	def updateDHT22(self, temperature, humidity):
		
		self.connectToDatabase()
		
		# Update the sensor data in the database table 'sensors'
					
		sql = """UPDATE sensors SET 
					time = NOW(), 
					temperature = %s, 
					humidity = %s"""

		data = (temperature, humidity)            

		self.mycursor.execute(sql, data)

		self.mydb.commit()   
		
		self.closeConnection()		
			
			
	def updatePH(self, pH):
		
		self.connectToDatabase()
		
		# Update the sensor data in the database table 'sensors'
					
		sql = """UPDATE sensors SET 
					time = NOW(), 
					phLevel = """ + str(pH)		

		self.mycursor.execute(sql)

		self.mydb.commit()   
		
		self.closeConnection()		
		
		
	def getUserInput(self):
		
		self.connectToDatabase()
		
		# Get the database table 'userInput'
		self.mycursor.execute("SELECT * FROM userInput")

		# Fetch all entries from the table
		result = self.mycursor.fetchall()

		# Print the table
		for x in result:
			print(x)

		# Copy the userInput data into the userInput class
		self.userInput.time = x[0]
		self.userInput.systemState = x[1]
		self.userInput.pHmeasureState = x[2]
		self.userInput.ledState = x[3]
		self.userInput.autoLedState = x[4]
		self.userInput.sunrise = x[5]
		self.userInput.sunset = x[6]
		self.userInput.autoHeightAdaptionState = x[7]
		self.userInput.plantingDate = x[8]
		self.userInput.ledUp = x[9]
		self.userInput.ledDown = x[10]
		
		self.closeConnection()
		
		return self.userInput		
		
	
	def closeConnection(self):
		
		# Close all database connections
		self.mycursor.close()
		self.mydb.close()
		
		
