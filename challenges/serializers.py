from rest_framework import serializers
from .models import Challenge, ChallengeRegistration

class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'is_active']

class ChallengeRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeRegistration
        fields = ['id', 'user', 'challenge', 'joined_at', 'completed']
        read_only_fields = ['user', 'joined_at']