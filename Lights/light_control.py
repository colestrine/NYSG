# Code to control the lights for the NYSG

from datetime import datetime,date,time,timedelta
import json
import os
from os.path import expanduser
from time import sleep
import random

class plant_light:
    def __init__(self, dark_hours, directsun_hours, indirectsun_hours):
        self.dark = timedelta(hours=dark_hours)
        self.direct= timedelta(hours=directsun_hours)
        self.indirect = timedelta(hours=indirectsun_hours)

def startdict(): # Create log to be used in the later functions at reset point
    d = {"DATE" : datetime.now(), "DARK" : timedelta() , "DIRECT" : timedelta(), "INDIRECT" : timedelta(), "ACTION" : 0, "LUX" : 0}
    #d["DATE"] = d["DATE"] - timedelta(days = 1)
    print("ld=")
    print(d)
    return d

def addtime(time, other):   # Add a time object to other datetime object
    x = datetime.combine(date.today(), time) + other
    return x

def addtimetime(time1,time2): # add two time objects
    x = datetime.combine(date.today(), time1) + datetime.combine(date.today(), time2)
    return x

def subtime(time1, time2): # subtract a time object
    ty1 = type(time1)
    ty2 = type(time2)
    if ty1 is time and ty2 is time:
        x = datetime.combine(date.today(), time1) - datetime.combine(date.today(), time2)
    elif ty1 is time:
        x = datetime.combine(date.today(), time1) - time2
    elif ty1 is timedelta:
        x = time1 - (datetime.combine(date.today(),time2) - datetime.combine(date.today(),time.min))
    else:
        x = time1 - datetime.combine(date.today(), time2)
    return x


def light(today_light,lux, plant_type): 

# FUNCTION TO BE CALLED BE MAIN LOOP
#PASS IN THE TIMESTEP BETWEEN CALLING IT IN MINUTES
#RETURNS 1 IF LIGHTS SHOULD BE ON, 0 IF OFF

    # DEFINE SOME VARIABLES AND BASIC INFO, READ FROM LOG
    DATETODAY = datetime.now()
    REFRESH = DATETODAY - today_light["DATE"]
    GROWSTART = time(6, 30)
    GROWSTOP = time(21,30)
    today_light["LUX"] = lux

    # TODAY's DATA


    if today_light["DATE"].date() != DATETODAY.date():
        print("New day")
        today_light = {"DATE" : DATETODAY, "DARK" : timedelta() , "DIRECT" : timedelta(), "INDIRECT" : timedelta(), "ACTION" : 0}
        healthy_levels_dict = read_healthy_levels()
        write_healthy_levels(healthy_levels_dict)
    else:
        print("Same day")
        today_light["DATE"] = DATETODAY


    #lux = random.randint(2000, 60000)

    if lux > 40000 or today_light["ACTION"]:
        today_light["DIRECT"] += REFRESH 
    elif lux > 800:
        today_light["INDIRECT"] += REFRESH
    else:
        today_light["DARK"] +=  REFRESH
    print(today_light)

    #DECISION MAKING ALGORITHM

    time_to_grow = subtime(GROWSTART, DATETODAY)
    time_to_sleep = subtime(GROWSTOP, DATETODAY)

    if time_to_grow > timedelta() or time_to_sleep <= timedelta():
        today_light["ACTION"] = 0
        return today_light
    else:

        if plant_type == "Full sun":
            lightcontrol =  plant_light(9,12,3)
        elif plant_type == "Part sun":
            lightcontrol = plant_light(9,8,7)
        elif plant_type == "Part shade":
            lightcontrol = plant_light(9,6,9)
        elif plant_type == "Full shade":
            lightcontrol = plant_light(9,4,11)
        
        direct_needed = lightcontrol.direct - today_light["DIRECT"]

        if lux < 45000 and direct_needed>=time_to_sleep:
            today_light["ACTION"] = 4
        else:
            today_light["ACTION"] = 0
        return today_light
    
    
def dynamic_soil_control(healthy_levels_dict):
    #print(healthy_levels_dict)
    if healthy_levels_dict["run"] == "0":
        healthy_levels_dict["soil_moisture"] = healthy_levels_dict["soil_moisture_static"]
        print(healthy_levels_dict)
        return healthy_levels_dict

    last_water_file = open(expanduser("~")+'/NYSG/Interface Files/dynamic_soil.json', 'r')
    last_json = last_water_file.read()
    last_water_file.close()
    last_dict = json.loads(last_json)

    print(last_dict)
    days = int(healthy_levels_dict["days"])
    today = date.today()
    t = last_dict["last"]
    t = date.fromisoformat(t)
    time_since_water = today -  t
    if time_since_water >= timedelta(days = days) or time_since_water == timedelta(days = 0) :
        healthy_levels_dict["soil_moisture"] = healthy_levels_dict["soil_moisture_wet"]
        today = today.isoformat()
        last_dict["last"] = today
        last_json = json.dumps(last_dict)
        last_water_file = open(expanduser("~")+'/NYSG/Interface Files/dynamic_soil.json', 'w')
        last_water_file.write(last_json)
        last_water_file.close()
    else:
        healthy_levels_dict["soil_moisture"] = healthy_levels_dict["soil_moisture_dry"]
    print(healthy_levels_dict)
    return healthy_levels_dict

def write_healthy_levels(levels_dict):
    levels_dict = dynamic_soil_control(levels_dict)
    levels_json = json.dumps(levels_dict)
    healthy_levels_file = open(expanduser(
        "~")+'/NYSG/Interface Files/healthy_levels.json', 'w')
    healthy_levels_file.write(levels_json)
    healthy_levels_file.close()

def read_healthy_levels():
    healthy_levels_file = open(expanduser(
        "~")+'/NYSG/Interface Files/healthy_levels.json', 'r')
    levels_json = healthy_levels_file.read()
    healthy_levels_file.close()
    levels_dict = json.loads(levels_json)
    return levels_dict
