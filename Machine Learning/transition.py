import json
import numpy

# ActionSet contains attributes and methods related to actions
class ActionSet:
	# ActionSet contains 3 attributes - water_action, ventilation_action, and heat_action, representing the three dimensions of actions that the system can take
	def __init__(self, water_action, ventilation_action, heat_action):
		self.water_action = water_action
		self.ventilation_action = ventilation_action
		self.heat_action = heat_action

	def __str__(self):
		return (self.water_action + ',' + self.ventilation_action + ',' + self.heat_action)

	# Used to decode from the string representation of an action set to the dictionary representation
	def decode(string):
		action_set = string.split(',')
		water_action = action_set[0]
		ventilation_action = action_set[1]
		heat_action = action_set[2]

		return {'water_action': water_action, 'ventilation_action': ventilation_action, 'heat_action': heat_action}

# EffectSet contains attributes and methods related to effects
class EffectSet():
	# EffectSet contains 3 attributes - temperature, humidity, and soil_moisture representing the three dimensions of measurements that the system can take
	def __init__(self, temperature, humidity, soil_moisture):
		self.temperature = temperature
		self.humidity = humidity
		self.soil_moisture = soil_moisture

	def __str__(self):
		return (str(self.temperature) + ',' + str(self.humidity) + ',' + str(self.soil_moisture))

	def __add__(self, other):
		return [float(self.temperature) + float(other.temperature), float(self.humidity) + float(other.humidity), float(self.soil_moisture) + float(other.soil_moisture)]

	# Used to decode from the string representation of an effect set to the dictionary representation
	def decode(string):
		effect_set = string.split(',')
		temperature = effect_set[0]
		humidity = effect_set[1]
		soil_moisture = effect_set[2]

		return {'temperature': float(temperature), 'humidity': float(humidity), 'soil_moisture': float(soil_moisture)}

	# Returns dictionary of current effects from transition.json based on action set and current value buckets
	def getEffect(action_set, temperature_bucket, humidity_bucket, soil_moisture_bucket):
		with open('Machine Learning/Files/transition.json', 'r') as transition_file:
			contents = transition_file.read()
			P = json.loads(contents)

			temperature_effect = P[str(action_set)]['temperature'][temperature_bucket]['effect']
			humidity_effect = P[str(action_set)]['humidity'][humidity_bucket]['effect']
			soil_moisture_effect = P[str(action_set)]['soil_moisture'][soil_moisture_bucket]['effect']

		return {'temperature': float(temperature_effect), 'humidity': float(humidity_effect), 'soil_moisture': float(soil_moisture_effect)}

	# Returns dictionary of bootstrap effects from transition_bootstrap.json based on action set and current value buckets
	def getBootstrapEffects():
		with open('Machine Learning/Files/transition_bootstrap.json', 'r') as transition_file:
			contents = transition_file.read()
			P = json.loads(contents)

		return P

	# Returns entire contents of transition.json as a dictionary
	def getEffects():
		with open('Machine Learning/Files/transition.json', 'r') as transition_file:
			contents = transition_file.read()
			P = json.loads(contents)

		return P

	# Computes 50/50 average of two effect sets on a dimension-by-dimension basis
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

	# Computes new observed effect based on last_state and current_state, and maps effect to action set-observation dimension-value bucket data
	# Specifying the fourth argument (data_collection_mode) as True will turn on data collection mode - this will write data to each of the 5 value buckets for each action set-observation dimension pairs, speeding up the data collection process 
	def putEffect(action_set, last_state, current_state, data_collection_mode=False):
		with open('Machine Learning/Files/transition.json', 'r') as transition_file:
			contents = transition_file.read()
			P = json.loads(contents)

		temperature_diff = current_state.temperature - last_state.temperature
		humidity_diff = current_state.humidity - last_state.humidity
		soil_moisture_diff = current_state.soil_moisture - last_state.soil_moisture

		effect_set = EffectSet(temperature_diff, humidity_diff, soil_moisture_diff)

		temperature_bucket = str(last_state.temperature).split('.')[0]
		humidity_bucket = str(last_state.humidity).split('.')[0]
		soil_moisture_bucket = str(last_state.soil_moisture).split('.')[0]

		old_effects = EffectSet.getEffect(action_set, temperature_bucket, humidity_bucket, soil_moisture_bucket)
		old_effects = EffectSet(old_effects['temperature'], old_effects['humidity'], old_effects['soil_moisture'])

		new_effects = EffectSet.avg(effect_set, old_effects)

		P[str(action_set)]['hits'] += 1

		if (data_collection_mode):
			for bucket in range(1, 6):
				P[str(action_set)]['temperature'][str(bucket)]['effect'] = new_effects[0]
				P[str(action_set)]['temperature'][str(bucket)]['hits'] += 1

				P[str(action_set)]['humidity'][str(bucket)]['effect'] = new_effects[1]
				P[str(action_set)]['humidity'][str(bucket)]['hits'] += 1

				P[str(action_set)]['soil_moisture'][str(bucket)]['effect'] = new_effects[2]
				P[str(action_set)]['soil_moisture'][str(bucket)]['hits'] += 1
		else:
			P[str(action_set)]['temperature'][temperature_bucket]['effect'] = new_effects[0]
			P[str(action_set)]['temperature'][temperature_bucket]['hits'] += 1

			P[str(action_set)]['humidity'][humidity_bucket]['effect'] = new_effects[1]
			P[str(action_set)]['humidity'][humidity_bucket]['hits'] += 1

			P[str(action_set)]['soil_moisture'][soil_moisture_bucket]['effect'] = new_effects[2]
			P[str(action_set)]['soil_moisture'][soil_moisture_bucket]['hits'] += 1

		with open('Machine Learning/Files/transition.json', 'w') as transition_file:
			json.dump(P, transition_file)

		return P[str(action_set)]

