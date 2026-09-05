#!/usr/bin/env python
"""
Setup script for Retail Copilot
Run this to initialize the database and generate sample data
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retail_copilot.settings')

# Initialize Django
django.setup()

def main():
    """Setup the application"""
    print("Setting up Retail Copilot...")
    print("=" * 60)

    # Run migrations
    print("Running migrations...")
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])

    # Generate sample data
    print("Generating sample data...")
    execute_from_command_line(['manage.py', 'generate_sample_data'])

    # Generate alerts
    print("Generating inventory alerts...")
    execute_from_command_line(['manage.py', 'generate_alerts'])

    print("=" * 60)
    print("Setup complete! You can now run: python app.py")

if __name__ == '__main__':
    main()