from django.shortcuts import render
from .models import Cryptocurrency, Rate, Candle
from .serializers import CryptocurrencySerializer, RateSerializer, CandleSerializer
from rest_framework import generics


class CryptocurrencyList(generics.ListCreateAPIView):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer


class CryptocurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer


class RateList(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class CandleList(generics.ListCreateAPIView):
    queryset = Candle.objects.all()
    serializer_class = CandleSerializer


class CandleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candle.objects.all()
    serializer_class = CandleSerializer
