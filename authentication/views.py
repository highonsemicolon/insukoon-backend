from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from referrals.models import Referrer, Transaction
from .models import CustomUser as User
from .serializers import UserSerializer, TokenSerializer


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            count = 1
            last_user = User.objects.last()
            if last_user:
                count = User.objects.last().id + 1

            role = request.data.get('role')
            username = f"insukoon_{role}_{count}"

            user = serializer.save(username=username)
            token, _ = Token.objects.get_or_create(user=user)

            referral_code = request.data.get('referral_code')
            if referral_code:
                try:
                    referrer = Referrer.objects.get(code=referral_code)
                    if referrer.usage_count < referrer.usage_limit:
                        Transaction.objects.create(referrer=referrer, referred_user=user).save()
                        referrer.usage_count += 1
                        referrer.save()
                        user.save()
                    else:
                        user.delete()
                        return Response({'error': 'Maximum referral limit reached'}, status=status.HTTP_400_BAD_REQUEST)
                except:
                    user.delete()
                    return Response({'error': 'Invalid referral code'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'token': token.key, 'username': username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(APIView):

    def get(self, request):
        request.user.auth_token.delete()
        return Response({'success': 'Logged out successfully'}, status=status.HTTP_200_OK)


# Requires test again - as of now tokens are set to expire never
class TokenRefreshAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            new_token, _ = Token.objects.get_or_create(user=request.user)
            return Response({'token': new_token.key}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            return Response({'message': 'Your email has been verified successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid verification link.'}, status=status.HTTP_400_BAD_REQUEST)
