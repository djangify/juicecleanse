from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MealRequestViewSet,
    MealRequestListView, MealRequestDetailView, MealRequestCreateView
)


router = DefaultRouter()
router.register(r'', MealRequestViewSet, basename='mealrequest')

app_name = 'mealplans'

urlpatterns = [
    # UI routes
    path('', MealRequestListView.as_view(), name='meal_request_list'),
    path('new/', MealRequestCreateView.as_view(), name='meal_request_new'),
    path('<int:pk>/', MealRequestDetailView.as_view(), name='meal_request_detail'),

    # API routes
    path('api/', include(router.urls)),
]