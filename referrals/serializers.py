from rest_framework import serializers

from .models import Referrer


class ReferrerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referrer
        fields = ['code']
