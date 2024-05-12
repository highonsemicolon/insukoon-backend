from django.conf import settings
from django.db import models

CURRENCY_CHOICES = [
    ('INR', 'Indian Rupees'),
    ('USD', 'US Dollars'),
]


class ProvisionalOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, choices=CURRENCY_CHOICES, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Transaction(models.Model):
    provisional_order = models.ForeignKey(ProvisionalOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Billing information for {self.provisional_order}'


class Pricing(models.Model):
    PLAN_CHOICES = [
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('school', 'School'),
    )

    COUNTRY_CHOICES = [
        ('IN', 'India'),
        ('US', 'United States'),
    ]

    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, default='IN')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="Parent")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default='quarterly')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
