"""
URL configuration for birthdays app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'birthdays'

router = DefaultRouter()
router.register('contacts', views.ContactViewSet, basename='contact')
router.register('events', views.EventViewSet, basename='event')
router.register('contact-events', views.ContactEventViewSet, basename='contact-event')
router.register('notifications', views.NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
