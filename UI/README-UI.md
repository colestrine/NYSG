# NYSG

## Overview
The purpose of this user interface (UI) is to provide functionality for remote user interaction with the Smart Greenhouse system. The UI will consist of five pages: Dashboard, Analysis, Germination, Settings, and Information. The UI will allow the user to select healthy levels for temperature, humidity, soil moisture, and sunlight (collectively referred to as "healthy levels"), set the operational mode for the system, and view visualizations related to the system status.

## Usage

## Dashboard Page
The Dashboard page receives bucket numbers and labels for the current healthy levels stored in healthy_levels.json, as well as the sensor data for the updates contained in log.json.
### Current Levels
The Current Levels plot compares the current healthy level buckets to sensor readings in the last system update. In Machine Learning mode (see below), the value buckets for temperature, humidity, and soil moisture are represented as light green horizontal ranges, and the current readings are reperesented as dark green vertical lines. When the system is performing optimally, the dark green lines should be in the center of the horizontal ranges, indicating that each environment variable is reading at the middle of its healthy value bucket. Functionally, this is acheived by loading the page with all ranges and values set to 0 (all horizontal ranges and vertical lines set to the left-most position). Note that the LED light is not controlled via tha ML algorithm, so there is no value bucket range for that parameter.
### Historical Levels
The Historical Levels Plot utilizes the log data to compare sensor readings over time. These values are extracted in JavaScript and displayed as a simple line plot using the chart.js plugin which is automatially loaded on each page load. Each environment variable is plotted as a separate line on a value vs. time plot.

## Analysis Page
The Analysis page receives historical performance data from log.json. It displays one large plot containing two data series: sensor data and action data. Sensor data is represented by the green line datapoints. Action data is represented by the blue bar datapoints. All backend data fetching is performed in scripts/data_handler.py, and all frontend processing and display is performed in a JS script in analysis.html. The plot itself is created using the Chart.js plugin, configured in the JS script mentioned above.

## Germination Page
The Germination page receives information from germination.json. It displays a pie chart of the total time elapsed since planting vs. total time until germination. Backend data fetching is performed by scripts/data_handler.py, and all frontend code is contained in templates/Analysis/germination.html.

## Settings Page
The Settings page receives a dictionary of healthy levels, a plant profile string, the healthy levels form, and the plant profile form. The healthy levels dictionary is the return of data_handler.read_healthy_levels(), which contains the healthy levels data from healthy_levels.json. The plant profile string is the return of data_handler.read_plant_profile(), which contains the name of the current plant profile stored in plant_profile.json. All backend data fetching is performed by scripts/data_handler.py. Frontend code is distributed between the Settings directory and templates/Settings/settings.html. All backend data is stored in the Interface Files directory.
### Modes
#### Machine Learning 
In Machine Learning mode, the user can specify healthy levels for a plant. In Machine Learning mode, the machine learning algorithm (Machine Learning/reinforcement-learning_static.py) will be used by the controller (controller_main.py) to choose actions to automatically approach those levels. Note that the algorithm needs time to learn its environment, so you may need to leave the system running for a few hours before the algorithm performs with relative accuracy.
##### Plant Profile
The Plant Profile form allows the user to choose a profile with an associated set of healthy levels. Some profiles are pre-loaded with the system, but by creating a new set of levels using the Healthy Levels form, the user can create a new profile. Creating a new profile will create a new profile instance in the system and will be available for future use. All profiles are stored in Interface Files/healthy_levels_by_profile.json.
##### Healthy Levels
The Healthy Levels form allows the user to view the healthy levels associated with a profile, as well as create new combinations of levels. When a new combination is created, the "Save as New Profile" button will appear. Clicking this will allow the user to create a new profile with the designated healthy levels. Expanding the Sidebar (see below) will allow the user to view the real-world values associated with each healthy level's available values. The user may reference the Information page (see below) for more information on what levels might be associated with a certain type of plant.
#### Manual
In Manual mode, the user can specify actions which the system will take. This mode will not utilize the machine learning algorithm, and will instead take actions based only on these settings.
### Advanced Settings
The Advanced Settings section can be expanded by clicking the arrow button to the right of the header. This section contains settings which affect the system's lower-level operation. Note that adjusting any performance-related settings will alter the applicability of the Machine Learning algorithm's prior learning, and may result in a period where the algorithm needs to re-learn its environment based on new parameters.

## Information Page
The Information page receives information from ui_plant_scrape.json. The data is fetched in scripts/data_handler.py and displayed using JS in templates/Information/information.html. All other supporting code is inside of the Information directory. This page is intended to be used as a reference when users are creating new plant profiles.

## Sidebar
The Sidebar element provides the user with a readout of the real-world values for the last sensor update. It also includes a section that displays the mapping between value buckets and the real-world values. All data is fetched via scripts/data_handler.py from Interface Files/log.json and Interface Files/value_buckets.json.

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