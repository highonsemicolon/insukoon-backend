from django.urls import path

from .views import ParentProfileDetailView, SchoolProfileDetailView, UserProfileView

urlpatterns = [
    path('parent/<str:pk>/', ParentProfileDetailView.as_view(), name='parent-profile-detail'),
    path('school/<str:pk>/', SchoolProfileDetailView.as_view(), name='school-profile-detail'),
    path('', UserProfileView.as_view(), name='profile'),
]
