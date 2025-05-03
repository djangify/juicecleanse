from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChallengeViewSet, ChallengeRegistrationViewSet,
    ChallengeListView, ChallengeDetailView, ChallengeRegisterView
)

app_name = 'challenges'
# Ensure the app name is set for namespacing

# API router
router = DefaultRouter()
router.register(r'', ChallengeViewSet, basename='challenge')
router.register(r'registrations', ChallengeRegistrationViewSet, basename='registration')

urlpatterns = [
    # UI routes (prefixed in project urls)
    path('', ChallengeListView.as_view(), name='challenge_list'),
    path('<int:pk>/', ChallengeDetailView.as_view(), name='challenge_detail'),
    path('<int:pk>/register/', ChallengeRegisterView.as_view(), name='challenge_register'),

    # API routes
    path('api/', include(router.urls)),
]