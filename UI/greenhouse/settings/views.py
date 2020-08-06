from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import HealthyLevelsForm, PlantProfileForm, SaveProfileForm, ModeForm, ActionForm, AlertForm, PwmForm, FreqForm, UpdateIntervalForm
from scripts.data_handler import data_handler
from collections import OrderedDict
import json

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


		# Check each form to see if it is valid. If valid, scrape data. If not, enter empty placeholder.
		if healthy_levels_form.is_valid():
			temperature = healthy_levels_form.cleaned_data['temperature']
			humidity = healthy_levels_form.cleaned_data['humidity']
			soil_moisture = healthy_levels_form.cleaned_data['soil_moisture']
			sunlight = healthy_levels_form.cleaned_data['sunlight']
		else:
			temperature = ''
			humidity = ''
			soil_moisture = ''
			sunlight = ''

		if plant_profile_form.is_valid():
			plant_profile = plant_profile_form.cleaned_data['plant_profile']
		else:
			plant_profile = ''

		if save_profile_form.is_valid():
			profile_name = save_profile_form.cleaned_data['profile_name']
			temperature = save_profile_form.cleaned_data['custom_temperature']
			humidity = save_profile_form.cleaned_data['custom_humidity']
			soil_moisture = save_profile_form.cleaned_data['custom_soil_moisture']
			sunlight = save_profile_form.cleaned_data['custom_sunlight']
		else:
			profile_name = ''
			custom_temperature = ''
			custom_humidity = ''
			custom_soil_moisture = ''
			custom_sunlight = ''

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
		else:
			rate = ''
			detail = ''

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


		# If data was submitted, write that data to the interface file
		# If healthy levels data was submitted, update healthy levels interface file, and save plant profile as "custom" in profile interface file
		if (temperature):
			data_handler.write_healthy_levels(temperature, humidity, soil_moisture, sunlight)
			data_handler.write_plant_profile("custom")
			can_save = True
		# If profile data was submitted, save profile in profile interface file
		if (plant_profile):
			data_handler.write_plant_profile(plant_profile)

			# If profile was not "custom", update healthy levels interface file with levels from that profile
			if (plant_profile != "custom"):
				healthy_levels = data_handler.get_healthy_levels_by_profile(plant_profile)

				temperature = healthy_levels['temperature']
				humidity = healthy_levels['humidity']
				soil_moisture = healthy_levels['soil_moisture']
				sunlight = healthy_levels['sunlight']

				data_handler.write_healthy_levels(temperature, humidity, soil_moisture, sunlight)
		# If a profile name was submitted, save data as a new profile, and set that profile to be the current profile
		if (profile_name):
			data_handler.save_profile(profile_name, temperature, humidity, soil_moisture, sunlight)
			data_handler.write_healthy_levels(temperature, humidity, soil_moisture, sunlight)
			data_handler.write_plant_profile(profile_name)
			can_save = False
		if (mode):
			data_handler.put_mode(mode)
		if (water != ''):
			### CALL CONTROLLER METHODS HERE ###

			data_handler.put_manual_actions(water, fan, heat, light)
			action_form = ActionForm(initial={'water': water, 'fan': fan, 'heat': heat, 'light': light})


		# check if the alert form was submitted and save teh data in the interface file 
		if (rate or detail):
			data_handler.put_alert_settings(rate, detail)

		if (fan_dc or light_dc):
			data_handler.put_dc_settings(fan_dc, light_dc)
		
		if (fan_freq or light_freq):
			data_handler.put_freq_settings(fan_freq, light_freq)

		if (interval):
			data_handler.put_interval_settings(interval)
		
		
		



	mode = data_handler.get_mode()
	current_manual_actions = data_handler.get_manual_actions()
	current_alert_settings = data_handler.get_alert_settings()
	current_dc_settings = data_handler.get_dc_settings()
	current_freq_settings = data_handler.get_freq_settings()
	current_interval_settings = data_handler.get_interval_settings()

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
	save_profile_form = SaveProfileForm()
	mode_form = ModeForm(initial={'mode': mode})
	action_form = ActionForm(initial=current_manual_actions)
	alert_form = AlertForm(initial = current_alert_settings)
	pwm_form = PwmForm(initial=current_dc_settings)
	freq_form = FreqForm(initial=current_freq_settings)
	update_interval = UpdateIntervalForm(initial=current_interval_settings)

	log_data = data_handler.get_log_data()
	log_data = OrderedDict(log_data)
	log_data = list(log_data.items())
	last_reading = {}
	last_reading_datetime, last_reading_values = log_data[-1]

	legend = data_handler.get_legend()

	last_temperature = data_handler.bucket_to_nominal("temperature", last_reading_values['temperature'])
	last_humidity = data_handler.bucket_to_nominal("humidity", last_reading_values['humidity'])
	last_soil_moisture = data_handler.bucket_to_nominal("soil_moisture", last_reading_values['soil_moisture'])
	last_sunlight = data_handler.bucket_to_nominal("sunlight", last_reading_values['sunlight'])

	return render(request, 'Settings/settings.html', {'action_form': action_form, 'mode': mode, 'mode_form': mode_form, 'legend': legend, 'last_temperature': last_temperature, 'last_humidity': last_humidity, 'last_soil_moisture': last_soil_moisture, 'last_sunlight': last_sunlight, 'last_reading_datetime': last_reading_datetime, 'save_profile_form': save_profile_form, 'can_save': can_save, 'healthy_levels_form': healthy_levels_form, 'plant_profile_form': plant_profile_form, 'healthy_levels': healthy_levels, 'plant_profile': plant_profile, 'alert_form': alert_form, 'pwm_form':pwm_form, 'freq_form':freq_form, 'fan_freq':fan_freq, 'light_freq':light_freq, 'fan_dc':fan_dc, 'light_dc':light_dc, 'update_interval':update_interval})
