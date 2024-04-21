from django.urls import path
from .views import CreateBillView, SubscriptionStatusView, ProvisionalPaymentView


urlpatterns = [
    path('', ProvisionalPaymentView.as_view(), name='create-bill'),
    path('create/', CreateBillView.as_view(), name='create-bill'),
    path('subscription-status/<int:user_id>/', SubscriptionStatusView.as_view(), name='subscription-status'),
]
