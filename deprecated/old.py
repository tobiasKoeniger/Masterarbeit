

            
			# variables to dict
			# dictionary = {}
			
			
			# for variable in ["humidity", "temperature", "height"]:
			#   dictionary[variable] = eval(variable)



# sys.path.append('hx711')

# from weightSensor import WeightSensor
    
    
    # weightsensor1 = WeightSensor()
    # print("Weight sensor init successful")
    
            
            
            # weight = weightsensor1.getLoad()
            
            # adjusted_weight = weightsensor1.temperatureCompensation(weight, temperature)

            # print ("Weight: {} g".format(weight))
            # print ("Temperature adjusted weight: {:.0f} g".format(adjusted_weight))
    
            

        # Insert one row
        # sql = "INSERT INTO userInput VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # data = ("NOW()", "FALSE", "FALSE", "FALSE", "TRUE", "08:00:00", "20:00:00", "TRUE", "CURDATE()", "FALSE", "FALSE")
        # mycursor.execute(sql, data)            



    
    # if 'sensors' in str(tableNames):

        # mycursor.execute("DROP TABLE sensors")
        
        # mycursor.execute("SHOW TABLES")
        # tableNames = mycursor.fetchall()
        
        
    # if 'userInput' in str(tableNames):

        # mycursor.execute("DROP TABLE userInput")
        
        # mycursor.execute("SHOW TABLES")
        # tableNames = mycursor.fetchall()
        
        
        
        
        
            # Now, start the program:
    
    # Initialize the GPIO functions
    
    # Initialize the power control transistors
    # transistor5V = LED(16)
    # transistor3V3 = LED(26)
    # transistorPH = LED(6)
    
    # Initialize the pumps
    
    
    # Set the GPIOs
    
    # # Power 5 V on
    # transistor5V.off()
    # print("5 V circuit powered on")
    
    # # Power 3.3 V on 
    # transistor3V3.off()
    # print("3.3 V circuit powered on")
    
    # # Power the pH sensor on 
    # transistorPH.off()
    # print("PH sensor powered on")
        
        
        
        
        
        
        
        
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
        
        
        
        
        # Get the database table 'userInput'
        mycursor.execute("SELECT * FROM userInput")

        # Fetch all entries from the table
        myresult = mycursor.fetchall()

        # Print the table
        for x in myresult:
            print(x)
        
        # Copy the userInput data into the userInput class
        userInput.time = x[0]
        userInput.systemState = x[1]
        userInput.pHmeasureState = x[2]
        userInput.ledState = x[3]
        userInput.autoLedState = x[4]
        userInput.sunrise = x[5]
        userInput.sunset = x[6]
        userInput.autoHeightAdaptionState = x[7]
        userInput.plantingDate = x[8]
        userInput.ledUp = x[9]
        userInput.ledDown = x[10]          
        
        
        
        # current_time = now.strftime("%H:%M:%S")
        # print(now.hour)
        # print(now.minute)
        
        # print(userInput.sunrise.hour)
        # print(userInput.sunrise.minute)
        
        # print(now - userInput.sunrise)
        
        # if()
        
        
        
        
        
        
# temperature = 0
# humidity = 0

# Thread

