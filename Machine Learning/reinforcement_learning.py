from numpy import random, mean, zeros
from matplotlib import pyplot
import importlib
#from transition import ActionSet, EffectSet
transition = importlib.import_module(
    'Machine Learning.transition')
from os.path import expanduser
import json

class State:
    # State class holds data for temperature, humidity, and soil moisture

    def __init__(self, temperature, humidity, soil_moisture):
        self.temperature = float(temperature)
        self.humidity = float(humidity)
        self.soil_moisture = float(soil_moisture)

    # When passed as a string, return data for each dimension
    def __str__(self):
        return f"({self.temperature},{self.humidity},{self.soil_moisture})"

    # When suntraction operator used, return tuple containing
    # self.data-other.data values
    def __sub__(self, other):
        return (self.temperature - other.temperature, self.humidity - other.humidity, self.soil_moisture - other.soil_moisture)

    # When != operator used, return truth value for equality of all dimensions
    def __ne__(self, other):
        if ((self.temperature == other.temperature) and (self.humidity == other.humidity) and (self.soil_moisture == other.soil_moisture)):
            return False
        else:
            return True

    # Return uniformly weighted total distance between self's variables and
    # other's variables
    def distance(self, other):
        return abs(self.temperature - other.temperature) + abs(self.humidity - other.humidity) + abs(self.soil_moisture - other.soil_moisture)

    def getGoal():
        healthy_levels_file = open(expanduser("~")+'/NYSG/Interface Files/healthy_levels.json', 'r')
        levels_json = healthy_levels_file.read()
        healthy_levels_file.close()
        levels = json.loads(levels_json)

        goal = State(float(levels['temperature']), float(levels['humidity']), float(levels['soil_moisture']))

        return goal

class Environment:
    # Return reward for agent's actions - incorporate considerations for:
    # movement towards goal state, close proximity to goal state, overall
    # distance from goal state

    def reward(last_state, next_state, goal_state, water_action, ventilation_action, heat_action):
        last_difference = State.distance(last_state, goal_state)
        next_difference = State.distance(next_state, goal_state)

        # # Encourage movement towards goal state
        # if last_difference > next_difference:
        #     reward = 100 * next_difference
        # elif last_difference < next_difference:
        #     reward = -1000
        # else:
        #     reward = 0

        # # Encourage maintaining close proximity to goal state
        # if next_difference < .25:
        #     reward += 7000
        # elif next_difference < .5:
        #     reward += 5000
        # elif next_difference < 1:
        #     reward += 2000
        # else:
        #     reward += -1000

        # # Scaled portion of reward based on distance from goal state
        # reward -= next_difference * 50

        # Set intitial reward, scaled based on distance from goal state
        reward = -100 * last_difference

        # Encourage efficiency
        if water_action == "none":
            reward += 10
        if ventilation_action == "none":
            reward += 10
        if heat_action == "none":
            reward += 10

        return reward

    # Take current state and actions, return next state based on model of
    # system
    def transition(current_state, water_action, ventilation_action, heat_action, prior_effects):
        next_state = State(current_state.temperature, current_state.humidity,
                           current_state.soil_moisture)

        big_random_low = 50
        big_random_high = 60

        small_random_low = 3
        small_random_high = 10

        if water_action == 'big_increase':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.soil_moisture += factor

            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.humidity += factor
        elif water_action == 'small_increase':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.soil_moisture += factor

            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.humidity += factor
        elif water_action == 'big_decrease':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.soil_moisture > factor:
                next_state.soil_moisture -= factor
            else:
                next_state.soil_moisture = 0

            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.humidity > factor:
                next_state.humidity -= factor
            else:
                next_state.humidity = 0
        elif water_action == 'small_decrease':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.soil_moisture > factor:
                next_state.soil_moisture -= factor
            else:
                next_state.soil_moisture = 0

            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.humidity > factor:
                next_state.humidity -= factor
            else:
                next_state.humidity = 0
        else:
            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.soil_moisture += factor

            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.humidity += factor

        if ventilation_action == 'big_increase':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.temperature > factor:
                next_state.temperature -= factor
            else:
                next_state.temperature = 0

            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.humidity > factor:
                next_state.humidity -= factor
            else:
                next_state.humidity = 0
        elif ventilation_action == 'small_increase':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.temperature > factor:
                next_state.temperature -= factor
            else:
                next_state.temperature = 0

            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.humidity > factor:
                next_state.humidity -= factor
            else:
                next_state.humidity = 0
        elif ventilation_action == 'big_decrease':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.temperature += factor

            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.humidity += factor
        elif ventilation_action == 'small_decrease':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.temperature += factor

            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.humidity += factor
        else:
            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.temperature += factor

            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.humidity += factor

        if heat_action == 'big_increase':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.temperature += factor
        elif heat_action == 'small_increase':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.temperature += factor
        elif heat_action == 'big_decrease':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.temperature > factor:
                next_state.temperature -= factor
            else:
                next_state.temperature = 0
        elif heat_action == 'small_decrease':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.temperature > factor:
                next_state.temperature -= factor
            else:
                next_state.temperature = 0
        else:
            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.temperature += factor

