from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MealRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_requests')
    preferences = models.TextField(help_text="Dietary preferences, allergies, etc.")
    calories = models.PositiveIntegerField(null=True, blank=True)
    plan = models.TextField(blank=True, null=True, help_text="Generated meal plan")
    status = models.CharField(max_length=20, choices=[('pending','Pending'),('completed','Completed'),('failed','Failed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"MealRequest #{self.id} by {self.user.email}"
    