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

	return render(request, 'Dashboard/dashboard.html', {'healthy_temperature': healthy_temperature, 'healthy_humidity': healthy_humidity, 'healthy_soil_moisture': healthy_soil_moisture, 'healthy_sunlight': healthy_sunlight})