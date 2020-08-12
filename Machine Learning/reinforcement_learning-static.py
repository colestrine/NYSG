from numpy import random, mean, zeros
from matplotlib import pyplot
import importlib
#from transition import ActionSet, EffectSet
transition = importlib.import_module(
    'Machine Learning.transition')
from os.path import expanduser
import json

class State:
    # State class holds bucket data for temperature, humidity, and soil moisture, values must be between 1.0 and 5.9
    def __init__(self, temperature, humidity, soil_moisture):
        if float(temperature) < 1.0:
            self.temperature = 1.0
        elif float(temperature) > 5.9:
            self.temperature = 5.9
        else:
            self.temperature = float(temperature)

        if float(humidity) < 1.0:
            self.humidity = 1.0
        elif float(humidity) > 5.9:
            self.humidity = 5.9
        else:
            self.humidity = float(humidity)

        if float(soil_moisture) < 1.0:
            self.soil_moisture = 1.0
        elif float(soil_moisture) > 5.9:
            self.soil_moisture = 5.9
        else:
            self.soil_moisture = float(soil_moisture)

    # When passed as a string, return data for each dimension
    def __str__(self):
        return f"({self.temperature},{self.humidity},{self.soil_moisture})"

    # When suntraction operator used, return tuple containing self.data-other.data values
    def __sub__(self, other):
        return (self.temperature - other.temperature, self.humidity - other.humidity, self.soil_moisture - other.soil_moisture)

    # When != operator used, return truth value for equality of all dimensions
    def __ne__(self, other):
        if ((self.temperature == other.temperature) and (self.humidity == other.humidity) and (self.soil_moisture == other.soil_moisture)):
            return False
        else:
            return True

    # Return uniformly weighted total distance between self's variables and other's variables
    def distance(self, other):
        return abs(self.temperature - other.temperature) + abs(self.humidity - other.humidity) + abs(self.soil_moisture - other.soil_moisture)

    # Returns the goal state, as specified in healthy_levels.json
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

        # Set intitial reward, scaled based on distance from goal state
        reward = -100 * last_difference

        goal_temperature_bucket = int(str(goal_state.temperature).split('.')[0])
        goal_humidity_bucket = int(str(goal_state.humidity).split('.')[0])
        goal_soil_moisture_bucket = int(str(goal_state.soil_moisture).split('.')[0])

        next_temperature_bucket = int(str(next_state.temperature).split('.')[0])
        next_humidity_bucket = int(str(next_state.humidity).split('.')[0])
        next_soil_moisture_bucket = int(str(next_state.soil_moisture).split('.')[0])

        if next_temperature_bucket == goal_temperature_bucket:
            reward += 20
        if next_humidity_bucket == goal_humidity_bucket:
            reward += 20
        if next_soil_moisture_bucket == goal_soil_moisture_bucket:
            reward += 20

        return reward

    # Take current state and actions, return next state based on model of system
    def transition(current_state, water_action, ventilation_action, heat_action, prior_effects):
        next_state = State(current_state.temperature, current_state.humidity, current_state.soil_moisture)

        action_set = transition.ActionSet(water_action, ventilation_action, heat_action)

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

        prior_temperature_effect = prior_effects[str(action_set)]['temperature'][temperature_bucket]['effect']
        prior_humidity_effect = prior_effects[str(action_set)]['humidity'][humidity_bucket]['effect']
        prior_soil_moisture_effect = prior_effects[str(action_set)]['soil_moisture'][soil_moisture_bucket]['effect']

        prior_temperature_hits = prior_effects[str(action_set)]['temperature'][temperature_bucket]['hits']
        prior_humidity_hits = prior_effects[str(action_set)]['humidity'][humidity_bucket]['hits']
        prior_soil_moisture_hits = prior_effects[str(action_set)]['soil_moisture'][soil_moisture_bucket]['hits']

        assert (prior_temperature_hits and prior_humidity_hits and prior_soil_moisture_hits), "transition.json not properly initialized - try training first"

        next_state.temperature = next_state.temperature + prior_temperature_effect

        next_state.humidity = next_state.humidity + prior_humidity_effect

        next_state.soil_moisture = next_state.soil_moisture + prior_soil_moisture_effect

        return next_state

class Agent:
    # Run RL algorithm
    def run(initial_state, goal_state):
        if initial_state == goal_state:
            return ({'water_action': water_action, 'ventilation_action': ventilation_action, 'heat_action': heat_action}, None)

        # Define action choices
        action_choices = ['off', 'low', 'high']


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

                        # Iterate through three timesteps (as we are not concerned with longer-term effects)
                        while(timestep < 3):
                            # Pick next actions
                            water_action = action_choices[random.randint(0, 3)]
                            ventilation_action = action_choices[random.randint(0, 3)]
                            heat_action = action_choices[random.randint(0, 3)]

                            # Look one step ahead, observe new state and reward
                            next_state = Environment.transition(current_state, water_action, ventilation_action, heat_action, prior_effects)
                            next_reward = Environment.reward(current_state, next_state, goal_state, water_action, ventilation_action, heat_action)

                            # Take transition
                            current_state = next_state
                            current_reward = next_reward

                            # Record discounted reward
                            total_reward += (discount**timestep) * current_reward

                            # Increment timestep
                            timestep += 1

                        # Append expected reward to episode_rewards
                        episode_rewards.append(total_reward)

                    # Find average of episode rewards, save data
                    avg_episode_reward = mean(episode_rewards)
                    avg_episode_rewards.append({'avg_episode_reward': avg_episode_reward, 'water_action': initial_water_action, 'ventilation_action': initial_ventilation_action, 'heat_action': initial_heat_action})

        # Find largest average episode reward, the actions used in these episodes are our choice actions
        avg_episode_rewards = sorted(avg_episode_rewards, key=lambda k: k['avg_episode_reward'], reverse=True)
        choice = avg_episode_rewards[0]

        return {'water_action':  choice['water_action'], 'fan_action':  choice['ventilation_action'], 'heat_action': choice['heat_action'], 'expected_reward': choice['avg_episode_reward']}

