import json

# water_actions = ['big_decrease', 'small_decrease', 'none', 'small_increase', 'big_increase']
# fan_actions = ['big_decrease', 'small_decrease', 'none', 'small_increase', 'big_increase']
# heat_actions = ['big_decrease', 'small_decrease', 'none', 'small_increase', 'big_increase']

water_actions = ['off', 'low', 'medium', 'high']
fan_actions = ['off', 'low', 'medium', 'high']
heat_actions = ['off', 'low', 'medium', 'high']

actions = {}
index = '1'

for water_action in water_actions:
	for fan_action in fan_actions:
		for heat_action in heat_actions:
			actions[index] = {'water': water_action, 'fan': fan_action, 'heat': heat_action}

			index = str(int(index) + 1)

with open('Files/actions.json', 'w') as file:
	json = json.dumps(actions)
	file.write(json)