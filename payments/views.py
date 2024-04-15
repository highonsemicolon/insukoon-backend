import os
from decimal import Decimal

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser as User
from referrals.models import Transaction
from .models import Payment
from .utils import encrypt


merchant_id = os.environ.get('MERCHANT_ID')
access_code = os.getenv('ACCESS_CODE')
encryption_key = os.getenv('ENCRYPTION_KEY')
redirect_url = os.getenv('PAYMENT_REDIRECT_URL')
cancel_url = os.getenv('PAYMENT_CANCEL_URL')
payment_gtw_url = os.getenv('PAYMENT_GTW_URL')


class CreateBillView(APIView):
    def put(self, request):
        try:
            amount = 0
            currency = 'INR'
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

            p_merchant_id = str(merchant_id)
            p_order_id = str(payment.id)
            p_currency = currency
            p_amount = str(amount)
            p_redirect_url = redirect_url
            p_cancel_url = cancel_url
            p_language = 'EN'

            p_billing_name = ''
            p_billing_address = ''
            p_billing_city = ''
            p_billing_state = ''
            p_billing_zip = ''
            p_billing_country = ''
            p_billing_tel = ''
            p_billing_email = ''

            p_delivery_name = ''
            p_delivery_address = ''
            p_delivery_city = ''
            p_delivery_state = ''
            p_delivery_zip = ''
            p_delivery_country = ''
            p_delivery_tel = ''
            p_merchant_param1 = ''
            p_merchant_param2 = ''
            p_merchant_param3 = ''
            p_merchant_param4 = ''
            p_merchant_param5 = ''
            p_promo_code = ''

            p_customer_identifier = str(user_id)

            merchant_data = (
                    'merchant_id=' + p_merchant_id + '&' + 'order_id=' + p_order_id + '&' + "currency=" + p_currency +
                    '&' + 'amount=' + p_amount + '&' + 'redirect_url=' + p_redirect_url + '&' +
                    'cancel_url=' + p_cancel_url + '&' + 'language=' + p_language + '&' +

                    'billing_name=' + p_billing_name + '&' + 'billing_address=' + p_billing_address + '&' +
                    'billing_city=' + p_billing_city + '&' + 'billing_state=' + p_billing_state + '&' +
                    'billing_zip=' + p_billing_zip + '&' + 'billing_country=' + p_billing_country + '&' +
                    'billing_tel=' + p_billing_tel + '&' + 'billing_email=' + p_billing_email + '&' +

                    'delivery_name=' + p_delivery_name + '&' + 'delivery_address=' + p_delivery_address + '&' +
                    'delivery_city=' + p_delivery_city + '&' + 'delivery_state=' + p_delivery_state + '&' +
                    'delivery_zip=' + p_delivery_zip + '&' + 'delivery_country=' + p_delivery_country + '&' +
                    'delivery_tel=' + p_delivery_tel + '&' + 'merchant_param1=' + p_merchant_param1 + '&' +
                    'merchant_param2=' + p_merchant_param2 + '&' + 'merchant_param3=' + p_merchant_param3 + '&' +
                    'merchant_param4=' + p_merchant_param4 + '&' + 'merchant_param5=' + p_merchant_param5 + '&' +
                    'promo_code=' + p_promo_code + '&' + 'customer_identifier=' + p_customer_identifier + '&'
            )

            encryption = encrypt(merchant_data.encode(), encryption_key)

            html_template = f'''\
            <html>
            <head>
            	<title>Sub-merchant checkout page</title>
            	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
            </head>
            <body>
            <form id="nonseamless" method="post" name="redirect" action="https://{payment_gtw_url}/transaction/transaction.do?command=initiateTransaction" > 
            		<input type="hidden" id="encRequest" name="encRequest" value={encryption}>
            		<input type="hidden" name="access_code" id="access_code" value={access_code}>
            		<script language='javascript'>document.redirect.submit();</script>
            </form>    
            </body>
            </html>
            '''

            return HttpResponse(html_template)

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
