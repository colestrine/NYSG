# Code to control the lights for the NYSG

from datetime import datetime,date,time,timedelta
import json
from time import sleep
import random

class plant_light:
    def __init__(self, dark_hours, directsun_hours, indirectsun_hours):
        self.dark = timedelta(hours=dark_hours)
        self.direct= timedelta(hours=directsun_hours)
        self.indirect = timedelta(hours=indirectsun_hours)

def startdict(): # Create log to be used in the later functions at reset point
    d = {"DATE" : datetime.now(), "DARK" : timedelta() , "DIRECT" : timedelta(), "INDIRECT" : timedelta(), "ACTION" : 0, "LUX" : 0}
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
        today_light = {"DATE" : DATETODAY, "DARK" : timedelta() , "DIRECT" : timedelta(), "INDIRECT" : timedelta(), "ACTION" : 0}
    else:
        today_light["DATE"] = DATETODAY


    #lux = random.randint(2000, 60000)

    if lux > 40000 or today_light["ACTION"]:
        today_light["DIRECT"] += REFRESH 
    elif lux > 800:
        today_light["INDIRECT"] += REFRESH
    else:
        today_light["DARK"] +=  REFRESH

    #DECISION MAKING ALGORITHM

    time_to_grow = subtime(GROWSTART, DATETODAY)
    time_to_sleep = subtime(GROWSTOP, DATETODAY)

    if time_to_grow > timedelta() or time_to_sleep <= timedelta():
        today_light["ACTION"] = 0
        return today_light
    else:

        if plant_type == "Full sun":
            lightcontrol =  plant_light(9,8,7)
        elif plant_type == "Part sun":
            lightcontrol = plant_light(9,5,10)
        elif plant_type == "Part shade":
            lightcontrol = plant_light(9,4,11)
        elif plant_type == "Full shade":
            lightcontrol = plant_light(9,2,13)
        
        direct_needed = lightcontrol.direct - today_light["DIRECT"]
        print(direct_needed)

        if lux < 45000 and direct_needed>=time_to_sleep:
            today_light["ACTION"] = 4
        else:
            today_light["ACTION"] = 0
        print(today_light)
        return today_light
