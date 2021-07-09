from abc import ABC

from rest_framework import serializers


class PredictionTypeSerializer(serializers.BaseSerializer, ABC):
    def to_representation(self, instance):
        return {
            'value': instance.value,
            'text': instance.label
        }
