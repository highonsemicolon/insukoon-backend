import random
import string
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def calculate_expiry_date(days):
    return datetime.now() + timedelta(days=days)


class Referrer(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=6, unique=True, default=generate_referral_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    max_limit = models.IntegerField(default=3)
    current_count = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_date = datetime.now() + timedelta(days=30)
        super().save(*args, **kwargs)


class Referral(models.Model):
    referrer = models.ForeignKey(Referrer, on_delete=models.SET_NULL, null=True, blank=True)
    Referred_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
