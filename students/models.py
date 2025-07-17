from django.db import models
from django.core.validators import RegexValidator
from schools.models import School


class Guardian(models.Model):
    """
    Model representing a guardian/parent who can have multiple students.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    relationship_choices = [
        ('MOTHER', 'Mother'),
        ('FATHER', 'Father'),
        ('GUARDIAN', 'Guardian'),
        ('GRANDMOTHER', 'Grandmother'),
        ('GRANDFATHER', 'Grandfather'),
        ('AUNT', 'Aunt'),
        ('UNCLE', 'Uncle'),
        ('OTHER', 'Other'),
    ]
    relationship = models.CharField(max_length=20, choices=relationship_choices)
    
    # Contact information
    phone_number = models.CharField(max_length=20, blank=True)
    alternative_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    
    # Address
    address = models.TextField(blank=True)
    
    # SMS preferences
    receive_sms = models.BooleanField(default=True)
    preferred_language = models.CharField(
        max_length=10,
        choices=[('EN', 'English'), ('NY', 'Nyanja'), ('BE', 'Bemba')],
        default='EN'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['last_name', 'first_name']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_relationship_display()})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    """
    Model representing a student in the system.
    """
    # Basic information
    student_id = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9]+$', 'Student ID must be uppercase letters and numbers')]
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    # School relationship
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    
    # Academic information
    grade_choices = [
        ('GRADE_1', 'Grade 1'),
        ('GRADE_2', 'Grade 2'),
        ('GRADE_3', 'Grade 3'),
        ('GRADE_4', 'Grade 4'),
        ('GRADE_5', 'Grade 5'),
        ('GRADE_6', 'Grade 6'),
        ('GRADE_7', 'Grade 7'),
        ('GRADE_8', 'Grade 8'),
        ('GRADE_9', 'Grade 9'),
        ('GRADE_10', 'Grade 10'),
        ('GRADE_11', 'Grade 11'),
        ('GRADE_12', 'Grade 12'),
    ]
    grade = models.CharField(max_length=10, choices=grade_choices)
    class_name = models.CharField(max_length=50, help_text='e.g., 7A, 8B')
    
    # Personal information
    date_of_birth = models.DateField(null=True, blank=True)
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    
    # Contact and location
    current_address = models.TextField()
    gps_coordinates = models.CharField(max_length=50, blank=True, help_text='Latitude,Longitude')
    
    # Guardian relationships
    guardians = models.ManyToManyField(Guardian, through='GuardianStudent', related_name='students')
    
    # Photos
    photo = models.ImageField(upload_to='students/photos/', blank=True)
    
    # Enrollment information
    enrollment_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    # Tracking fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['school', 'grade', 'class_name', 'last_name', 'first_name']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['school', 'grade', 'class_name']),
            models.Index(fields=['school', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_primary_guardian(self):
        """Get the primary guardian (first one added)."""
        guardian_student = self.guardianstudent_set.filter(is_primary=True).first()
        return guardian_student.guardian if guardian_student else None
    
    def get_current_attendance_rate(self):
        """Calculate current attendance rate (placeholder - will implement after attendance app)."""
        # This will be implemented when attendance app is created
        return 0


class GuardianStudent(models.Model):
    """
    Through model for Guardian-Student relationship with additional fields.
    """
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)
    can_receive_calls = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['guardian', 'student']
    
    def __str__(self):
        return f"{self.guardian.get_full_name()} - {self.student.get_full_name()}"


# Placeholder models for other apps - will be moved to appropriate apps
class AttendanceRecord(models.Model):
    """Placeholder for attendance tracking."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status_choices = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
        ('EXCUSED', 'Excused'),
    ]
    status = models.CharField(max_length=10, choices=status_choices)
    marked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'date']
        ordering = ['-date']