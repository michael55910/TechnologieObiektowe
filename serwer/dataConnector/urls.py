from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from dataConnector import views

urlpatterns = [
    path('dataConnector/', views.CryptocurrencyList.as_view()),
    path('dataConnector/<int:pk>/', views.CryptocurrencyDetail.as_view()),
]