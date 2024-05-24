from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
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
        fields = ('email', 'password', 'role', 'country')

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

        # Send verification email
        subject = 'Insukoon - Email Verification'
        message = (f'Hi {user.username}, thank you for registering with Insukoon. Click the following link to verify '
                   f'your email: {settings.HOST}{verification_url}')
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        try:
            send_mail(subject, message, email_from, recipient_list)

            # Sending email notification to admin
            if user.role == "school":
                try:
                    subject = f"New school just signed up - {user.username}"
                    message = f"Username: {user.username} \nEmail: {user.email}"

                    send_mail(
                        subject=subject,
                        message=message,
                        from_email=email_from,
                        recipient_list=[settings.DEFAULT_ADMIN_EMAIL, ]
                    )

                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

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


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        return value
