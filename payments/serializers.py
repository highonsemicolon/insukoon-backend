from rest_framework import serializers

from .models import Pricing, ProvisionalOrder, PaymentGatewayResponse


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'


class ProvisionalPaymentSerializer(serializers.Serializer):
    plan = serializers.CharField()
    referral_code = serializers.CharField(required=False)


class PaymentGatewayResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayResponse
        fields = '__all__'
