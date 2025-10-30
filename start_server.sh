#!/bin/bash
# Render startup script for CampLand Django application

echo "Starting CampLand Django application..."
echo "Django settings module: $DJANGO_SETTINGS_MODULE"
echo "Debug mode: $DEBUG"

# Start the application with gunicorn
exec gunicorn campland.wsgi:application \
    --bind 0.0.0.0:${PORT:-8000} \
    --workers 2 \
    --timeout 30 \
    --log-level info \
    --access-logfile - \
    --error-logfile -