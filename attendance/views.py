from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def attendance_dashboard(request):
    """Placeholder view for attendance dashboard."""
    return render(request, 'attendance/dashboard.html')