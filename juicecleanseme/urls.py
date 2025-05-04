# juicecleanse_me/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from challenges.webhooks import stripe_webhook

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts (signup, login, logout, profile, stripe subscribe & webhook)
    path(
        'accounts/',
        include(('accounts.urls', 'accounts'), namespace='accounts')
    ),

    # Blog
    path(
        'blog/',
        include(('blog.urls', 'blog'), namespace='blog')
    ),

    # Core (homepage, about, etc.)
    path(
        '',
        include(('core.urls', 'core'), namespace='core')
    ),

    # Challenges (UI & API)
    path(
        'challenges/',
        include(('challenges.urls', 'challenges_ui'), namespace='challenges')
    ),
    path(
        'api/challenges/',
        include(('challenges.urls', 'challenges_api'), namespace='challenges_api')
    ),

    # Mealplans (UI & API)
    path(
        'mealplans/',
        include(('mealplans.urls', 'mealplans_ui'), namespace='mealplans')
    ),
    path(
        'api/mealplans/',
        include(('mealplans.urls', 'mealplans_api'), namespace='mealplans_api')
    ),

    # Stripe webhook
    path('webhooks/stripe/', stripe_webhook, name='stripe_webhook'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
