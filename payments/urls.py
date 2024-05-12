from django.urls import path
from .views import CreateBillView, SubscriptionStatusView, ProvisionalPaymentView, PaymentResponseView, PricingList

urlpatterns = [
    path('', ProvisionalPaymentView.as_view(), name='payment-provisional'),
    path('pricing/', PricingList.as_view(), name='pricing-list'),
    path('create/', CreateBillView.as_view(), name='payment-init'),
    path('response/', PaymentResponseView.as_view(), name='payment-response'),
    path('subscription-status/<int:user_id>/', SubscriptionStatusView.as_view(), name='subscription-status'),
]
