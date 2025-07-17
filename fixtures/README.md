# Sample Data Fixtures

This directory contains sample data fixtures for development and testing purposes.

## Files Overview

1. **01_schools.json** - Three sample schools (Bauleni, Chawama, Mtendere)
2. **02_zones.json** - Geographic zones for each school (2 zones per school)
3. **03_users.json** - Users with different roles (admins, teachers, field officers)
4. **04_school_settings.json** - Configuration settings for each school
5. **05_guardians.json** - Sample guardians/parents
6. **06_students.json** - Sample students enrolled in the schools
7. **07_guardian_students.json** - Relationships between guardians and students
8. **08_zone_assignments.json** - Zone assignments for field officers

## Sample Data Structure

### Schools
- **Legacy Academy Bauleni (LAB)** - 5 students, 4 staff
- **Legacy Academy Chawama (LAC)** - 4 students, 3 staff  
- **Legacy Academy Mtendere (LAM)** - 4 students, 3 staff

### Users by Role
- **Super Admin**: admin (username: admin, password: admin123)
- **School Admins**: 3 (one per school)
- **Teachers**: 4 (distributed across schools)
- **Field Officers**: 3 (one per school, assigned to zones)

### Students by School
- **Bauleni**: 5 students (Grades 4-8)
- **Chawama**: 4 students (Grades 5-8)
- **Mtendere**: 4 students (Grades 5-8)

## Loading Fixtures

### Load All Fixtures
```bash
python manage.py loaddata fixtures/*.json
```

### Load Specific Fixture
```bash
python manage.py loaddata fixtures/01_schools.json
```

### Load in Order (recommended)
```bash
python manage.py loaddata \
    fixtures/01_schools.json \
    fixtures/02_zones.json \
    fixtures/03_users.json \
    fixtures/04_school_settings.json \
    fixtures/05_guardians.json \
    fixtures/06_students.json \
    fixtures/07_guardian_students.json \
    fixtures/08_zone_assignments.json
```

## Test User Credentials

All test users have the password: **testpass123**

### Sample Login Credentials
- **Super Admin**: admin / admin123
- **Bauleni Admin**: admin_bauleni / testpass123
- **Chawama Admin**: admin_chawama / testpass123
- **Mtendere Admin**: admin_mtendere / testpass123
- **Teacher**: teacher_bauleni_1 / testpass123
- **Field Officer**: field_officer_bauleni / testpass123

## Data Relationships

### Guardian-Student Relationships
- Some students have both parents as guardians
- Some have single guardians
- Some have alternative guardians (grandmother, aunt)

### Zone Assignments
- Each field officer is assigned to all zones in their school
- Field officers can perform home visits in their assigned zones

### Geographic Data
- All locations use Lusaka coordinates
- GPS coordinates provided for mapping functionality
- Zone boundaries defined using polygon coordinates

## Resetting Data

To clear and reload fixtures:
```bash
python manage.py flush --noinput
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@legacyacademy.zm
python manage.py loaddata fixtures/*.json
```

## Notes

- All phone numbers are fictional
- Email addresses use placeholder domains
- GPS coordinates are approximate Lusaka locations
- Student IDs follow pattern: {SchoolCode}{Year}{SequentialNumber}
- Employee numbers follow pattern: {SchoolCode}{SequentialNumber}