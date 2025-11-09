from django.contrib import admin
from .models import Prediction, MLModel

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['id', 'prediction', 'confidence', 'prediction_type', 'created_at']
    list_filter = ['prediction_type', 'created_at']
    search_fields = ['prediction']

@admin.register(MLModel)
class MLModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'accuracy', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']

# Register your models here.
