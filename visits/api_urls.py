from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# Will add viewsets when implementing

urlpatterns = [
    path('', include(router.urls)),
]