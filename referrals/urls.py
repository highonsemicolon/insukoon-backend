from django.urls import path
from .views import ReferralListCreateAPIView, ReferralRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('', ReferralListCreateAPIView.as_view(), name='referral-list-create'),
    path('<int:pk>/', ReferralRetrieveUpdateDestroyAPIView.as_view(), name='referral-detail'),
]
