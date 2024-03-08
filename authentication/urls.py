from django.urls import path
from .views import (UserLoginAPIView, UserRegistrationAPIView, TokenRefreshAPIView, VerifyEmailView)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
    path('verify-email/<str:uidb64>/<str:token>/', VerifyEmailView.as_view(), name='email_verification'),
]
