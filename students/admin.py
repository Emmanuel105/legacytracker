from django.contrib import admin
from .models import Student, Guardian, GuardianStudent


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'first_name', 'last_name', 'school', 'grade', 'class_name', 'is_active']
    list_filter = ['school', 'grade', 'gender', 'is_active']
    search_fields = ['student_id', 'first_name', 'last_name']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.role == 'SUPER_ADMIN':
            return qs
        if request.user.school:
            return qs.filter(school=request.user.school)
        return qs.none()


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'relationship', 'phone_number']
    search_fields = ['first_name', 'last_name', 'phone_number']


@admin.register(GuardianStudent)
class GuardianStudentAdmin(admin.ModelAdmin):
    list_display = ['guardian', 'student', 'is_primary', 'can_receive_calls']