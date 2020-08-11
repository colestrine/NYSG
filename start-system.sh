#! /bin/bash

echo "Starting UI And Controller...";
python3 controller_main.py & $HOME/NYSG/UI/greenhouse/start-ui.sh;
PID=$!;
echo "CURRENT PID: $PID";

trap "kill $PID; python3 set.py;" SIGINT;

wait;

echo "All processes have completed";
