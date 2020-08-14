# SOLUTIONS
# Part 1
init_dict = init()

# Part 2
light_sensor = LightSensor(i2c_channel)
temp_humid_sensor = TempHumiditySensor(i2c_channel)
moisture_sensor = MoistureSensor()

# Part 3
valve = SolenoidValve(pin_constants.VALVE, 20)
heat = HeatPad(pin_constants.HEAT, 20)
fan = Fan(pin_constants.VENT, 20)  # inverts duty cycles inside class
light = PlantLight(pin_constants.LED, 20)

# Part 4
manual_control = pin_constants.load_data(manual_control_path)

manual_results = pin_constants.load_data(manual_actions_path)

email_settings = pin_constants.load_data(email_settings_path)

pwm_settings = pin_constants.load_data(pwm_settings_path)

freq_settings = pin_constants.load_data(freq_settings_path)

# Part 5
if healthy_light >= 4:
    return "Full sun"
elif healthy_light >= 3:
    return "Part sun"
elif healthy_light >= 2:
    return "Part shade"
elif healthy_light >= 1:
    return "Full shade"

# Part 6
if action == 0 or action == "off":
    return "off"
elif action == 1:
    return "big_decrease"
elif action == 2 or action == "low":
    return "low"
elif action == 3:
    return "small_increase"
elif action == 4 or action == "high":
    return "high"

# Part 7
while True:
    await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,alert_log, max_log_size, interval)

# Part 8
for _ in range(max_iter):
    await one_cycle(init_dict, manual_control_path, manual_actions_path, email_settings_path, pwm_settings_path, freq_settings_path, sensor_log_path, ml_action_log,
                    alert_log, max_log_size, interval)