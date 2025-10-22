"""
Tests for Birthdays app.
"""
import pytest
from datetime import datetime, timedelta
from django.urls import reverse
from rest_framework import status

from .models import Contact, Event


@pytest.mark.django_db
class TestContactAPI:
    """Tests for Contact API endpoints."""

    def test_create_contact(self, authenticated_client, user):
        """Test creating a new contact."""
        url = reverse('birthdays:contact-list')
        data = {
            'name': 'John Doe',
            'birthday': '1990-05-15',
            'email': 'john@example.com',
            'phone': '+1234567890',
        }

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Contact.objects.filter(owner=user, name='John Doe').exists()

    def test_list_contacts(self, authenticated_client, user):
        """Test listing contacts."""
        # Create test contacts
        Contact.objects.create(
            owner=user,
            name='Alice',
            birthday=datetime(1985, 3, 20).date()
        )
        Contact.objects.create(
            owner=user,
            name='Bob',
            birthday=datetime(1992, 8, 10).date()
        )

        url = reverse('birthdays:contact-list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2

    def test_upcoming_birthdays(self, authenticated_client, user):
        """Test getting upcoming birthdays."""
        today = datetime.now().date()
        next_week = today + timedelta(days=7)

        # Create contact with birthday next week
        Contact.objects.create(
            owner=user,
            name='Birthday Soon',
            birthday=next_week.replace(year=1990)
        )

        url = reverse('birthdays:contact-upcoming-birthdays')
        response = authenticated_client.get(url, {'days': 30})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_cannot_access_other_users_contacts(self, authenticated_client, user, admin_user):
        """Test that users can only see their own contacts."""
        # Create contact for another user
        Contact.objects.create(
            owner=admin_user,
            name='Other User Contact',
            birthday=datetime(1990, 1, 1).date()
        )

        url = reverse('birthdays:contact-list')
        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 0


@pytest.mark.django_db
class TestContactModel:
    """Tests for Contact model."""

    def test_age_calculation(self, user):
        """Test age calculation."""
        birthday = datetime(1990, 5, 15).date()
        contact = Contact.objects.create(
            owner=user,
            name='Test User',
            birthday=birthday
        )

        today = datetime.now().date()
        expected_age = today.year - birthday.year
        if (today.month, today.day) < (birthday.month, birthday.day):
            expected_age -= 1

        assert contact.age == expected_age

    def test_next_birthday_calculation(self, user):
        """Test next birthday calculation."""
        contact = Contact.objects.create(
            owner=user,
            name='Test User',
            birthday=datetime(1990, 5, 15).date()
        )

        today = datetime.now().date()
        next_bday = contact.next_birthday

        assert next_bday.month == 5
        assert next_bday.day == 15
        assert next_bday >= today


@pytest.mark.django_db
class TestEventAPI:
    """Tests for Event API endpoints."""

    def test_create_event(self, authenticated_client, user):
        """Test creating a new event."""
        url = reverse('birthdays:event-list')
        data = {
            'type': 'anniversary',
            'name': 'Wedding Anniversary',
            'date': '2020-06-15',
            'recurs_annually': True,
        }

        response = authenticated_client.post(url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert Event.objects.filter(owner=user, name='Wedding Anniversary').exists()

    def test_upcoming_events(self, authenticated_client, user):
        """Test getting upcoming events."""
        today = datetime.now().date()
        next_week = today + timedelta(days=7)

        Event.objects.create(
            owner=user,
            type='holiday',
            name='Upcoming Holiday',
            date=next_week.replace(year=2020),
            recurs_annually=True
        )

        url = reverse('birthdays:event-upcoming-events')
        response = authenticated_client.get(url, {'days': 30})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
