"""
sernsor-peripheral_test.py contains test for 
all the sensors and peripjeralds
"""
from sensor_class import create_channel


def test_all():
    i2c_channel = create_channel()


if __name__ == "__main__":
    test_all()
