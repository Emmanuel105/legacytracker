from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import School, Zone, User, SchoolSettings


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'contact_person', 'phone_number', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'contact_person']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'address', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'phone_number', 'email')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Operational Settings', {
            'fields': ('school_start_time', 'school_end_time', 'attendance_cutoff_time'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'SUPER_ADMIN':
            return qs
        if request.user.school:
            return qs.filter(id=request.user.school.id)
        return qs.none()


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'created_at']
    list_filter = ['school', 'created_at']
    search_fields = ['name', 'school__name']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'SUPER_ADMIN':
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if request.user.role != 'SUPER_ADMIN' and request.user.school:
                kwargs["queryset"] = School.objects.filter(id=request.user.school.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'get_full_name', 'employee_number', 'role', 'school', 'is_active', 'last_login']
    list_filter = ['role', 'school', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'employee_number', 'email']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Legacy Academy Fields', {
            'fields': ('role', 'school', 'employee_number', 'phone_number', 'assigned_zones')
        }),
        ('Security', {
            'fields': ('is_password_changed', 'last_login_ip'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Legacy Academy Fields', {
            'fields': ('role', 'school', 'employee_number', 'phone_number', 'first_name', 'last_name', 'email')
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'SUPER_ADMIN':
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if request.user.role != 'SUPER_ADMIN' and request.user.school:
                kwargs["queryset"] = School.objects.filter(id=request.user.school.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "assigned_zones":
            if request.user.role != 'SUPER_ADMIN' and request.user.school:
                kwargs["queryset"] = Zone.objects.filter(school=request.user.school)
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    
    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username
    get_full_name.short_description = 'Full Name'


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = ['school', 'absence_threshold_days', 'auto_generate_visits', 'notify_parents_sms']
    list_filter = ['auto_generate_visits', 'notify_parents_sms', 'notify_admin_email']
    
    fieldsets = (
        ('Attendance Monitoring', {
            'fields': ('absence_threshold_days', 'absence_monitoring_period')
        }),
        ('Visit Management', {
            'fields': ('auto_generate_visits', 'visit_priority_threshold')
        }),
        ('Notifications', {
            'fields': ('notify_parents_sms', 'notify_admin_email', 'daily_report_time')
        }),
        ('Academic Calendar', {
            'fields': ('term_start_date', 'term_end_date'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'SUPER_ADMIN':
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "school":
            if request.user.role != 'SUPER_ADMIN' and request.user.school:
                kwargs["queryset"] = School.objects.filter(id=request.user.school.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)