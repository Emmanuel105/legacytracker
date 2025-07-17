#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@legacyacademy.zm', 'admin123')
    print('Superuser created successfully')
else:
    print('Superuser already exists')
"

# Load sample data fixtures
echo "Loading sample data fixtures..."
python manage.py loaddata fixtures/*.json || echo "Fixtures already loaded or not found"