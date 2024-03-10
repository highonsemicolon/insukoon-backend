from django.urls import path
from .views import GenerateReferralCode, ReferredUsernames, VerifyReferralCode

urlpatterns = [
    path('generate/', GenerateReferralCode.as_view(), name='generate_referral_code'),
    path('', ReferredUsernames.as_view(), name='referred_usernames'),
    path('verify/<str:referral_code>/', VerifyReferralCode.as_view(), name='verify_referral_code'),
]
