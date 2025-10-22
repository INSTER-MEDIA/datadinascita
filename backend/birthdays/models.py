"""
Models for birthday and event tracking.
Modernized from the legacy Google App Engine Datastore models.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from datetime import datetime, timedelta


class Event(models.Model):
    """
    Represents an event type (birthday, anniversary, etc.).
    """
    EVENT_TYPES = [
        ('birthday', 'Birthday'),
        ('anniversary', 'Anniversary'),
        ('holiday', 'Holiday'),
        ('other', 'Other'),
    ]

    type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default='birthday',
        help_text='Type of event'
    )
    name = models.CharField(
        max_length=100,
        help_text='Name or description of the event'
    )
    date = models.DateField(
        help_text='Date of the event'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        help_text='User who owns this event'
    )
    recurs_annually = models.BooleanField(
        default=True,
        help_text='Whether this event recurs every year'
    )
    notify_days_before = models.IntegerField(
        default=7,
        validators=[MinValueValidator(0)],
        help_text='Days before event to send notification'
    )
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about the event'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['date', 'name']
        indexes = [
            models.Index(fields=['owner', 'date']),
            models.Index(fields=['type', 'date']),
        ]

    def __str__(self):
        return f"{self.name} - {self.date}"

    @property
    def next_occurrence(self):
        """Calculate the next occurrence of this event."""
        if not self.recurs_annually:
            return self.date

        today = datetime.now().date()
        current_year = today.year

        # Create event date for current year
        next_date = self.date.replace(year=current_year)

        # If date has passed this year, use next year
        if next_date < today:
            next_date = next_date.replace(year=current_year + 1)

        return next_date

    @property
    def days_until_next(self):
        """Calculate days until next occurrence."""
        next_date = self.next_occurrence
        today = datetime.now().date()
        return (next_date - today).days


class Contact(models.Model):
    """
    Represents a person with associated events (birthdays, anniversaries, etc.).
    Modernized from the legacy Person/Contact models.
    """
    name = models.CharField(
        max_length=200,
        help_text='Full name of the contact'
    )
    email = models.EmailField(
        blank=True,
        help_text='Email address of the contact'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text='Phone number of the contact'
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        help_text='Birthday of the contact'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contacts',
        help_text='User who owns this contact'
    )
    photo = models.ImageField(
        upload_to='contacts/photos/',
        blank=True,
        null=True,
        help_text='Profile photo of the contact'
    )
    notes = models.TextField(
        blank=True,
        help_text='Additional notes about the contact'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contacts'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['name']
        indexes = [
            models.Index(fields=['owner', 'name']),
            models.Index(fields=['owner', 'birthday']),
        ]
        unique_together = [['owner', 'name']]

    def __str__(self):
        return self.name

    @property
    def age(self):
        """Calculate current age based on birthday."""
        if not self.birthday:
            return None

        today = datetime.now().date()
        age = today.year - self.birthday.year

        # Adjust if birthday hasn't occurred yet this year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1

        return age

    @property
    def next_birthday(self):
        """Calculate the next birthday."""
        if not self.birthday:
            return None

        today = datetime.now().date()
        current_year = today.year

        # Create birthday for current year
        next_bday = self.birthday.replace(year=current_year)

        # If birthday has passed this year, use next year
        if next_bday < today:
            next_bday = next_bday.replace(year=current_year + 1)

        return next_bday

    @property
    def days_until_birthday(self):
        """Calculate days until next birthday."""
        next_bday = self.next_birthday
        if not next_bday:
            return None

        today = datetime.now().date()
        return (next_bday - today).days

    @property
    def upcoming_age(self):
        """Calculate age at next birthday."""
        if not self.birthday or not self.next_birthday:
            return None

        return self.next_birthday.year - self.birthday.year


class ContactEvent(models.Model):
    """
    Links contacts to events beyond just birthdays.
    Allows tracking multiple events per contact (anniversary, etc.).
    """
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        related_name='events',
        help_text='Associated contact'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='contacts',
        help_text='Associated event'
    )
    relationship = models.CharField(
        max_length=100,
        blank=True,
        help_text='Relationship description (e.g., "Wedding Anniversary")'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact_events'
        verbose_name = 'Contact Event'
        verbose_name_plural = 'Contact Events'
        unique_together = [['contact', 'event']]

    def __str__(self):
        return f"{self.contact.name} - {self.event.name}"


class Notification(models.Model):
    """
    Tracks sent notifications to avoid duplicates.
    """
    NOTIFICATION_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='User who received the notification'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        help_text='Related event'
    )
    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='notifications',
        help_text='Related contact'
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES,
        default='email'
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(
        help_text='Notification message content'
    )

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-sent_at']
        indexes = [
            models.Index(fields=['user', '-sent_at']),
        ]

    def __str__(self):
        return f"{self.notification_type} to {self.user.email} at {self.sent_at}"
