from django import forms
from .models import MealRequest

class MealRequestForm(forms.ModelForm):
    class Meta:
        model = MealRequest
        fields = ['preferences', 'calories']