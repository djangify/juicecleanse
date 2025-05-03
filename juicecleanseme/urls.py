from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Challenges
    path('api/challenges/', include('challenges.urls')),
    path('challenges/', include('challenges.urls')),

    # Mealplans
    path('api/mealplans/', include('mealplans.urls')),
    path('mealplans/', include('mealplans.urls')),
]