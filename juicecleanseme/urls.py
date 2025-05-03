from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Challenges
    # UI routes with distinct application namespace 'challenges_ui'
    path('challenges/', include(('challenges.urls', 'challenges_ui'), namespace='challenges')),
    # API routes with distinct application namespace 'challenges_api'
    path('api/challenges/', include(('challenges.urls', 'challenges_api'), namespace='challenges_api')),

    # Mealplans
    # UI routes with distinct application namespace 'mealplans_ui'
    path('mealplans/', include(('mealplans.urls', 'mealplans_ui'), namespace='mealplans')),
    # API routes with distinct application namespace 'mealplans_api'
    path('api/mealplans/', include(('mealplans.urls', 'mealplans_api'), namespace='mealplans_api')),
]