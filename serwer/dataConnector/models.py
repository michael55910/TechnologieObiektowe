from django.db import models
from coinpaprika import client as Coinpaprika
from binance.client import Client

BinanceClient = Client("y4IYuRu7rcBuBRxbT57hdrUE12UpvMZdzJOdqPGrdS4jTU2oi9onl4bNxvZ6qMEj",
                       "BZ3y4qZ8019zzU6F2hv4WLbDnpeIQMBIuefMHxb1qPeloUayZUbOv1Che8Fzy34C")
CoinpaprikaClient = Coinpaprika.Client()

available_coins = CoinpaprikaClient.coins()


# print(available_coins)


class Cryptocurrency(models.Model):
    #     class CoinType(models.TextChoices):
    #         COIN = 1, 'coin'
    #         TOKEN = 2, 'token'

    COIN_TYPE = (
        ('coin', 'coin'),
        ('token', 'token'),
    )

    id = models.CharField(max_length=50, primary_key=True, blank=False)
    name = models.CharField(max_length=50, blank=False)
    symbol = models.CharField(max_length=10, blank=False)
    rank = models.IntegerField(blank=False)
    is_new = models.BooleanField(blank=False)
    is_active = models.BooleanField(blank=False)
    type = models.CharField(choices=COIN_TYPE, max_length=5, blank=False)

    def str(self):
        return self.name


class Rate(models.Model):
    symbol = models.CharField(max_length=8, blank=False)
    price_change = models.FloatField(blank=False)
    price_change_percent = models.FloatField(blank=False)
    weighted_avg_price = models.FloatField(blank=False)
    prev_close_price = models.FloatField(blank=False)
    last_price = models.FloatField(blank=False)
    last_qty = models.FloatField(blank=False)
    bid_price = models.FloatField(blank=False)
    ask_price = models.FloatField(blank=False)
    open_price = models.FloatField(blank=False)
    high_price = models.FloatField(blank=False)
    low_price = models.FloatField(blank=False)
    volume = models.FloatField(blank=False)
    quote_volume = models.FloatField(blank=False)
    open_time = models.IntegerField(blank=False)
    close_time = models.IntegerField(blank=False)
    first_id = models.IntegerField(blank=False)
    last_id = models.IntegerField(blank=False)
    count = models.IntegerField(blank=False)

    def str(self):
        return self.symbol


class Candle(models.Model):
    open_time = models.BigIntegerField(blank=False, default="0")
    open = models.FloatField(blank=False, default="0")
    high = models.FloatField(blank=False, default="0")
    low = models.FloatField(blank=False, default="0")
    close = models.FloatField(blank=False, default="0")
    volume = models.FloatField(blank=False, default="0")
    close_time = models.BigIntegerField(blank=False, default="0")
    quote_asset_volume = models.FloatField(blank=False, default="0")
    number_of_trades = models.IntegerField(blank=False, default="0")
    taker_buy_base_asset_volume = models.FloatField(blank=False, default="0")
    taker_buy_quote_asset_volume = models.FloatField(blank=False, default="0")
    ignore = models.FloatField(blank=False, default="0")

    def str(self):
        return self.number_of_trades


coins_list = []

for x in available_coins:
    new_coin = Cryptocurrency(id=x['id'], name=x['name'], symbol=x['symbol'], rank=x['rank'],
                              is_new=x['is_new'], is_active=x['is_active'], type=x['type'])
    coins_list.append(new_coin)

# Cryptocurrency.objects.bulk_create(coins_list)
