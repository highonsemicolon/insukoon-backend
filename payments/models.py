from django.conf import settings
from django.db import models

CURRENCY_CHOICES = [
    ('INR', 'Indian Rupees'),
    ('USD', 'US Dollars'),
]

PLAN_CHOICES = [
    ('quarterly', 'Quarterly'),
    ('yearly', 'Yearly'),
]


class ProvisionalOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    plan = models.CharField(max_length=8, choices=CURRENCY_CHOICES, default='yearly')
    quantity = models.IntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, choices=CURRENCY_CHOICES, default='INR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Order(models.Model):
    provisional_order = models.ForeignKey(ProvisionalOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('success', 'Success'), ('failed', 'Failed')])
    created_at = models.DateTimeField(auto_now_add=True)
    payment_intent_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'Billing information for {self.provisional_order}'


class Pricing(models.Model):
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


class PaymentGatewayResponse(models.Model):
    order_id = models.CharField(max_length=20)
    tracking_id = models.CharField(max_length=20)
    bank_ref_no = models.CharField(max_length=100, null=True, blank=True)
    order_status = models.CharField(max_length=20)
    status_code = models.CharField(max_length=20, null=True, blank=True)
    status_message = models.TextField()
    currency = models.CharField(max_length=5)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    billing_name = models.CharField(max_length=100)
    billing_email = models.EmailField(null=True, blank=True)
    payment_mode = models.CharField(max_length=50, null=True, blank=True)
    card_name = models.CharField(max_length=100, null=True, blank=True)
    billing_address = models.TextField(null=True, blank=True)
    billing_city = models.CharField(max_length=50, null=True, blank=True)
    billing_state = models.CharField(max_length=50, null=True, blank=True)
    billing_zip = models.CharField(max_length=20, null=True, blank=True)
    billing_country = models.CharField(max_length=50, null=True, blank=True)
    billing_tel = models.CharField(max_length=20, null=True, blank=True)
    delivery_name = models.CharField(max_length=100, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    delivery_city = models.CharField(max_length=50, null=True, blank=True)
    delivery_state = models.CharField(max_length=50, null=True, blank=True)
    delivery_zip = models.CharField(max_length=20, null=True, blank=True)
    delivery_country = models.CharField(max_length=50, null=True, blank=True)
    delivery_tel = models.CharField(max_length=20, null=True, blank=True)
    vault = models.CharField(max_length=1)
    offer_type = models.CharField(max_length=20, null=True, blank=True)
    offer_code = models.CharField(max_length=20, null=True, blank=True)
    discount_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    mer_amount = models.DecimalField(max_digits=15, decimal_places=2)
    eci_value = models.CharField(max_length=20, null=True, blank=True)
    retry = models.CharField(max_length=1)
    response_code = models.CharField(max_length=20, null=True, blank=True)
    trans_date = models.DateTimeField()
    bin_country = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentGatewayResponse for order {self.order_id}"
