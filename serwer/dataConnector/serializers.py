from rest_framework import serializers
from .models import Cryptocurrency


class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = ('id', 'name', 'symbol', 'rank', 'is_new', 'is_active', 'type')
