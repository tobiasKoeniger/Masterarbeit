		
		waterTemperature = self.waterTemperatureSensor.getTemperature()
		print ("Water temperature: {:.1f} °C".format(waterTemperature) )
		
		
		self.transistorEC.on()
		
		time.sleep(0.03)

		chan = AnalogIn(self.ads, ADS.P1)
		
		u = chan.voltage
		
		time.sleep(0.03)
		
		transistorEC.off()
		
		
		transistorAntiEC.on()
		
		time.sleep(0.06)
		
		transistorAntiEC.off()

		
		print("voltage: {:.2f} V".format(u))
		
		u_power = 3.265
		resistance_R1 = 470

		# resistance in ohm
		r = (u * resistance_R1) / (u_power - u)
		kohm = r/1000
		print("resistance: {:.1f} kOhm".format(kohm))

		#print("resistance: {} Ohm".format(r))
		# mS/cm
		# cell_constant = 25/18
		cell_constant = 1.356
		ec_raw = (cell_constant) * (1/r) * 1000

		print("ec raw: {:.2f} mS/cm".format(ec_raw))


		# temperature compensation
		T = waterTemperature
		ec25 = ec_raw / (1 + 0.019*(T-25))
		print("ec 25: {:.2f} mS/cm".format(ec25))
		
		
		# linear correction
		ec = 0.642 + ( (1.59 - 0.642) / (1.36 - 0.93) ) * (ec25 - 0.93)
		print("ec: {:.2f} mS/cm".format(ec))
		
		
		
		
		
		
