from rest_framework import serializers
from .models import Cryptocurrency, Rate, Candle


class CryptocurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = ('id', 'name', 'symbol', 'rank', 'is_new', 'is_active', 'type')


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ('symbol', 'price_change', 'price_change_percent', 'weighted_avg_price', 'prev_close_price',
                  'last_price', 'last_qty', 'bid_price', 'ask_price', 'open_price', 'high_price', 'low_price',
                  'volume', 'quote_volume', 'open_time', 'close_time', 'first_id', 'last_id', 'count')


class CandleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candle
        fields = ('open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume',
                  'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore')
