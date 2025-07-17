from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class School(models.Model):
    """
    Model representing a school in the Legacy Academy system.
    Each school operates independently with its own data.
    """
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(
        max_length=10, 
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]+$', 'School code must be uppercase letters and numbers only')]
    )
    address = models.TextField()
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    contact_person = models.CharField(max_length=100, blank=True)
    
    # GPS coordinates for mapping
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Operational settings
    school_start_time = models.TimeField(default='07:30')
    school_end_time = models.TimeField(default='14:30')
    attendance_cutoff_time = models.TimeField(
        default='08:00',
        help_text='Students arriving after this time are marked as late'
    )
    
    # Tracking fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    def get_active_students_count(self):
        """Get count of active students in this school"""
        return self.students.filter(is_active=True).count()
    
    def get_zones(self):
        """Get geographical zones for this school"""
        return self.zones.all()


class Zone(models.Model):
    """
    Geographical zones within a school's catchment area for visit assignment.
    """
    name = models.CharField(max_length=100)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='zones')
    description = models.TextField(blank=True)
    
    # Zone boundaries (simplified)
    boundary_coordinates = models.JSONField(
        default=dict,
        blank=True,
        help_text='JSON array of coordinates defining zone boundaries'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['name', 'school']
        ordering = ['school', 'name']
    
    def __str__(self):
        return f"{self.school.code} - {self.name}"


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    All users belong to a school and have specific roles.
    """
    
    ROLE_CHOICES = [
        ('SUPER_ADMIN', 'Super Administrator'),
        ('SCHOOL_ADMIN', 'School Administrator'),
        ('TEACHER', 'Teacher'),
        ('FIELD_OFFICER', 'Field Officer'),
    ]
    
    # Core fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='TEACHER')
    school = models.ForeignKey(
        School, 
        on_delete=models.CASCADE, 
        related_name='users',
        null=True,
        blank=True,
        help_text='School assignment (null for super admins)'
    )
    
    # Contact information
    employee_number = models.CharField(
        max_length=20, 
        unique=True,
        blank=True,
        null=True,
        validators=[RegexValidator(r'^[A-Z0-9]+$', 'Employee number must be uppercase letters and numbers')]
    )
    phone_number = models.CharField(max_length=20, blank=True)
    
    # Assignment fields
    assigned_zones = models.ManyToManyField(
        Zone,
        blank=True,
        related_name='assigned_officers',
        help_text='Zones assigned to field officers'
    )
    
    # Profile fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    is_password_changed = models.BooleanField(
        default=False,
        help_text='Whether user has changed default password'
    )
    
    class Meta:
        ordering = ['school', 'last_name', 'first_name']
        indexes = [
            models.Index(fields=['employee_number']),
            models.Index(fields=['role']),
            models.Index(fields=['school', 'role']),
        ]
    
    def __str__(self):
        if self.school:
            return f"{self.get_full_name()} ({self.employee_number}) - {self.school.code}"
        return f"{self.get_full_name()} ({self.employee_number})"
    
    def get_role_display_short(self):
        """Get shortened role display"""
        role_map = {
            'SUPER_ADMIN': 'Super Admin',
            'SCHOOL_ADMIN': 'Admin',
            'TEACHER': 'Teacher',
            'FIELD_OFFICER': 'Field Officer',
        }
        return role_map.get(self.role, self.role)
    
    def can_access_school(self, school):
        """Check if user can access data for a specific school"""
        if self.role == 'SUPER_ADMIN':
            return True
        return self.school == school
    
    def get_accessible_schools(self):
        """Get queryset of schools this user can access"""
        if self.role == 'SUPER_ADMIN':
            return School.objects.all()
        return School.objects.filter(id=self.school.id) if self.school else School.objects.none()
    
    def save(self, *args, **kwargs):
        # Handle superuser creation - automatically set role to SUPER_ADMIN
        if self.is_superuser:
            self.role = 'SUPER_ADMIN'
        
        # Super admins don't need school assignment or employee number
        if self.role == 'SUPER_ADMIN':
            self.school = None
            if not self.employee_number:
                self.employee_number = f"ADMIN{self.id or '001'}"
        elif self.role and self.role != 'SUPER_ADMIN' and not self.school_id:
            # Non-super admin users must be assigned to a school
            raise ValueError("Non-super admin users must be assigned to a school")
            
        super().save(*args, **kwargs)


class SchoolSettings(models.Model):
    """
    Configurable settings for each school.
    """
    school = models.OneToOneField(School, on_delete=models.CASCADE, related_name='settings')
    
    # Attendance settings
    absence_threshold_days = models.PositiveIntegerField(
        default=2,
        help_text='Number of absences in rolling period to trigger flag'
    )
    absence_monitoring_period = models.PositiveIntegerField(
        default=7,
        help_text='Rolling period in days for absence monitoring'
    )
    
    # Visit settings
    auto_generate_visits = models.BooleanField(
        default=True,
        help_text='Automatically generate home visits for flagged students'
    )
    visit_priority_threshold = models.PositiveIntegerField(
        default=3,
        help_text='Number of absences for high priority visits'
    )
    
    # Notification settings
    notify_parents_sms = models.BooleanField(default=False)
    notify_admin_email = models.BooleanField(default=True)
    daily_report_time = models.TimeField(
        default='16:00',
        help_text='Time to send daily attendance reports'
    )
    
    # Academic calendar
    term_start_date = models.DateField(null=True, blank=True)
    term_end_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = "School Settings"
        verbose_name_plural = "School Settings"
    
    def __str__(self):
        return f"Settings for {self.school.name}"