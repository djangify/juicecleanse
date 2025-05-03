from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MealRequestViewSet,
    MealRequestListView, MealRequestDetailView, MealRequestCreateView
)

app_name = 'mealplans'

router = DefaultRouter()
router.register(r'', MealRequestViewSet, basename='mealrequest')

urlpatterns = [
    # UI routes
    path('', MealRequestListView.as_view(), name='meal_request_list'),
    path('new/', MealRequestCreateView.as_view(), name='meal_request_new'),
    path('<int:pk>/', MealRequestDetailView.as_view(), name='meal_request_detail'),

    # API routes
    path('api/', include(router.urls)),
]