from numpy import random, mean
from matplotlib import pyplot

class State:
	# State class holds data for temperature, humidity, soil moisture, and sunlight
	def __init__(self, temperature, humidity, soil_moisture, sunlight):
		self.temperature = temperature
		self.humidity = humidity
		self.soil_moisture = soil_moisture
		self.sunlight = sunlight

	# When passed as a string, return data for each dimension
	def __str__(self):
		return f"({self.temperature},{self.humidity},{self.soil_moisture},{self.sunlight})"

	# When suntraction operator used, return tuple containing self.data-other.data values
	def __sub__(self, other):
		return (self.temperature - other.temperature, self.humidity - other.humidity, self.soil_moisture - other.soil_moisture, self.sunlight - other.sunlight)

	# When != operator used, return truth value for eqality of all dimensions
	def __ne__(self, other):
		if ((self.temperature == other.temperature) and (self.humidity == other.humidity) and (self.soil_moisture == other.soil_moisture) and (self.sunlight == other.sunlight)):
			return False
		else:
			return True

	# Return uniformly weighted total distance between self's variables and other's variables
	def distance(self, other):
		return abs(self.temperature - other.temperature) + abs(self.humidity - other.humidity) + abs(self.soil_moisture - other.soil_moisture) + abs(self.sunlight - other.sunlight)

class Environment:
	# Return reward for agent's actions - incorporate considerations for: movement towards goal state, close proximity to goal state, overall distance from goal state
	def reward(last_state, next_state, goal_state):
		last_difference = State.distance(last_state, goal_state)
		next_difference = State.distance(next_state, goal_state)

		# Encourage movement towards goal state
		if last_difference > next_difference:
			reward = 500
		elif last_difference < next_difference:
			reward = -1000
		else:
			reward = 0

		# Encourage maintaining close proximity to goal state
		if next_difference < 1:
			reward += 2000
		elif next_difference < 2:
			reward += 1000
		elif next_difference < 3:
			reward += 500
		else:
			reward += -100

		# Scaled portion of reward based on distance from goal state
		reward -= next_difference * 10

		return reward

	# Take current state and actions, return next state based on model of system
	def transition(current_state, light_action, water_action, ventilation_action):
		next_state = State(current_state.temperature, current_state.humidity, current_state.soil_moisture, current_state.sunlight)

		if light_action == 'increase':
			factor = round(random.randint(80, 100)/100, 1)
			next_state.sunlight += factor

			factor = round(random.randint(80, 100)/100, 1)
			next_state.temperature += factor
		elif light_action == 'decrease':
			factor = round(random.randint(80, 100)/100, 1)
			if next_state.sunlight > factor:
				next_state.sunlight -= factor
			else:
				next_state.sunlight = 0

			factor = round(random.randint(80, 100)/100, 1)
			if next_state.temperature > factor:
				next_state.temperature -= factor
			else:
				next_state.temperature = 0
		else:
			factor = round(random.randint(-2, 3)/10, 1)
			next_state.temperature += factor

			factor = round(random.randint(-2, 3)/10, 1)
			next_state.sunlight += factor

		if water_action == 'increase':
			factor = round(random.randint(80, 100)/100, 1)
			next_state.soil_moisture += factor

			factor = round(random.randint(0, 20)/100, 1)
			next_state.humidity += factor
		elif water_action == 'decrease':
			factor = round(random.randint(80, 100)/100, 1)
			if next_state.soil_moisture > factor:
				next_state.soil_moisture -= factor
			else:
				next_state.soil_moisture = 0

			factor = round(random.randint(0, 20)/100, 1)
			if next_state.humidity > factor:
				next_state.humidity -= factor
			else:
				next_state.humidity = 0
		else:
			factor = round(random.randint(-2, 3)/10, 1)
			next_state.soil_moisture += factor

			factor = round(random.randint(-2, 3)/10, 1)
			next_state.humidity += factor

		if ventilation_action == 'increase':
			factor = round(random.randint(80, 100)/100, 1)
			if next_state.temperature > factor:
				next_state.temperature -= factor
			else:
				next_state.temperature = 0

			factor = round(random.randint(80, 100)/100, 1)
			if next_state.humidity > factor:
				next_state.humidity -= factor
			else:
				next_state.humidity = 0
		elif ventilation_action == 'decrease':
			factor = round(random.randint(80, 100)/100, 1)
			next_state.temperature += factor

			factor = round(random.randint(80, 100)/100, 1)
			next_state.humidity += factor
		else:
			factor = round(random.randint(-2, 3)/10, 1)
			next_state.temperature += factor

			factor = round(random.randint(-2, 3)/10, 1)
			next_state.humidity += factor

		return next_state

