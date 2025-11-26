#!/bin/bash
set -e

# Kill any existing processes on port 8000
echo "Checking for existing processes..."
pkill -9 -f "manage.py runserver" 2>/dev/null || true
pkill -9 -f "subscribe_alerts" 2>/dev/null || true
sleep 1

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

echo "✅ All services started!"
echo "Django server: http://0.0.0.0:8000"
echo "MQTT subscriber: Running in background"

# Wait for both processes
wait
