from django.http import HttpResponseBadRequest
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cryptocurrency, ExchangeInfo, Rate, Candle
from .serializers import CryptocurrencySerializer, ExchangeInfoSerializer, RateSerializer, CandleSerializer, \
    PairsSerializer, IntervalsSerializer, LineValuesSerializer
from .submodels import update_candles
from .submodels import update_coins
from .submodels import update_exchanges
from .submodels import update_rates


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


# class CandleList(generics.ListCreateAPIView):
#     queryset = Candle.objects.all().order_by('-close_time')
#     serializer_class = CandleSerializer
#     search_fields = ['symbol__symbol']
#     filter_backends = (filters.SearchFilter,)


class CandleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candle.objects.all()
    serializer_class = CandleSerializer


class CandlesPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class CandlesSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_terms = self.get_search_terms(request)
        # search_fields = self.get_search_fields(view, request)

        if not search_terms:
            return queryset.none()

            # Alternatively, an error can be raise
            # raise ValidationError(
            #     "%s parameter is required!" % self.search_param
            # )

        # for field in search_fields:
        #     if not search_terms[field]:
        #         return queryset.none()

        return super().filter_queryset(request, queryset, view)


class CandlesList(generics.ListAPIView):
    queryset = Candle.objects.all().order_by('-close_time')  # [:500]
    serializer_class = CandleSerializer
    pagination_class = CandlesPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['symbol', 'interval', 'is_real']
    # ordering_fields = ['-close_time']

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('symbol') is None or request.GET.get('interval') is None:
            return HttpResponseBadRequest()
        if not request.GET.get('interval') in set((item[0] for item in Candle.KLINE_INTERVAL)):
            return HttpResponseBadRequest()
        update_candles(symbol=request.GET.get('symbol'), interval=request.GET.get('interval'))
        response = super().dispatch(request, *args, **kwargs)
        return response


class LineValuesList(generics.ListAPIView):
    queryset = Candle.objects.all().only('close', 'close_time').order_by('-close_time')
    serializer_class = LineValuesSerializer
    pagination_class = CandlesPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['symbol', 'interval', 'is_real']

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('symbol') is None or request.GET.get('interval') is None:
            return HttpResponseBadRequest()
        if not request.GET.get('interval') in set((item[0] for item in Candle.KLINE_INTERVAL)):
            return HttpResponseBadRequest()
        update_candles(symbol=request.GET.get('symbol'), interval=request.GET.get('interval'))
        response = super().dispatch(request, *args, **kwargs)
        return response


class PairsList(generics.ListAPIView):
    queryset = ExchangeInfo.objects.all()
    serializer_class = PairsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['symbol', 'status', 'base_asset__symbol', 'quote_asset__symbol']


class IntervalsList(generics.ListAPIView):
    queryset = Candle.KLINE_INTERVAL
    serializer_class = IntervalsSerializer
