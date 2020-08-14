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
from datetime import datetime, time

import requests
import re

LAT = round(45.516022, 4)  # portland, OR, lat lon
LON = round(-122.681427, 4)

ADDRESS_JSON_PATH = "Interface Files/home_address.json"
DEFAULT_ADDRESS_JSON_PATH = "Interface Files/default_home_address.json"


def request_geographic_location(geo_path, default_geo_path):
    """
    request_geographic_location(geo_path, default_geo_path) finds the current geographic location of the user
    """
    fp = open(geo_path, "r")
    geo_json = json.load(fp)
    fp.close()

    street_address = geo_json["street_address"]
    city = geo_json["city"]
    state = geo_json["state"]
    zip_code = geo_json["zip"]
    CENSUS_PAGE = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={street_address}&city={city}&state={state}&zip={zip_code}&benchmark=Public_AR_Census2010&format=json"

    response = requests.get(CENSUS_PAGE)
    location_json = response.json()

    try:
        coordinates = location_json["result"]["addressMatches"][0]["coordinates"]
        long = coordinates["x"]
        lat = coordinates["y"]
    except:
        fp = open(default_geo_path, "r")
        geo_json = json.load(fp)
        fp.close()

        street_address = geo_json["street_address"]
        city = geo_json["city"]
        state = geo_json["state"]
        zip_code = geo_json["zip"]
        CENSUS_PAGE = f"https://geocoding.geo.census.gov/geocoder/locations/address?street={street_address}&city={city}&state={state}&zip={zip_code}&benchmark=Public_AR_Census2010&format=json"

        response = requests.get(CENSUS_PAGE)
        location_json = response.json()

        coordinates = location_json["result"]["addressMatches"][0]["coordinates"]
        long = coordinates["x"]
        lat = coordinates["y"]

    return (long, lat)


LON, LAT = request_geographic_location(
    ADDRESS_JSON_PATH, DEFAULT_ADDRESS_JSON_PATH)
LON = round(float(LON), 4)
LAT = round(float(LAT), 4)
NWS_PREFIX = f"https://api.weather.gov/points/{LAT},{LON}"

