from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, TokenSerializer


class UserRegistrationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_type = request.data.get('user_type')
        if user_type not in ['parent', 'school']:
            return Response({'error': 'Invalid user type'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            count = User.objects.filter(username__startswith=f'insukoon_{user_type}_').count() + 1
            username = f"insukoon_{user_type}_{count}"

            user = serializer.save(username=username)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Requires test again - as of now tokens are set to expire never
class TokenRefreshAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
            new_token, _ = Token.objects.get_or_create(user=request.user)
            return Response({'token': new_token.key}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)
