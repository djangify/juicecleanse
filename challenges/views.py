from rest_framework import viewsets, permissions
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.conf import settings
import stripe

from .models import Challenge, ChallengeRegistration, Subscription
from .serializers import ChallengeSerializer, ChallengeRegistrationSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY

# -- API ViewSets --

class ChallengeViewSet(viewsets.ModelViewSet):
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Challenge.objects.filter(is_active=True)
        if not self.request.user.is_authenticated:
            return qs.filter(is_premium=False)
        is_subscribed = Subscription.objects.filter(
            user=self.request.user, status='active'
        ).exists()
        return qs if is_subscribed else qs.filter(is_premium=False)

class ChallengeRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ChallengeRegistration.objects.all()
    serializer_class = ChallengeRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# -- Template Views --

class ChallengeListView(ListView):
    model = Challenge
    template_name = 'challenges/challenge_list.html'
    context_object_name = 'challenges'

    def get_queryset(self):
        qs = super().get_queryset().filter(is_active=True)
        if not self.request.user.is_authenticated:
            return qs.filter(is_premium=False)
        is_subscribed = Subscription.objects.filter(
            user=self.request.user, status='active'
        ).exists()
        return qs if is_subscribed else qs.filter(is_premium=False)

class ChallengeDetailView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_detail.html'
    context_object_name = 'challenge'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['registered'] = (
            user.is_authenticated and
            ChallengeRegistration.objects.filter(user=user, challenge=self.object).exists()
        )
        return ctx

class ChallengeRegisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        challenge = get_object_or_404(Challenge, pk=pk, is_premium=False)
        ChallengeRegistration.objects.get_or_create(user=request.user, challenge=challenge)
        return redirect('challenges:challenge_detail', pk=pk)

class CreateCheckoutSessionView(LoginRequiredMixin, View):
    def post(self, request, pk):
        challenge = get_object_or_404(Challenge, pk=pk, is_premium=True)
        user = request.user

        # Ensure Stripe Customer
        if not getattr(user, 'stripe_customer_id', None):
            customer = stripe.Customer.create(email=user.email)
            user.stripe_customer_id = customer.id
            user.save()
        customer_id = user.stripe_customer_id

        session = stripe.checkout.Session.create(
            customer=customer_id,
            payment_method_types=['card'],
            line_items=[{'price': challenge.stripe_price_id, 'quantity': 1}],
            mode='subscription',
            success_url=request.build_absolute_uri(
                reverse('challenges:checkout_success')
            ),
            cancel_url=request.build_absolute_uri(
                reverse('challenges:checkout_cancel')
            ),
        )
        return redirect(session.url)
