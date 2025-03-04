"""
WSGI config for PR Tracker project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments.
"""

import os
import sys

# Add the project directory to the sys.path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ave_calculator.settings')

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# For Render deployment
app = application 