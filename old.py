

            
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
        