# def dht22reading(dht22):
    
    # while(True):
        
        # # Read the humidity and temperature values from the DHT22
        # global temperature
        # global humidity
        
        # print("Reading sensors")
        # [humidity, temperature] = dht22.getValues()
        # print ("Humidity: {:.1f} %".format(humidity) )
        # print ("Temperature: {:.1f} °C".format(temperature) )
        
        
        
        
            # # DHT22: temperature and humidity
    # print("Temperature and humidity sensor init.. ", end = '')
    # dht22 = DHT22()
    # print("successful")
    
    
    
    
    
    # # Detect plant height
                    # gpioExpander.setSensor(7)
                    # time.sleep(0.1)
                    
                    # # Reinitialize sensor
                    # distance_sensor = DistanceSensor()
                    
                    # distance1 = distance_sensor.getDistance()
                    # print ("Distance plant height sensor 1: {0} mm".format(distance1) ) 
                    
                    
                    # gpioExpander.setSensor(8)
                    # time.sleep(0.1)
                    
                    # # Reinitialize sensor
                    # distance_sensor = DistanceSensor()
                    
                    # distance2 = distance_sensor.getDistance()
                    # print ("Distance plant height sensor 2: {0} mm".format(distance2) ) 
                    
                    
                    # gpioExpander.setSensor(9)
                    # time.sleep(0.1)
                    
                    # # Reinitialize sensor
                    # distance_sensor = DistanceSensor()
                    
                    # distance3 = distance_sensor.getDistance()
                    # print ("Distance plant height sensor 3: {0} mm".format(distance3) ) 
                    
                    
                    
                    
                                        
                    # # Detect plant height
                    # gpioExpander.setSensor(7)
                    # time.sleep(0.1)
                    
                    # # Reinitialize sensor
                    # distance_sensor = DistanceSensor()
                    
                    # distance1 = distance_sensor.getDistance()
                    # print ("Distance plant height sensor 1: {0} mm".format(distance1) ) 
                    
                    
                    # gpioExpander.setSensor(8)
                    # time.sleep(0.1)
                    
                    # # Reinitialize sensor
                    # distance_sensor = DistanceSensor()
                    
                    # distance2 = distance_sensor.getDistance()
                    # print ("Distance plant height sensor 2: {0} mm".format(distance2) ) 
                    
                    
                    # gpioExpander.setSensor(9)
                    # time.sleep(0.1)
                    
                    # # Reinitialize sensor
                    # distance_sensor = DistanceSensor()
                    
                    # distance3 = distance_sensor.getDistance()
                    # print ("Distance plant height sensor 3: {0} mm".format(distance3) ) 
                    
                    
                    
                    
                    
                    
                # time.sleep(100)
                
                # # Set main tank level sensor
                # gpioExpander.setSensor(0)
                
                # # time.sleep(0.1)
                
                # # Reinitialize sensor
                # mainTankLevelSensor = DistanceSensor()
                # print("Main tank sensor reinitialized")                                            
            
            
                # Read sensors
                                
                # Read the humidity and temperature values from the DHT22
                
                # threading.Thread(target=dht22reading(dht22)).start()
                
                
                
                
                                
                
                # # Read the main water level sensor
                # try:
                    # distance = mainTankLevelSensor.getDistance()
                    # waterLevelMainTank = 247 - distance
                    
                    # print ("Distance of main tank level sensor: {0} mm".format(distance) )                                                         
                    # print ("Water level main tank: {0} mm".format(waterLevelMainTank) )   
                    
                    # time.sleep(0.5)
                    
                    # skipLevelSensor = False
                    
                # # Catch an error message and display the message
                # except (KeyboardInterrupt, SystemExit, OSError):
                    # print("Skipping main tank level sensor")
                    # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                    # skipLevelSensor = True
                                    
                # time.sleep(100)
                
                
                
                
                # Extract 
                # sunrise_hour = int(userInput.sunrise.seconds / (60*60))
                # sunset_hour = int(userInput.sunset.seconds / (60*60))
                
                
                
                # time_delta_ecLevel = current_time - last_ecLevel_detection
                # ecLevelDetectionRunning = (time_delta_ecLevel.seconds > 60*60) or (ec_start_up == True)
                
                # if( (dth_start_up == True) or ( (not ecLevelDetectionRunning) and (time_delta_dht22.seconds > 10 ) ) ):
                
                
                
                
                
                                        # try:
                            # distance_sensor
                        # except NameError:
                            # pass
                        # else: 
                            # del distance_sensor
                            # print("deleted")
                        # time.sleep(100)
                        # Reinitialize sensor





# waterLevelMainTankUpdates = 0
                    
                    # sensorRepetitions = 0
                    
                    # while(sensorRepetitions < 25):
                    
                        # # Read the main water level sensor
                        # try:
                            # distance = mainTankLevelSensor.getDistance()
                            # waterLevelMainTank = 247 - distance
                            
                            # # print ("Distance of main tank level sensor: {0} mm".format(distance) )                                                         
                            # print ("Water level main tank: {0} mm".format(waterLevelMainTank) )   
                            
                            # # time.sleep(0.5)
                            
                            # skipLevelSensor = False
                                                                                    
                            
                        # # Catch an error message and display the message
                        # except (KeyboardInterrupt, SystemExit, OSError):
                            # print("Skipping main tank level sensor")
                            # print("X"*85)
                            # skipLevelSensor = True
                                                        
                            
                        # if (skipLevelSensor == False):
                        
                            # # Set first value of buffer                
                            # waterLevelMainTankBuffer[0] = waterLevelMainTank
                            # waterLevelMainTankUpdates += 1
                            
                            # # Rotate buffer
                            # waterLevelMainTankBuffer = waterLevelMainTankBuffer[-1:] + waterLevelMainTankBuffer[:-1]     
                            
                            # sensorRepetitions += 1    
                        
                        
                    # print(waterLevelMainTankBuffer)
                    
                    # # Calculate mean water level
                    # meanWaterLevelMainTank = sum(waterLevelMainTankBuffer) / len(waterLevelMainTankBuffer)
            
                    # print("Current water tank level mean: {:.0f}".format(meanWaterLevelMainTank))
