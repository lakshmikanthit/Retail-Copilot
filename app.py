#!/usr/bin/env python
"""
Retail Copilot - NexusTiq24 Hackathon Solution
TRACK_ID=PS03 - Retail Sales and Inventory Copilot

This is the main entry point for the application.
Run: python app.py
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
    """Main entry point for the application"""
    print("Retail Copilot - NexusTiq24 Hackathon Solution")
    print("TRACK_ID=PS03 - Retail Sales and Inventory Copilot")
    print("=" * 60)
    print("Starting application on http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)

    # Run Django development server
    execute_from_command_line(['manage.py', 'runserver', '8000'])

if __name__ == '__main__':
    main()