from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ActionForm
from scripts.data_handler import data_handler
from collections import OrderedDict
import json

# Create your views here.
def index(request):
	log_data = data_handler.get_log_data()
	labels = ''
	temperatures = ''
	humidities = ''
	soil_moistures = ''
	sunlights = ''
	water_actions = ''
	fan_actions = ''
	heat_actions = ''
	light_actions = ''
	for record in log_data:
		labels += str(record) + ','
		temperatures += str(log_data[record]['temperature']) + ','
		humidities += str(log_data[record]['humidity']) + ','
		soil_moistures += str(log_data[record]['soil_moisture']) + ','
		sunlights += str(log_data[record]['sunlight']) + ','
		water_actions += str(log_data[record]['water_action']) + ','
		fan_actions += str(log_data[record]['fan_action']) + ','
		heat_actions += str(log_data[record]['heat_action']) + ','
		light_actions += str(log_data[record]['light_action']) + ','

	temperatures = temperatures[:-1]
	humidities = humidities[:-1]
	soil_moistures = soil_moistures[:-1]
	sunlights = sunlights[:-1]
	water_actions = water_actions[:-1]
	fan_actions = fan_actions[:-1]
	heat_actions = heat_actions[:-1]
	light_actions = light_actions[:-1]
	labels = labels[:-1]

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

	action_form = ActionForm()

	return render(request, 'Manual/manual.html', {'water_actions': water_actions, 'fan_actions': fan_actions, 'heat_actions': heat_actions, 'light_actions': light_actions, 'legend': legend, 'last_temperature': last_temperature, 'last_humidity': last_humidity, 'last_soil_moisture': last_soil_moisture, 'last_sunlight': last_sunlight, 'last_reading_datetime': last_reading_datetime, 'labels': labels, 'temperatures': temperatures, 'humidities': humidities, 'soil_moistures': soil_moistures, 'sunlights': sunlights, 'action_form': action_form})