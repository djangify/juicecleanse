import stripe
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomSignupForm, LoginForm
from .models import Subscription
from .tasks import send_welcome_to_premium_email

stripe.api_key = settings.STRIPE_SECRET_KEY

# Signup, Login, Logout, Profile (as before)
# ... existing signup_view, login_view, logout_view, profile_view ...

def subscribe_view(request):
    domain = settings.DOMAIN
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.user.email,
        line_items=[{
            'price': 'PRICE_ID_FROM_STRIPE',
            'quantity': 1,
        }],
        mode='subscription',
        success_url=f"{domain}/accounts/profile/",
        cancel_url=f"{domain}/accounts/profile/",
    )
    return redirect(session.url)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        email = session.get('customer_email')
        user = stripe.Customer.list(email=email).data[0] if email else None
        # Alternatively, query your User by email
        from django.contrib.auth.models import User
        user = User.objects.filter(email=email).first()
        if user:
            # Create or update subscription record
            Subscription.objects.create(
                user=user,
                plan_name=session['display_items'][0]['plan']['nickname'],
                active=True,
                manage_url=session['subscription']['latest_invoice'] # or billing portal URL
            )
            send_welcome_to_premium_email.delay(user.id)
    return HttpResponse(status=200)