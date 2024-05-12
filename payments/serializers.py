from rest_framework import serializers

from .models import Pricing, ProvisionalOrder, PaymentGatewayResponse


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'


class ProvisionalOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvisionalOrder
        fields = '__all__'


class PaymentGatewayResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayResponse
        fields = '__all__'
