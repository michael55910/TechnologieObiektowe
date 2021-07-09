from django.urls import path
from Predictor import views

urlpatterns = [
    path('learn', views.LearnModel.as_view()),
    path('predictionmethods', views.PredictionMethods.as_view()),
]
