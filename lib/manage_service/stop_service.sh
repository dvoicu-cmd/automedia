#!/bin/bash
# $1 -> location to place service & timer files
# $2 -> name of .timer file
# $3 -> name of .service file

# Navigate to the service dir
echo "navigating to service dir"
cd $1

# stop the timer file
systemctl stop $2

# disable the service file
systemctl disable $3

# Then disable the timer file
systemctl disable $2

# Refresh the dameons
systemctl daemon-reload

