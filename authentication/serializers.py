from django.contrib.auth import authenticate
from rest_framework import serializers

from authentication.models import CustomUser
from profiles.models import ParentProfile, SchoolProfile


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'role')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        if user.role == 'parent':
            ParentProfile.objects.create(user=user)
        else:
            SchoolProfile.objects.create(user=user)
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                return data
        raise serializers.ValidationError("Incorrect Credentials")
