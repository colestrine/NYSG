import json

with open('../initial_plant_scrape.json', 'r') as file:
	data_str = file.read()

data = json.loads(data_str)

profiles = {}
for profile in data:
	profiles[profile] = {}
	profiles[profile]['temperature'] = data[profile]['Germ_Temp']
	profiles[profile]['germ_time'] = data[profile]['Germ_Time']
	profiles[profile]['sunlight'] = '10' if (data[profile]['Sun'] == 'full sun') else ''

data_out = json.dumps(profiles)

with open('plant_profile_data_temp.json', 'w') as file:
	file.write(data_out)