"""
Custom User model for DataDiNascita.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Uses email as the primary identifier instead of username.
    """
    email = models.EmailField(
        'email address',
        unique=True,
        help_text='Required. A valid email address.'
    )

    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text='User timezone for birthday notifications'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return self.email
