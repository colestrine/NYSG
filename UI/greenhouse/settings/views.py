from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import HealthyLevelsForm, PlantProfileForm, SaveProfileForm
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

	healthy_levels = data_handler.read_healthy_levels()
	plant_profile = data_handler.read_plant_profile()
	plant_profile_form = PlantProfileForm(initial=plant_profile)
	healthy_levels_form = HealthyLevelsForm(initial=healthy_levels)
	save_profile_form = SaveProfileForm()

	log_data = data_handler.get_log_data()
	log_data = OrderedDict(log_data)
	log_data = list(log_data.items())
	last_reading = {}
	last_reading_datetime, last_reading_values = log_data[-1]

	legend = data_handler.get_legend()
	print(legend)

	return render(request, 'Settings/settings.html', {'legend': legend, 'last_temperature': last_reading_values['temperature'], 'last_humidity': last_reading_values['humidity'], 'last_soil_moisture': last_reading_values['soil_moisture'], 'last_sunlight': last_reading_values['sunlight'], 'last_reading_datetime': last_reading_datetime, 'save_profile_form': save_profile_form, 'can_save': can_save, 'healthy_levels_form': healthy_levels_form, 'plant_profile_form': plant_profile_form, 'healthy_levels': healthy_levels, 'plant_profile': plant_profile})