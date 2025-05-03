from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Challenge(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ChallengeRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_registrations')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='registrations')
    joined_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'challenge')

    def __str__(self):
        return f"{self.user.email} - {self.challenge.title}"