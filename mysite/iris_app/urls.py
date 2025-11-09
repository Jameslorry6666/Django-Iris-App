
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('predict/', views.predict_iris, name='predict'),
    path('api/predict/', views.api_predict_iris, name='api_predict'),
    path('train/', views.train_model, name='train_model'),
    path('history/',views.prediction_history, name='history'),
]