PRECIPITATION_RE = "[0-9][0-9]*%"
HIGH_LOW_RE = "[0-9][0-9]*"


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
    # last_reading = {}
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

    # weather stuff

    forecast_json = request_weather_data(NWS_PREFIX)

    forecast_data = forecast_json["properties"]["periods"]

    # add in precipitation
    for _dict in forecast_data:
        _dict["precipitation"] = get_precipitation(_dict["detailedForecast"])

    # ADD IN HIGHS AND LOWS
    l = len(forecast_data)
    i = 0
    while (i < l):
        highs_dict = forecast_data[i]
        try:
            lows_dict = forecast_data[i + 1]
            high, low = get_high_low(
                highs_dict['detailedForecast'], lows_dict["detailedForecast"])
        except:
            high, low = "NA", "NA"  # random number!!!
            lows_dict = {}

        highs_dict["high"] = high
        highs_dict["low"] = low
        lows_dict["high"] = high
        lows_dict["low"] = low

        i += 2

    weather_format_file = open("Interface Files/temp_format.json")
    weather_format_json = json.load(weather_format_file)
    weather_format_file.close()

    weather_format = weather_format_json["temp"]
    degree_symbol = "F"
    is_fahrenheit = True
    if weather_format == "Celsius":
        is_fahrenheit = False
        degree_symbol = "C"
        for _dict in forecast_data:
            _dict["temperature"] = f_to_c(
                _dict["temperature"])
            _dict["high"] = f_to_c(
                _dict["high"])
            _dict["low"] = f_to_c(
                _dict["low"])

    today_data = forecast_data[0]
    remaining_days_data = forecast_data[1:]  # could be empty I suppose

    today_temp = today_data["temperature"]
    today_windspeed = today_data["windSpeed"]
    today_winddirection = today_data["windDirection"]
    today_sun = today_data["icon"]
    today_short = today_data["shortForecast"]
    today_detailed = today_data["detailedForecast"]
    today_high = today_data["high"]
    today_low = today_data["low"]
    today_precipitation = today_data["precipitation"]
    today_is_day = today_data["isDaytime"]
    today_is_day = str(today_is_day).lower()

    curr_time = datetime.now()
    date_string = curr_time.strftime("%-m/%-d/%Y, %-I:%M %p")
    numeric_weekday = datetime.today().weekday()
    str_weekday = convert_weekday(numeric_weekday)
    date_string = str_weekday + ", " + date_string

    # get city and state
    fp = open(ADDRESS_JSON_PATH, "r")
    geo_json = json.load(fp)
    fp.close()

    city = geo_json["city"]
    state = geo_json["state"]

    # convert to lowercase bool strings for JS
    is_rainy = str(is_raining(today_detailed)).lower()
    is_cloudy = str(is_cloud(today_detailed)).lower()
    is_snowy = str(is_snow(today_detailed)).lower()
    is_stormy = str(is_thunder_lightning(today_detailed)).lower()

    is_high_temp = (int(today_high) > (
        85 if is_fahrenheit else (85 - 32) * 5/9))

    is_morning = (datetime.now().time() > time(
        5) and datetime.now().time() < time(9))

    is_sundown = (datetime.now().time() > time(
        7 + 12, 30) and datetime.now().time() < time(9 + 12, 30))

    is_night = (datetime.now().time() >= time(9 + 12, 30)
                or datetime.now().time() <= time(5))

    temp_mode = "Temperature in " + \
        ("Fahrenheit" if is_fahrenheit else "Celsius")

    return render(request, 'Weather/weather.html', {'temp_mode': temp_mode, 'degree_symbol': degree_symbol, 'is_night': is_night, 'is_sundown': is_sundown, 'is_morning': is_morning, 'is_high_temp': is_high_temp, 'is_stormy': is_stormy, 'is_snowy': is_snowy, 'is_cloudy': is_cloudy, 'is_rainy': is_rainy, 'today_is_day': today_is_day, 'city': city, 'state': state, 'today_low': today_low, 'today_high': today_high, 'remaining_days_data': remaining_days_data, 'date_string': date_string, 'today_precipitation': today_precipitation, 'today_detailed': today_detailed, 'today_short': today_short, 'today_sun': today_sun, 'today_winddirection': today_winddirection, 'today_windspeed': today_windspeed, 'today_temp': today_temp, 'water_actions': water_actions, 'fan_actions': fan_actions, 'heat_actions': heat_actions, 'light_actions': light_actions, 'legend': legend, 'last_temperature': last_temperature, 'last_humidity': last_humidity, 'last_soil_moisture': last_soil_moisture, 'last_sunlight': last_sunlight, 'last_reading_datetime': last_reading_datetime, 'labels': labels, 'temperatures': temperatures, 'humidities': humidities, 'soil_moistures': soil_moistures, 'sunlights': sunlights, 'fan_freq': fan_freq, 'light_freq': light_freq, 'fan_dc': fan_dc, 'light_dc': light_dc})


def f_to_c(string_temp):
    """
    f_to_c converts a fahrenheit degree value to celsius and returns celsius.
                                                                                                                                    Converts the number from string to float and then back to stirng
    If value is not a number, returns the same string
    """
    try:
        f_temp = float(string_temp)
        celsius_temp = (f_temp - 32) * 5/9
        celsius_temp = int(round(celsius_temp, 0))  # return int
        return str(celsius_temp)
    except:
        return string_temp


def convert_weekday(numeric_weekday):
    """
    convert_weekday(numeric_weekday) converts a 0 to 6 inclusive integer to a weekday
    where 0 is Monday and 6 is Sunday
    """
    if numeric_weekday == 0:
        return "Monday"
    elif numeric_weekday == 1:
        return "Tuesday"
    elif numeric_weekday == 2:
        return "Wednesday"
    elif numeric_weekday == 3:
        return "Thursday"
    elif numeric_weekday == 4:
        return "Friday"
    elif numeric_weekday == 5:
        return "Saturday"
    elif numeric_weekday == 6:
        return "Sunday"
    assert (0 == 1)  # raise error, not a valid weekday


