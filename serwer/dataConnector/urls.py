from django.urls import path
from dataConnector import views

urlpatterns = [
    path('candles', views.CandlesList.as_view()),
    path('pairs', views.PairsList.as_view()),
    path('intervals', views.IntervalsList.as_view()),
    path('line', views.LineValuesList.as_view()),
    path('cryptocurrency/', views.CryptocurrencyList.as_view()),
    path('cryptocurrency/<int:pk>/', views.CryptocurrencyDetail.as_view()),
    path('exchangeinfo/', views.ExchangeInfoList.as_view()),
    path('exchangeinfo/<int:pk>/', views.ExchangeInfoDetail.as_view()),
    path('rate/', views.RateList.as_view()),
    path('rate/<int:pk>/', views.RateDetail.as_view()),
    path('candle/<int:pk>/', views.CandleDetail.as_view()),
    path('cryptocurrencyupdate/', views.CryptocurrencyUpdate.as_view()),
    path('exchangeinfoupdate/', views.ExchangeInfoUpdate.as_view()),
    path('rateupdate/', views.RateUpdate.as_view()),
    path('candleupdate/', views.CandleUpdate.as_view()),
]
