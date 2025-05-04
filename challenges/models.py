from django.db import models
from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

User = get_user_model()

class Challenge(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)  # mark premium
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)  # link to Stripe price
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='subscriptions')
    stripe_customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Subscription for {self.user.email} on {self.challenge.title} ({self.status})"

class ChallengeRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_registrations')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='registrations')
    joined_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.email} - {self.challenge.title}"