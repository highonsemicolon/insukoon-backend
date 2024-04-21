from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Referral, Referrer


class GenerateCode(APIView):
    def get(self, request):
        referrer, _ = Referrer.objects.get_or_create(user_id=request.user.id)
        referral_code = referrer.code
        return Response({'referral_code': referral_code}, status=status.HTTP_200_OK)


class ReferredUsernames(APIView):
    def get(self, request):
        transactions = Referral.objects.filter(referrer__user_id=request.user)
        referred_usernames = [txn.referred_user.username for txn in transactions]
        return Response(referred_usernames, status=status.HTTP_200_OK)


class VerifyReferralCode(APIView):
    permission_classes = [AllowAny]

    def get(self, request, referral_code):
        try:
            ref = Referrer.objects.get(code=referral_code)
            if ref.expiration_date > timezone.now() and ref.usage_count < ref.usage_limit:
                return Response({"exists": True}, status=status.HTTP_200_OK)
            return Response({"exists": False}, status=status.HTTP_417_EXPECTATION_FAILED)
        except Referrer.DoesNotExist:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)
