from django.urls import path
from . import views

urlpatterns = [
    path('', views.visits_dashboard, name='visits_dashboard'),
]