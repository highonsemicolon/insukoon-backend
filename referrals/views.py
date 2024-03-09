from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Transaction, Referrer


class GenerateReferralCode(APIView):
    def get(self, request):
        referrer, _ = Referrer.objects.get_or_create(user_id=request.user)
        referral_code = referrer.referral_code
        return Response({'referral_code': referral_code}, status=status.HTTP_200_OK)


class ReferredUsernames(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(referrer__user_id=request.user)
        referred_usernames = [txn.referral.referred_user.username for txn in transactions]
        return Response(referred_usernames, status=status.HTTP_200_OK)


class VerifyReferralCode(APIView):
    permission_classes = [AllowAny]

    def get(self, request, referral_code):
        try:
            Referrer.objects.get(referral_code=referral_code)
            return Response({"exists": True}, status=status.HTTP_200_OK)
        except Referrer.DoesNotExist:
            return Response({"exists": False}, status=status.HTTP_404_NOT_FOUND)
