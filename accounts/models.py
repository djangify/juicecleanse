# accounts/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dietary_preferences = models.CharField(max_length=100, blank=True)

    def has_active_subscription(self):
        return self.user.account_subscriptions.filter(active=True).exists()

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='account_subscriptions',
        on_delete=models.CASCADE
    )
    plan_name   = models.CharField(max_length=100)
    active      = models.BooleanField(default=True)
    manage_url  = models.URLField(blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.plan_name} ({'Active' if self.active else 'Inactive'})"
