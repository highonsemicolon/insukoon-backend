from rest_framework import serializers

from .models import ParentProfile, SchoolProfile


class ParentProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = ParentProfile
        fields = '__all__'

    def get_username(self, obj):
        return obj.user.username


class SchoolProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = SchoolProfile
        fields = '__all__'

    def get_username(self, obj):
        return obj.user.username
