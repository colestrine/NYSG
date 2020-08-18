
import json
import os
from os.path import expanduser
from datetime import date,timedelta


class data_handler:
    def write_healthy_levels(temperature, humidity, soil_moisture_static, soil_moisture_dry,soil_moisture_wet, run, days, sunlight):
        levels_dict = {'temperature': temperature, 'humidity': humidity,
                       'soil_moisture_wet': soil_moisture_wet, 'soil_moisture_dry': soil_moisture_dry,
                       'soil_moisture_static': soil_moisture_static, 'days' : days, 'run' : run, 'sunlight': sunlight}
        levels_dict = dynamic_soil_control(levels_dict)
        levels_json = json.dumps(levels_dict)
        healthy_levels_file = open(expanduser(
            "~")+'/NYSG/Interface Files/healthy_levels.json', 'w')
        healthy_levels_file.write(levels_json)
        healthy_levels_file.close()

    def read_healthy_levels():
        healthy_levels_file = open(expanduser(
            "~")+'/NYSG/Interface Files/healthy_levels.json', 'r')
        levels_json = healthy_levels_file.read()
        healthy_levels_file.close()
        levels_dict = json.loads(levels_json)

        return levels_dict

    def write_plant_profile(plant_profile):
        profile_dict = {'plant_profile': plant_profile}
        profile_json = json.dumps(profile_dict)

        plant_profile_file = open(expanduser(
            "~")+'/NYSG/Interface Files/plant_profile.json', 'w')
        plant_profile_file.write(profile_json)
        plant_profile_file.close()

    def read_plant_profile():
        plant_profile_file = open(expanduser(
            "~")+'/NYSG/Interface Files/plant_profile.json', 'r')
        profile_json = plant_profile_file.read()
        plant_profile_file.close()
        profile_dict = json.loads(profile_json)

        return profile_dict

    def get_healthy_levels_by_profile(profile):
        healthy_levels_by_profile_file = open(expanduser(
            "~")+'/NYSG/Interface Files/healthy_levels_by_profile.json', 'r')
        healthy_levels_by_profile_json = healthy_levels_by_profile_file.read()
        healthy_levels_by_profile_file.close()
        healthy_levels_by_profile_dict = json.loads(
            healthy_levels_by_profile_json)

        return healthy_levels_by_profile_dict[profile]

    def get_available_profiles():
        available_profiles_file = open(expanduser(
            "~")+'/NYSG/Interface Files/healthy_levels_by_profile.json', 'r')
        available_profiles_json = available_profiles_file.read()
        available_profiles_file.close()
        available_profiles_dict = json.loads(available_profiles_json)

        profiles = []
        for profile in available_profiles_dict:
            profiles.append((profile, profile))

        return profiles

    def get_available_temperatures():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        temperatures = []
        for bucket in available_buckets_dict['temperature']:
            label = available_buckets_dict['temperature'][bucket]['label']

            temperatures.append((bucket, label))

        return temperatures

    def get_available_humidities():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        humidities = []
        for bucket in available_buckets_dict['humidity']:
            label = available_buckets_dict['humidity'][bucket]['label']

            humidities.append((bucket, label))

        return humidities

    def get_available_sunlights():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        sunlights = []
        for bucket in available_buckets_dict['sunlight']:
            label = available_buckets_dict['sunlight'][bucket]['label']

            sunlights.append((bucket, label))

        return sunlights

    def get_available_soil_moisture_statics():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        soil_moistures = []
        for bucket in available_buckets_dict['soil_moisture_static']:
            label = available_buckets_dict['soil_moisture_static'][bucket]['label']

            soil_moistures.append((bucket, label))

        return soil_moistures

    def get_available_soil_moisture_wets():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        soil_moistures = []
        for bucket in available_buckets_dict['soil_moisture_wet']:
            label = available_buckets_dict['soil_moisture_wet'][bucket]['label']

            soil_moistures.append((bucket, label))

        return soil_moistures

    def get_available_soil_moisture_drys():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        soil_moistures = []
        for bucket in available_buckets_dict['soil_moisture_dry']:
            label = available_buckets_dict['soil_moisture_dry'][bucket]['label']

            soil_moistures.append((bucket, label))

        return soil_moistures

    def get_available_days():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        soil_moistures = []
        for bucket in available_buckets_dict['days']:
            label = available_buckets_dict['days'][bucket]['label']

            soil_moistures.append((bucket, label))

        return soil_moistures

    def get_available_runs():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        soil_moistures = []
        for bucket in available_buckets_dict['run']:
            label = available_buckets_dict['run'][bucket]['label']

            soil_moistures.append((bucket, label))

        return soil_moistures
    
    def get_available_soil_moistures():
        available_buckets_file = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        available_buckets_json = available_buckets_file.read()
        available_buckets_file.close()
        available_buckets_dict = json.loads(available_buckets_json)

        soil_moistures = []
        for bucket in available_buckets_dict['soil_moisture']:
            label = available_buckets_dict['soil_moisture'][bucket]['label']

            soil_moistures.append((bucket, label))

        return soil_moistures

    def get_log_data():
        log_file = open(expanduser("~")+'/NYSG/Interface Files/log.json', 'r')
        log_json = log_file.read()
        log_file.close()
        log_dict = json.loads(log_json)

        for update in log_dict:
            log_dict[update]['temperature'] = round(
                log_dict[update]['temperature'], 2)
            log_dict[update]['humidity'] = round(
                log_dict[update]['humidity'], 2)
            log_dict[update]['soil_moisture'] = round(
                log_dict[update]['soil_moisture'], 2)
            log_dict[update]['sunlight'] = round(
                log_dict[update]['sunlight'], 2)

        return log_dict

    def save_profile(profile_name, temperature, humidity, soil_moisture_static, soil_moisture_dry,soil_moisture_wet, run, days, sunlight):
        healthy_levels_by_profile_file_r = open(expanduser(
            "~")+'/NYSG/Interface Files/healthy_levels_by_profile.json', 'r')
        healthy_levels_by_profile_json = healthy_levels_by_profile_file_r.read()
        healthy_levels_by_profile_file_r.close()
        healthy_levels_by_profile_dict = json.loads(
            healthy_levels_by_profile_json)

        new_profile = {'temperature': temperature, 'humidity': humidity,
                       'soil_moisture_wet': soil_moisture_wet, 'soil_moisture_dry': soil_moisture_dry,
                       'soil_moisture_static': soil_moisture_wet, 'days' : days, 'run' : run, 'sunlight': sunlight}

        healthy_levels_by_profile_dict[profile_name] = new_profile

        healthy_levels_by_profile_file_w = open(expanduser(
            "~")+'/NYSG/Interface Files/healthy_levels_by_profile.json', 'w')
        healthy_levels_by_profile_file_w.write(
            json.dumps(healthy_levels_by_profile_dict))
        healthy_levels_by_profile_file_w.close()

    def get_legend():
        value_buckets_file_r = open(expanduser(
            "~")+'/NYSG/Interface Files/value_buckets.json', 'r')
        value_buckets_json = value_buckets_file_r.read()
        value_buckets_file_r.close()
        value_buckets_dict = json.loads(value_buckets_json)

        return value_buckets_dict

    # Variable is element in ['temperature', 'humidity', 'soil_moisture', 'sunlight'], value is a float in [0.0, 6.0)
    def bucket_to_nominal(variable, value):
        legend = data_handler.get_legend()
        legend = legend[variable]

        value_base = str(value).split('.')[0]
        value_fraction_str = str(value).split('.')[1]
        value_fraction = int(value_fraction_str)/(10**len(value_fraction_str))

        if (variable == 'sunlight') and (value_base == '5'):
            value_base = '4'

        legend = legend[value_base]
        low = int(legend['low'])
        high = int(legend['high'])
        label = legend['label']

        difference = high - low

        nominal = round(low + (difference * value_fraction), 2)

        return nominal

    def put_manual_actions(water, fan, heat, light):
        actions_file = open(expanduser(
            "~")+'/NYSG/Interface Files/manual_actions.json', 'w')

        actions = {'water': water, 'fan': fan, 'heat': heat, 'light': light}
        actions_file.write(json.dumps(actions))
        actions_file.close()

    def get_manual_actions():
        actions_file = open(expanduser(
            "~")+'/NYSG/Interface Files/manual_actions.json', 'r')
        actions_json = actions_file.read()
        actions_file.close()

        return json.loads(actions_json)

    def get_mode():
        mode_file = open(expanduser(
            "~")+'/NYSG/Interface Files/mode.json', 'r')
        mode_json = mode_file.read()
        mode_file.close()

        return json.loads(mode_json)["mode"]

    def put_mode(mode):
        mode_file = open(expanduser(
            "~")+'/NYSG/Interface Files/mode.json', 'w')

        mode = {"mode": mode}

        mode_file.write(json.dumps(mode))

        mode_file.close()

    def put_alert_settings(rate, detail, email, password):
        alert_settings_file = open(expanduser(
            "~")+'/NYSG/Interface Files/email_settings.json', 'w')

        alert_settings = {"rate": rate, "detail": detail}

        alert_settings_file.write(json.dumps(alert_settings))

        alert_settings_file.close()

        old_alert_settings = data_handler.get_alert_settings()

        if not(email):
            print('no email')
            email = old_alert_settings['email']

        if not(password):
            password = old_alert_settings['password']

        with open(expanduser("~")+'/NYSG/Controller/configuration.json', 'w') as email_file:
            email_settings = {"email_address": email,
                              "email_password": password, "receiver_email_address": [email]}

            email_file.write(json.dumps(email_settings))

    def get_alert_settings():
        alert_settings_file = open(expanduser(
            "~")+'/NYSG/Interface Files/email_settings.json', 'r')
        alert_settings_json = alert_settings_file.read()
        alert_settings_file.close()

        json_out = json.loads(alert_settings_json)

        with open(expanduser("~")+'/NYSG/Controller/configuration.json', 'r') as email_file:
            email_settings = json.loads(email_file.read())

            json_out['email'] = email_settings['email_address']
            json_out['password'] = email_settings['email_password']

        return json_out

    def put_dc_settings(fan_dc, light_dc):
        dc_file = open(expanduser(
            "~")+'/NYSG/Interface Files/pwm_settings.json', 'w')

        dc_settings = {
            "light": {
                "duty_cycles": light_dc
            },
            "fan": {
                "duty_cycles": fan_dc
            }
        }

        dc_file.write(json.dumps(dc_settings))

        dc_file.close()

    def get_dc_settings():
        dc_file = open(expanduser(
            "~")+'/NYSG/Interface Files/pwm_settings.json', 'r')
        dc_settings_json = dc_file.read()
        dc_file.close()
        loaded_data = json.loads(dc_settings_json)
        return {"fan_dc": loaded_data["fan"]["duty_cycles"], "light_dc": loaded_data["light"]["duty_cycles"]}

    def put_freq_settings(fan_freq, light_freq):
        freq_file = open(expanduser(
            "~")+'/NYSG/Interface Files/freq_settings.json', 'w')

        freq_settings = {
            "light": {
                "frequency": light_freq
            },
            "fan": {
                "frequency": fan_freq
            }
        }

        freq_file.write(json.dumps(freq_settings))

        freq_file.close()

    def get_freq_settings():
        freq_file = open(expanduser(
            "~")+'/NYSG/Interface Files/freq_settings.json', 'r')
        freq_settings_json = freq_file.read()
        freq_file.close()
        loaded_data = json.loads(freq_settings_json)
        return {"fan_freq": loaded_data["fan"]["frequency"], "light_freq": loaded_data["light"]["frequency"]}

    def put_interval_settings(interval):
        interval_file = open(expanduser(
            "~")+'/NYSG/Interface Files/interval_settings.json', 'w')

        interval_settings = {"interval": interval}

        interval_file.write(json.dumps(interval_settings))

        interval_file.close()

    def get_interval_settings():
        interval_file = open(expanduser(
            "~")+'/NYSG/Interface Files/interval_settings.json', 'r')
        interval_settings_json = interval_file.read()
        interval_file.close()
        loaded_data = json.loads(interval_settings_json)
        return loaded_data

    def delete_main_log_data():
        # get old data
        main_log_file = open(expanduser(
            "~")+'/NYSG/Interface Files/log.json', 'r')
        old_main_log_json = main_log_file.read()
        main_log_file.close()
        old_main_log = json.loads(old_main_log_json)

        # clear main log
        main_log_file = open(expanduser(
            "~")+'/NYSG/Interface Files/log.json', 'w')
        main_log = {
            "31-07-2020 11:02:58": {
                "sunlight": 0,
                "temperature": 0,
                "humidity": 0,
                "soil_moisture": 0,
                "water_action": 0,
                "fan_action": 0,
                "heat_action": 0,
                "light_action": 0
            }}
        main_log_file.write(json.dumps(main_log))
        main_log_file.close()

        # backup old data
        backup_log_file = open(expanduser(
            "~")+'/NYSG/Interface Files/log_backup1.json', 'w')
        backup_log_file.write(json.dumps(old_main_log))
        backup_log_file.close()

    def get_germination_settings():
        germ_file = open(expanduser(
            "~")+'/NYSG/Interface Files/germination.json', 'r')
        germ_json = germ_file.read()
        germ_file.close()
        germ_data = json.loads(germ_json)
        return germ_data

    def set_germination_settings(d1, m1, y1, d2, m2, y2):
        germ_file = open(expanduser(
            "~")+'/NYSG/Interface Files/germination.json', 'w')
        germ_log = {
            "start_date": str(y1) + "-" + str(m1) + "-" + str(d1),
            "end_date": str(y2) + "-" + str(m2) + "-" + str(d2)
        }
        germ_file.write(json.dumps(germ_log))
        germ_file.close()

    def get_plant_profiles():
        plant_profiles_file = open(expanduser(
            "~")+'/NYSG/Jupyter Notebooks/ui_plant_scrape.json', 'r')
        plant_profiles_json = plant_profiles_file.read()
        plant_profiles_file.close()
        plant_data = json.loads(plant_profiles_json)
        # plant_data = plant_json["data"]
        return plant_data

    def set_address_profiles(street_address, city, state, zip_code):
        address_file = open(expanduser(
            "~")+'/NYSG/Interface Files/home_address.json', 'w')
        address_json = {
            "street_address": street_address,
            "city": city,
            "state": state,
            "zip": zip_code
        }
        address_file.write(json.dumps(address_json))
        address_file.close()

    def get_address_profiles():
        plant_profiles_file = open(expanduser(
            "~")+'/NYSG/Interface Files/home_address.json', 'r')
        plant_profiles_json = plant_profiles_file.read()
        plant_profiles_file.close()
        plant_data = json.loads(plant_profiles_json)
        # plant_data = plant_json["data"]
        new_data = {}
        new_data["street_address"] = plant_data["street_address"]
        new_data["city_address"] = plant_data["city"]
        new_data["state_address"] = plant_data["state"]
        new_data["zip_code"] = plant_data["zip"]
        new_data["submit_form"] = "No"
        return new_data

    def get_temp_profile():
        temp_profiles_file = open(expanduser(
            "~")+'/NYSG/Interface Files/temp_format.json', 'r')
        temp_profiles_json = temp_profiles_file.read()
        temp_profiles_file.close()
        temp_data = json.loads(temp_profiles_json)
        return temp_data

    def set_temp_profile(temp):
        temp_file = open(expanduser(
            "~")+'/NYSG/Interface Files/temp_format.json', 'w')
        temp_json = {
            "temp": temp
        }
        temp_file.write(json.dumps(temp_json))
        temp_file.close()

