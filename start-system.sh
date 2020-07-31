#! /bin/bash

# Start UI
echo "Starting UI...";
$HOME/NYSG/UI/greenhouse/start-ui.sh & pid=$!
PID_LIST+=" $pid";

# Start Controller
echo "Starting UI...";
$"python3 controller_main.py" & pid=$!
PID_LIST+=" $pid";

trap "kill $PID_LIST" SIGINT

echo "Parallel processes have started";

wait $PID_LIST

echo
echo "All processes have completed";