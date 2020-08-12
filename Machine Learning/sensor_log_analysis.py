import json
from statistics import stdev, mean as avg
from matplotlib import pyplot as plt

with open('../Interface Files/sensor_log.json', 'r') as file:
	contents = file.read()
	log = json.loads(contents)

temperatures = []
humidities = []
soil_moistures = []
sunlights = []
records = []

for record in log:
	temperature = log[record]['temperature']
	humidity = log[record]['humidity']
	soil_moisture = log[record]['soil_moisture']
	sunlight = log[record]['sunlight']

	temperatures.append(temperature)
	humidities.append(humidity)
	soil_moistures.append(soil_moisture)
	sunlights.append(sunlight)
	records.append(record)

avg_temperature = avg(temperatures)
avg_humidity = avg(humidities)
avg_soil_moisture = avg(soil_moistures)
avg_sunlight = avg(sunlights)

stdev_temperature = stdev(temperatures)
stdev_humidity = stdev(humidities)
stdev_soil_moisture = stdev(soil_moistures)
stdev_sunlight = stdev(sunlights)

max_temperature = max(temperatures)
max_humidity = max(humidities)
max_soil_moisture = max(soil_moistures)
max_sunlight = max(sunlights)

min_temperature = min(temperatures)
min_humidity = min(humidities)
min_soil_moisture = min(soil_moistures)
min_sunlight = min(sunlights)

print(f'AVERAGE TEMPERATURE: {avg_temperature}')
print(f'STANDARD DEVIATION TEMPERATURE: {stdev_temperature}')
print(f'MAX TEMPERATURE: {max_temperature}')
print(f'MIN TEMPERATURE: {min_temperature}\n')

print(f'AVERAGE HUMIDITY: {avg_humidity}')
print(f'STANDARD DEVIATION HUMDIITY: {stdev_humidity}')
print(f'MAX HUMIDITY: {max_humidity}')
print(f'MIN HUMIDITY: {min_humidity}\n')

print(f'AVERAGE SOIL MOISTURE: {avg_soil_moisture}')
print(f'STANDARD DEVIATION SOIL MOISTURE: {stdev_soil_moisture}')
print(f'MAX SOIL MOISTURE: {max_soil_moisture}')
print(f'MIN SOIL MOISTURE: {min_soil_moisture}\n')

print(f'AVERAGE LIGHT: {avg_sunlight}')
print(f'STANDARD DEVIATION LIGHT: {stdev_sunlight}')
print(f'MAX LIGHT: {max_sunlight}')
print(f'MIN LIGHT: {min_sunlight}\n')

x = range(0, len(records))

plt.subplot(221)
plt.plot(x, temperatures)
plt.title('TEMPERATURE')

plt.subplot(222)
plt.plot(x, humidities)
plt.title('HUMIDITY')

plt.subplot(223)
plt.plot(x, soil_moistures)
plt.title('SOIL MOISTURE')

plt.subplot(224)
plt.plot(x, sunlights)
plt.title('LIGHT')

plt.show()