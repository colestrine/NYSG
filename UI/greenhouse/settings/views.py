from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import HealthyLevelsForm, PlantProfileForm, SaveProfileForm, ModeForm, ActionForm, AlertForm, PwmForm, FreqForm, UpdateIntervalForm, DeleteForm, StartDateForm, AddressForm, DaysForm, TempForm
from scripts.data_handler import data_handler
from collections import OrderedDict
import json
from datetime import datetime, timedelta


def is_valid_date(y, m, d):
    try:
        datetime(year=int(y), month=int(m), day=int(d))
        return True
    except:
        return False

# Create your views here.


def index(request):
    # Set can_save flag to default False
    can_save = False

    # If request is POST type, form was submitted - process request
    if request.method == 'POST':
        # Instantiate form objects with POST data
        plant_profile_form = PlantProfileForm(request.POST)
        healthy_levels_form = HealthyLevelsForm(request.POST)
        save_profile_form = SaveProfileForm(request.POST)
        mode_form = ModeForm(request.POST)
        action_form = ActionForm(request.POST)
        alert_form = AlertForm(request.POST)
        pwm_form = PwmForm(request.POST)
        freq_form = FreqForm(request.POST)
        update_interval = UpdateIntervalForm(request.POST)
        delete_form = DeleteForm(request.POST)
        start_date_form = StartDateForm(request.POST)
        address_form = AddressForm(request.POST)
        days_form = DaysForm(request.POST)
        temp_form = TempForm(request.POST)

        # Check each form to see if it is valid. If valid, scrape data. If not, enter empty placeholder.
        if healthy_levels_form.is_valid():
            temperature = healthy_levels_form.cleaned_data['temperature']
            humidity = healthy_levels_form.cleaned_data['humidity']
            sunlight = healthy_levels_form.cleaned_data['sunlight']
            soil_moisture_static = healthy_levels_form.cleaned_data['soil_moisture_static']
            soil_moisture_wet = healthy_levels_form.cleaned_data['soil_moisture_wet']
            soil_moisture_dry = healthy_levels_form.cleaned_data['soil_moisture_dry']
            run = healthy_levels_form.cleaned_data['run']
            days = healthy_levels_form.cleaned_data['days']

        else:
            temperature = ''
            humidity = ''
            sunlight = ''
            soil_moisture_static = ''
            soil_moisture_dry = ''
            soil_moisture_wet = ''
            run = ''
            days = ''

        if plant_profile_form.is_valid():
            plant_profile = plant_profile_form.cleaned_data['plant_profile']
        else:
            plant_profile = ''

        if save_profile_form.is_valid():
            profile_name = save_profile_form.cleaned_data['profile_name']
            temperature = save_profile_form.cleaned_data['custom_temperature']
            humidity = save_profile_form.cleaned_data['custom_humidity']
            sunlight = save_profile_form.cleaned_data['custom_sunlight']
            soil_moisture_static = save_profile_form.cleaned_data['custom_soil_moisture_static']
            soil_moisture_wet = save_profile_form.cleaned_data['custom_soil_moisture_wet']
            soil_moisture_dry = save_profile_form.cleaned_data['custom_soil_moisture_dry']
            days = save_profile_form.cleaned_data['custom_days']
            run = save_profile_form.cleaned_data['custom_run']
        else:
            profile_name = ''
            custom_temperature = ''
            custom_humidity = ''
            custom_sunlight = ''
            custom_soil_moisture_static = ''
            custom_soil_moisture_wet = ''
            custom_soil_moisture_dry = ''
            custom_days = ''
            custom_run = ''

        if mode_form.is_valid():
            mode = mode_form.cleaned_data['mode']
        else:
            mode = ''

        if action_form.is_valid():
            water = action_form.cleaned_data['water']
            fan = action_form.cleaned_data['fan']
            heat = action_form.cleaned_data['heat']
            light = action_form.cleaned_data['light']
        else:
            water = ''
            fan = ''
            heat = ''
            light = ''

        if alert_form.is_valid():
            rate = alert_form.cleaned_data['rate']
            detail = alert_form.cleaned_data['detail']
            email = alert_form.cleaned_data['email']
            password = alert_form.cleaned_data['password']
        else:
            rate = ''
            detail = ''
            email = ''
            password = ''

        if pwm_form.is_valid():
            fan_dc = pwm_form.cleaned_data['fan_dc']
            light_dc = pwm_form.cleaned_data['light_dc']
        else:
            fan_dc = ''
            light_dc = ''

        if freq_form.is_valid():
            fan_freq = freq_form.cleaned_data['fan_freq']
            light_freq = freq_form.cleaned_data['light_freq']
        else:
            fan_freq = ''
            light_freq = ''

        if update_interval.is_valid():
            interval = update_interval.cleaned_data['interval']
        else:
            interval = ''

        if delete_form.is_valid():
            data_handler.delete_main_log_data()

        if start_date_form.is_valid():
            start_day = start_date_form.cleaned_data['start_day']
            start_month = start_date_form.cleaned_data['start_month']
            start_year = start_date_form.cleaned_data['start_year']
            end_day = start_date_form.cleaned_data['end_day']
            end_month = start_date_form.cleaned_data['end_month']
            end_year = start_date_form.cleaned_data['end_year']
        else:
            start_day = ''
            start_month = ''
            start_year = ''
            end_day = ''
            end_month = ''
            end_year = ''

        if address_form.is_valid():
            street_address = address_form.cleaned_data['street_address']
            city_address = address_form.cleaned_data['city_address']
            state_address = address_form.cleaned_data['state_address']
            zip_code = address_form.cleaned_data['zip_code']
            submit_form = address_form.cleaned_data['submit_form']
        else:
            street_address = ""
            city_address = ""
            state_address = ""
            zip_code = ""
            submit_form = ''

        if days_form.is_valid():
            day = days_form.cleaned_data["day"]
        else:
            day = ""

        if temp_form.is_valid():
            temp = temp_form.cleaned_data["temp"]
        else:
            temp = ""

        # If data was submitted, write that data to the interface file
        # If healthy levels data was submitted, update healthy levels interface file, and save plant profile as "custom" in profile interface file
        if (temperature):
            data_handler.write_healthy_levels(
                temperature, humidity, soil_moisture_static, soil_moisture_dry,
		soil_moisture_wet, run, days, sunlight)
            data_handler.write_plant_profile("custom")
            can_save = True
        # If profile data was submitted, save profile in profile interface file
        if (plant_profile):
            data_handler.write_plant_profile(plant_profile)

            # If profile was not "custom", update healthy levels interface file with levels from that profile
            if (plant_profile != "custom"):
                healthy_levels = data_handler.get_healthy_levels_by_profile(
                    plant_profile)

                temperature = healthy_levels['temperature']
                humidity = healthy_levels['humidity']
                soil_moisture_static = healthy_levels['soil_moisture_static']
                soil_moisture_wet = healthy_levels['soil_moisture_wet']
                soil_moisture_dry = healthy_levels['soil_moisture_dry']
                days = healthy_levels['days']
                run = healthy_levels['run']
                sunlight = healthy_levels['sunlight']

                data_handler.write_healthy_levels(
                    temperature, humidity, soil_moisture_static, 
                    soil_moisture_dry,soil_moisture_wet, run, days, sunlight)
        # If a profile name was submitted, save data as a new profile, and set that profile to be the current profile
        if (profile_name):
            data_handler.save_profile(
                profile_name, temperature, humidity, soil_moisture_static, soil_moisture_dry,soil_moisture_wet, run, days, sunlight)
            data_handler.write_healthy_levels(
                temperature, humidity, soil_moisture_static, soil_moisture_dry,soil_moisture_wet, run, days, sunlight)
            data_handler.write_plant_profile(profile_name)
            can_save = False
        if (mode):
            data_handler.put_mode(mode)
        if (water != ''):
            ### CALL CONTROLLER METHODS HERE ###

            data_handler.put_manual_actions(water, fan, heat, light)
            action_form = ActionForm(
                initial={'water': water, 'fan': fan, 'heat': heat, 'light': light})

        # check if the alert form was submitted and save teh data in the interface file
        if (rate or detail or email or password):
            data_handler.put_alert_settings(rate, detail, email, password)

        if (fan_dc or light_dc):
            data_handler.put_dc_settings(fan_dc, light_dc)

        if (fan_freq or light_freq):
            data_handler.put_freq_settings(fan_freq, light_freq)

        if (interval):
            data_handler.put_interval_settings(interval)

        if start_day:
            if is_valid_date(start_year, start_month, start_day) and is_valid_date(end_year, end_month, end_day):
                data_handler.set_germination_settings(
                    start_day, start_month, start_year, end_day, end_month, end_year)

        if submit_form:
            data_handler.set_address_profiles(
                street_address, city_address, state_address, zip_code)

        if day:
            curr_date = datetime.now()
            d1 = curr_date.day
            d1 = str(d1)
            d1 = "0"+d1 if len(d1) < 2 else d1
            m1 = curr_date.month
            m1 = str(m1)
            m1 = "0"+m1 if len(m1) < 2 else m1
            y1 = curr_date.year
            delta = timedelta(days=int(day))
            new_date = curr_date + delta
            d2 = new_date.day
            d2 = str(d2)
            d2 = "0"+d2 if len(d2) < 2 else d2
            m2 = new_date.month
            m2 = str(m2)
            m2 = "0"+m2 if len(m2) < 2 else m2
            y2 = new_date.year
            data_handler.set_germination_settings(d1, m1, y1, d2, m2, y2)

        if temp:
            data_handler.set_temp_profile(temp)

    mode = data_handler.get_mode()
    current_manual_actions = data_handler.get_manual_actions()
    current_alert_settings = data_handler.get_alert_settings()
    current_dc_settings = data_handler.get_dc_settings()
    current_freq_settings = data_handler.get_freq_settings()
    current_interval_settings = data_handler.get_interval_settings()
    current_start_date = data_handler.get_germination_settings()
    current_address = data_handler.get_address_profiles()
    temp_format = data_handler.get_temp_profile()

    start_date = current_start_date["start_date"]
    split_start = start_date.split("-")
    # split_start = list(map(lambda s : int(s), split_start))
    start_year = split_start[0]
    start_month = split_start[1]
    start_day = split_start[2]
    end_date = current_start_date["end_date"]
    split_end = end_date.split("-")
    # split_end= list(map(lambda s : int(s), split_end))
    end_year = split_end[0]
    end_month = split_end[1]
    end_day = split_end[2]

    # extract duty cycles for view render
    fan_dc = current_dc_settings["fan_dc"]
    light_dc = current_dc_settings["light_dc"]
    # extract frequencies for view render
    fan_freq = current_freq_settings["fan_freq"]
    light_freq = current_freq_settings["light_freq"]

    healthy_levels = data_handler.read_healthy_levels()
    plant_profile = data_handler.read_plant_profile()
    plant_profile_form = PlantProfileForm(initial=plant_profile)
    healthy_levels_form = HealthyLevelsForm(initial=healthy_levels)
    save_profile_form = SaveProfileForm(initial=plant_profile)
    mode_form = ModeForm(initial={'mode': mode})
    action_form = ActionForm(initial=current_manual_actions)
    alert_form = AlertForm(initial=current_alert_settings)
    pwm_form = PwmForm(initial=current_dc_settings)
    freq_form = FreqForm(initial=current_freq_settings)
    update_interval = UpdateIntervalForm(initial=current_interval_settings)
    delete_form = DeleteForm(initial={'delete_field': 'no'})
    start_date_form = StartDateForm(initial={'start_day': start_day, 'start_month': start_month,
                                             'start_year': start_year, 'end_day': end_day, 'end_month': end_month, 'end_year': end_year})
    address_form = AddressForm(initial=current_address)
    days_form = DaysForm(initial={"day": 0})
    temp_form = TempForm(initial=temp_format)

    log_data = data_handler.get_log_data()
    log_data = OrderedDict(log_data)
    log_data = list(log_data.items())
    last_reading = {}
    last_reading_datetime, last_reading_values = log_data[-1]

    legend = data_handler.get_legend()

    last_temperature = data_handler.bucket_to_nominal(
        "temperature", last_reading_values['temperature'])
    last_humidity = data_handler.bucket_to_nominal(
        "humidity", last_reading_values['humidity'])
    last_soil_moisture = data_handler.bucket_to_nominal(
        "soil_moisture", last_reading_values['soil_moisture'])
    last_sunlight = data_handler.bucket_to_nominal(
        "sunlight", last_reading_values['sunlight'])

    return render(request, 'Settings/settings.html', {'temp_form': temp_form, 'days_form': days_form, 'action_form': action_form, 'mode': mode, 'mode_form': mode_form, 'legend': legend, 'last_temperature': last_temperature, 'last_humidity': last_humidity, 'last_soil_moisture': last_soil_moisture, 'last_sunlight': last_sunlight, 'last_reading_datetime': last_reading_datetime, 'save_profile_form': save_profile_form, 'can_save': can_save, 'healthy_levels_form': healthy_levels_form, 'plant_profile_form': plant_profile_form, 'healthy_levels': healthy_levels, 'plant_profile': plant_profile, 'alert_form': alert_form, 'pwm_form': pwm_form, 'freq_form': freq_form, 'fan_freq': fan_freq, 'light_freq': light_freq, 'fan_dc': fan_dc, 'light_dc': light_dc, 'update_interval': update_interval, 'delete_form': delete_form, 'start_date_form': start_date_form, 'address_form': address_form})
