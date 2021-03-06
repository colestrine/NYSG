from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from scripts.data_handler import data_handler
from collections import OrderedDict
from scripts.data_handler import data_handler
import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from scripts.data_handler import data_handler
from collections import OrderedDict
from scripts.data_handler import data_handler
import json
from datetime import datetime

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

	current_dc_settings = data_handler.get_dc_settings()
	current_freq_settings = data_handler.get_freq_settings()

	# extract duty cycles for view render
	fan_dc = current_dc_settings["fan_dc"]
	light_dc = current_dc_settings["light_dc"]
	# extract frequencies for view render
	fan_freq = current_freq_settings["fan_freq"]
	light_freq = current_freq_settings["light_freq"]

	length = len(log_data)
	
	germ_data = data_handler.get_germination_settings()
	start_date = germ_data['start_date']
	start_datetime = datetime.fromisoformat(start_date)
	end_date = germ_data['end_date']
	end_datetime = datetime.fromisoformat(end_date)
	now = datetime.now()
	delta_passed = now - start_datetime
	delta_passed_days = delta_passed.days
	delta_remain = end_datetime - now
	delta_remain_days = delta_remain.days
	if delta_remain_days < 0:
		delta_remain_days = 0
	if delta_passed_days < 0:
		delta_passed_days = 0

	correct_ordered_dates = start_datetime < end_datetime

	finished_germination = delta_remain_days == 0

	return render(request, 'Germination/germination.html', {'water_actions': water_actions, 'fan_actions': fan_actions, 'heat_actions': heat_actions, 'light_actions': light_actions, 'legend': legend, 'last_temperature': last_temperature, 'last_humidity': last_humidity, 'last_soil_moisture': last_soil_moisture, 'last_sunlight': last_sunlight, 'last_reading_datetime': last_reading_datetime, 'labels': labels, 'temperatures': temperatures, 'humidities': humidities, 'soil_moistures': soil_moistures, 'sunlights': sunlights, 'fan_freq':fan_freq, 'light_freq':light_freq, 'fan_dc':fan_dc, 'light_dc':light_dc, 'length':length, 'start_date':start_date, 'end_date':end_date, 'now':now, 'delta_passed_days':delta_passed_days,'delta_remain_days':delta_remain_days, 'correct_ordered_dates':correct_ordered_dates, 'finished_germination':finished_germination })