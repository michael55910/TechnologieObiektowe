from django.urls import path
from Predictor import views

urlpatterns = [
    path('learn', views.LearnModel.as_view()),
    path('predictionmethods', views.PredictionMethods.as_view()),
    path('predictionmodels', views.PredictionModels.as_view()),
    path('predictions', views.AvailablePredictionsList.as_view()),
    path('predicteddata', views.PredictedDataList.as_view()),
    path('predict', views.Predict.as_view()),
]
