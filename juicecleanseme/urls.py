from django.urls import path, include
from challenges.webhooks import stripe_webhook
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('blog/', include('blog.urls')),
    # Core landing page
    path('', include(('core.urls', 'core'), namespace='core')),


    # Authentication (login, logout, password change, etc.)
    # path('accounts/', include('django.contrib.auth.urls')),

    # Challenges
    path('challenges/', include(('challenges.urls', 'challenges_ui'), namespace='challenges')),
    path('api/challenges/', include(('challenges.urls', 'challenges_api'), namespace='challenges_api')),

    # Mealplans
    path('mealplans/', include(('mealplans.urls', 'mealplans_ui'), namespace='mealplans')),
    path('api/mealplans/', include(('mealplans.urls', 'mealplans_api'), namespace='mealplans_api')),

    # Webhooks
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
]