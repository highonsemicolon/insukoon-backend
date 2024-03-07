from django.shortcuts import render
from rest_framework import generics

from referrals.models import Referral
from referrals.serializers import ReferralSerializer


class ReferralListCreateAPIView(generics.ListCreateAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer


class ReferralRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
