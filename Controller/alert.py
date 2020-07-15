"""
alert deals with possible alert messages
"""

WATER_LEVEL = 100


def alert_message_generator(water_level):
    return "Water Level is Low"


def alert(water_level):
    if water_level < WATER_LEVEL:
        return alert_message_generator
    else:
        return None
