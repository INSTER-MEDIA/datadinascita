"""
Admin configuration for Birthdays app.
"""
from django.contrib import admin
from .models import Event, Contact, ContactEvent, Notification


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for Contact model."""

    list_display = ['name', 'birthday', 'owner', 'days_until_birthday', 'created_at']
    list_filter = ['owner', 'created_at', 'birthday']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'age', 'next_birthday', 'days_until_birthday']

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'owner', 'birthday', 'email', 'phone')
        }),
        ('Additional Info', {
            'fields': ('photo', 'notes')
        }),
        ('Computed Fields', {
            'fields': ('age', 'next_birthday', 'days_until_birthday'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model."""

    list_display = ['name', 'type', 'date', 'owner', 'recurs_annually', 'days_until_next']
    list_filter = ['type', 'recurs_annually', 'owner', 'date']
    search_fields = ['name', 'notes']
    readonly_fields = ['created_at', 'updated_at', 'next_occurrence', 'days_until_next']

    fieldsets = (
        ('Event Details', {
            'fields': ('name', 'type', 'date', 'owner')
        }),
        ('Settings', {
            'fields': ('recurs_annually', 'notify_days_before', 'notes')
        }),
        ('Computed Fields', {
            'fields': ('next_occurrence', 'days_until_next'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ContactEvent)
class ContactEventAdmin(admin.ModelAdmin):
    """Admin interface for ContactEvent model."""

    list_display = ['contact', 'event', 'relationship', 'created_at']
    list_filter = ['created_at']
    search_fields = ['contact__name', 'event__name', 'relationship']
    raw_id_fields = ['contact', 'event']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""

    list_display = ['user', 'notification_type', 'contact', 'event', 'sent_at']
    list_filter = ['notification_type', 'sent_at']
    search_fields = ['user__email', 'message']
    readonly_fields = ['sent_at']
    raw_id_fields = ['user', 'contact', 'event']
