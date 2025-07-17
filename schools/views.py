from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import School, User, Zone


def login_view(request):
    """
    Custom login view supporting both username/email and employee number.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try authentication
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            # Update last login IP
            user.last_login_ip = get_client_ip(request)
            user.save(update_fields=['last_login_ip'])
            
            # Check if password change required
            if not user.is_password_changed:
                messages.warning(request, 'Please change your default password for security.')
                return redirect('password_change')
            
            # Redirect to dashboard
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'schools/login.html')


def logout_view(request):
    """Logout user and redirect to login."""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard(request):
    """
    Main dashboard showing school overview and statistics.
    """
    user = request.user
    
    # Get user's accessible schools
    accessible_schools = user.get_accessible_schools()
    
    # Get current school (for non-super admins)
    current_school = user.school
    
    # Calculate statistics
    context = {
        'user': user,
        'current_school': current_school,
        'accessible_schools': accessible_schools,
    }
    
    if current_school:
        # School-specific statistics
        today = timezone.now().date()
        
        # Get counts from related models (will be available after creating other apps)
        context.update({
            'total_students': current_school.students.filter(is_active=True).count() if hasattr(current_school, 'students') else 0,
            'total_teachers': current_school.users.filter(role='TEACHER', is_active=True).count(),
            'total_field_officers': current_school.users.filter(role='FIELD_OFFICER', is_active=True).count(),
            'total_zones': current_school.zones.count(),
        })
    
    return render(request, 'schools/dashboard.html', context)


@login_required
def school_profile(request):
    """
    Display and edit school profile information.
    """
    if request.user.role not in ['SUPER_ADMIN', 'SCHOOL_ADMIN']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    school = request.user.school
    if not school and request.user.role != 'SUPER_ADMIN':
        messages.error(request, 'No school assigned to your account.')
        return redirect('dashboard')
    
    # Super admins can select school
    if request.user.role == 'SUPER_ADMIN':
        school_id = request.GET.get('school')
        if school_id:
            school = get_object_or_404(School, id=school_id)
        else:
            schools = School.objects.all()
            return render(request, 'schools/select_school.html', {'schools': schools})
    
    if request.method == 'POST':
        # Update school information
        school.name = request.POST.get('name', school.name)
        school.address = request.POST.get('address', school.address)
        school.phone_number = request.POST.get('phone_number', school.phone_number)
        school.email = request.POST.get('email', school.email)
        school.contact_person = request.POST.get('contact_person', school.contact_person)
        
        try:
            school.save()
            messages.success(request, 'School profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating school profile: {str(e)}')
    
    context = {
        'school': school,
        'zones': school.zones.all() if school else [],
        'users': school.users.all() if school else [],
    }
    
    return render(request, 'schools/profile.html', context)


@login_required
def manage_zones(request):
    """
    Manage geographical zones for field officer assignment.
    """
    if request.user.role not in ['SUPER_ADMIN', 'SCHOOL_ADMIN']:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard')
    
    school = request.user.school
    if not school and request.user.role != 'SUPER_ADMIN':
        messages.error(request, 'No school assigned to your account.')
        return redirect('dashboard')
    
    zones = school.zones.all() if school else Zone.objects.none()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_zone':
            zone_name = request.POST.get('zone_name')
            zone_description = request.POST.get('zone_description', '')
            
            if zone_name:
                try:
                    Zone.objects.create(
                        name=zone_name,
                        school=school,
                        description=zone_description
                    )
                    messages.success(request, f'Zone "{zone_name}" created successfully.')
                except Exception as e:
                    messages.error(request, f'Error creating zone: {str(e)}')
        
        elif action == 'delete_zone':
            zone_id = request.POST.get('zone_id')
            try:
                zone = Zone.objects.get(id=zone_id, school=school)
                zone.delete()
                messages.success(request, 'Zone deleted successfully.')
            except Zone.DoesNotExist:
                messages.error(request, 'Zone not found.')
    
    context = {
        'school': school,
        'zones': zones,
    }
    
    return render(request, 'schools/manage_zones.html', context)


@login_required
@require_http_methods(["POST"])
def assign_field_officer(request):
    """
    AJAX endpoint to assign field officer to zones.
    """
    if request.user.role not in ['SUPER_ADMIN', 'SCHOOL_ADMIN']:
        return JsonResponse({'success': False, 'error': 'Permission denied'})
    
    officer_id = request.POST.get('officer_id')
    zone_ids = request.POST.getlist('zone_ids')
    
    try:
        officer = User.objects.get(
            id=officer_id,
            role='FIELD_OFFICER',
            school=request.user.school
        )
        
        # Clear existing assignments
        officer.assigned_zones.clear()
        
        # Add new assignments
        zones = Zone.objects.filter(id__in=zone_ids, school=request.user.school)
        officer.assigned_zones.set(zones)
        
        return JsonResponse({
            'success': True,
            'message': f'Zones assigned to {officer.get_full_name()} successfully.'
        })
    
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Field officer not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def get_client_ip(request):
    """
    Get client IP address from request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip