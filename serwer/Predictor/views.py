from django.http import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.generics import ListAPIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from Predictor.models import PredictionType, get_available_prediction_models
from Predictor.serializers import PredictionTypeSerializer, PredictionModelSerializer
from Predictor.service import Learning
from dataConnector.submodels import Candle


# @csrf_exempt
# @method_decorator(require_http_methods(["POST"]), name='dispatch')
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
