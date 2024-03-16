import random
import string
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from authentication.models import CustomUser as User


def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def calculate_expiry_date(days):
    return timezone.now() + timedelta(days=days)


class Referrer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=6, unique=True, default=generate_code)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    usage_limit = models.IntegerField(default=3)
    usage_count = models.IntegerField(default=0)
    comment = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiration_date = timezone.now() + timedelta(days=30) - timedelta(seconds=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'referral code:  {self.code}'


class Transaction(models.Model):
    referrer = models.ForeignKey(Referrer, on_delete=models.SET_NULL, null=True, blank=True)
    referred_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.referrer.usage_count < self.referrer.usage_limit:
            self.referrer.usage_count += 1
            self.referrer.save()
            super().save(*args, **kwargs)

        else:
            raise OverflowError('Maximum usage limit reached')
