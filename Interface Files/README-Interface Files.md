# NYSG

## Interface Files
Interface files serve as the exchange and storage medium for information between software subsystems. In this project, we chose to make use of the JSON format (as opposed to .txt or databases) for simplicity and ease of use for the end-users (high school students). THese files are also meant to provide configurability to the user. Changes to the information in these files will propagate throughout the entire software system.

The files are read from in both the controller_main.py and also in the settings page, analysis page and dashboard pages of the UI. The settings page also writes back data to the interface files, so that data can be updated. This shows how the data can persist and be updated and changed. Essentally, the interface files are a memory medium, rather like RAM or a database, excepy we structure it by JSON for simplicity in this small scale project.

### Healthy Levels (healthy_levels.json)
This file stores healthy levels as specified by the user in the Settings page of the UI. Each level is represented by a bucket number corresponding to bucket in value_buckets.json. These levels serve as goals onto which the machine learning algorithm will seek to optimize.

### Healthy Levels By Profile (healthy_levels_by_profile.json)
This file maps profiles to sets of healthy levels. These profiles will appear in the drop down menu on the Settings page of the UI as pre-configured plant profiles.

### Healthy Levels By Profile SAMPLE (healthy_levels_by_profile_SAMPLE.json)
This file maps profiles to sets of healthy levels. These profiles will appear in the drop down menu on the Settings page of the UI as pre-configured plant profiles. **THIS IS A SAMPLE FILE** that allows the user to have a basic idea of what they will see in the user interface and is not meant to be used except as a sample or default method.

### Log (log.json)
This file holds information pertaining to the updates of the system. It contains one record for each update, labeled with the datetime of that update. Inside of these records, information on the sensor readings is stored, as well as the actions that were taken during that update. All values are presented on a scale from 0-5.9. There are different keys: sunlight, temperature, humidity, soil_moisture, water_action, heat_action, fan_action and light_action.

### Backup Log (log_backup1.json)
This file holds information pertaining to the updates of the system. It contains one record for each update, labeled with the datetime of that update. Inside of these records, information on the sensor readings is stored, as well as the actions that were taken during that update. All values are presented on a scale from 0-5.9. There are different keys: sunlight, temperature, humidity, soil_moisture, water_action, heat_action, fan_action and light_action.

**THis file is a backup file** which means when the user clears all data on the advanced settings page, all data is deleted in log.json and exported to log_backup1.json. In the case you clear data agin from log, log_backup1 is permanently cleared forever!

### Sample Log (log_SAMPLE.json)
This file holds information pertaining to the updates of the system. It contains one record for each update, labeled with the datetime of that update. Inside of these records, information on the sensor readings is stored, as well as the actions that were taken during that update. All values are presented on a scale from 0-5.9. There are different keys: sunlight, temperature, humidity, soil_moisture, water_action, heat_action, fan_action and light_action.

**This file is a sample file**. It is mean t as a sample for the UI for the user to visualize how data would show up and be seen. It is not meant for production use. 

### Manual Actions (manual_actions.json)
This file contains the last-submitted set of manual actions. When the system is in "Manual" mode (as set in the Settings page of the UI), the system will take these actions on each update. These actions are set in the user interface file directly and are reflected in the JSON files. 

Actions can be low, high and off, and it is for the water, fan, heater and light
peripherals. 

### Mode (mode.json)
This file contains the mode that the system is currently in. The mode is either manual or machine learning. it is read in in the controller_main to decide what happens in the update cycle; either the UI manual actions are taken or the ML actions for that cycle are called and taken. The mode is itself written tok by the user in the advanced settings tab of the UI. 

### Plant Profile (plant_profile.json)
This file contains the current plant profile (as set in the Settings page of the UI). The profile maps to one of the profiles in healthy_levels_by_profile.json. The profile could be custom, or someother preloaded one like "tomatoes" that the user could not change. 

### Value Buckets (value_buckets.json)
This file maps buckets to nominal values. Buckets are used to interpret data throughout the system. For each environment variable (temperature, humidity, soil moisture, sunlight) there are 5 buckets. Each bucket is associated with a label, and low value, and a high value. The label is used in the UI to associate the bucket with relatively familiar concepts (cold/warn/hot), the low value is the floor of nominal values that would be associated with that bucket, and the high value is the ceiling of nominal values that would be associated with that bucket.

