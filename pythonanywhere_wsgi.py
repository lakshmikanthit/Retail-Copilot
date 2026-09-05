"""
PythonAnywhere WSGI configuration for Retail Copilot
"""

import os
import sys

# Add the project directory to the Python path
path = '/home/YOUR_USERNAME/Retail-Copilot'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_copilot.settings')

# Import Django and get the WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
