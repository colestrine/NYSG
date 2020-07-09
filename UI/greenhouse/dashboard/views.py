from django.shortcuts import render
from django.http import HttpResponse
from scripts.data_handler import data_handler
import json

# Create your views here.
def index(request):
	healthy_levels = data_handler.read_healthy_levels()
	healthy_temperature = healthy_levels['temperature']
	healthy_humidity = healthy_levels['humidity']
	healthy_soil_moisture = healthy_levels['soil_moisture']
	healthy_sunlight = healthy_levels['sunlight']

	available_temperatures = data_handler.get_available_temperatures()
	available_humidities = data_handler.get_available_humidities()
	available_soil_moistures = data_handler.get_available_soil_moistures()
	available_sunlights = data_handler.get_available_sunlights()

	for available_temperature in available_temperatures:
		if healthy_temperature == available_temperature[0]:
			healthy_temperature_label = available_temperature[1]
			break

	for available_humidity in available_humidities:
		if healthy_humidity == available_humidity[0]:
			healthy_humidity_label = available_humidity[1]
			break

	for available_soil_moisture in available_soil_moistures:
		if healthy_soil_moisture == available_soil_moisture[0]:
			healthy_soil_moisture_label = available_soil_moisture[1]
			break

	for available_sunlight in available_sunlights:
		if healthy_sunlight == available_sunlight[0]:
			healthy_sunlight_label = available_sunlight[1]
			break


	log_data = data_handler.get_log_data()
	labels = ''
	temperatures = ''
	humidities = ''
	soil_moistures = ''
	sunlights = ''
	for record in log_data:
		labels += str(record) + ','
		temperatures += str(log_data[record]['temperature']) + ','
		humidities += str(log_data[record]['humidity']) + ','
		soil_moistures += str(log_data[record]['soil_moisture']) + ','
		sunlights += str(log_data[record]['sunlight']) + ','

	return render(request, 'Dashboard/dashboard.html', {'healthy_temperature': healthy_temperature, 'healthy_temperature_label': healthy_temperature_label, 'healthy_humidity': healthy_humidity, 'healthy_humidity_label': healthy_humidity_label, 'healthy_soil_moisture': healthy_soil_moisture, 'healthy_soil_moisture_label': healthy_soil_moisture_label, 'healthy_sunlight': healthy_sunlight, 'healthy_sunlight_label': healthy_sunlight_label, 'labels': labels, 'temperatures': temperatures, 'humidities': humidities, 'soil_moistures': soil_moistures, 'sunlights': sunlights})