#<<<<<<< HEAD
        ########################################################################
        action_set = ActionSet(ventilation_action, water_action, heat_action)
# =======
        action_set = transition.ActionSet(ventilation_action, water_action, heat_action)
# >>>>>>> demo-tuesday-august-4

        if current_state.temperature < 1.0 :
            current_state.temperature = 1.0
        elif current_state.temperature > 5.9:
            current_state.temperature = 5.9

        if current_state.humidity < 1.0 :
            current_state.humidity = 1.0
        elif current_state.humidity > 5.9:
            current_state.humidity = 5.9

        if current_state.soil_moisture < 1.0 :
            current_state.soil_moisture = 1.0
        elif current_state.soil_moisture > 5.9:
            current_state.soil_moisture = 5.9

        temperature_bucket = str(current_state.temperature).split('.')[0]
        humidity_bucket = str(current_state.humidity).split('.')[0]
        soil_moisture_bucket = str(current_state.soil_moisture).split('.')[0]

        # bootstrap_effects = EffectSet.getBootstrapEffects()

        # bootstrap_temperature_effect = bootstrap_effects[str(action_set)]['temperature'][temperature_bucket]['effect']
        # bootstrap_humidity_effect = bootstrap_effects[str(action_set)]['humidity'][humidity_bucket]['effect']
        # bootstrap_soil_moisture_effect = bootstrap_effects[str(action_set)]['soil_moisture'][soil_moisture_bucket]['effect']

        # boostrap_temperature_hits = bootstrap_effects[str(action_set)]['temperature'][temperature_bucket]['hits']
        # bootstrap_humidity_hits = bootstrap_effects[str(action_set)]['humidity'][humidity_bucket]['hits']
        # bootstrap_soil_moisture_hits = bootstrap_effects[str(action_set)]['soil_moisture'][soil_moisture_bucket]['hits']

        prior_temperature_effect = prior_effects[str(action_set)]['temperature'][temperature_bucket]['effect']
        prior_humidity_effect = prior_effects[str(action_set)]['humidity'][humidity_bucket]['effect']
        prior_soil_moisture_effect = prior_effects[str(action_set)]['soil_moisture'][soil_moisture_bucket]['effect']

        prior_temperature_hits = prior_effects[str(action_set)]['temperature'][temperature_bucket]['hits']
        prior_humidity_hits = prior_effects[str(action_set)]['humidity'][humidity_bucket]['hits']
        prior_soil_moisture_hits = prior_effects[str(action_set)]['soil_moisture'][soil_moisture_bucket]['hits']

        if (prior_temperature_hits):
            next_state.temperature = .2*next_state.temperature + .8*(next_state.temperature + prior_temperature_effect) #REPLACE WITH BOOTSTRAP DATA

        if (prior_humidity_hits):
            next_state.humidity = .2*next_state.humidity + .8*(next_state.humidity + prior_humidity_effect) #REPLACE WITH BOOTSTRAP DATA

        if (prior_soil_moisture_hits):
            next_state.soil_moisture = .2*next_state.soil_moisture + .8*(next_state.soil_moisture + prior_soil_moisture_effect) #REPLACE WITH BOOTSTRAP DATA

        return next_state

