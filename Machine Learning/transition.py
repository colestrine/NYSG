import json
import numpy


class ActionSet:
	def __init__(self, light_action, water_action, ventilation_action, heat_action):
		self.light_action = light_action
		self.water_action = water_action
		self.ventilation_action = ventilation_action
		self.heat_action = heat_action

	def __str__(self):
		return (self.light_action + ',' + self.water_action + ',' + self.ventilation_action + ',' + self.heat_action)

	def decode(string):
		action_set = string.split(',')
		light_action = action_set[0]
		water_action = action_set[1]
		ventilation_action = action_set[2]
		heat_action = action_set[3]

		return {'light_action': light_action, 'water_action': water_action, 'ventilation_action': ventilation_action, 'heat_action': heat_action}

class EffectSet():
	def __init__(self, temperature, humidity, soil_moisture, sunlight):
		self.temperature = temperature
		self.humidity = humidity
		self.soil_moisture = soil_moisture
		self.sunlight = sunlight

	def __str__(self):
		return (str(self.temperature) + ',' + str(self.humidity) + ',' + str(self.soil_moisture) + ',' + str(self.sunlight))

	def __add__(self, other):
		return [float(self.temperature) + float(other.temperature), float(self.humidity) + float(other.humidity), float(self.soil_moisture) + float(other.soil_moisture), float(self.sunlight) + float(other.sunlight)]

	def decode(string):
		effect_set = string.split(',')
		temperature = effect_set[0]
		humidity = effect_set[1]
		soil_moisture = effect_set[2]
		sunlight = effect_set[3]

		return {'temperature': float(temperature), 'humidity': float(humidity), 'soil_moisture': float(soil_moisture), 'sunlight': float(sunlight)}

	def getEffect(action_set):
		with open('Files/transition.json', 'r') as transition_file:
			contents = transition_file.read()
			P = json.loads(contents)

			effects = P[str(action_set)]

		return EffectSet.decode(effects)

	def getEffects():
		with open('Files/transition.json', 'r') as transition_file:
			contents = transition_file.read()
			P = json.loads(contents)

		return P

	def avg(self, other):
		if other.temperature:
			temperature = float(other.temperature)
		else:
			temperature = float(self.temperature)

		if other.humidity:
			humidity = float(other.humidity)
		else:
			humidity = float(self.humidity)

		if other.soil_moisture:
			soil_moisture = float(other.soil_moisture)
		else:
			soil_moisture = float(self.soil_moisture)

		if other.sunlight:
			sunlight = float(other.sunlight)
		else:
			sunlight = float(self.sunlight)

		return [.8*float(self.temperature) + .2*temperature, .8*float(self.humidity) + .2*humidity, .8*float(self.soil_moisture) + .2*soil_moisture, .8*float(self.sunlight) + .2*sunlight]

	def putEffect(action_set, effect_set):
		with open('Files/transition.json', 'r') as transition_file:
			contents = transition_file.read()
			P = json.loads(contents)

		old_effects = EffectSet.getEffect(action_set)
		old_effects = EffectSet(old_effects['temperature'], old_effects['humidity'], old_effects['soil_moisture'], old_effects['sunlight'])

		new_effects = EffectSet.avg(effect_set, old_effects)

		P[str(action_set)] = str(new_effects[0]) + ',' + str(new_effects[1]) + ',' + str(new_effects[2]) + ',' + str(new_effects[3])

		with open('Files/transition.json', 'w') as transition_file:
			json.dump(P, transition_file)

		return P[str(action_set)]

def initializeToZeros(action_choices):
	P = {}

	for light_action in action_choices:
		for water_action in action_choices:
			for ventilation_action in action_choices:
				for heat_action in action_choices:
					action_set = ActionSet(light_action, water_action, ventilation_action, heat_action)
					effect_set = EffectSet(0, 0, 0, 0)

					P[str(action_set)] = str(effect_set)

	with open('Files/transition.json', 'w') as transition_file:
		json.dump(P, transition_file)

	return P


if __name__ == '__main__':
	action_choices = ['big_decrease', 'small_decrease', 'none', 'small_increase', 'big_increase']

	y_n = input("WARNING: Transition file will be zeroed-out. Enter (y) to continue, any other key to exit.\n")

	if (y_n == 'y'):
		initializeToZeros(action_choices)
		input("Transition file successfully zeroed! Press any key to continue.")