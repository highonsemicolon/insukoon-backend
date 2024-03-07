import random
import string

from django.contrib.auth.models import User
from django.db import models


def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class Referral(models.Model):
    code = models.CharField(max_length=6, unique=True, default=generate_referral_code)
    expiration_date = models.DateField()
    max_uses = models.IntegerField(default=3)
    referrer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals_made')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    created_at = models.DateTimeField(auto_now_add=True)
