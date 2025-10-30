#!/bin/bash

# CampLand Start Script

echo "🏕️  Starting CampLand Camping Booking System..."
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Build CSS if needed
echo "Building Tailwind CSS..."
npm run build:css

echo ""
echo "Starting Django development server..."
echo "Access the site at: http://127.0.0.1:8000/"
echo "Access admin at: http://127.0.0.1:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python manage.py runserver
