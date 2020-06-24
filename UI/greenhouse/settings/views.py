from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import HealthyLevelsForm, PlantProfileForm
from scripts.data_handler import data_handler

# Create your views here.
def index(request):
	# If request is POST type, form was submitted - process request
	if request.method == 'POST':
		# Instantiate form objects with POST data
		plant_profile_form = PlantProfileForm(request.POST)
		healthy_levels_form = HealthyLevelsForm(request.POST)

		# Check each form to see if it is valid. If valid, scrape data. If not, enter empty placeholder.
		if healthy_levels_form.is_valid():
			temperature = healthy_levels_form.cleaned_data['temperature']
			humidity = healthy_levels_form.cleaned_data['humidity']
			soil_moisture = healthy_levels_form.cleaned_data['soil_moisture']
			sunlight = healthy_levels_form.cleaned_data['sunlight']

			data_handler.write_healthy_levels(temperature, humidity, soil_moisture, sunlight)

		else:
			temperature = ''
			humidity = ''
			soil_moisture = ''
			sunlight = ''

		if plant_profile_form.is_valid():
			plant_profile = plant_profile_form.cleaned_data['plant_profile']
		else:
			plant_profile = ''

	# If not POST, then no form submitted - instantiate blank forms
	else:
		temperature = ''
		humidity = ''
		soil_moisture = ''
		sunlight = ''
		plant_profile = ''

		plant_profile_form = PlantProfileForm()
		healthy_levels_form = HealthyLevelsForm()

	return render(request, 'Settings/settings.html', {'healthy_levels_form': healthy_levels_form, 'plant_profile_form': plant_profile_form, 'temperature': temperature, 'humidity': humidity, 'soil_moisture': soil_moisture, 'sunlight': sunlight, 'plant_profile': plant_profile})