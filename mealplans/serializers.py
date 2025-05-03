from rest_framework import serializers
from .models import MealRequest

class MealRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealRequest
        fields = ['id', 'user', 'preferences', 'calories', 'plan', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user', 'plan', 'status', 'created_at', 'updated_at']