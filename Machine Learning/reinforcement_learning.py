from numpy import random, mean
from copy import copy

class State:
	def __init__(self, temperature, humidity, soil_moisture, sunlight):
		self.temperature = temperature
		self.humidity = humidity
		self.soil_moisture = soil_moisture
		self.sunlight = sunlight

	def __str__(self):
		return f"({self.temperature},{self.humidity},{self.soil_moisture},{self.sunlight})"

	def __sub__(self, other):
		return (self.temperature - other.temperature, self.humidity - other.humidity, self.soil_moisture - other.soil_moisture, self.sunlight - other.sunlight)

	def __ne__(self, other):
		if ((self.temperature == other.temperature) and (self.humidity == other.humidity) and (self.soil_moisture == other.soil_moisture) and (self.sunlight == other.sunlight)):
			return False
		else:
			return True

	def distance(self, other):
		return abs(self.temperature - other.temperature) + abs(self.humidity - other.humidity) + abs(self.soil_moisture - other.soil_moisture) + abs(self.sunlight - other.sunlight)

class Environment:
	def reward(last_state, next_state, goal_state):
		last_difference = State.distance(last_state, goal_state)
		next_difference = State.distance(next_state, goal_state)

		if last_difference > next_difference:
			reward = 500
		elif last_difference < next_difference:
			reward = -1000
		else:
			reward = 0

		if next_difference < 2:
			reward += 1000
		elif next_difference < 4:
			reward += 500
		else:
			reward += -100

		return reward

	def transition(current_state, light_action, water_action, ventilation_action):
		next_state = State(current_state.temperature, current_state.humidity, current_state.soil_moisture, current_state.sunlight)

		if light_action == 'increase':
			factor = round(random.randint(50, 100)/100, 1)
			next_state.sunlight += factor

			factor = round(random.randint(0, 50)/100, 1)
			next_state.temperature += factor
		elif light_action == 'decrease':
			factor = round(random.randint(50, 100)/100, 1)
			if next_state.sunlight > factor:
				next_state.sunlight -= factor
			else:
				next_state.sunlight = 0

			factor = round(random.randint(0, 50)/100, 1)
			if next_state.temperature > factor:
				next_state.temperature -= factor
			else:
				next_state.temperature = 0

		if water_action == 'increase':
			factor = round(random.randint(50, 100)/100, 1)
			next_state.soil_moisture += factor

			factor = round(random.randint(0, 50)/100, 1)
			next_state.humidity += factor
		elif water_action == 'decrease':
			factor = round(random.randint(50, 100)/100, 1)
			if next_state.soil_moisture > factor:
				next_state.soil_moisture -= factor
			else:
				next_state.soil_moisture = 0

			factor = round(random.randint(0, 50)/100, 1)
			if next_state.humidity > factor:
				next_state.humidity -= factor
			else:
				next_state.humidity = 0

		if ventilation_action == 'increase':
			factor = round(random.randint(50, 100)/100, 1)
			if next_state.temperature > factor:
				next_state.temperature -= factor
			else:
				next_state.temperature = 0

			factor = round(random.randint(50, 100)/100, 1)
			if next_state.humidity > factor:
				next_state.humidity -= factor
			else:
				next_state.humidity = 0
		elif ventilation_action == 'decrease':
			factor = round(random.randint(50, 100)/100, 1)
			next_state.temperature += factor

			factor = round(random.randint(50, 100)/100, 1)
			next_state.humidity += factor

		return next_state

class Agent:
	def run(initial_state, goal_state):
		if initial_state == goal_state:
			return ({'light_action': light_action, 'water_action': water_action, 'ventilation_action': ventilation_action}, None)

		action_choices = ['increase', 'decrease', 'none']

		avg_episode_rewards = []
		for initial_light_action in action_choices:
				for initial_water_action in action_choices:
					for initial_ventilation_action in action_choices:
						episode_rewards = []
						for episode in range(0, 100):
							timestep = 0

							discount = .7

							# Look one step ahead, observe next state and reward
							next_state = Environment.transition(initial_state, initial_light_action, initial_water_action, initial_ventilation_action)
							next_reward = Environment.reward(initial_state, next_state, goal_state)

							# print(f'state 0: {initial_state}')
							# print(f'light action: {initial_light_action} water action: {initial_water_action} ventilation action: {initial_ventilation_action}')
							# print(f'state 1: {next_state} reward: {next_reward}')

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

								light_action = max_next_reward['light_action']
								water_action = max_next_reward['water_action']
								ventilation_action = max_next_reward['ventilation_action']

								# # Pick a random action
								# light_action = action_choices[random.randint(0, len(action_choices))]
								# water_action = action_choices[random.randint(0, len(action_choices))]
								# ventilation_action = action_choices[random.randint(0, len(action_choices))]

								# Look one step ahead, observe new state and reward
								next_state = Environment.transition(current_state, light_action, water_action, ventilation_action)
								next_reward = Environment.reward(current_state, next_state, goal_state)

								# Take transition
								current_state = copy(next_state)
								current_reward = next_reward

								# Record discounted reward
								total_reward = (discount**timestep) * current_reward

								timestep += 1

							episode_rewards.append(total_reward)

						avg_episode_reward = mean(episode_rewards)
						avg_episode_rewards.append({'avg_episode_reward': avg_episode_reward, 'light_action': initial_light_action, 'water_action': initial_water_action, 'ventilation_action': initial_ventilation_action})

		avg_episode_rewards = sorted(avg_episode_rewards, key=lambda k: k['avg_episode_reward'], reverse=True)
		choice = avg_episode_rewards[0]

		return {'light_action': choice['light_action'], 'water_action':  choice['water_action'], 'ventilation_action':  choice['ventilation_action'], 'avg_episode_rewards': avg_episode_rewards}

current_state = State(12, 12, 10, 12)
goal_state = State(10, 10, 10, 10)

print(f"current state: {current_state}, goal state: {goal_state}")
print('------------')

results = Agent.run(current_state, goal_state)

light_action = results['light_action']
water_action = results['water_action']
ventilation_action = results['ventilation_action']

print(f'light action: {light_action}, water action: {water_action}, ventilation action: {ventilation_action}')
print('------------')

for reward in results['avg_episode_rewards']:
	print(f"average reward: {reward['avg_episode_reward']}, light action: {reward['light_action']}, water action: {reward['water_action']}, ventilation action: {reward['ventilation_action']}")