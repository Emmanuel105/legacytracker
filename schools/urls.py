from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.school_profile, name='school_profile'),
    path('zones/', views.manage_zones, name='manage_zones'),
    path('assign-officer/', views.assign_field_officer, name='assign_field_officer'),
]