from django.contrib import admin
from .models import Challenge, ChallengeRegistration, Subscription

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display  = ('title', 'is_active', 'is_premium', 'start_date', 'end_date')
    list_filter   = ('is_active', 'is_premium', 'start_date', 'end_date')
    search_fields = ('title', 'description')

@admin.register(ChallengeRegistration)
class ChallengeRegistrationAdmin(admin.ModelAdmin):
    list_display  = ('user', 'challenge', 'joined_at', 'completed')
    list_filter   = ('challenge', 'completed')
    search_fields = ('user__email', 'challenge__title')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display  = ('user', 'challenge', 'status', 'created_at')
    list_filter   = ('status',)
    search_fields = ('user__email', 'challenge__title', 'stripe_subscription_id')