class Agent:
	# Run RL algorithm
	def run(initial_state, goal_state):
		if initial_state == goal_state:
			return ({'light_action': light_action, 'water_action': water_action, 'ventilation_action': ventilation_action}, None)

		action_choices = ['increase', 'decrease', 'none']

		# Iterate through all possible action vectors
		avg_episode_rewards = []
		for initial_light_action in action_choices:
				for initial_water_action in action_choices:
					for initial_ventilation_action in action_choices:
						episode_rewards = []
						for episode in range(0, 50):
							timestep = 0

							discount = .7

							# Look one step ahead, observe next state and reward
							next_state = Environment.transition(initial_state, initial_light_action, initial_water_action, initial_ventilation_action)
							next_reward = Environment.reward(initial_state, next_state, goal_state)

							# Take transition
							current_state = next_state
							current_reward = next_reward

							# Record discounted reward
							total_reward = (discount**timestep) * current_reward

							while((State.distance(current_state, goal_state) > 1) and (timestep < 4)):
								# Pick actions according to greedy policy
								max_next_reward = {'reward': -200, 'light_action': None, 'water_action': None, 'ventilation_action': None}
								for light_action in action_choices:
									for water_action in action_choices:
										for ventilation_action in action_choices:
											next_state = Environment.transition(current_state, light_action, water_action, ventilation_action)
											next_reward = Environment.reward(current_state, next_state, goal_state)

											if next_reward > max_next_reward['reward']:
												max_next_reward = {'reward': next_reward, 'light_action': light_action, 'water_action': water_action, 'ventilation_action': ventilation_action}

								# Extract actions from return of greedy policy
								light_action = max_next_reward['light_action']
								water_action = max_next_reward['water_action']
								ventilation_action = max_next_reward['ventilation_action']

								# Look one step ahead, observe new state and reward
								next_state = Environment.transition(current_state, light_action, water_action, ventilation_action)
								next_reward = Environment.reward(current_state, next_state, goal_state)

								# Take transition
								current_state = next_state
								current_reward = next_reward

								# Record discounted reward
								total_reward += (discount**timestep) * current_reward

								timestep += 1

							episode_rewards.append(total_reward)

						# Find average of episode rewards, save data
						avg_episode_reward = mean(episode_rewards)
						avg_episode_rewards.append({'avg_episode_reward': avg_episode_reward, 'light_action': initial_light_action, 'water_action': initial_water_action, 'ventilation_action': initial_ventilation_action})

		# Find largest average episode reward, the actions used in these episodes are our choice actions
		avg_episode_rewards = sorted(avg_episode_rewards, key=lambda k: k['avg_episode_reward'], reverse=True)
		choice = avg_episode_rewards[0]

		return {'light_action': choice['light_action'], 'water_action':  choice['water_action'], 'ventilation_action':  choice['ventilation_action'], 'avg_episode_rewards': avg_episode_rewards}

class Test:
	# Run simulation test
	def run(current_state, goal_state, timesteps):
		# Start at timestep 0
		timestep = 0

		# Record current state, goal state
		current_states = [current_state]
		goal_states = [goal_state]

		# Display timestep
		print(f'timestep {timestep}')

		for timestep in range(1, timesteps):
			print('------------')

			# Display timestep
			print(f'timestep {timestep}')

			# Run algorithm to get new decision from current state
			results = Agent.run(current_state, goal_state)

			# Extract actions from decision
			light_action = results['light_action']
			water_action = results['water_action']
			ventilation_action = results['ventilation_action']

			print('------------')
			print(f'state: {current_state}')
			print(f'light: {light_action} water: {water_action} ventilation: {ventilation_action}')

			# Take actions and observe new state
			current_state = Environment.transition(current_state, light_action, water_action, ventilation_action)

			# Record current state, goal state
			current_states.append(current_state)
			goal_states.append(goal_state)


		return {'current_states': current_states, 'goal_states': goal_states}

	# Plot simulation data
	def plot(current_states, goal_states):
		if len(current_states) == len(goal_states):
			length = len(current_states)
		else:
			print(f'plot: len(current_states) ({len(current_states)}) != len(goal_states) ({len(goal_states)})')
			return -1

		current_temperatures = []
		current_humidities = []
		current_soil_moistures = []
		current_sunlights = []

		goal_temperatures = []
		goal_humidities = []
		goal_soil_moistures = []
		goal_sunlights = []

		for current_state in current_states:
			current_temperatures.append(current_state.temperature)
			current_humidities.append(current_state.humidity)
			current_soil_moistures.append(current_state.soil_moisture)
			current_sunlights.append(current_state.sunlight)

		for goal_state in goal_states:
			goal_temperatures.append(goal_state.temperature)
			goal_humidities.append(goal_state.humidity)
			goal_soil_moistures.append(goal_state.soil_moisture)
			goal_sunlights.append(goal_state.sunlight)

		pyplot.plot(range(length), current_temperatures, 'r-', label="Temperature")
		pyplot.plot(range(length), current_humidities, 'g-', label="Humiditiy")
		pyplot.plot(range(length), current_soil_moistures, 'b-', label="Soil Moisture")
		pyplot.plot(range(length), current_sunlights, 'y-', label="Sunlight")

		pyplot.plot(range(length), goal_temperatures, 'r--')
		pyplot.plot(range(length), goal_humidities, 'g--')
		pyplot.plot(range(length), goal_soil_moistures, 'b--')
		pyplot.plot(range(length), goal_sunlights, 'y--')

		pyplot.xlabel('Timestep')
		pyplot.ylabel('Value')

		bottom, top = pyplot.ylim()
		pyplot.ylim(0, top*1.5)

		pyplot.title(f'Simulation Over {length} Timesteps')

		pyplot.legend()

		pyplot.show()

current_state = State(25, 20, 28, 20)
goal_state = State(10, 10, 10, 10)

print(f"PARAMS: current state: {current_state}, goal state: {goal_state}")
print('------------')

results = Test.run(current_state, goal_state, 50)

current_states = results['current_states']
goal_states = results['goal_states']

print('------------')
for (index, state) in enumerate(current_states):
	print(f'timestep: {index} state: {state}')

Test.plot(current_states, goal_states)