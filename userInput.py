from datetime import datetime

class UserInput:
		
	time = datetime.now()
	systemState = False	
	pHmeasureState = False
	ledState = False
	autoLedState = True
	sunrise = datetime.now()
	sunset = datetime.now()
	autoHeightAdaptionState = True
	plantingDate = datetime.now()
	ledUp = False
	ledDown = False
	
	def __init__(self):
		pass
		
		# self.systemState = False		

            # query = """ CREATE TABLE userInput (
                # time DATETIME,
                # systemState BOOLEAN,
                # pHmeasureState BOOLEAN,
                # ledState BOOLEAN,
                # autoLedState BOOLEAN,
                # sunrise TIME,
                # sunset TIME,
                # autoHeightAdaptionState BOOLEAN,
                # plantingDate DATE, 
                # ledUp BOOLEAN,
                # ledDown BOOLEAN
            # ); """
