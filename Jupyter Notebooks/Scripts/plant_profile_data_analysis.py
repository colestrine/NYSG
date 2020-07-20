import json
from matplotlib import pyplot
from statistics import mean

with open('plant_profile_data.json', 'r') as file:
    data_in = file.read()

data = json.loads(data_in)

temperatures = []
humidities = []
soil_moistures = []
sunlights = []
germ_times = []
for record in data:
    temperatures.append(data[record]['temperature'])
    humidities.append(data[record]['humidity'])
    soil_moistures.append(int(data[record]['soil_moisture']))
    sunlights.append(int(data[record]['sunlight']))
    germ_times.append(data[record]['germ_time'])

length = len(data)

temperature_lows = []
temperature_highs = []
temperature_widths = []
temperature_averages = []
for temperature in temperatures:
	strings = temperature.split('_')
	low = int(strings[0])
	high = int(strings[1])
	width = high - low
	average = (high + low)/2

	temperature_lows.append(low)
	temperature_highs.append(high)
	temperature_widths.append(width)
	temperature_averages.append(average)

humidity_lows = []
humidity_highs = []
humidity_widths = []
humidity_averages = []
for humidity in humidities:
	strings = humidity.split('_')
	low = int(strings[0])
	high = int(strings[1])
	width = high - low
	average = (high + low)/2

	humidity_lows.append(low)
	humidity_highs.append(high)
	humidity_widths.append(width)
	humidity_averages.append(average)

germ_time_lows = []
germ_time_highs = []
germ_time_widths = []
germ_time_averages = []
for germ_time in germ_times:
	strings = germ_time.split('_')
	low = int(strings[0])
	high = int(strings[1])
	width = high - low
	average = (high + low)/2

	germ_time_lows.append(low)
	germ_time_highs.append(high)
	germ_time_widths.append(width)
	germ_time_averages.append(average)

print(f'Number of Profiles: {length}')

print("Temperature Data:")
print(f"\tAbsolute Min: {min(temperature_lows)}")
print(f"\tAbsolute Max: {max(temperature_highs)}")
print(f"\tAverage Min: {mean(temperature_lows)}")
print(f"\tAverage Max: {mean(temperature_highs)}")
print(f"\tAverage Width: {mean(temperature_widths)}")
print(f"\tAverage Mean: {mean(temperature_averages)}")

print("Humidity Data:")
print(f"\tAbsolute Min: {min(humidity_lows)}")
print(f"\tAbsolute Max: {max(humidity_highs)}")
print(f"\tAverage Min: {mean(humidity_lows)}")
print(f"\tAverage Max: {mean(humidity_highs)}")
print(f"\tAverage Width: {mean(humidity_widths)}")
print(f"\tAverage Mean: {mean(humidity_averages)}")

print("Soil Moisture Data:")
print(f"\tAverage: {mean(soil_moistures)}")

print("Sunlight Data:")
print(f"\tAverage: {mean(sunlights)}")

print("Germination Time Data:")
print(f"\tAbsolute Min: {min(germ_time_lows)}")
print(f"\tAbsolute Max: {max(germ_time_highs)}")
print(f"\tAverage Min: {mean(germ_time_lows)}")
print(f"\tAverage Max: {mean(germ_time_highs)}")
print(f"\tAverage Width: {mean(germ_time_widths)}")
print(f"\tAverage Mean: {mean(germ_time_averages)}")

pyplot.figure(1)

pyplot.subplot(2,2,1)
pyplot.plot(range(length), temperatures, label="Temperature")
pyplot.title('Temperature')

pyplot.subplot(2,2,2)
pyplot.plot(range(length), humidities, label="Humiditiy")
pyplot.title('Humidity')

pyplot.subplot(2,2,3)
pyplot.plot(range(length), soil_moistures, label="Soil Moisture")
pyplot.title('Soil Moisture')

pyplot.subplot(2,2,4)
pyplot.plot(range(length), sunlights, label="Sunlight")
pyplot.title('Sunlight')

pyplot.show()

# pyplot.figure(2)
# pyplot.plot(range(length), germ_times, label="Germination Time")
