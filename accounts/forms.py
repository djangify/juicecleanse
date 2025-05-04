from django import forms
from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    dietary_preferences = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'class': 'border rounded w-full p-2', 'placeholder': 'Dietary preferences'})
    )

    def save(self, request):
        user = super().save(request)
        user.profile.dietary_preferences = self.cleaned_data['dietary_preferences']
        user.profile.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'border rounded w-full p-2',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'border rounded w-full p-2',
        'placeholder': 'Password'
    }))