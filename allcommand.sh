#!/bin/bash
set -e

# Activate virtual environment
echo "Activating virtual environment..."
source env/bin/activate

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Start Django server in background
echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8000 &

# Start subscribe_alerts in background
echo "Starting subscribe_alerts..."
python manage.py subscribe_alerts &

# Wait for both processes
wait
