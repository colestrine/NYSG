# NYSG

## Overview
The purpose of this user interface (UI) is to provide functionality for remote user interaction with the Smart Greenhouse system. The UI will consist of five pages: Dashboard, Analysis, Germination, Settings, and Information. The UI will allow the user to select healthy levels for temperature, humidity, soil moisture, and sunlight (collectively referred to as "healthy levels"), set the operational mode for the system, and view visualizations related to the system status.

## Usage

## Dashboard Page
The Dashboard page receives bucket numbers and labels for the current healthy levels stored in healthy_levels.json, as well as the sensor data for the updates contained in log.json.
### Current Levels
The Current Levels plot compares the current healthy level buckets to sensor readings in the last system update. The value buckets are represented as light green horizontal ranges, and the current readings are reperesented as dark green vertical lines. When the system is performing optimally, the dark green lines should be in the center of the horizontal ranges, indicating that each environment variable is reading at the middle of its healthy value bucket. Functionally, this is acheived by loading the page with all ranges and values set to 0 (all horizontal ranges and vertical lines set to the left-most position). Then, a custom JavaScript script in templates/Dashboard/dashboard.html uses the context data listed above to reposition the ranges and lines to their appropriate spots by overwriting the "margin-left" CSS paramter.
### Historical Levels
The Historical Levels Plot utilizes the log data to compare sensor readings over time. These values are extracted in JavaScript and displayed as a simple line plot using the chart.js plugin which is automatially loaded on each page load. Each environment variable is plotted as a separate line on a value vs. time plot.

## Analysis Page
The Analysis page receives historical performance data from log.json. It displays one large plot containing two data series: sensor data and action data. Sensor data is represented by the green line datapoints. Action data is represented by the blue bar datapoints. All backend data fetching is performed in scripts/data_handler.py, and all frontend processing and display is performed in a JS script in analysis.html. The plot itself is created using the Chart.js plugin, configured in the JS script mentioned above.

## Germination Page
The Germination page receives information from germination.json. It displays a pie chart of the total time elapsed since planting vs. total time until germination. Backend data fetching is performed by scripts/data_handler.py, and all frontend code is contained in templates/Analysis/germination.html.

## Settings Page
The Settings page receives a dictionary of healthy levels, a plant profile string, the healthy levels form, and the plant profile form. The healthy levels dictionary is the return of data_handler.read_healthy_levels(), which contains the healthy levels data from healthy_levels.json. The plant profile string is the return of data_handler.read_plant_profile(), which contains the name of the current plant profile stored in plant_profile.json. All backend data fetching is performed by scripts/data_handler.py. Frontend code is distributed between the Settings directory and templates/Settings/settings.html.
### Modes
#### Machine Learning 
##### Healthy Levels
The healthy levels form is a HealthyLevelsForm object, with the 'initial' parameter set to be equal to the healthy levels dictionary. This will provide a form with drop down selectors for temperature, humidity, soil moisture, and sunlight. The options for each parameter will be set to the labels for each bucket stored in value_bucket.json, with the initially-selected value equal to the label of the bucket identified in the healthy levels dictionary for each parameter.
##### Plant Profile
The plant profile form is a PlantProfileForm object, with the 'initial' paramter set to be equal to the plant profile string. This will provide a form with a single drop down selector for the plant profile. The options will be populated with all profile names contained in healthy_levels_by_profile.json, with the inital selection set to the current profile stored in plant_profile.json.

The page will display both forms, stacked on top of each other in paragraph display (the plant profile form will be on top). Both forms will be configured to submit upon the change of any of their respective inputs - functionally, when any input is changed, the form which that input belongs to will automatically submit. The healthy levels form will update the healthy_levels.json file, and the plant profile form will update the plant_profile.json file (each file will only be updated when its associated form was submitted). 

## Information Page
The Information page receives information from ui_plant_scrape.json. The data is fetched in scripts/data_handler.py and displayed using JS in templates/Information/information.html. All other supporting code is inside of the Information directory. This page is intended to be used as a reference when users are creating new plant profiles.

## Sidebar

## Starting The UI
### Accessing The UI From Your Laptop
- Open a command window and navigate to /UI/greenhouse
- Type the command: python manage.py runserver
- In a web browser, navigate to the web address provided

### Accessing The UI From Your Phone
- Open a command window and navigate to /UI/greenhouse
- Type the command: ipconfig (Windows)/ifconfig (Mac/Linux), and note your LAN IP address
- Type the command: python manage.py runserver [your ip adddress]:8080
- In a web browser, navigate to the web address provided