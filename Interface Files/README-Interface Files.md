# NYSG

## Interface Files
Interface files serve as the exchange and storage medium for information between software subsystems. In this project, we chose to make use of the JSON format (as opposed to .txt or databases) for simplicity and ease of use for the end-users (high school students). THese files are also meant to provide configurability to the user. Changes to the information in these files will propagate throughout the entire software system.

### Healthy Levels (healthy_levels.json)
This file stores healthy levels as specified by the user in the Settings page of the UI. Each level is represented by a bucket number corresponding to bucket in value_buckets.json. These levels serve as goals onto which the machine learning algorithm will seek to optimize.

### Healthy Levels By Profile (healthy_levels_by_profile.json)
This file maps profiles to sets of healthy levels. These profiles will appear in the drop down menu on the Settings page of the UI as pre-configured plant profiles.

### Log (log.json)
This file holds information pertaining to the updates of the system. It contains one record for each update, labeled with the datetime of that update. Inside of these records, information on the sensor readings is stored, as well as the actions that were taken during that update. All values are presented on a scale from 0-5.9.

### Manual Actions (manual_actions.json)
This file contains the last-submitted set of manual actions. When the system is in "Manual" mode (as set in the Settings page of the UI), the system will take these actions on each update.

### Mode (mode.json)
This file contains the mode that the system is currently in.

### Plant Profile (plant_profile.json)
This file contains the current plant profile (as set in the Settings page of the UI). The profile maps to one of the profiles in healthy_levels_by_profile.json.

### Value Buckets (value_buckets.json)
This file maps buckets to nominal values. Buckets are used to interpret data throughout the system. For each environment variable (temperature, humidity, soil moisture, sunlight) there are 5 buckets. Each bucket is associated with a label, and low value, and a high value. The label is used in the UI to associate the bucket with relatively familiar concepts (cold/warn/hot), the low value is the floor of nominal values that would be associated with that bucket, and the high value is the ceiling of nominal values that would be associated with that bucket.