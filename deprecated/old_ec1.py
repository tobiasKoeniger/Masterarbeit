        # timeBetweenECMeasurements = 7 # 30                    
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
            # meanECLevel = sum(ecLevelBuffer[1:ecLevelRepetitions]) / (len(ecLevelBuffer) - 1)
            # # meanECLevel = sum(ecLevelBuffer) / len(ecLevelBuffer)
            
            # database.updateEC(meanECLevel)                                                                            
                                    
            # ecReadingNumber = 0                
            
            # last_ecLevel_detection = datetime.now()   
            
            # print("===================================================================================") 
    
            # print("Current EC level mean: {:.3f}".format(meanECLevel))    
            
            # ec_start_up = False                                            
    
    
    
    
    
    
    # if (ecLevel != 1):                    
        # print("Mean EC level: {}".format(ecLevel))
        
    # ecLevel = 1.2
    
    # if (ecLevelBuffer[-1] != ecLevel):
        
        # # Set first value of buffer                
        # ecLevelBuffer[0] = ecLevel
        # ecLevelUpdates += 1
        
        # # Rotate buffer
        # ecLevelBuffer = ecLevelBuffer[-1:] + ecLevelBuffer[:-1]
        
        # print(ecLevelBuffer)
        
    # # Calculate mean EC level
    # meanECLevel = sum(ecLevelBuffer) / len(ecLevelBuffer)   
    
    # print("Mean EC level: {:.0f}".format(meanECLevel))        
