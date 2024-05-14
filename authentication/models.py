from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('school', 'School'),
    )
    COUNTRY_CHOICES = [
        ('IN', 'India'),
        ('US', 'United States'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, blank=False, null=False)
    is_email_verified = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.username
