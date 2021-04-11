from django.shortcuts import render
from .models import Cryptocurrency
from .serializers import CryptocurrencySerializer
from rest_framework import generics


class CryptocurrencyList(generics.ListCreateAPIView):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer


class CryptocurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer
