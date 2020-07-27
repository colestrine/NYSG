from reinforcement_learning import Environment, State

last_state = State(1, 1, 1, 1)
next_state = State(2, 2, 2, 2)
goal_state = State(3, 3, 3, 3)

reward = Environment.reward(last_state, next_state, goal_state)

print(reward)




