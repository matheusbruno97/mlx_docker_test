#!/bin/bash

Xvfb DISPLAY=:1 -screen 0 1440x900x24 &

sleep 2

DISPLAY=:1 /opt/mlx/agent.bin --headless &

sleep 60

echo "Running main script now. Check /app/mlx-app for the launcher logs and for the automation script logs. They will be in that folder."

cd /app/mlx-app

python3 -u automation.py >> mlx-automation.log 2>&1

tail -f mlx-automation.log
