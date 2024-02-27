from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SchoolProfile, ParentProfile
from .serializers import ParentProfileSerializer, SchoolProfileSerializer


class UserProfileView(APIView):

    def get(self, request):
        user = request.user
        return Response({'username': user.username, "user": user.email}, status=status.HTTP_200_OK)


class ParentProfileDetailView(APIView):
    def get(self, request):
        user = request.user  # Assuming the user is authenticated
        try:
            profile = ParentProfile.objects.get(user=user)
            serializer = ParentProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ParentProfile.DoesNotExist:
            return Response({"error": "Parent profile does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        profile, created = ParentProfile.objects.get_or_create(user=user)
        serializer = ParentProfileSerializer(profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = SchoolProfile.objects.all()
    serializer_class = SchoolProfileSerializer
