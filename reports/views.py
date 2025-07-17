from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def reports_dashboard(request):
    """Placeholder view for reports dashboard."""
    return render(request, 'reports/dashboard.html')