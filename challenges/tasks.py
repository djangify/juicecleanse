from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Challenge, ChallengeRegistration

@shared_task
def send_daily_reminders():
    """
    Runs daily via Celery Beat: finds active challenges for today and emails all registered users
    who haven't yet completed their daily task.
    """
    today = timezone.now().date()
    # Query active challenges running today
    challenges = Challenge.objects.filter(
        is_active=True,
        start_date__lte=today,
        end_date__gte=today
    )
    for challenge in challenges:
        # For each user registered and not completed
        regs = ChallengeRegistration.objects.filter(
            challenge=challenge,
            completed=False
        )
        for reg in regs:
            user = reg.user
            # Subject of the reminder email
            subject = f"Reminder: '{challenge.title}' Challenge for {today}"
            # This is the email body/message you asked about:
            message = (
                f"Hi {user.get_full_name() or user.email},\n"
                f"Don't forget to complete today's tasks for the '{challenge.title}' challenge!"
            )
            # send_mail sends the email using your SMTP settings
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
                )