class Agent:
    # Run RL algorithm

    def run(initial_state, goal_state):
        if initial_state == goal_state:
            return ({'water_action': water_action, 'ventilation_action': ventilation_action, 'heat_action': heat_action}, None)

        # Define action choices
        action_choices = ['big_increase', 'big_decrease', 'small_increase', 'small_decrease', 'none']

        # Get prior effects
        prior_effects = transition.EffectSet.getEffects()

        # Iterate through all possible action vectors
        avg_episode_rewards = []
        for initial_water_action in action_choices:
            for initial_ventilation_action in action_choices:
                for initial_heat_action in action_choices:
                    episode_rewards = []
                    for episode in range(0, 75):
                        timestep = 0

                        discount = .7

                        # Look one step ahead, observe next state and reward
                        next_state = Environment.transition(initial_state, initial_water_action, initial_ventilation_action, initial_heat_action, prior_effects)
                        next_reward = Environment.reward(initial_state, next_state, goal_state, initial_water_action, initial_ventilation_action, initial_heat_action)

                        # Take transition
                        current_state = next_state
                        current_reward = next_reward

                        # Record discounted reward
                        total_reward = (discount**timestep) * current_reward

                        while(timestep < 3):
                            # Pick next actions
                            water_action = action_choices[random.randint(0, 5)]
                            ventilation_action = action_choices[random.randint(0, 5)]
                            heat_action = action_choices[random.randint(0, 5)]

                            # Look one step ahead, observe new state and reward
                            next_state = Environment.transition(current_state, water_action, ventilation_action, heat_action, prior_effects)
                            next_reward = Environment.reward(current_state, next_state, goal_state, water_action, ventilation_action, heat_action)

                            # Take transition
                            current_state = next_state
                            current_reward = next_reward

                            # Record discounted reward
                            total_reward += (discount**timestep) * current_reward

                            timestep += 1

                        episode_rewards.append(total_reward)

                    # Find average of episode rewards, save data
                    avg_episode_reward = mean(episode_rewards)
                    avg_episode_rewards.append({'avg_episode_reward': avg_episode_reward, 'water_action': initial_water_action, 'ventilation_action': initial_ventilation_action, 'heat_action': initial_heat_action})

        # Find largest average episode reward, the actions used in these
        # episodes are our choice actions
        avg_episode_rewards = sorted(avg_episode_rewards, key=lambda k: k['avg_episode_reward'], reverse=True)
        choice = avg_episode_rewards[0]

        return {'water_action':  choice['water_action'], 'ventilation_action':  choice['ventilation_action'], 'heat_action': choice['heat_action'], 'expected_reward': choice['avg_episode_reward']}

