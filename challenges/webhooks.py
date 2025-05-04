import stripe
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        user = get_user_model().objects.get(email=session.customer_email)
        sub = stripe.Subscription.retrieve(session.subscription)
        Subscription.objects.update_or_create(
            user=user,
            challenge_id=session.client_reference_id,  # if you passed it
            defaults={
                'stripe_customer_id': session.customer,
                'stripe_subscription_id': sub.id,
                'status': sub.status,
            }
        )
    # handle other events (updated, canceled) as needed

    return HttpResponse(status=200)
