from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from dataConnector import views

urlpatterns = [
    path('cryptocurrency/', views.CryptocurrencyList.as_view()),
    path('cryptocurrency/<int:pk>/', views.CryptocurrencyDetail.as_view()),
    path('rate/', views.RateList.as_view()),
    path('rate/<int:pk>/', views.RateDetail.as_view()),
    path('candle/', views.CandleList.as_view()),
    path('candle/<int:pk>/', views.CandleDetail.as_view()),
]
