from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
from .views import CreateCheckoutSessionView
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
    # subscribe to challenge
     path('<int:pk>/subscribe/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('checkout/success/<int:pk>/', TemplateView.as_view(template_name='checkout/checkout_success.html'), name='checkout_success'),
    path('checkout/cancel/', TemplateView.as_view(template_name='checkout/checkout_cancel.html'), name='checkout_cancel'),

    # API routes
    path('api/', include(router.urls)),
]