import random
import string

from django.contrib.auth.models import AbstractUser
from django.db import models


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('school', 'School'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email_verified = models.BooleanField(default=False)

    # Referral
    referral_code = models.CharField(max_length=6, unique=True, default=generate_referral_code, null=True, blank=True)
    referred_by = models.ForeignKey('self', on_delete=models.CASCADE, related_name='referral_by', null=True, blank=True)

    def __str__(self):
        return f"{self.username} is referred by {self.referred_by}"