def get_precipitation(detailed_forecast_str):
    """
    get_precipitation(detailed_forecast_str) gets any precipiation chance listed if any
    """
    split_list = detailed_forecast_str.split(".")
    for sentence in split_list:
        if "precipitation" in sentence:
            numeral = re.search(PRECIPITATION_RE, sentence)
            if numeral == None:
                return "0%"
            else:
                return str(numeral.group(0))
    return "0%"


def get_high_low(detailed_forecast_str1, detailed_forecast_str2):
    """
    get_high_low() gets highs and lows
    """
    highs_list1 = detailed_forecast_str1.split(".")
    lows_list2 = detailed_forecast_str2.split(".")

    for sentence in highs_list1:
        if "high" in sentence:
            numeral = re.search(HIGH_LOW_RE, sentence)
            if numeral == None:
                high = "NA"

            else:
                high = str(numeral.group(0))
                break
        else:
            high = "NA"

    for sentence in lows_list2:
        if "low" in sentence:
            numeral = re.search(HIGH_LOW_RE, sentence)
            if numeral == None:
                low = "NA"
            else:
                low = str(numeral.group(0))
                break
        else:
            low = "NA"

    if high == "NA" or low == "NA":
        for sentence in lows_list2:
            if "high" in sentence:
                numeral = re.search(HIGH_LOW_RE, sentence)
                if numeral == None:
                    high = "NA"
                else:
                    high = str(numeral.group(0))
                    break
            else:
                high = "NA"

        for sentence in highs_list1:
            if "low" in sentence:
                numeral = re.search(HIGH_LOW_RE, sentence)
                if numeral == None:
                    low = "NA"

                else:
                    low = str(numeral.group(0))
                    break
            else:
                low = "NA"

    return (high, low)


def request_weather_data(weather_site=NWS_PREFIX):
    """
        request_weather_data(weather_site = NWS_PREFIX) pulls a forecast json from the NWS
        website and returns the  json

        SPEICIFIC TO NWS API ONLY
        """
    response = requests.get(weather_site)
    nws_json = response.json()
    nws_forecast_url = nws_json["properties"]["forecast"]
    forecast_response = requests.get(nws_forecast_url)
    forecast_json = forecast_response.json()
    return forecast_json


def is_raining(weather_text):
    """
    is_raining(weather_text) is True iff showers" or "rain" or "drizzle" is in
    weathertext else False
    """
    rainy_words = ["showers", "rain", "drizzle"]
    weather_text = weather_text.lower()
    for word in rainy_words:
        if word in weather_text:
            return True
    return False


def is_thunder_lightning(weather_text):
    """
    is_thunder_lightning(weather_text) is True iff "thunder"" or "lightning" or "storm" is
                                                                                                                                                                                                                                                                    in weather_text else False
    """
    thunder_words = ["thunder", "lightning", "storm"]
    weather_text = weather_text.lower()
    for word in thunder_words:
        if word in weather_text:
            return True
    return False


def is_snow(weather_text):
    """
    is_snow(weather_text) is True iff "snow"" or "blizzard" or "ice" is
                                                                                                                                                                                                                                                                    in weather_text else False
    """
    snow_words = ["snow", "blizzard", "ice"]
    weather_text = weather_text.lower()
    for word in snow_words:
        if word in weather_text:
            return True
    return False


def is_cloud(weather_text):
    """
                                                                                                                                                                                                                                                                    is_cloud(weather_text) is True iff "cloud"" or "cover" or "fog" is
                                                                                                                                                                                                                                                                    in weather_text else False
                                                                                                                                                                                                                                                                    """
    cloud_words = ["cloud", "cover", "fog"]
    weather_text = weather_text.lower()
    for word in cloud_words:
        if word in weather_text:
            return True
    return False
