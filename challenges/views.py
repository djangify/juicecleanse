from rest_framework import viewsets, permissions
from django.views.generic import ListView, DetailView, CreateView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Challenge, ChallengeRegistration
from .serializers import ChallengeSerializer, ChallengeRegistrationSerializer

# API ViewSets
class ChallengeViewSet(viewsets.ModelViewSet):
    queryset = Challenge.objects.filter(is_active=True)
    serializer_class = ChallengeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ChallengeRegistrationViewSet(viewsets.ModelViewSet):
    queryset = ChallengeRegistration.objects.all()
    serializer_class = ChallengeRegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Template Views
class ChallengeListView(ListView):
    model = Challenge
    template_name = 'challenges/challenge_list.html'
    context_object_name = 'challenges'

class ChallengeDetailView(DetailView):
    model = Challenge
    template_name = 'challenges/challenge_detail.html'
    context_object_name = 'challenge'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['registered'] = False
        if user.is_authenticated:
            context['registered'] = ChallengeRegistration.objects.filter(user=user, challenge=self.object).exists()
        return context

class ChallengeRegisterView(LoginRequiredMixin, View):
    def post(self, request, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        ChallengeRegistration.objects.get_or_create(user=request.user, challenge=challenge)
        return redirect('challenge_detail', pk=pk)