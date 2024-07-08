#!/bin/bash

# Start the Django server in the background
python manage.py runserver 0.0.0.0:8000 &

# Infinite loop to run your cron job
while true; do
  python manage.py runcrons
  # Wait for a specified interval (e.g., every minute)
  sleep 60
done
