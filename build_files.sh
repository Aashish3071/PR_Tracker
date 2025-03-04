#!/bin/bash

# Build the project
echo "Building the project..."
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -m django --version)"

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Create a superuser (optional)
# python manage.py createsuperuser --noinput --username admin --email admin@example.com

# List files in the current directory
echo "Files in the current directory:"
ls -la

# List files in the ave_calculator directory
echo "Files in the ave_calculator directory:"
ls -la ave_calculator/

echo "Build completed successfully!" 