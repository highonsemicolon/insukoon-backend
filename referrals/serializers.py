from rest_framework import serializers
from .models import Transaction, Referrer


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class ReferrerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referrer
        fields = ['referral_code']
