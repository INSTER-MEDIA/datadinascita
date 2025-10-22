"""
Serializers for Birthdays API.
"""
from rest_framework import serializers
from .models import Contact, Event, ContactEvent, Notification


class ContactSerializer(serializers.ModelSerializer):
    """Serializer for Contact model."""

    # Computed read-only fields
    age = serializers.ReadOnlyField()
    next_birthday = serializers.ReadOnlyField()
    days_until_birthday = serializers.ReadOnlyField()
    upcoming_age = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = [
            'id', 'name', 'email', 'phone', 'birthday', 'photo', 'notes',
            'age', 'next_birthday', 'days_until_birthday', 'upcoming_age',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create contact with current user as owner."""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class ContactListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for contact lists."""

    days_until_birthday = serializers.ReadOnlyField()
    upcoming_age = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = ['id', 'name', 'birthday', 'days_until_birthday', 'upcoming_age']


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model."""

    # Computed read-only fields
    next_occurrence = serializers.ReadOnlyField()
    days_until_next = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = [
            'id', 'type', 'name', 'date', 'recurs_annually',
            'notify_days_before', 'notes', 'next_occurrence',
            'days_until_next', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        """Create event with current user as owner."""
        validated_data['owner'] = self.context['request'].user
        return super().create(validated_data)


class EventListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for event lists."""

    days_until_next = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = ['id', 'type', 'name', 'date', 'days_until_next']


class ContactEventSerializer(serializers.ModelSerializer):
    """Serializer for ContactEvent model."""

    contact_name = serializers.CharField(source='contact.name', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)

    class Meta:
        model = ContactEvent
        fields = ['id', 'contact', 'contact_name', 'event', 'event_name', 'relationship', 'created_at']
        read_only_fields = ['id', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""

    contact_name = serializers.CharField(source='contact.name', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'contact', 'contact_name',
            'event', 'event_name', 'message', 'sent_at'
        ]
        read_only_fields = ['id', 'sent_at']


class BulkImportSerializer(serializers.Serializer):
    """Serializer for bulk importing contacts from CSV."""

    csv_file = serializers.FileField(
        help_text='CSV file with columns: name, birthday (MM/DD/YYYY), email, phone, notes'
    )
    skip_duplicates = serializers.BooleanField(
        default=True,
        help_text='Skip contacts with duplicate names'
    )


class UpcomingBirthdaysSerializer(serializers.Serializer):
    """Serializer for upcoming birthdays query parameters."""

    days = serializers.IntegerField(
        default=30,
        min_value=1,
        max_value=365,
        help_text='Number of days to look ahead'
    )