# Resets transition.json to blank/all zeros
def initializeToZeros(action_choices):
	P = {}

	temperature_buckets = ['1', '2', '3', '4', '5']
	humidity_buckets = ['1', '2', '3', '4', '5']
	soil_moisture_buckets = ['1', '2', '3', '4', '5']

	for water_action in action_choices:
		for ventilation_action in action_choices:
			for heat_action in action_choices:
				action_set = ActionSet(water_action, ventilation_action, heat_action)
				effect_set = EffectSet(0, 0, 0)

				P[str(action_set)] = {'hits': 0, 'temperature': {}, 'humidity': {}, 'soil_moisture': {}}

				for bucket in temperature_buckets:
					P[str(action_set)]['temperature'][bucket] = {}
					P[str(action_set)]['temperature'][bucket]['effect'] = 0
					P[str(action_set)]['temperature'][bucket]['hits'] = 0

				for bucket in humidity_buckets:
					P[str(action_set)]['humidity'][bucket] = {}
					P[str(action_set)]['humidity'][bucket]['effect'] = 0
					P[str(action_set)]['humidity'][bucket]['hits'] = 0

				for bucket in soil_moisture_buckets:
					P[str(action_set)]['soil_moisture'][bucket] = {}
					P[str(action_set)]['soil_moisture'][bucket]['effect'] = 0
					P[str(action_set)]['soil_moisture'][bucket]['hits'] = 0

	with open('Machine Learning/Files/transition.json', 'w') as transition_file:
		json.dump(P, transition_file)

	return P

if __name__ == '__main__':
	action_choices = ['big_decrease', 'small_decrease', 'none', 'small_increase', 'big_increase']
	#action_choices = ['off', 'low', 'medium', 'high']

	y_n = input("WARNING: Transition file will be zeroed-out. Enter (y) to continue, any other key to exit.\n")

	if (y_n == 'y'):
		initializeToZeros(action_choices)
		input("Transition file successfully zeroed! Press any key to continue.")
