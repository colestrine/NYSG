import json
import numpy


class ActionSet:
	def __init__(self, water_action, ventilation_action, heat_action):
		self.water_action = water_action
		self.ventilation_action = ventilation_action
		self.heat_action = heat_action

	def __str__(self):
		return (self.water_action + ',' + self.ventilation_action + ',' + self.heat_action)

	def decode(string):
		action_set = string.split(',')
		water_action = action_set[0]
		ventilation_action = action_set[1]
		heat_action = action_set[2]

		return {'water_action': water_action, 'ventilation_action': ventilation_action, 'heat_action': heat_action}

class EffectSet():
	def __init__(self, temperature, humidity, soil_moisture):
		self.temperature = temperature
		self.humidity = humidity
		self.soil_moisture = soil_moisture

	def __str__(self):
		return (str(self.temperature) + ',' + str(self.humidity) + ',' + str(self.soil_moisture))

	def __add__(self, other):
		return [float(self.temperature) + float(other.temperature), float(self.humidity) + float(other.humidity), float(self.soil_moisture) + float(other.soil_moisture)]

	def decode(string):
		effect_set = string.split(',')
		temperature = effect_set[0]
		humidity = effect_set[1]
		soil_moisture = effect_set[2]

		return {'temperature': float(temperature), 'humidity': float(humidity), 'soil_moisture': float(soil_moisture)}

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

		return [.5*float(self.temperature) + .5*temperature, .5*float(self.humidity) + .5*humidity, .5*float(self.soil_moisture) + .5*soil_moisture]

	def putEffect(action_set, effect_set):
		with open('Files/transition.json', 'r') as transition_file:
			contents = transition_file.read()
			P = json.loads(contents)

		old_effects = EffectSet.getEffect(action_set)
		old_effects = EffectSet(old_effects['temperature'], old_effects['humidity'], old_effects['soil_moisture'])

		new_effects = EffectSet.avg(effect_set, old_effects)

		P[str(action_set)] = str(new_effects[0]) + ',' + str(new_effects[1]) + ',' + str(new_effects[2])

		with open('Files/transition.json', 'w') as transition_file:
			json.dump(P, transition_file)

		return P[str(action_set)]

def initializeToZeros(action_choices):
	P = {}

	for water_action in action_choices:
		for ventilation_action in action_choices:
			for heat_action in action_choices:
				action_set = ActionSet(water_action, ventilation_action, heat_action)
				effect_set = EffectSet(0, 0, 0)

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