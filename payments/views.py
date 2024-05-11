import os
from decimal import Decimal

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser as User
from .models import Transaction, Pricing
from .utils import encrypt

merchant_id = os.environ.get('MERCHANT_ID')
access_code = os.getenv('ACCESS_CODE')
encryption_key = os.getenv('ENCRYPTION_KEY')
redirect_url = os.getenv('PAYMENT_REDIRECT_URL')
cancel_url = os.getenv('PAYMENT_CANCEL_URL')
payment_gtw_url = os.getenv('PAYMENT_GTW_URL')


def extract_plan_from_request(request):
    try:
        plan = request.data['plan']
    except KeyError:
        return None, Response({'error': 'Plan is missing'}, status=400)

    if not plan:
        return None, Response({'error': 'Plan cannot be empty'}, status=400)

    return plan, None


class CreateBillView(APIView):
    def put(self, request):
        try:
            plan, error_response = extract_plan_from_request(request)
            if error_response:
                return error_response
            country = request.user.country
            role = request.user.role.capitalize()
            amount, currency = calculate_total_price(role, country, plan)

            txn = Transaction.objects.create(user_id=request.user.id, currency=currency, amount=amount,
                                             status='pending')

            p_merchant_id = str(merchant_id)
            p_order_id = str(txn.id)
            p_currency = currency
            p_amount = str(amount)
            p_redirect_url = redirect_url
            p_cancel_url = cancel_url
            p_language = 'EN'
            p_customer_identifier = str(request.user.id)

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
            has_subscription = Transaction.objects.filter(user=user).exists()
            return Response({"has_subscription": has_subscription})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class ProvisionalPaymentView(APIView):
    def get(self, request):
        plan, error_response = extract_plan_from_request(request)
        if error_response:
            return error_response

        country = request.user.country
        role = request.user.role.capitalize()
        amount, currency = calculate_total_price(role, country, plan)
        return Response({'amount': amount, 'currency': currency}, status=200)


def calculate_total_price(role, country, plan):
    try:
        try:
            pricing = Pricing.objects.get(role=role, plan=plan, country=country)
        except Pricing.DoesNotExist:
            # Handle case when pricing is not found
            raise ValueError(f"Pricing not found for the role: {role}, country: {country} and plan: {plan}.")

        amount = Decimal(pricing.price)
        currency = pricing.currency

        return amount, currency
    except Exception as e:
        # Log or handle the error appropriately
        print(f"An error occurred: {e}")
        return None, None
