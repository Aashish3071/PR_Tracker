#!/bin/bash

# Build the project
echo "Building the project..."
python manage.py collectstatic --noinput
python manage.py migrate

echo "Build completed successfully!" 