# NYSG

## About
The goal of this project is to create a smart mini greenhouse, capable of monitoring and controlling its own climate. The greenhouse will employ a user interface which will allow for remote interaction with the system. Through the interface, the user will be able to visualize the current and historical performance of the system, as well as set healthy environment variables for their plant, which the system will optimize towards. The system will utilize a custom reinforcement learning algorithm to determine which actions it should take upon each update in order to optimize its climate. The system will also include a software controller which schedules updates, carries out I/O operations, and manages sub-system processes.

This repository contains the software elements of our system, as well as Jupyter Notebook files related to the overall system.

This project is created for the NYSG Internship program at Lockheed Martin, and will serve the Engineering Explorers Program in the future.

## System Requirements
- Python 3.6+

## Required Modules
- Django (pip3 install Django)
- Scipy (pip3 install scipy)
- screen (sudo apt get screen)

## Usage
This software is intended to be run on a Raspberry Pi running the Raspberry Pi OS (with recommended software). Development is intended to be conducted via SSH. All instructions hereafter assume that these conditions are met.

### Install Dependencies
- Run 'pip3 install Django'
- Run 'pip3 install scipy'
- Run 'sudo apt get screen'

### If Not Already Done, Clone This Repository
- Run 'git clone https://github.com/colestrine/NYSG.git'

### Navigate To Local Instantiation
- Run 'cd NYSG'

### Start New Screen Session
- Run 'screen -S greenhouse'
- This will create a new screen session called 'greenhouse'
- Before ending our SSH session, we can detach from this screen session, and it will continue to run as a separate shell process on the Raspberry Pi

### Start System
- Run './start-system.sh'
- Wait for system to start up
- Once the success message appears, you can navigate to the specified IP address in your browser to access the UI

### Detach Screen Session
- Type 'ctrl+a', then 'd' to detach your shell session from the current SSH shell session
- This will return you to the original SSH session, and move the screen session to the background
- When we close our SSH connection, the screen process will continue to run on the Raspberry Pi

### Close SSH Connection
- You are now free to close your SSH connection

### Resuming Screen Session
- Open a new SSH connection
- Run 'screen -r greenhouse'
- You will now be returned to your screen session
- Be sure to detach your screen session (see above) before closing your SSH connection to keep the system running