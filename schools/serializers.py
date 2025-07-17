from rest_framework import serializers
from .models import School, Zone, User, SchoolSettings


class SchoolSerializer(serializers.ModelSerializer):
    """Serializer for School model."""
    
    total_students = serializers.SerializerMethodField()
    total_teachers = serializers.SerializerMethodField()
    total_zones = serializers.SerializerMethodField()
    
    class Meta:
        model = School
        fields = [
            'id', 'name', 'code', 'address', 'phone_number', 'email',
            'contact_person', 'latitude', 'longitude', 'school_start_time',
            'school_end_time', 'attendance_cutoff_time', 'is_active',
            'created_at', 'updated_at', 'total_students', 'total_teachers',
            'total_zones'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_total_students(self, obj):
        return obj.students.filter(is_active=True).count() if hasattr(obj, 'students') else 0
    
    def get_total_teachers(self, obj):
        return obj.users.filter(role='TEACHER', is_active=True).count()
    
    def get_total_zones(self, obj):
        return obj.zones.count()


class ZoneSerializer(serializers.ModelSerializer):
    """Serializer for Zone model."""
    
    school_name = serializers.CharField(source='school.name', read_only=True)
    assigned_officers_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Zone
        fields = [
            'id', 'name', 'school', 'school_name', 'description',
            'boundary_coordinates', 'created_at', 'assigned_officers_count'
        ]
        read_only_fields = ['created_at']
    
    def get_assigned_officers_count(self, obj):
        return obj.assigned_officers.count()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    full_name = serializers.SerializerMethodField()
    school_name = serializers.CharField(source='school.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    assigned_zones_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'email', 'employee_number', 'phone_number', 'role',
            'role_display', 'school', 'school_name', 'assigned_zones',
            'assigned_zones_count', 'is_active', 'date_joined',
            'last_login', 'is_password_changed'
        ]
        read_only_fields = ['date_joined', 'last_login', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    def get_assigned_zones_count(self, obj):
        return obj.assigned_zones.count()
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        
        if password:
            user.set_password(password)
            user.save()
        
        return user


class SchoolSettingsSerializer(serializers.ModelSerializer):
    """Serializer for SchoolSettings model."""
    
    school_name = serializers.CharField(source='school.name', read_only=True)
    
    class Meta:
        model = SchoolSettings
        fields = [
            'id', 'school', 'school_name', 'absence_threshold_days',
            'absence_monitoring_period', 'auto_generate_visits',
            'visit_priority_threshold', 'notify_parents_sms',
            'notify_admin_email', 'daily_report_time',
            'term_start_date', 'term_end_date'
        ]