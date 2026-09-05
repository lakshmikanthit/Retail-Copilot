#!/bin/bash
# Build script for Render deployment

# Run migrations
python manage.py migrate --noinput

# Create superuser if it doesn't exist (for demo purposes)
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Created superuser: admin / admin123")
EOF

# Generate sample data if no products exist
python manage.py shell << 'EOF'
from inventory.models import Product
if Product.objects.count() == 0:
    import subprocess
    subprocess.run(['python', 'manage.py', 'generate_sample_data'])
    subprocess.run(['python', 'manage.py', 'generate_alerts'])
    print("Generated sample data and alerts")
EOF

# Collect static files
python manage.py collectstatic --noinput
