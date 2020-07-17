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
	for record in log_data:
		labels += str(record) + ','
		temperatures += str(log_data[record]['temperature']) + ','
		humidities += str(log_data[record]['humidity']) + ','
		soil_moistures += str(log_data[record]['soil_moisture']) + ','
		sunlights += str(log_data[record]['sunlight']) + ','

	temperatures = temperatures[:-1]
	humidities = humidities[:-1]
	soil_moistures = soil_moistures[:-1]
	sunlights = sunlights[:-1]
	labels = labels[:-1]

	action_form = ActionForm()

	return render(request, 'Manual/manual.html', {'labels': labels, 'temperatures': temperatures, 'humidities': humidities, 'soil_moistures': soil_moistures, 'sunlights': sunlights, 'action_form': action_form})