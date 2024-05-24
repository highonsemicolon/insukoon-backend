import os
from decimal import Decimal
from urllib.parse import parse_qs

from dateutil import parser as date_parser
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser as User
from profiles.models import SchoolProfile
from referrals.models import Referral, Referrer
from .models import Order, Pricing, ProvisionalOrder
from .serializers import PaymentGatewayResponseSerializer, ProvisionalPaymentSerializer, PricingSerializer
from .utils import encrypt, decrypt

merchant_id = os.environ.get('MERCHANT_ID')
access_code = os.getenv('ACCESS_CODE')
encryption_key = os.getenv('ENCRYPTION_KEY')
redirect_url = os.getenv('PAYMENT_REDIRECT_URL')
cancel_url = os.getenv('PAYMENT_CANCEL_URL')
payment_gtw_url = os.getenv('PAYMENT_GTW_URL')


class PricingList(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer


class CreateBillView(APIView):
    def put(self, request):
        try:
            try:
                order_id = request.data.pop('order_id', None)
                if order_id is None:
                    return Response({'error': 'order_id is missing'}, status=status.HTTP_404_NOT_FOUND)
                provisional_order = ProvisionalOrder.objects.get(id=order_id)
            except ProvisionalOrder.DoesNotExist as e:
                return Response({'error': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)
            if provisional_order is None or provisional_order.user != request.user:
                return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

            price = provisional_order.amount
            currency = provisional_order.currency
            amount = price * provisional_order.quantity

            txn = Order.objects.create(provisional_order=provisional_order, status='pending', insukoon_user_id=request.user.id)
            p_merchant_id = str(merchant_id)
            p_order_id = str(txn.id)
            p_currency = currency
            p_amount = str(amount)
            p_redirect_url = redirect_url
            p_cancel_url = cancel_url
            p_language = 'EN'
            p_customer_identifier = str(request.user.id) + '-' + request.user.username

            p_billing_name = ''
            p_billing_address = ''
            p_billing_city = ''
            p_billing_state = ''
            p_billing_zip = ''
            p_billing_country = ''
            p_billing_tel = ''
            p_billing_email = request.user.email

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
    def get(self, request):
        try:
            user = request.user
            return Response({"has_subscription": user.is_paid})
        except User.DoesNotExist:
            return Response({"error": "No subscription found"}, status=404)


class ProvisionalPaymentView(APIView):
    def put(self, request):
        serializer = ProvisionalPaymentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        plan = serializer.validated_data['plan']
        referral_code = serializer.validated_data.get('referral_code')

        user = request.user
        country = user.country
        role = user.role.lower()

        # Check if referral code exists
        if referral_code:
            try:
                referrer = Referrer.objects.get(code=referral_code)
                Referral.objects.create(referrer=referrer, referred_user=user)
            except:
                return Response({'error': 'Invalid referral code'}, status=status.HTTP_400_BAD_REQUEST)

        quantity = 1
        if user.role == 'school':
            quantity = SchoolProfile.objects.filter(user=user).last().total_students

        price, currency = calculate_price(role, country, plan)

        try:
            amount = price * quantity
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_204_NO_CONTENT)

        provisional_order = ProvisionalOrder.objects.create(
            user=user,
            plan=plan,
            amount=amount,
            price=price,
            quantity=quantity,
            currency=currency
        )

        return Response({
            'order_id': provisional_order.id,
            'total_amount': provisional_order.amount,
            'currency': provisional_order.currency,
            'quantity': provisional_order.quantity,
            'price': provisional_order.price,
            'plan': provisional_order.plan,
        }, status=status.HTTP_200_OK)


def calculate_price(role, country, plan):
    try:
        try:
            pricing = Pricing.objects.get(role=role, plan=plan, country=country)
        except Pricing.DoesNotExist:
            # Handle case when pricing is not found
            raise ValueError(f"Pricing not found for the role: {role}, country: {country} and plan: {plan}.")

        price = Decimal(pricing.price)
        currency = pricing.currency

        return price, currency
    except Exception as e:
        # Log or handle the error appropriately
        print(f"An error occurred: {e}")
        return None, None


class PaymentResponseView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
            body_str = request.body.decode('utf-8')
            request_data = QueryDict(body_str)
            dec_resp = decrypt(request_data.get('encResp', ''), encryption_key)
            response = parse_qs(dec_resp)
            data = {k: v[0] for k, v in response.items()}

            if 'trans_date' in data:
                try:
                    data['trans_date'] = date_parser.parse(data['trans_date'])
                except ValueError:
                    return Response({'error': 'Invalid trans_date format'}, status=400)

            serializer = PaymentGatewayResponseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

            order_id = int(data.get('order_id', '0'))
            order = get_object_or_404(Order, id=order_id, status='pending')
            order.status = data.get('order_status', 'pending')
            order.save()
            if order.status == 'Success':
                user = get_object_or_404(User, id=order.insukoon_user_id)
                user.is_paid = True
                user.save()
                return HttpResponseRedirect('https://www.insukoon.com/setpassword', content_type='text/html')
            else:
                return HttpResponseRedirect(request.META.get('HOST', 'https://www.insukoon.com'),
                                            content_type='text/html')

        return Response({'error': 'something went wrong'}, content_type='text/html', status=400)
