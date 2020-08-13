#! /bin/bash

echo "Starting UI And Controller...";
python3 controller_main.py & $HOME/NYSG/UI/greenhouse/start-ui.sh;
PID=$!

echo "PID: $PID";

trap "kill $PID; pkill python3;" SIGINT;

wait;

echo "All processes have completed";
