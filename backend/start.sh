#!/bin/bash
# Render deployment script
echo "Starting deployment..."
cd backend
echo "Installing production requirements..."
pip install -r requirements-production.txt
echo "Starting application..."
gunicorn --bind 0.0.0.0:$PORT app_production:app