# Contains methods used specifically for testing and demonstration purposes - not to be used in production
class Test:
    def increase(reading, low, high, weight):
        move = random.randint(low, high)/100

        reading += (move * weight)

        if reading > 5.9:
            reading = 5.9
        elif reading < 1.0:
            reading = 1.0

        return reading

    def decrease(reading, low, high, weight):
        move = random.randint(low, high)/100

        reading -= (move * weight)

        if reading > 5.9:
            reading = 5.9
        elif reading < 1.0:
            reading = 1.0

        return reading

    def temper(reading, weight):
        # Weight between 0 and 1, 0: reading, 1: 3.5
        return (weight * 3.5) + ((1-weight) * reading)

    def transition(current_state, water_action, ventilation_action, heat_action):
        next_state = State(current_state.temperature, current_state.humidity, current_state.soil_moisture)

        actions = {
            'none': {
                'low': 0,
                'high': 3
            },
            'low': {
                'low': 4,
                'high': 10
            }, 
            'medium': {
                'low': 11,
                'high': 30
            }, 
            'high': {
                'low': 50,
                'high': 100
            },
        }

        for action in actions:
            if water_action == action:
                next_state.soil_moisture = Test.increase(next_state.soil_moisture, actions[action]['low'], actions[action]['high'], 1)
                next_state.humidity = Test.increase(next_state.humidity, actions[action]['low'], actions[action]['high'], .6)
            if ventilation_action == action:
                next_state.temperature = Test.decrease(next_state.temperature, actions[action]['low'], actions[action]['high'], 1)
                next_state.humidity = Test.decrease(next_state.humidity, actions[action]['low'], actions[action]['high'], .9)
                next_state.soil_moisture = Test.decrease(next_state.soil_moisture, actions[action]['low'], actions[action]['high'], .4)
            if heat_action == action:
                next_state.temperature = Test.increase(next_state.temperature, actions[action]['low'], actions[action]['high'], .7)
                next_state.humidity = Test.increase(next_state.humidity, actions[action]['low'], actions[action]['high'], 1)

        next_state.temperature = Test.temper(next_state.temperature, .05)
        next_state.humidity = Test.temper(next_state.humidity, .04)
        next_state.soil_moisture = Test.temper(next_state.soil_moisture, .01)

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

            # Create action set
            action_set = transition.ActionSet(water_action, ventilation_action, heat_action)

            # Record transition in transition.json
            put = transition.EffectSet.putEffect(action_set, last_state, current_state, True)

            print(f'ending state: {current_state}')
            print(f'effects: {put}')

            # Record current state, goal state, expected reward, actual reward
            current_states.append(current_state)
            goal_states.append(goal_state)
            expected_rewards.append(expected_reward)

        return {'current_states': current_states, 'goal_states': goal_states, 'expected_rewards': expected_rewards}

    # Run training test
    def train(current_state):
        # Read actions.json
        with open('Machine Learning/Files/actions.json', 'r') as file:
            contents = file.read()
            actions = json.loads(contents)

        timesteps = len(actions) + 1

        current_states = [current_state]

        for timestep in range(1, timesteps):
            print('------------')

            # Display timestep
            print(f'timestep {timestep}')

            # Extract actions from decision
            water_action = actions[str(timestep)]['water']
            ventilation_action = actions[str(timestep)]['fan']
            heat_action = actions[str(timestep)]['heat']

            print('------------')
            print(f'starting state: {current_state}')
            print(f'water: {water_action} ventilation: {ventilation_action} heat: {heat_action}')

            # Save last state
            last_state = current_state

            # Take actions and observe new state
            current_state = Test.transition(current_state, water_action, ventilation_action, heat_action)

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

            # Create action set
            action_set = transition.ActionSet(water_action, ventilation_action, heat_action)

            # Record transition in transition.json
            put = transition.EffectSet.putEffect(action_set, last_state, current_state, True)

            print(f'ending state: {current_state}')
            print(f'effects: {put}')

            # Record current state, goal state, expected reward, actual reward
            current_states.append(current_state)

        return {'current_states': current_states}

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
    MODE = "run"

    if MODE == "run":
        iterations = 10

        for i in range(0, iterations):
            current_state = State(3.5, 3.5, 3.5)
            goal_state = State(random.randint(250, 450)/100, random.randint(250, 450)/100, random.randint(250, 450)/100) #State.getGoal()

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

            Test.plot(current_states, goal_states, expected_rewards, distances)
    elif MODE == "train":
        current_state = State(3.5, 3.5, 3.5)
        goal_state = State(random.randint(250, 450)/100, random.randint(250, 450)/100, random.randint(250, 450)/100) #State.getGoal()

        print(f"PARAMS: current state: {current_state}, goal state: {goal_state}")
        print('------------')

        observed_states = Test.train(current_state)
