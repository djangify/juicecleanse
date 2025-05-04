from celery import shared_task
from django.utils import timezone
from .models import MealRequest
from .services import OpenAIService

@shared_task
def process_meal_request(request_id: int):
    """
    Fetches a MealRequest by ID, calls the OpenAI stub, saves the plan, and updates status.
    """
    try:
        req = MealRequest.objects.get(pk=request_id)
        plan_text = OpenAIService.generate_meal_plan(req.preferences, req.calories)
        req.plan = plan_text
        req.status = 'completed'
        req.updated_at = timezone.now()
        req.save()
    except MealRequest.DoesNotExist:
        # handle missing request
        pass