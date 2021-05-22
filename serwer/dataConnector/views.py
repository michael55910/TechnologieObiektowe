from .models import Cryptocurrency, ExchangeInfo, Rate, Candle
from .submodels import update_coins
from .submodels import update_exchanges
from .submodels import update_rates
from .submodels import update_candles
from .serializers import CryptocurrencySerializer, ExchangeInfoSerializer, RateSerializer, CandleSerializer
from rest_framework import generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response


class CryptocurrencyUpdate(APIView):
    def get(self, request, *args, **kwargs):
        return Response(update_coins())


class ExchangeInfoUpdate(APIView):
    def get(self, request, *args, **kwargs):
        return Response(update_exchanges())


class RateUpdate(APIView):
    def get(self, request, *args, **kwargs):
        return Response(update_rates())


class CandleUpdate(APIView):
    def get(self, request, *args, **kwargs):
        return Response(update_candles())


class CryptocurrencyList(generics.ListCreateAPIView):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer


class CryptocurrencyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializer


class ExchangeInfoList(generics.ListCreateAPIView):
    queryset = ExchangeInfo.objects.all()
    serializer_class = ExchangeInfoSerializer


class ExchangeInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExchangeInfo.objects.all()
    serializer_class = ExchangeInfoSerializer


class RateList(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class CandleList(generics.ListCreateAPIView):
    queryset = Candle.objects.all()
    serializer_class = CandleSerializer
    search_fields = ['symbol']
    filter_backends = (filters.SearchFilter,)


class CandleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candle.objects.all()
    serializer_class = CandleSerializer
