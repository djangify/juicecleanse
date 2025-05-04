from django.contrib import admin
from .models import MealRequest

@admin.register(MealRequest)
class MealRequestAdmin(admin.ModelAdmin):
    list_display  = ('id', 'user', 'status', 'created_at')
    list_filter   = ('status', 'created_at')
    search_fields = ('user__email', 'preferences')
    ordering = ('-created_at',)
    list_editable = ('status',)