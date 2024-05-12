from django.urls import path
from .views import CreateBillView, SubscriptionStatusView, ProvisionalPaymentView, PaymentResponseView

urlpatterns = [
    path('', ProvisionalPaymentView.as_view(), name='payment-provisional'),
    path('create/', CreateBillView.as_view(), name='payment-init'),
    path('response/', PaymentResponseView.as_view(), name='payment-response'),
    path('subscription-status/<int:user_id>/', SubscriptionStatusView.as_view(), name='subscription-status'),
]
