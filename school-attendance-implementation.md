# Django School Attendance & Home Visit Management System - Implementation Guide

## Project Setup Instructions

### Prerequisites
- Python 3.10+
- PostgreSQL 14+
- Redis (for caching and Celery)
- Node.js 18+ (for frontend tooling)

### Initial Setup Commands
```bash
# Create project directory
mkdir school_attendance_system
cd school_attendance_system

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install core dependencies
pip install django==4.2.* djangorestframework psycopg2-binary celery redis python-decouple pillow

# Create Django project
django-admin startproject config .

# Create apps
python manage.py startapp accounts
python manage.py startapp schools
python manage.py startapp students
python manage.py startapp attendance
python manage.py startapp visits
python manage.py startapp reports
python manage.py startapp api
```

## Project Structure
```
school_attendance_system/
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── accounts/
│   ├── models.py          # CustomUser, UserProfile
│   ├── views.py           # Authentication views
│   ├── serializers.py     # DRF serializers
│   ├── permissions.py     # Custom permissions
│   └── managers.py        # Custom user manager
├── schools/
│   ├── models.py          # School, SchoolSettings
│   ├── views.py           # School management views
│   └── admin.py           # School admin interface
├── students/
│   ├── models.py          # Student, Guardian, Class
│   ├── views.py           # Student CRUD views
│   ├── serializers.py     # Student API serializers
│   └── utils.py           # Bulk import utilities
├── attendance/
│   ├── models.py          # AttendanceRecord, AbsencePattern
│   ├── views.py           # Attendance marking views
│   ├── tasks.py           # Celery tasks for monitoring
│   └── services.py        # Business logic for flagging
├── visits/
│   ├── models.py          # HomeVisit, VisitReport
│   ├── views.py           # Visit management views
│   ├── serializers.py     # Visit API serializers
│   └── utils.py           # Route optimization logic
├── reports/
│   ├── views.py           # Report generation views
│   ├── generators.py      # Report creation logic
│   └── exports.py         # PDF/Excel export utilities
├── api/
│   ├── v1/
│   │   ├── urls.py        # API URL routing
│   │   └── views.py       # API viewsets
│   └── middleware.py      # API middleware
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── media/
│   ├── students/
│   └── visits/
├── templates/
│   ├── base.html
│   ├── accounts/
│   ├── attendance/
│   ├── students/
│   ├── visits/
│   └── reports/
├── locale/             # For translations
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── .env.example
├── .gitignore
└── manage.py
```

## Implementation Phases

### Phase 1: Core Setup & Authentication (Week 1)

#### 1.1 Configure Settings
- Split settings into base, development, and production
- Configure PostgreSQL database connection
- Set up static and media file handling
- Configure allowed hosts and CORS
- Set up environment variables with python-decouple

#### 1.2 Custom User Model
- Extend Django's AbstractUser
- Add fields: role, phone_number, employee_id
- Create UserProfile model with additional fields
- Implement role choices: SUPER_ADMIN, SCHOOL_ADMIN, TEACHER, FIELD_OFFICER

#### 1.3 Authentication System
- Implement JWT authentication for API
- Create login/logout views
- Build password reset functionality
- Add role-based permissions
- Create user registration workflow

#### 1.4 School Model & Multi-tenancy
- Create School model with fields: name, code, address, contact_info
- Implement school-based data isolation
- Add school assignment to users
- Create school switching functionality for super admins

### Phase 2: Student Management (Week 2)

#### 2.1 Student Models
- Student model with fields:
  - Personal: first_name, last_name, date_of_birth, gender, photo
  - Academic: student_id, grade, class_name, enrollment_date
  - Contact: current_address, gps_coordinates
- Guardian model with relationship to students
- Class/Section model for grouping

#### 2.2 Student CRUD Operations
- Create views for adding/editing students
- Implement bulk import from CSV/Excel
- Add student search and filtering
- Create student transfer between schools functionality
- Build student profile view with history

#### 2.3 Guardian Management
- CRUD operations for guardians
- Link multiple children to one guardian
- Store multiple contact numbers
- SMS notification preferences

### Phase 3: Attendance Module (Week 3)

#### 3.1 Attendance Models
- AttendanceRecord model:
  - student (FK), date, status, marked_by, marked_at
  - Status choices: PRESENT, ABSENT, LATE, EXCUSED
- AttendanceSession model for class-wise marking
- AbsencePattern model for tracking patterns

#### 3.2 Attendance Marking Interface
- Create class-based attendance sheet view
- Implement quick marking interface (grid layout)
- Add bulk actions (mark all present)
- Build offline-capable marking with localStorage
- Create attendance editing with audit trail

#### 3.3 Automated Monitoring
- Celery task to analyze daily attendance
- Flag students with 2 absences in rolling 7 days
- Create configurable rules engine
- Generate daily absence reports
- Send automated notifications

### Phase 4: Home Visit Management (Week 4)

#### 4.1 Visit Models
- HomeVisit model:
  - student, assigned_to, scheduled_date, priority
  - status: PENDING, COMPLETED, RESCHEDULED, CANCELLED
- VisitReport model:
  - visit, conducted_date, outcome, notes, photos
  - gps_coordinates, parent_present, follow_up_required

#### 4.2 Visit Assignment System
- Auto-generate visit lists from flagged students
- Zone-based assignment to field officers
- Priority ranking algorithm
- Workload balancing across officers

