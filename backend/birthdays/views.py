"""
API views for birthdays and contacts management.
"""
import csv
from datetime import datetime, timedelta
from io import TextIOWrapper

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Contact, Event, ContactEvent, Notification
from .serializers import (
    ContactSerializer,
    ContactListSerializer,
    EventSerializer,
    EventListSerializer,
    ContactEventSerializer,
    NotificationSerializer,
    BulkImportSerializer,
    UpcomingBirthdaysSerializer,
)


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing contacts.

    List, create, retrieve, update, and delete contacts.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['birthday']
    search_fields = ['name', 'email', 'phone', 'notes']
    ordering_fields = ['name', 'birthday', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return ContactListSerializer
        return ContactSerializer

    def get_queryset(self):
        """Return contacts owned by current user."""
        return Contact.objects.filter(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming_birthdays(self, request):
        """Get contacts with upcoming birthdays."""
        serializer = UpcomingBirthdaysSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        days = serializer.validated_data['days']
        today = datetime.now().date()

        # Get all contacts with birthdays
        contacts = self.get_queryset().exclude(birthday__isnull=True)

        # Filter contacts with birthdays in the next N days
        upcoming = []
        for contact in contacts:
            if contact.days_until_birthday is not None and 0 <= contact.days_until_birthday <= days:
                upcoming.append(contact)

        # Sort by days until birthday
        upcoming.sort(key=lambda c: c.days_until_birthday)

        serializer = ContactSerializer(upcoming, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        """Import contacts from CSV file."""
        serializer = BulkImportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        csv_file = serializer.validated_data['csv_file']
        skip_duplicates = serializer.validated_data['skip_duplicates']

        try:
            # Parse CSV
            csv_data = TextIOWrapper(csv_file.file, encoding='utf-8')
            reader = csv.DictReader(csv_data)

            created_count = 0
            skipped_count = 0
            errors = []

            for row_num, row in enumerate(reader, start=2):
                try:
                    name = row.get('name', '').strip()
                    birthday_str = row.get('birthday', '').strip()
                    email = row.get('email', '').strip()
                    phone = row.get('phone', '').strip()
                    notes = row.get('notes', '').strip()

                    if not name:
                        errors.append(f"Row {row_num}: Name is required")
                        continue

                    # Check for duplicates
                    if skip_duplicates and Contact.objects.filter(
                        owner=request.user, name=name
                    ).exists():
                        skipped_count += 1
                        continue

                    # Parse birthday
                    birthday = None
                    if birthday_str:
                        try:
                            birthday = datetime.strptime(birthday_str, '%m/%d/%Y').date()
                        except ValueError:
                            try:
                                birthday = datetime.strptime(birthday_str, '%Y-%m-%d').date()
                            except ValueError:
                                errors.append(
                                    f"Row {row_num}: Invalid birthday format for {name}. "
                                    "Use MM/DD/YYYY or YYYY-MM-DD"
                                )
                                continue

                    # Create contact
                    Contact.objects.create(
                        owner=request.user,
                        name=name,
                        birthday=birthday,
                        email=email,
                        phone=phone,
                        notes=notes,
                    )
                    created_count += 1

                except Exception as e:
                    errors.append(f"Row {row_num}: {str(e)}")

            return Response({
                'message': 'Import completed',
                'created': created_count,
                'skipped': skipped_count,
                'errors': errors,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': f'Failed to parse CSV: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """Export contacts to CSV file."""
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

        writer = csv.writer(response)
        writer.writerow(['name', 'birthday', 'email', 'phone', 'notes'])

        contacts = self.get_queryset()
        for contact in contacts:
            birthday_str = contact.birthday.strftime('%m/%d/%Y') if contact.birthday else ''
            writer.writerow([
                contact.name,
                birthday_str,
                contact.email,
                contact.phone,
                contact.notes,
            ])

        return response

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        """Delete all contacts for current user."""
        count = self.get_queryset().count()
        self.get_queryset().delete()
        return Response({
            'message': f'Deleted {count} contacts'
        }, status=status.HTTP_200_OK)


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing events.

    List, create, retrieve, update, and delete events.
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type', 'recurs_annually']
    search_fields = ['name', 'notes']
    ordering_fields = ['name', 'date', 'created_at']
    ordering = ['date']

    def get_serializer_class(self):
        """Use lightweight serializer for list view."""
        if self.action == 'list':
            return EventListSerializer
        return EventSerializer

    def get_queryset(self):
        """Return events owned by current user."""
        return Event.objects.filter(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming_events(self, request):
        """Get upcoming events in the next N days."""
        serializer = UpcomingBirthdaysSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        days = serializer.validated_data['days']

        # Get all events
        events = self.get_queryset()

        # Filter events in the next N days
        upcoming = []
        for event in events:
            if event.days_until_next is not None and 0 <= event.days_until_next <= days:
                upcoming.append(event)

        # Sort by days until event
        upcoming.sort(key=lambda e: e.days_until_next)

        serializer = EventSerializer(upcoming, many=True)
        return Response(serializer.data)


class ContactEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing contact-event relationships.
    """
    serializer_class = ContactEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return contact-events for current user's contacts."""
        return ContactEvent.objects.filter(contact__owner=self.request.user)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing notifications (read-only).
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-sent_at']

    def get_queryset(self):
        """Return notifications for current user."""
        return Notification.objects.filter(user=self.request.user)
