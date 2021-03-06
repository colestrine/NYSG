from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from scripts.data_handler import data_handler
from collections import OrderedDict, defaultdict
from scripts.data_handler import data_handler
import json
from copy import deepcopy
from numpy import quantile

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

    last_temperature = data_handler.bucket_to_nominal(
        "temperature", last_reading_values['temperature'])
    last_humidity = data_handler.bucket_to_nominal(
        "humidity", last_reading_values['humidity'])
    last_soil_moisture = data_handler.bucket_to_nominal(
        "soil_moisture", last_reading_values['soil_moisture'])
    last_sunlight = data_handler.bucket_to_nominal(
        "sunlight", last_reading_values['sunlight'])

    current_dc_settings = data_handler.get_dc_settings()
    current_freq_settings = data_handler.get_freq_settings()

    # extract duty cycles for view render
    fan_dc = current_dc_settings["fan_dc"]
    light_dc = current_dc_settings["light_dc"]
    # extract frequencies for view render
    fan_freq = current_freq_settings["fan_freq"]
    light_freq = current_freq_settings["light_freq"]

    length = len(log_data)

    # get top 10 statistics
    top_10, original10 = get_last_n(log_data, 10)
    top_20, original20 = get_last_n(log_data, 30)
    top_30, original30 = get_last_n(log_data, 20)
    top_all, original40 = get_last_n(log_data, len(log_data))

    max_all = [max(original40[key]) for key in original40]
    min_all = [min(original40[key]) for key in original40]

    max_min = list(zip(max_all, min_all))
    items_range = list(map(lambda pair: float(round(pair[0] - pair[1], 2)), max_min))

    q25 = quantile_calc(0.25, original40)
    q50 = quantile_calc(0.5, original40)
    q75 = quantile_calc(0.75, original40)

    return render(request, 'Analysis/analysis.html', {'q25': q25, 'q50': q50, 'q75': q75, 'items_range': items_range, 'max_min': max_min, 'top_10': top_10, 'top_20': (top_20), 'top_30': (top_30), 'top_all': (top_all), 'water_actions': water_actions, 'fan_actions': fan_actions, 'heat_actions': heat_actions, 'light_actions': light_actions, 'legend': legend, 'last_temperature': last_temperature, 'last_humidity': last_humidity, 'last_soil_moisture': last_soil_moisture, 'last_sunlight': last_sunlight, 'last_reading_datetime': last_reading_datetime, 'labels': labels, 'temperatures': temperatures, 'humidities': humidities, 'soil_moistures': soil_moistures, 'sunlights': sunlights, 'fan_freq': fan_freq, 'light_freq': light_freq, 'fan_dc': fan_dc, 'light_dc': light_dc, 'length': length})


def quantile_calc(q, _dict):
    return [round(quantile(_dict[key], q), 3) for key in _dict]


def get_last_n(log_data, n):
    top_all = defaultdict(list)
    l = len(log_data)
    start = max(0, l - n)
    for _, record in log_data[start: len(log_data)]:
        top_all['temperature'].append(record['temperature'])
        top_all['humidity'].append(record['humidity'])
        top_all['soil_moisture'].append(record['soil_moisture'])
        top_all['sunlight'].append(record['sunlight'])
        top_all['water_action'].append(record['water_action'])
        top_all['fan_action'].append(record['fan_action'])
        top_all['heat_action'].append(record['heat_action'])
        top_all['light_action'] .append(record['light_action'])
    original = deepcopy(top_all)
    for key in top_all:
        top_all[key] = round(sum(top_all[key])/(n if n != 0 else 1), 3)
        top_all = dict(top_all)
    return top_all, original
