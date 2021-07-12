from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from Predictor.models import PredictionType, get_available_prediction_models, PredictedData, Prediction
from Predictor.serializers import PredictionTypeSerializer, PredictionModelSerializer, PredictionSerializer, \
    PredictedDataSerializer
from Predictor.service import Learning, predict_using_mlr_with_windows
from dataConnector.submodels import Candle, update_candles


# @csrf_exempt
# @method_decorator(require_http_methods(["POST"]), name='dispatch')
from dataConnector.views import CandlesPagination


class LearnModel(APIView):
    def post(self, request):
        params = JSONParser().parse(request)
        symbol = params['symbol']
        interval = params['interval']
        window_size = params['windowSize']
        prediction_size = params['predictionSize']
        method = params['predictionMethod']
        if symbol is None or interval is None or window_size is None or prediction_size is None or method is None:
            return HttpResponseBadRequest()
        if interval not in set(item[0] for item in Candle.KLINE_INTERVAL):
            return HttpResponseBadRequest()
        if method not in set(item.value for item in PredictionType):
            return HttpResponseBadRequest()

        update_candles(symbol=symbol, interval=interval)
        learning = Learning(pair_symbol=symbol, interval=interval, window_size=window_size,
                            response_size=prediction_size)
        learning.learn(method)
        return Response(status=status.HTTP_200_OK)


class PredictionMethods(ListAPIView):
    queryset = PredictionType
    serializer_class = PredictionTypeSerializer


class PredictionModels(ListAPIView):
    queryset = get_available_prediction_models()
    serializer_class = PredictionModelSerializer


class AvailablePredictionsList(ListAPIView):
    queryset = Prediction.objects.all().order_by('-prediction_time')
    serializer_class = PredictionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['symbol', 'interval']

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('symbol') is None or request.GET.get('interval') is None:
            return HttpResponseBadRequest()
        if not request.GET.get('interval') in set((item[0] for item in Candle.KLINE_INTERVAL)):
            return HttpResponseBadRequest()
        response = super().dispatch(request, *args, **kwargs)
        return response


class PredictedDataList(ListAPIView):
    queryset = PredictedData.objects.all().order_by('-close_time')
    serializer_class = PredictedDataSerializer
    pagination_class = CandlesPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prediction']

    def dispatch(self, request, *args, **kwargs):
        if request.GET.get('prediction') is None:
            return HttpResponseBadRequest()
        response = super().dispatch(request, *args, **kwargs)
        return response


class Predict(APIView):
    def post(self, request):
        params = JSONParser().parse(request)
        symbol = params['symbol']
        interval = params['interval']
        prediction_model = params['predictionModel']
        if symbol is None or interval is None or prediction_model is None:
            return HttpResponseBadRequest()
        if interval not in set(item[0] for item in Candle.KLINE_INTERVAL):
            return HttpResponseBadRequest()
        if prediction_model + '.pkl' not in get_available_prediction_models():
            return HttpResponseBadRequest()
        predict_using_mlr_with_windows(symbol=symbol, interval=interval, prediction_model=prediction_model)
        return Response(status=status.HTTP_200_OK)
