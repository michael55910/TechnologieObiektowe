from django.db import models
from coinpaprika import client as Coinpaprika
from binance.client import Client
import schedule, time

BinanceClient = Client("y4IYuRu7rcBuBRxbT57hdrUE12UpvMZdzJOdqPGrdS4jTU2oi9onl4bNxvZ6qMEj",
                       "BZ3y4qZ8019zzU6F2hv4WLbDnpeIQMBIuefMHxb1qPeloUayZUbOv1Che8Fzy34C")
CoinpaprikaClient = Coinpaprika.Client()

available_coins = CoinpaprikaClient.coins()

exchange_info = BinanceClient.get_exchange_info()

print(exchange_info)


class ExchangeInfo(models.Model):
    timezone = models.CharField(max_length=3, blank=False)
    server_time = models.BigIntegerField(blank=False, default="0")
    symbol = models.CharField(max_length=20, primary_key=True, blank=False)
    status = models.CharField(max_length=20, blank=False)
    base_asset = models.IntegerField(blank=False, default="0")
    base_asset_precision = models.IntegerField(blank=False, default="0")
    quote_asset = models.IntegerField(blank=False, default="0")
    quote_precision = models.IntegerField(blank=False, default="0")
    quote_asset_precision = models.IntegerField(blank=False, default="0")

    def str(self):
        return self.symbol


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
    symbol = models.ForeignKey(ExchangeInfo, on_delete=models.CASCADE)
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
    open_time = models.BigIntegerField(blank=False)
    close_time = models.BigIntegerField(blank=False)
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

def update_rates():
    exchange_rates = BinanceClient.get_ticker()

    exchange_list = []

    for x in exchange_rates:
        new_rate = Rate(symbol=x['symbol'], price_change=x['priceChange'],
                        price_change_percent=x['priceChangePercent'], weighted_avg_price=x['weightedAvgPrice'],
                        prev_close_price=x['prevClosePrice'], last_price=x['lastPrice'], last_qty=x['lastQty'],
                        bid_price=x['bidPrice'], ask_price=x['askPrice'], open_price=x['openPrice'],
                        high_price=x['highPrice'], low_price=x['lowPrice'], volume=x['volume'],
                        quote_volume=x['quoteVolume'], open_time=x['openTime'], close_time=x['closeTime'],
                        first_id=x['firstId'], last_id=x['lastId'], count=x['count'])
        exchange_list.append(new_rate)

    Rate.objects.bulk_create(exchange_list)
    print("Exchange rates updated successfully!")


def update_candles():
    candles = BinanceClient.get_historical_klines("BNBBTC", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

    candle_list = []

    for x in candles:
        new_candle = Candle(open_time=x[0], open=x[1], high=x[2], low=x[3],
                            close=x[4], volume=x[5], close_time=x[6],
                            quote_asset_volume=x[7], number_of_trades=x[8],
                            taker_buy_base_asset_volume=x[9], taker_buy_quote_asset_volume=x[10],
                            ignore=x[11])
        candle_list.append(new_candle)

    Candle.objects.bulk_create(candle_list)
    print("Candles updated successfully!")


# schedule.every(5).seconds.do(update_rates)
# schedule.every(5).seconds.do(update_candles)

# schedule.every().day.at("10:00").do(update_rates)
# schedule.every().day.at("10:00").do(update_candles)
"""
while True:
    schedule.run_pending()
    time.sleep(1)
"""
