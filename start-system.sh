#! /bin/bash

# Start UI
echo "Starting UI And Controller...";
python3 controller_main.py & $HOME/NYSG/UI/greenhouse/start-ui.sh;
PID=$!;
echo "CURRENT PID: $PID";

trap "kill $PID" SIGINT;

wait $pid;

echo "All processes have completed";
