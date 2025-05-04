# accounts/views.py

import stripe
from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomSignupForm, LoginForm
from .models import Subscription
from .tasks import send_welcome_to_premium_email

# Configure Stripe with your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


def signup_view(request):
    """
    Display & process the signup form.
    """
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = CustomSignupForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """
    Display & process the login form.
    """
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    Log the user out.
    """
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """
    Display the user's profile. Superusers bypass subscription check.
    """
    user = request.user
    if not user.is_superuser and not user.profile.has_active_subscription():
        return render(request, 'accounts/no_subscription.html')

    subscriptions = None
    if not user.is_superuser:
        subscriptions = Subscription.objects.filter(user=user, active=True)

    return render(request, 'accounts/profile.html', {
        'subscriptions': subscriptions
    })


@login_required
def subscribe_view(request):
    """
    Create a Stripe Checkout Session for a subscription.
    """
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.user.email,
        line_items=[{
            'price': 'PRICE_ID_FROM_STRIPE',
            'quantity': 1
        }],
        mode='subscription',
        success_url=f"{settings.DOMAIN}/accounts/profile/",
        cancel_url=f"{settings.DOMAIN}/accounts/profile/",
    )
    return redirect(session.url)


@csrf_exempt
def stripe_webhook(request):
    """
    Handle incoming Stripe webhooks.
    """
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
        email = session.get('customer_email')

        # Look up the corresponding Django user
        from django.contrib.auth.models import User
        user = User.objects.filter(email=email).first()

        if user:
            # Create the subscription record
            Subscription.objects.create(
                user=user,
                plan_name=session['display_items'][0]['plan']['nickname'],
                active=True,
                manage_url=session['subscription']  # or billing portal URL
            )
            # Send the welcome email asynchronously
            send_welcome_to_premium_email.delay(user.id)

    return HttpResponse(status=200)
