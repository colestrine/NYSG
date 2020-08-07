from gpiozero import MCP3001

def calibrate_soil_sensor():
    buckets = [0,0]
    sensor = MCP3001()
    input("Place soil moisture sensor in air, then hit any key. ")

    buckets[0] = sensor.value
    print("Dry soil value: " + str(buckets[0]))
    input("Place soil moisture sensor in water NO HIGHER THAN THE LINE, then hit any key. ")
    buckets[1] = sensor.value
    print("Wet soil value: " +  str(buckets[1]))
    return


calibrate_soil_sensor()