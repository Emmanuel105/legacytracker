# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL DEPLOYMENT INFORMATION
**PRODUCTION BRANCH: `staging`**  
**Render.com deploys from the `staging` branch, NOT `main`**  
All production changes MUST be pushed to the `staging` branch.

### 📝 Git Workflow for Production
```bash
# Always work on staging for production changes
git checkout staging
git add .
git commit -m "Your commit message"
git push origin staging  # This triggers Render deployment
```

**⚠️ IMPORTANT**: The `main` branch is NOT used for deployment. All production changes must go through the `staging` branch.

## 🏗️ System Architecture Overview

### Legacy Academy Tracking System

A Django-based school attendance and home visit management system designed for multi-school deployment with automated absence monitoring and field officer coordination.

## 🔧 Common Development Commands

### Initial Setup
```bash
# Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py migrate
python manage.py makemigrations

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test schools
python manage.py test students
python manage.py test attendance
python manage.py test visits
python manage.py test reports

# Run specific test module
python manage.py test schools.tests.test_models
python manage.py test attendance.tests.test_flagging

# Run with verbose output
python manage.py test --verbosity=2
```

### Build & Deployment
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check deployment readiness
python manage.py check --deploy

# Production server (Render.com)
gunicorn attendance_system.wsgi:application --bind 0.0.0.0:$PORT

# Deploy script
./build.sh  # Used by Render for deployment
```

### Data Management Commands
```bash
# Create sample data for development
python manage.py loaddata fixtures/sample_data.json

# Import students from CSV
python manage.py import_students <csv_file>

# Generate visit assignments
python manage.py generate_visits

# Process daily attendance analysis
python manage.py analyze_attendance

# Create school admin user
python manage.py create_school_admin <username> <school_id>
```

### Linting
```bash
# Python linting
flake8

# Django checks
python manage.py check
```

## 🏗️ Architecture Overview

### Technology Stack
- **Backend**: Django 4.2.17 + Django REST Framework 3.16.0
- **Database**: PostgreSQL (prod) / SQLite (dev)
- **Frontend**: Server-side templates + Bootstrap 5.3.3 + Vanilla JS
- **PDF Generation**: ReportLab 4.4.1
- **Deployment**: Render.com with automatic CI/CD
- **Analytics**: Metabase-ready PostgreSQL views

### Project Structure
```
legacy-academy-tracking/
├── attendance_system/          # Django project settings
│   ├── settings.py            # Environment-based configuration
│   ├── urls.py                # Root URL routing
│   ├── wsgi.py                # WSGI configuration
│   └── asgi.py                # ASGI configuration
├── schools/                   # School management & user auth
│   ├── models.py              # User, School, Role models
│   ├── views.py               # Authentication & school views
│   └── management/commands/   # School management commands
├── students/                  # Student & guardian management
│   ├── models.py              # Student, Guardian, Class models
│   ├── views.py               # Student CRUD operations
│   └── utils.py               # CSV import utilities
├── attendance/                # Attendance tracking core
│   ├── models.py              # AttendanceRecord, patterns
│   ├── views.py               # Attendance marking interface
│   ├── services.py            # Flagging business logic
│   └── tasks.py               # Automated monitoring
├── visits/                    # Home visit management
│   ├── models.py              # HomeVisit, VisitReport models
│   ├── views.py               # Visit assignment & reporting
│   └── utils.py               # Route optimization
├── reports/                   # Analytics & reporting
│   ├── views.py               # Dashboard & report generation
│   ├── generators.py          # PDF/Excel generators
│   └── metabase_views.py      # Database views for Metabase
├── templates/                 # Bootstrap-based UI templates
│   ├── base.html              # Base template with navigation
│   ├── schools/               # School management UI
│   ├── students/              # Student management UI
│   ├── attendance/            # Attendance marking UI
│   ├── visits/                # Visit management UI
│   └── reports/               # Dashboard & reports UI
├── static/                    # Static files (CSS, JS, images)
│   ├── css/                   # Custom stylesheets
│   ├── js/                    # JavaScript functionality
│   └── images/                # Logo and assets
├── fixtures/                  # Sample data for development
├── render.yaml                # Render deployment configuration
└── build.sh                   # Build script for Render
```

### Core Models & Relationships
```python
# schools/models.py
User (AbstractUser)
├── role: SCHOOL_ADMIN, TEACHER, FIELD_OFFICER, SUPER_ADMIN
├── school: ForeignKey to School
├── employee_number: CharField
└── phone_number: CharField

School
├── name: CharField
├── code: CharField (unique)
├── address: TextField
├── contact_info: JSONField
└── zones: Many-to-many with Zone

# students/models.py
Student
├── student_id: CharField (unique)
├── school: ForeignKey to School
├── grade: CharField
├── class_name: CharField
├── guardians: Many-to-many with Guardian
├── current_address: TextField
└── gps_coordinates: CharField