class Test:
    def transition(current_state, water_action, ventilation_action, heat_action):
        next_state = State(current_state.temperature, current_state.humidity, current_state.soil_moisture)

        big_random_low = 86
        big_random_high = 88

        small_random_low = 19
        small_random_high = 21

        if water_action == 'big_increase':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.soil_moisture += factor

            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.humidity += factor
        elif water_action == 'small_increase':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.soil_moisture += factor

            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.humidity += factor
        elif water_action == 'big_decrease':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.soil_moisture > factor:
                next_state.soil_moisture -= factor
            else:
                next_state.soil_moisture = 0

            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.humidity > factor:
                next_state.humidity -= factor
            else:
                next_state.humidity = 0
        elif water_action == 'small_decrease':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.soil_moisture > factor:
                next_state.soil_moisture -= factor
            else:
                next_state.soil_moisture = 0

            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.humidity > factor:
                next_state.humidity -= factor
            else:
                next_state.humidity = 0
        else:
            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.soil_moisture += factor

            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.humidity += factor

        if ventilation_action == 'big_increase':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.temperature > factor:
                next_state.temperature -= factor
            else:
                next_state.temperature = 0

            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.humidity > factor:
                next_state.humidity -= factor
            else:
                next_state.humidity = 0
        elif ventilation_action == 'small_increase':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.temperature > factor:
                next_state.temperature -= factor
            else:
                next_state.temperature = 0

            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.humidity > factor:
                next_state.humidity -= factor
            else:
                next_state.humidity = 0
        elif ventilation_action == 'big_decrease':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.temperature += factor

            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.humidity += factor
        elif ventilation_action == 'small_decrease':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.temperature += factor

            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.humidity += factor
        else:
            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.temperature += factor

            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.humidity += factor

        if heat_action == 'big_increase':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            next_state.temperature += factor
        elif heat_action == 'small_increase':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            next_state.temperature += factor
        elif heat_action == 'big_decrease':
            factor = round(random.randint(
                big_random_low, big_random_high) / 100, 1)
            if next_state.temperature > factor:
                next_state.temperature -= factor
            else:
                next_state.temperature = 0
        elif heat_action == 'small_decrease':
            factor = round(random.randint(
                small_random_low, small_random_high) / 100, 1)
            if next_state.temperature > factor:
                next_state.temperature -= factor
            else:
                next_state.temperature = 0
        else:
            factor = round(random.randint(-2, 3) / 100, 1)
            next_state.temperature += factor

        return next_state

    # Run simulation test
    def run(current_state, goal_state, timesteps):
        # Start at timestep 0
        timestep = 0

        # Record current state, goal state
        current_states = [current_state]
        goal_states = [goal_state]

        expected_rewards = [0]

        # Display timestep
        print(f'timestep {timestep}')

        for timestep in range(1, timesteps):
            print('------------')

            # Display timestep
            print(f'timestep {timestep}')

            # Run algorithm to get new decision from current state
            results = Agent.run(current_state, goal_state)

            # Extract actions from decision
            water_action = results['water_action']
            ventilation_action = results['ventilation_action']
            heat_action = results['heat_action']

            # Extract expected reward
            expected_reward = results['expected_reward']

            print('------------')
            print(f'starting state: {current_state}')
            print(f'water: {water_action} ventilation: {ventilation_action} heat: {heat_action}\nexpected reward: {expected_reward}')

            # Save last state
            last_state = current_state

            # Take actions and observe new state
            current_state = Test.transition(current_state, water_action, ventilation_action, heat_action)

            # Add an extra layer of randomness +/- [0, .02]
            current_state.temperature += random.randint(-1, 2)/50
            current_state.humidity += random.randint(-1, 2)/50
            current_state.soil_moisture += random.randint(-1, 2)/50

            # Constrain values between 1.0 and 5.9
            if current_state.temperature < 1.0 :
                current_state.temperature = 1.0
            elif current_state.temperature > 5.9:
                current_state.temperature = 5.9

            if current_state.humidity < 1.0 :
                current_state.humidity = 1.0
            elif current_state.humidity > 5.9:
                current_state.humidity = 5.9

            if current_state.soil_moisture < 1.0 :
                current_state.soil_moisture = 1.0
            elif current_state.soil_moisture > 5.9:
                current_state.soil_moisture = 5.9

            # # Temperature Floor
            # if current_state.temperature < 2.8:
            #     current_state.temperature = 2.8

            # Create action set
            action_set = transition.ActionSet(water_action, ventilation_action, heat_action)

            # Record transition in transition.json
            put = transition.EffectSet.putEffect(action_set, last_state, current_state)

            print(f'ending state: {current_state}')
            print(f'effects: {put}')

            # Record current state, goal state, expected reward, actual reward
            current_states.append(current_state)
            goal_states.append(goal_state)
            expected_rewards.append(expected_reward)

        return {'current_states': current_states, 'goal_states': goal_states, 'expected_rewards': expected_rewards}

    # Plot simulation data
    def plot(current_states, goal_states, expected_rewards, distances):
        if len(current_states) == len(goal_states):
            length = len(current_states)
        else:
            print(f'plot: len(current_states) ({len(current_states)}) != len(goal_states) ({len(goal_states)})')
            return -1

        current_temperatures = []
        current_humidities = []
        current_soil_moistures = []

        goal_temperatures = []
        goal_humidities = []
        goal_soil_moistures = []

        for current_state in current_states:
            current_temperatures.append(current_state.temperature)
            current_humidities.append(current_state.humidity)
            current_soil_moistures.append(current_state.soil_moisture)

        for goal_state in goal_states:
            goal_temperatures.append(goal_state.temperature)
            goal_humidities.append(goal_state.humidity)
            goal_soil_moistures.append(goal_state.soil_moisture)

        pyplot.figure(1)

        pyplot.plot(range(length), current_temperatures,
                    'r-', label="Temperature")
        pyplot.plot(range(length), current_humidities, 'g-', label="Humiditiy")
        pyplot.plot(range(length), current_soil_moistures,
                    'b-', label="Soil Moisture")

        pyplot.plot(range(length), goal_temperatures, 'r--')
        pyplot.plot(range(length), goal_humidities, 'g--')
        pyplot.plot(range(length), goal_soil_moistures, 'b--')

        pyplot.xlabel('Timestep')
        pyplot.ylabel('Value')

        bottom, top = pyplot.ylim()
        pyplot.ylim(0, top * 1.5)

        pyplot.title(f'Simulation Over {length} Timesteps')

        pyplot.legend()

        pyplot.figure(2)

        pyplot.plot(range(length), expected_rewards)

        pyplot.xlabel('Timestep')
        pyplot.ylabel('Value')

        pyplot.title(f'Expected Rewards Over {length} Timesteps')

        pyplot.figure(3)

        pyplot.plot(range(length), distances)
        pyplot.plot(range(length), zeros(length))

        pyplot.xlabel('Timestep')
        pyplot.ylabel('Value')

        pyplot.title(f'Distance From Goal State Over {length} Timesteps')

        pyplot.show()

if __name__ == '__main__':
    for i in range(0, 10):
        current_state = State(random.randint(150, 550)/100, random.randint(150, 550)/100, random.randint(150, 550)/100)
        goal_state = State(random.randint(150, 550)/100, random.randint(150, 550)/100, random.randint(150, 550)/100) #State.getGoal() #State(2.5, 2.8, 4.5)

        print(f"PARAMS: current state: {current_state}, goal state: {goal_state}")
        print('------------')

        results = Test.run(current_state, goal_state, 60)

        current_states = results['current_states']
        goal_states = results['goal_states']
        expected_rewards = results['expected_rewards']

        distances = []
        print('------------')
        for (index, state) in enumerate(current_states):
            print(f'timestep: {index} state: {state}')
            distance = State.distance(state, goal_state)
            distances.append(distance)
            print(f'distance from goal state: {distance}')

#<<<<<<< HEAD
        Test.plot(current_states, goal_states, expected_rewards, distances)
# =======
#    Test.plot(current_states, goal_states, expected_rewards, distances)
# >>>>>>> demo-tuesday-august-4
