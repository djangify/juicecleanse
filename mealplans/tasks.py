from celery import shared_task
from django.utils import timezone
from .models import MealRequest
from .services import OpenAIService

@shared_task
def process_meal_request(request_id: int):
    """
    Fetch and process a MealRequest by ID, calling the OpenAI stub,
    saving the plan, and updating status.
    """
    try:
        req = MealRequest.objects.get(pk=request_id)
        plan_text = OpenAIService.generate_meal_plan(req.preferences, req.calories)
        req.plan = plan_text
        req.status = 'completed'
        req.updated_at = timezone.now()
        req.save()
    except MealRequest.DoesNotExist:
        # optionally log or ignore
        pass