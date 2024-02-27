from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ParentProfile, SchoolProfile
from .serializers import ParentProfileSerializer, SchoolProfileSerializer


class UserProfileView(APIView):

    def get(self, request):
        user = request.user
        return Response({'username': user.username}, status=status.HTTP_200_OK)


class ParentProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = ParentProfile.objects.all()
    serializer_class = ParentProfileSerializer


class SchoolProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = SchoolProfile.objects.all()
    serializer_class = SchoolProfileSerializer