### ML Training (actions.json)
This file contains all training operations that the ML can tsake over 64 time
steps to check what the ML does and to train it properly. For each time step,
there is a decision listed for the water, fan and heater, in terms of high, and
low and off status. There are 64 time steps specified in total. 

### Alert (alert_log.json)
This file contains all the alerts that the system alerts by time to the water
level that is recorded. 

### Default Home Address (defaul_home_address.json)
This file contains the defaul home address in Suitville Maryland for the
National Weather Service Address reading. This file __MUST NEVER BE CHANGED__
because it is a default setting to display should the user give a faulty or incorrectly entered home address.

### Email Settings (email_settings.json)
This file contains the user email settings that is in terms of rate
of email sending and the detail of the email. This file is changed by the advanced settings of the user page in the UI settings. You can set minutely, hourly and daily updates of emails and high and low settings of detail where high is all information and extreme data while low just shows extreme data. The user changes these settings in the advanced settings.

### Frequency (freq_settings.json)
This file contains the user frequency settings for the pwm frequency settings for
the fan and the plant light. The keys are fan and light and the inner keys is frequency. The user changes the frequency individually for light and fan on the UI advanced settings page. The frequency can be cahanged in units of 10 from 0 to 500
hertz. 

### Germination (germination.json)
This file contains the germination start and end date with day, month and year. It holds start and end dates. The start **can** be equal to the end date and but it can **never** be after the end date. Note that the UI disallows the satrt being after the end. Also note that the start can be in the future and the end in the future. The start date could also be in the past. Both start and end are specified in the UI advanced settings where the user manually sets six fields of day, month and year for the start and end dates.

### Home Address (home_address.json)
This file holds the home address for the user including street address, city, state and zip code. It must be a valid american street address. It could be an invalid address becaudse the UI does nto check for invalidity. It is iset in the UI settings advanced settings tab and the user types in street address and city and zip code and state is chosen in a drop down. This influences what weather forecast is received by the user in the weather page. The user should set a local address for local weather forecasts.

### Constants (interface_constants.py)
This contains constants used for the interface files like log path, germination path and other paths. 

### Update Interval (interval_settings.json)
This file contains the update interval in **seconds**. It could be any value in 60, 180 and 300 seconds. This file can be changed in the User interface advanced settings tab. This file interacts with the controller and tells the controller how long to await for the next update cycle in an await sleep call. 

### ML Log (ml_action_log.json)
This file contains the actions of the ML taken in the last cycle including keys of water, fan heat, light and expected reward. It is logged from controller_main and it cannot be changed or deleted from the UI. 

### Duty Cycles (pwm_settings.json)
This file contains the user duty cycle settings for the pwm duty cycle settings for
the fan and the plant light. The keys are fan and light and the inner keys is duty_cycle. The user changes the duty cycle individually for light and fan on the UI advanced settings page. The duty cycle can be cahanged in units of 10 from 0 to 100
% duty cycles. 

### Sensor Log (sensor_log.json)
This file contains the sensor measurements of the controller taken in the all cycles including keys of sunlight, soil_moisture, temperature and humdiity with the primary key of a datetime string. It is logged from controller_main and it cannot be changed or deleted from the UI. Sunlight units are unscaled from 0 to 120000 lumens / square meter, temperature is between 0 and 100 degrees F, humidity is between 0 and 100% RH and soil_moisture is inverted and then scaled between 0 and 100 in this log. These are essentially exact readings and not converted to value buckets for the ML!

### Temperature Settings (temp_format.json)
This file contains the temperature scale in **Fahrenheit or Celsius**. It could be any value in fahreneheit or celsius. This file can be changed in the User interface advanced settings tab. Currently, this file only changes what the temperature in the weather page in the UI is displayed as. 

### Utilities (utilities.py)
This contains utilities to translate actions to numbers: e.g. off is 0, low is 2 and high is 4. These functions are called in the controlelr_main to convert for units for the peripheral changes which only takes in values from 0 to 4. 