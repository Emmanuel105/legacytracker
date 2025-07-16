"""
URL configuration for Legacy Academy Tracking System.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    
    # App URLs
    path('', include('schools.urls')),
    path('students/', include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('visits/', include('visits.urls')),
    path('reports/', include('reports.urls')),
    
    # API URLs
    path('api/', include('schools.api_urls')),
    path('api/students/', include('students.api_urls')),
    path('api/attendance/', include('attendance.api_urls')),
    path('api/visits/', include('visits.api_urls')),
    path('api/reports/', include('reports.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Legacy Academy Tracking System"
admin.site.site_title = "Legacy Academy Admin"
admin.site.index_title = "Welcome to Legacy Academy Administration"