from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
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

        # Generate verification token
        token_generator = default_token_generator
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        # Build verification URL
        verification_url = reverse('email_verification', kwargs={'uidb64': uid, 'token': token})
        print(verification_url)

        # Send verification email
        # send_mail(
        #     'Verify Your Email',
        #     f'Click the following link to verify your email: {verification_url}',
        #     'from@example.com',
        #     [user.email],
        #     fail_silently=False,
        # )

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
