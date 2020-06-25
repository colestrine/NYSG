import json

class data_handler:
	def write_healthy_levels(temperature, humidity, soil_moisture, sunlight):
		levels_dict = {'temperature': temperature, 'humidity': humidity, 'soil_moisture': soil_moisture, 'sunlight': sunlight}
		levels_json = json.dumps(levels_dict)

		healthy_levels_file = open('../../Interface Files/healthy_levels.json', 'w')
		healthy_levels_file.write(levels_json)
		healthy_levels_file.close()

	def read_healthy_levels():
		healthy_levels_file = open('../../Interface Files/healthy_levels.json', 'r')
		levels_json = healthy_levels_file.read()
		healthy_levels_file.close()
		levels_dict = json.loads(levels_json)

		return levels_dict

	def write_plant_profile(plant_profile):
		profile_dict = {'plant_profile': plant_profile}
		profile_json = json.dumps(profile_dict)

		plant_profile_file = open('../../Interface Files/plant_profile.json', 'w')
		plant_profile_file.write(profile_json)
		plant_profile_file.close()

	def read_plant_profile():
		plant_profile_file = open('../../Interface Files/plant_profile.json', 'r')
		profile_json = plant_profile_file.read()
		plant_profile_file.close()
		profile_dict = json.loads(profile_json)

		return profile_dict