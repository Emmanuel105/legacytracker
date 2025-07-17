from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def student_list(request):
    """Placeholder view for student list."""
    return render(request, 'students/list.html', {'students': []})


@login_required
def add_student(request):
    """Placeholder view for adding student."""
    return render(request, 'students/add.html')


@login_required
def student_detail(request, pk):
    """Placeholder view for student detail."""
    return render(request, 'students/detail.html', {'student': None})