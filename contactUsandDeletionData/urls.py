from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactUsViewSet, DeletiondataViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'contact', ContactUsViewSet, basename='contact')
router.register(r'deletiondata', DeletiondataViewSet, basename='deletiondata')

# The API URLs are automatically determined by the router
urlpatterns = [
    path('', include(router.urls)),
]
