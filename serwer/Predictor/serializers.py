from abc import ABC

from rest_framework import serializers

from Predictor.models import Prediction, PredictedData


class PredictionTypeSerializer(serializers.BaseSerializer, ABC):
    def to_representation(self, instance):
        return {
            'value': instance.value,
            'text': instance.label
        }


class PredictionModelSerializer(serializers.BaseSerializer, ABC):
    def to_representation(self, instance):
        return {
            'name': instance.replace('.pkl', '', 1)
        }


class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = ('id', 'symbol', 'interval', 'prediction_model', 'prediction_time')


class PredictedDataSerializer(serializers.BaseSerializer, ABC):
    def to_representation(self, instance):
        return {
            'timestamp': instance.close_time,
            'value': instance.predicted_y
        }