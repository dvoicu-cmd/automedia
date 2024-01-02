#!/bin/bash
# $1 -> location to place service & timer files
# $2 -> name of .timer file
# $3 -> name of .service file

# Navigate to the service dir
echo "navigating to service dir"
cd $1

# Refresh the dameons
systemctl daemon-reload

# Enable the timer file
systemctl enable $2

# Enable the service file
systemctl enable $3

# Then start the timer file
systemctl start $2
