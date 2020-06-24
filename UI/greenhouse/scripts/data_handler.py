class data_handler:
	def write_healthy_levels(temperature, humidity, soil_moisture, sunlight):
		healthy_levels_file = open('healthy_levels.txt', 'w')
		healthy_levels_file.write("test")
		healthy_levels_file.close()