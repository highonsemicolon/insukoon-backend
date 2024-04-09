from decimal import Decimal

from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser as User
from referrals.models import Transaction
from .models import Payment


class CreateBillView(APIView):
    def get(self, request):
        try:
            amount = None
            currency = "INR"
            user_id = request.user.id
            profile_type = request.user.role

            if profile_type == 'parent':
                amount = Decimal('10')
            elif profile_type == 'school':
                amount = Decimal('100')

            referral = Transaction.objects.filter(referred_user=user_id)
            if referral.exists():
                amount = round(amount * Decimal(0.95), 2)

            payment = Payment.objects.create(user_id=user_id, currency=currency, amount=amount,
                                             payment_intent_id='temp', status='pending')

            redirect_url = f"/payment-gateway?amount={amount}&transaction_id={payment.id}"
            return Response({"redirect_url": redirect_url})

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class SubscriptionStatusView(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            has_subscription = Payment.objects.filter(user=user).exists()
            return Response({"has_subscription": has_subscription})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
