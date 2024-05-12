from rest_framework import serializers

from .models import Pricing, ProvisionalOrder, PaymentGatewayResponse


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'


class ProvisionalPaymentSerializer(serializers.Serializer):
    plan = serializers.CharField()
    referral_code = serializers.CharField(required=False)


class ProvisionalOrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class PaymentGatewayResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayResponse
        fields = '__all__'
