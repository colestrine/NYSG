# NYSG

## Overview
The purpose of this user interface (UI) is to provide functionality for remote user interaction with the Smart Greenhouse system. The UI will consist of two pages: Settings and Dashboard, which will allow the user to select healthy levels for temperature, humidity, soil moisture, and sunlight (collectively referred to as "healthy levels"), and view visualizations related to current and historical performance of the system, respectively. In the Settings page, the user will be able to choose from any number of plant profiles with pre-defined healthy levels, or create their own custom set of healthy levels. These levels will be used by the ML algorithm as a goal state which the system will attempt to optimize towards. In the Dashboard page, the user will be presented with two visualizations: Current Levels and Historical Levels. The Current Levels visualization will compare the current healthy levels with the last update of the sensor readings. The Historical Levels visualization will display the sensor readings over time.

## Settings Page
On load, the Settings page receives a dictionary of healthy levels, a plant profile string, the healthy levels form, and the plant profile form. The healthy levels dictionary is the return of data_handler.read_healthy_levels(), which contains the healthy levels data from healthy_levels.json. The plant profile string is the return of data_handler.read_plant_profile(), which contains the name of the current plant profile stored in plant_profile.json. The healthy levels form is a HealthyLevelsForm object, with the 'initial' parameter set to be equal to the healthy levels dictionary. This will provide a form with drop down selectors for temperature, humidity, soil moisture, and sunlight. The options for each parameter will be set to the labels for each bucket stored in value_bucket.json, with the initially-selected value equal to the label of the bucket identified in the healthy levels dictionary for each parameter. The plant profile form is a PlantProfileForm object, with the 'initial' paramter set to be equal to the plant profile string. This will provide a form with a single drop down selector for the plant profile. The options will be populated with all profile names contained in healthy_levels_by_profile.json, with the inital selection set to the current profile stored in plant_profile.json.

The page will display both forms, stacked on top of each other in paragraph display (the plant profile form will be on top). Both forms will be configured to submit upon the change of any of their respective inputs - functionally, when any input is changed, the form which that input belongs to will automatically submit. The healthy levels form will update the healthy_levels.json file, and the plant profile form will update the plant_profile.json file (each file will only be updated when its associated form was submitted). 

## Dashboard Page


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