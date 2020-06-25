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

def stateDifference(self, other):
	return abs(self.temperature - other.temperature) + abs(self.humidity - other.humidity) + (self.soil_moisture - other.soil_moisture) + abs(self.sunlight - other.sunlight)

class Environment:
	def reward(current_state, goal_state):
		difference = stateDifference(current_state, goal_state)

		if difference < 1:
			reward = 100
		elif difference < 5:
			reward = 0
		else:
			reward = -100

		return reward

	def transition(current_state, light_action, water_action, ventilation_action):
		next_state = State(current_state.temperature, current_state.humidity, current_state.soil_moisture, current_state.sunlight)

		if light_action == 'increase':
			factor = random.randint(0, 10)/10
			next_state.sunlight += factor

			factor = random.randint(0, 10)/10
			next_state.temperature += factor
		elif light_action == 'decrease':
			factor = random.randint(0, 10)/10
			if next_state.sunlight > factor:
				next_state.sunlight -= factor
			else:
				next_state.sunlight = 0

			factor = random.randint(0, 10)/10
			if next_state.temperature > factor:
				next_state.temperature -= factor
			else:
				next_state.temperature = 0

		if water_action == 'increase':
			factor = round(random.randint(0, 20)/10, 1)
			next_state.soil_moisture += factor

			factor = random.randint(0, 10)/10
			next_state.humidity += factor
		elif water_action == 'decrease':
			factor = round(random.randint(0, 20)/10, 1)
			if next_state.soil_moisture > factor:
				next_state.soil_moisture -= factor
			else:
				next_state.soil_moisture = 0

			factor = random.randint(0, 10)/10
			if next_state.humidity > factor:
				next_state.humidity -= factor
			else:
				next_state.humidity = 0

		if ventilation_action == 'increase':
			factor = round(random.randint(0, 20)/10, 1)
			if next_state.temperature > factor:
				next_state.temperature -= factor
			else:
				next_state.temperature = 0

			factor = round(random.randint(0, 20)/10, 1)
			if next_state.humidity > factor:
				next_state.humidity -= factor
			else:
				next_state.humidity = 0
		elif ventilation_action == 'decrease':
			factor = round(random.randint(0, 20)/10, 1)
			next_state.temperature += factor

			factor = round(random.randint(0, 20)/10, 1)
			next_state.humidity += factor

		return next_state

class Agent:
	def runEpisode(initial_state, goal_state, light_action, water_action, ventilation_action):
		# Take 1 step according to given actions, observe new state
		current_state = Environment.transition(initial_state, light_action, water_action, ventilation_action)

		action_choices = ['increase', 'decrease', 'none']

		discount = .9

		episode_reward = Environment.reward(current_state, goal_state)

		# Take actions according to greedy policy until goal state is found or timesteps == 100
		timestep = 1

		while ((stateDifference(current_state, goal_state) > 2) and (timestep < 100)):
			# Observe reward
			current_reward = Environment.reward(current_state, goal_state)

			# # Find actions with max reward according to transition model (greedy policy)
			# max_next_reward = {'reward': -200, 'light_action': None, 'water_action': None, 'ventilation_action': None}
			# for light_action in action_choices:
			# 	for water_action in action_choices:
			# 		for ventilation_action in action_choices:
			# 			next_state = Environment.transition(current_state, light_action, water_action, ventilation_action)
			# 			next_reward = Environment.reward(next_state, goal_state)

			# 			if next_reward > max_next_reward['reward']:
			# 				max_next_reward = {'reward': next_reward, 'light_action': light_action, 'water_action': water_action, 'ventilation_action': ventilation_action}

			# Pick random actions
			light_action = action_choices[random.randint(0, 2)]
			water_action = action_choices[random.randint(0, 2)]
			ventilation_action = action_choices[random.randint(0, 2)]

			# Take actions and observe enxt reward
			next_state = Environment.transition(current_state, light_action, water_action, ventilation_action)
			next_reward = Environment.reward(next_state, goal_state)

			episode_reward += (discount**timestep) * next_reward

			timestep += 1

		return episode_reward

	def runSimulation(current_state, goal_state):
		if current_state == goal_state:
			return ({'light_action': light_action, 'water_action': water_action, 'ventilation_action': ventilation_action}, None)

		action_choices = ['increase', 'decrease']

		avg_episode_rewards = []
		for light_action in action_choices:
				for water_action in action_choices:
					for ventilation_action in action_choices:
						episode_rewards = []
						for episode in range(0, 150):
							episode_reward = Agent.runEpisode(current_state, goal_state, light_action, water_action, ventilation_action)
							episode_rewards.append(episode_reward)

						avg_episode_reward = mean(episode_rewards)
						avg_episode_rewards.append({'avg_episode_reward': avg_episode_reward, 'light_action': light_action, 'water_action': water_action, 'ventilation_action': ventilation_action})

		avg_episode_rewards = sorted(avg_episode_rewards, key=lambda k: k['avg_episode_reward'], reverse=True)
		choice = avg_episode_rewards[0]

		return {'light_action': choice['light_action'], 'water_action':  choice['water_action'], 'ventilation_action':  choice['ventilation_action'], 'avg_episode_rewards': avg_episode_rewards}

current_state = State(12, 10, 10, 10)
goal_state = State(10, 10, 10, 10)

print(f"current state: {current_state}, goal state: {goal_state}")

results = Agent.runSimulation(current_state, goal_state)

light_action = results['light_action']
water_action = results['water_action']
ventilation_action = results['ventilation_action']

print(f'light action: {light_action}, water action: {water_action}, ventilation action: {ventilation_action}')

for reward in results['avg_episode_rewards']:
	print(f"average reward: {reward['avg_episode_reward']}, light action: {reward['light_action']}, water action: {reward['water_action']}, ventilation action: {reward['ventilation_action']}")