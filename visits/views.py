from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def visits_dashboard(request):
    """Placeholder view for visits dashboard."""
    return render(request, 'visits/dashboard.html')