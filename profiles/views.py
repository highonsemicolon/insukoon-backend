from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import CustomUser
from .models import SchoolProfile, ParentProfile
from .serializers import ParentProfileSerializer, SchoolProfileSerializer


class ProfileDetailView(APIView):
    profile_model = None
    serializer_class = None

    def get_profile(self, user):
        try:
            custom_user = CustomUser.objects.get(id=user.id)
            user_type = custom_user.role

            if user_type == 'parent':
                self.profile_model = ParentProfile
                self.serializer_class = ParentProfileSerializer
            else:
                self.profile_model = SchoolProfile
                self.serializer_class = SchoolProfileSerializer

            return self.profile_model.objects.get(user_id=user.id)
        except self.profile_model.DoesNotExist:
            return None

    def get(self, request):
        user = request.user
        profile = self.get_profile(user)
        if profile is None or profile.user != user:
            return Response({"error": f"{self.profile_model.__name__} profile does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        profile = self.get_profile(user)
        if profile is None or profile.user != user:
            return Response({"error": f"{self.profile_model.__name__} profile does not exist"},
                            status=status.HTTP_404_NOT_FOUND)

        new_username = request.data.get('username', None)

        # Update username if provided
        if new_username is not None:
            if new_username != user.username:
                if CustomUser.objects.filter(username=new_username).exists():
                    return Response({"error": f"{new_username} already exists"}, status=status.HTTP_400_BAD_REQUEST)

                user.username = new_username
                user.save()

        serializer = self.serializer_class(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
