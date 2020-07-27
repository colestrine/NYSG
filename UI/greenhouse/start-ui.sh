#! /bin/bash

# Get IP address
ip_addr=$(hostname -I)

# Trim trailing whitespace from IP address
ip_addr="$(echo -e "${ip_addr}" | sed -e 's/[[:space:]]*$//')"

# Start UI
python3 $HOME/NYSG/UI/greenhouse/manage.py runserver $ip_addr:8080