def dynamic_soil_control(healthy_levels_dict):
    print(healthy_levels_dict)
    if healthy_levels_dict["run"] == "0":
        healthy_levels_dict["soil_moisture"] = healthy_levels_dict["soil_moisture_static"]
        return healthy_levels_dict

    last_water_file = open(expanduser("~")+'/NYSG/Interface Files/dynamic_soil.json', 'r')
    last_json = last_water_file.read()
    last_water_file.close()
    last_dict = json.loads(last_json)

    print(last_json)
    days = int(healthy_levels_dict["days"])
    today = date.today()
    t = last_dict["last"]
    t = date.fromisoformat(t)
    time_since_water = today -  t
    if time_since_water >= timedelta(days = days) or time_since_water == timedelta(days = 0) :
        healthy_levels_dict["soil_moisture"] = healthy_levels_dict["soil_moisture_wet"]
        today = today.isoformat()
        last_dict["last"] = today
        last_json = json.dumps(last_dict)
        last_water_file = open(expanduser("~")+'/NYSG/Interface Files/dynamic_soil.json', 'w')
        last_water_file.write(last_json)
        last_water_file.close()

    else:
        healthy_levels_dict["soil_moisture"] = healthy_levels_dict["soil_moisture_dry"]
    return healthy_levels_dict
