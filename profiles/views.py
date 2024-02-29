from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SchoolProfile, ParentProfile
from .serializers import ParentProfileSerializer, SchoolProfileSerializer


class UserProfileView(APIView):

    def get(self, request):
        user = request.user
        return Response({'username': user.username, "user": user.email}, status=status.HTTP_200_OK)


class ProfileDetailView(APIView):
    profile_model = None
    serializer_class = None

    def get_profile(self, user):
        try:
            print(self.profile_model.objects.get(user_id=user.id))
            return self.profile_model.objects.get(user_id=user.id)
        except self.profile_model.DoesNotExist:
            return None

    def get(self, request):
        user = request.user
        profile = self.get_profile(user)
        if profile is None:
            return Response({"error": f"{self.profile_model.__name__} profile does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            profile = self.profile_model.objects.get(user=user)
            serializer = self.serializer_class(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except self.profile_model.DoesNotExist:
            return Response({"error": f"{self.profile_model.__name__} profile does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        profile = self.get_profile(user)
        if profile is None:
            return Response({"error": f"{self.profile_model.__name__} profile does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            profile, created = self.profile_model.objects.get_or_create(user_id=user.id)
            serializer = self.serializer_class(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.validated_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except self.profile_model.DoesNotExist:
            return Response({"error": f"{self.profile_model.__name__} profile does not exist"},
                            status=status.HTTP_404_NOT_FOUND)


class ParentProfileDetailView(ProfileDetailView):
    profile_model = ParentProfile
    serializer_class = ParentProfileSerializer

    def get_profile(self, user):
        profile = super().get_profile(user)
        if profile is None:
            return None
        if profile.user != user:
            return None
        return profile


class SchoolProfileDetailView(ProfileDetailView):
    profile_model = SchoolProfile
    serializer_class = SchoolProfileSerializer

    def get_profile(self, user):
        profile = super().get_profile(user)
        if profile is None:
            return None
        if profile.user != user:
            return None
        return profile
