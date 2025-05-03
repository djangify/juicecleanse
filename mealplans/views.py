from rest_framework import viewsets, permissions
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MealRequest
from .serializers import MealRequestSerializer
from .forms import MealRequestForm

# API ViewSet
class MealRequestViewSet(viewsets.ModelViewSet):
    queryset = MealRequest.objects.all()
    serializer_class = MealRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Template Views
class MealRequestListView(LoginRequiredMixin, ListView):
    model = MealRequest
    template_name = 'mealplans/meal_request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return MealRequest.objects.filter(user=self.request.user)

class MealRequestDetailView(LoginRequiredMixin, DetailView):
    model = MealRequest
    template_name = 'mealplans/meal_request_detail.html'
    context_object_name = 'request'

class MealRequestCreateView(LoginRequiredMixin, CreateView):
    model = MealRequest
    form_class = MealRequestForm
    template_name = 'mealplans/meal_request_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)