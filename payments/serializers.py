from rest_framework import serializers
from .models import Pricing, ProvisionalOrder


class PricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'


class ProvisionalOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProvisionalOrder
        fields = '__all__'
