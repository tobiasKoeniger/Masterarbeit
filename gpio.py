
from gpiozero import LED
from gpiozero import PWMLED


class GPIO:
	
	# According to BCM numbering
	
	transistor5V = LED(16)
	transistor3V3 = LED(26)
	transistorPH = LED(6)
	
	pumpFloraGro = PWMLED(24)
	pumpFloraBloom = PWMLED(25)
	pumpFloraMicro = PWMLED(23)
	pumpFloraClean = PWMLED(17)
	
	pumpPHdowner = PWMLED(27)
	pumpWater = PWMLED(18)
	pumpCirculation = PWMLED(8)
	
	ledUp = PWMLED(7)
	ledDown = PWMLED(5)
	
	leds13 = PWMLED(12)
	leds15 = PWMLED(13)


	def __init__(self):

		# Turn the power circuits with the transistors off
		
		# Power 5 V off
		self.transistor5V.on()
		print("5 V circuit powered off")

		# Power 3.3 V off 
		self.transistor3V3.on()
		print("3.3 V circuit powered off")

		# Power the pH sensor off 
		self.transistorPH.on()
		print("PH sensor powered off")
		
		
		# Turn the nutrient pumps off
		
		# Turn the FloraMicro pump off 
		self.pumpFloraMicro.off()
		print("Pump for FloraMicro turned off")
		
		# Turn the FloraGro pump off 
		self.pumpFloraGro.off()
		print("Pump for FloraGro turned off")
		
		# Turn the FloraGro pump off 
		self.pumpFloraBloom.off()
		print("Pump for FloraBloom turned off")
		
		# Turn the FloraClean pump off 
		self.pumpFloraClean.off()
		print("Pump for FloraClean turned off")
		
		
		# Turn additional pumps off
		
		# Turn the PH downer pump off 
		self.pumpPHdowner.off()
		print("Pump for FloraClean turned off")
		
		# Turn the Water pump off 
		self.pumpWater.off()
		print("Pump for FloraClean turned off")
		
		# Turn the circulation pump off 
		self.pumpCirculation.off()
		print("Pump for FloraClean turned off")
		
		
		# Turn the actuator off
		
		# Turn the actuator up off
		self.ledUp.off()
		print("Actuator for LEDs up turned off")
		
		# Turn the actuator down
		self.ledDown.off()
		print("Actuator for LEDs down turned off")
		
		
		# Turn the lighting off
		
		# Turn the 1:3 LEDs off
		self.leds13.off()
		print("1:3 LEDs turned off")
		
		# Turn the 1:5 LEDs off
		self.leds15.off()
		print("1:5 LEDs turned off")