#### 4.3 Mobile Visit Interface
- Mobile-optimized visit list view
- GPS navigation integration
- Offline-capable visit form
- Photo upload with compression
- Signature capture for confirmation

### Phase 5: Reporting & Analytics (Week 5)

#### 5.1 Dashboard Development
- School-level attendance dashboard
- Charts using Chart.js or similar:
  - Daily attendance trends
  - Chronic absenteeism rates
  - Grade-wise comparisons
- Real-time statistics updates

#### 5.2 Report Generation
- Implement report generators:
  - Daily attendance summary
  - Weekly absence report
  - Monthly statistical analysis
  - Field officer performance report
- Add filtering by date range, school, grade

#### 5.3 Export Functionality
- PDF generation using ReportLab
- Excel export using openpyxl
- Scheduled report emails
- Bulk data export for analysis

### Phase 6: Mobile Optimization & PWA (Week 6)

#### 6.1 Progressive Web App Setup
- Configure service worker
- Implement offline caching strategy
- Add web app manifest
- Enable install prompts

#### 6.2 Mobile UI Optimization
- Implement touch-friendly interfaces
- Optimize images and assets
- Add loading states and skeletons
- Implement pull-to-refresh
- Create bottom navigation for mobile

#### 6.3 Performance Optimization
- Implement pagination and lazy loading
- Add database query optimization
- Configure Redis caching
- Minimize JavaScript bundle size
- Enable compression

### Phase 7: Communication & Notifications (Week 7)

#### 7.1 SMS Integration
- Integrate SMS gateway (Twilio/African providers)
- Create message templates
- Implement bulk SMS for absences
- Add delivery tracking

#### 7.2 In-App Notifications
- Real-time notifications using WebSockets
- Push notifications for PWA
- Email notifications for reports
- Notification preferences per user

### Phase 8: Testing & Deployment (Week 8)

#### 8.1 Testing Implementation
- Unit tests for models and utilities
- Integration tests for API endpoints
- Frontend testing with Selenium
- Load testing for 14,000 users
- Create test data generators

#### 8.2 Deployment Setup
- Dockerize application
- Configure Nginx + Gunicorn
- Set up PostgreSQL replication
- Configure Redis clustering
- Implement backup strategies
- Set up monitoring (Sentry, New Relic)

## Key Implementation Details

### Database Optimization
- Add indexes on frequently queried fields
- Implement database partitioning for attendance records
- Use select_related and prefetch_related
- Configure connection pooling

### Security Implementation
- Enable HTTPS only
- Implement CSRF protection
- Add rate limiting on API
- Configure secure headers
- Implement audit logging
- Data encryption for sensitive fields

### API Design Guidelines
- RESTful endpoints with proper HTTP methods
- Consistent JSON response format
- Pagination on list endpoints
- Filtering and search capabilities
- Proper error handling and status codes
- API versioning strategy

### Frontend Guidelines
- Mobile-first responsive design
- Maximum 3-tap navigation depth
- 48px minimum touch target size
- Contrast ratio compliance (WCAG 2.1)
- Loading states for all async operations
- Form validation with clear error messages

### Celery Tasks to Implement
1. Daily attendance analysis
2. Absence pattern detection
3. Visit reminder notifications
4. Report generation
5. Data export jobs
6. SMS queue processing

### Third-party Integrations
- SMS Gateway (Twilio/Africa's Talking)
- Email service (SendGrid/Amazon SES)
- File storage (AWS S3/Local)
- Maps API for route optimization
- PDF generation library

## Development Best Practices

### Code Organization
- Follow Django's app structure conventions
- Separate business logic into services.py
- Use managers for complex queries
- Implement proper error handling
- Add comprehensive logging

### Git Workflow
- Feature branches for new functionality
- Meaningful commit messages
- Pull request reviews
- Automated testing on CI/CD

### Documentation Requirements
- API documentation with Swagger/ReDoc
- Code comments for complex logic
- README files for each app
- Deployment documentation
- User manual for administrators

## Performance Targets
- Page load: < 3 seconds on 3G
- API response: < 500ms average
- Attendance marking: < 30 seconds per class
- Report generation: < 10 seconds
- 99.9% uptime SLA

## Monitoring & Maintenance
- Error tracking with Sentry
- Performance monitoring
- Database query analysis
- User activity analytics
- Regular security audits
- Automated backups

## Additional Features for Future
- Biometric attendance integration
- Parent mobile app
- Advanced analytics with ML
- Integration with school management systems
- Automated calling system for follow-ups

---

## Notes for AI Implementation

When implementing this system:
1. Start with Phase 1 and complete each phase before moving to the next
2. Write comprehensive tests for each component
3. Follow Django best practices and conventions
4. Prioritize mobile performance and offline functionality
5. Ensure all features work on low-end devices
6. Implement proper error handling and user feedback
7. Add detailed comments and documentation
8. Consider localization needs from the start
9. Build with scalability in mind for 14,000+ users
10. Implement gradual rollout capabilities per school

Each model should include:
- Proper field validation
- str() and repr() methods
- Meta class with ordering and indexes
- Custom managers where needed
- Model methods for business logic
- Proper related_name on foreign keys

Each view should include:
- Permission checking
- School-based filtering
- Proper error handling
- Audit logging
- Mobile-responsive templates
- AJAX capabilities where appropriate