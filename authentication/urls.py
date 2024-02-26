from django.urls import path
from .views import UserLoginAPIView, UserRegistrationAPIView, TokenRefreshAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshAPIView.as_view(), name='token_refresh'),
]
