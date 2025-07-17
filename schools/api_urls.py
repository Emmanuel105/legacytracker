from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'schools', api_views.SchoolViewSet)
router.register(r'zones', api_views.ZoneViewSet)
router.register(r'users', api_views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]