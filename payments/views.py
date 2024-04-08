from decimal import Decimal
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Payment
from authentication.models import CustomUser as User


class CreateBillView(APIView):
    def post(self, request):
        try:
            amount = None
            currency = None
            user_id = request.user.id
            profile_type = request.user.role

            if profile_type == 'parent':
                amount = Decimal('9.99')
            elif profile_type == 'school':
                amount = Decimal('29.99')

            payment = Payment.objects.create(user_id=user_id, amount=amount, payment_intent_id='temp')

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