# attendance/models.py
AttendanceRecord
├── student: ForeignKey to Student
├── date: DateField
├── status: CharField (PRESENT, ABSENT, LATE, EXCUSED)
├── marked_by: ForeignKey to User
└── marked_at: DateTimeField

# visits/models.py
HomeVisit
├── student: ForeignKey to Student
├── assigned_to: ForeignKey to User (field officer)
├── priority: CharField (HIGH, MEDIUM, LOW)
├── status: CharField (PENDING, COMPLETED, CANCELLED)
└── created_from_absence: BooleanField

VisitReport
├── visit: OneToOne to HomeVisit
├── conducted_date: DateTimeField
├── outcome: CharField
├── notes: TextField
├── photos: ImageField
└── gps_coordinates: CharField
```

### Key Business Logic

#### Attendance Flagging System
- **Trigger**: 2 or more absences in a rolling 7-day period
- **Processing**: Daily automated task analyzes attendance patterns
- **Action**: Auto-generates HomeVisit records with priority ranking
- **Location**: `attendance/services.py` - `AttendanceFlaggingService`

#### Multi-School Data Isolation
- **Implementation**: School-based queryset filtering in all views
- **Security**: Row-level security via Django permissions
- **Location**: `schools/middleware.py` - `SchoolIsolationMiddleware`

#### Visit Assignment Algorithm
- **Zone-based**: Field officers assigned to specific geographical zones
- **Priority ranking**: High (3+ absences), Medium (2 absences), Low (other)
- **Workload balancing**: Distributes visits evenly across officers
- **Location**: `visits/services.py` - `VisitAssignmentService`

### Metabase Integration

#### Database Views for Analytics
```sql
-- Key views created for Metabase reporting
attendance_summary_view          # Daily attendance rates by school
chronic_absenteeism_view        # Students with patterns
visit_completion_rates_view     # Field officer performance
school_performance_metrics_view # Overall school statistics
```

#### Connection Configuration
- **Database**: PostgreSQL on Render
- **User**: `metabase_reader` (read-only)
- **Tables**: All application tables + custom views
- **Location**: `reports/metabase_views.py`

### Environment Variables

#### Required for Production
```bash
SECRET_KEY=<django-secret-key>
DATABASE_URL=<postgresql-connection-string>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
ADMIN_URL=secure-admin-panel/
```

#### Optional Configuration
```bash
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
```

### Development Workflow

#### Feature Development
1. Work on `main` branch for development
2. Create feature branches for major changes
3. Test locally with SQLite
4. Deploy to staging branch for testing
5. Merge to staging for production

#### Database Migrations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Production deployment
# Migrations run automatically via build.sh
```

### Security Considerations

#### Role-Based Access Control
- **School Admin**: Full access to their school's data
- **Teacher**: Read/write access to their classes
- **Field Officer**: Access to visit management
- **Super Admin**: System-wide access

#### Data Protection
- **School isolation**: Automatic filtering by user's school
- **Secure admin URL**: Customizable admin panel path
- **HTTPS enforcement**: SSL redirect in production
- **CSRF protection**: Django's built-in CSRF middleware

### Performance Optimization

#### Database Optimization
- **Indexes**: On frequently queried fields (student_id, date, school)
- **Select related**: Optimized queries with prefetch_related
- **Connection pooling**: Disabled for Render compatibility

#### Caching Strategy
- **Static files**: WhiteNoise for efficient serving
- **Database queries**: Django's built-in caching framework
- **Session storage**: Database-backed sessions

### Testing Strategy

#### Unit Tests
- **Models**: Test business logic and relationships
- **Views**: Test authentication and permissions
- **Services**: Test attendance flagging and visit assignment
- **APIs**: Test serializers and endpoints

#### Integration Tests
- **Workflows**: End-to-end attendance and visit processes
- **Multi-school**: Test data isolation
- **Permissions**: Test role-based access

### Common Issues & Solutions

#### Database Connection Issues
- **Problem**: Connection timeouts on Render
- **Solution**: `conn_max_age=0` in database configuration

#### Static Files Not Loading
- **Problem**: CSS/JS not found in production
- **Solution**: Verify `collectstatic` runs in build.sh

#### School Data Isolation
- **Problem**: Users seeing other schools' data
- **Solution**: Ensure all views filter by `request.user.school`

### Future Enhancements

#### Planned Features
- **Mobile PWA**: Offline-capable attendance marking
- **SMS Integration**: Automated parent notifications
- **Biometric attendance**: Hardware integration
- **Advanced analytics**: Machine learning patterns

#### Scalability Considerations
- **Database sharding**: School-based partitioning
- **Caching layer**: Redis for session management
- **CDN integration**: Static file delivery
- **API versioning**: Backward compatibility