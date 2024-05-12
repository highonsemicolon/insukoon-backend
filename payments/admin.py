from django.contrib import admin
from .models import Pricing, Order, PaymentGatewayResponse

admin.site.register(Pricing)
admin.site.register(Order)
admin.site.register(PaymentGatewayResponse)
