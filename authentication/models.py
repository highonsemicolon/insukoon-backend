from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('school', 'School'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
