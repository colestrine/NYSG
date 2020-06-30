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

	def get_healthy_levels_by_profile(profile):
		healthy_levels_by_profile_file = open('../../Interface Files/healthy_levels_by_profile.json', 'r')
		healthy_levels_by_profile_json = healthy_levels_by_profile_file.read()
		healthy_levels_by_profile_file.close()
		healthy_levels_by_profile_dict = json.loads(healthy_levels_by_profile_json)

		return healthy_levels_by_profile_dict[profile]

	def get_available_profiles():
		available_profiles_file = open('../../Interface Files/healthy_levels_by_profile.json', 'r')
		available_profiles_json = available_profiles_file.read()
		available_profiles_file.close()
		available_profiles_dict = json.loads(available_profiles_json)

		profiles = []
		for profile in available_profiles_dict:
			profiles.append((profile, profile))

		return profiles

	def get_available_temperatures():
		available_profiles_file = open('../../Interface Files/healthy_levels_by_profile.json', 'r')
		available_profiles_json = available_profiles_file.read()
		available_profiles_file.close()
		available_profiles_dict = json.loads(available_profiles_json)

		temperatures = []
		for profile in available_profiles_dict:
			temperatures.append((available_profiles_dict[profile]['temperature'], available_profiles_dict[profile]['temperature'].replace('_', '-')+'%'))

		return temperatures

	def get_available_humidities():
		available_profiles_file = open('../../Interface Files/healthy_levels_by_profile.json', 'r')
		available_profiles_json = available_profiles_file.read()
		available_profiles_file.close()
		available_profiles_dict = json.loads(available_profiles_json)

		humidities = []
		for profile in available_profiles_dict:
			humidities.append((available_profiles_dict[profile]['humidity'], available_profiles_dict[profile]['humidity'].replace('_', '-')+'%'))

		return humidities