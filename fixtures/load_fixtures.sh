#!/bin/bash

# Load sample data fixtures for Legacy Academy Tracking System
# Usage: ./fixtures/load_fixtures.sh

echo "Loading Legacy Academy sample data fixtures..."

# Check if we're in the project root
if [ ! -f "manage.py" ]; then
    echo "Error: Please run this script from the project root directory (where manage.py is located)"
    exit 1
fi

# Load fixtures in correct order to handle dependencies
echo "Loading schools..."
python manage.py loaddata fixtures/01_schools.json

echo "Loading zones..."
python manage.py loaddata fixtures/02_zones.json

echo "Loading users..."
python manage.py loaddata fixtures/03_users.json

echo "Loading school settings..."
python manage.py loaddata fixtures/04_school_settings.json

echo "Loading guardians..."
python manage.py loaddata fixtures/05_guardians.json

echo "Loading students..."
python manage.py loaddata fixtures/06_students.json

echo "Loading guardian-student relationships..."
python manage.py loaddata fixtures/07_guardian_students.json

echo "Loading zone assignments..."
python manage.py loaddata fixtures/08_zone_assignments.json

echo ""
echo "✅ Sample data fixtures loaded successfully!"
echo ""
echo "Sample login credentials:"
echo "  Super Admin: admin / admin123"
echo "  School Admin (Bauleni): admin_bauleni / testpass123"
echo "  Teacher (Bauleni): teacher_bauleni_1 / testpass123"
echo "  Field Officer (Bauleni): field_officer_bauleni / testpass123"
echo ""
echo "Run 'python manage.py runserver' to start the development server."