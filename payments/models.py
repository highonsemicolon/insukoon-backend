from django.db import models
from authentication.models import CustomUser as User


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, choices=[('USD', 'Dollars'), ('INR', 'Inr')], default='USD')
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Billing information for {self.user.username}'
