from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User

@shared_task
def send_welcome_to_premium_email(user_id):
    user = User.objects.get(id=user_id)
    send_mail(
        'Welcome to Premium!',
        'Thank you for subscribing to our premium challenge!',
        'no-reply@juicecleanseme.com',
        [user.email]
    )