# NYSG

## About
The goal of this project is to create a smart mini greenhouse, capable of monitoring and controlling its own climate. The greenhouse will employ a user interface which will allow for remote interaction with the system. Through the interface, the user will be able to visualize the current and historical performance of the system, as well as set healthy environment variables for their plant, which the system will optimize towards. The system will utilize a custom reinforcement learning algorithm to determine which actions it should take upon each update in order to optimize its climate. The system will also include a software controller which schedules updates, carries out I/O operations, and manages sub-system processes.

This repository contains the software elements of our system, as well as Jupyter Notebook files related to the overall system.

This project is created for the NYSG Internship program at Lockheed Martin, and will serve the Engineering Explorers Program in the future.

## System Requirements
- Python 3.6+

## Required Modules
- Django (pip install Django)
- Scipy (pip install scipy)

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