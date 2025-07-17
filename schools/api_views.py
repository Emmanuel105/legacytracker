from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import School, Zone, User
from .serializers import SchoolSerializer, ZoneSerializer, UserSerializer


class SchoolIsolationMixin:
    """
    Mixin to ensure users only see data from their school.
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        
        if self.request.user.role == 'SUPER_ADMIN':
            return queryset
        
        if hasattr(queryset.model, 'school'):
            # Model has direct school relationship
            return queryset.filter(school=self.request.user.school)
        
        return queryset


class SchoolViewSet(SchoolIsolationMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing schools.
    Super admins can see all schools, others see only their own.
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'SUPER_ADMIN':
            return School.objects.all()
        if self.request.user.school:
            return School.objects.filter(id=self.request.user.school.id)
        return School.objects.none()
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get statistics for a specific school."""
        school = self.get_object()
        
        # Ensure user can access this school
        if not request.user.can_access_school(school):
            return Response({'error': 'Permission denied'}, status=403)
        
        stats = {
            'total_students': school.students.filter(is_active=True).count() if hasattr(school, 'students') else 0,
            'total_teachers': school.users.filter(role='TEACHER', is_active=True).count(),
            'total_field_officers': school.users.filter(role='FIELD_OFFICER', is_active=True).count(),
            'total_zones': school.zones.count(),
        }
        
        return Response(stats)


class ZoneViewSet(SchoolIsolationMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing zones within a school.
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        # Auto-assign school for non-super admins
        if self.request.user.role != 'SUPER_ADMIN':
            serializer.save(school=self.request.user.school)
        else:
            serializer.save()


class UserViewSet(SchoolIsolationMixin, viewsets.ModelViewSet):
    """
    ViewSet for managing users within a school.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'SUPER_ADMIN':
            return User.objects.all()
        if self.request.user.school:
            return User.objects.filter(school=self.request.user.school)
        return User.objects.none()
    
    @action(detail=False, methods=['get'])
    def field_officers(self, request):
        """Get all field officers for the user's school."""
        queryset = self.get_queryset().filter(role='FIELD_OFFICER', is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def assign_zones(self, request, pk=None):
        """Assign zones to a field officer."""
        user = self.get_object()
        
        if user.role != 'FIELD_OFFICER':
            return Response({'error': 'User is not a field officer'}, status=400)
        
        zone_ids = request.data.get('zone_ids', [])
        
        # Validate zones belong to user's school
        zones = Zone.objects.filter(
            id__in=zone_ids,
            school=user.school
        )
        
        user.assigned_zones.set(zones)
        
        return Response({
            'message': f'Assigned {zones.count()} zones to {user.get_full_name()}'
        })