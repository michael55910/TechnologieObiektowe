from django.db import models
from django.db.models import Max
from .exchangeinfo import ExchangeInfo
from binance.client import Client

BinanceClient = Client("y4IYuRu7rcBuBRxbT57hdrUE12UpvMZdzJOdqPGrdS4jTU2oi9onl4bNxvZ6qMEj",
                       "BZ3y4qZ8019zzU6F2hv4WLbDnpeIQMBIuefMHxb1qPeloUayZUbOv1Che8Fzy34C")


class Candle(models.Model):
    symbol = models.ForeignKey(ExchangeInfo, on_delete=models.CASCADE)
    interval = models.CharField(max_length=3, blank=False)
    open_time = models.BigIntegerField(blank=False, default="0")  # max_length=14
    # open_time = models.DateTimeField(blank=False)
    open = models.DecimalField(blank=False, default="0", decimal_places=8, max_digits=14)
    high = models.DecimalField(blank=False, default="0", decimal_places=8, max_digits=14)
    low = models.DecimalField(blank=False, default="0", decimal_places=8, max_digits=14)
    close = models.DecimalField(blank=False, default="0", decimal_places=8, max_digits=14)
    volume = models.DecimalField(blank=False, default="0", decimal_places=8, max_digits=14)
    close_time = models.BigIntegerField(blank=False, default="0")  # max_length=14
    quote_asset_volume = models.DecimalField(blank=False, default="0", decimal_places=8, max_digits=14)
    number_of_trades = models.IntegerField(blank=False, default="0")
    taker_buy_base_asset_volume = models.DecimalField(blank=False, default="0", decimal_places=8, max_digits=14)
    taker_buy_quote_asset_volume = models.DecimalField(blank=False, default="0", decimal_places=8, max_digits=14)
    is_real = models.BooleanField(blank=False, default=True)

    class Meta:
        unique_together = ('symbol', 'interval', 'open_time', 'close_time', 'is_real')
        get_latest_by = 'open_time'

    def str(self):
        return self.number_of_trades


def update_candles():
    print("Candle update start")

    candle_pairs = ["BNBBTC", "ETHBTC"]

    current_symbol = "BNBBTC"
    interval = Client.KLINE_INTERVAL_1MINUTE

    args_candles = Candle.objects.filter(symbol=current_symbol, interval=interval, is_real=True)
    last_candle = args_candles.aggregate(Max('open_time'))
    if last_candle['open_time__max']:
        max_open_time = last_candle['open_time__max']
    else:
        max_open_time = 0

    if ExchangeInfo.objects.filter(symbol=current_symbol).count() > 0:
        print("Fetching data from API")

        # candles = BinanceClient.get_historical_klines(current_symbol, interval, "1 day ago UTC")
        candles = BinanceClient.get_historical_klines(current_symbol, interval, max_open_time)

        candle_list = []

        current_symbol_fk = ExchangeInfo.objects.get(symbol=current_symbol)
        for x in candles:
            new_candle = Candle(symbol=current_symbol_fk, interval=interval,
                                open_time=x[0],
                                open=x[1], high=x[2], low=x[3], close=x[4], volume=x[5], close_time=x[6],
                                quote_asset_volume=x[7], number_of_trades=x[8],
                                taker_buy_base_asset_volume=x[9], taker_buy_quote_asset_volume=x[10], is_real=True)
            candle_list.append(new_candle)

        print("Inserting data to database")

        Candle.objects.bulk_create(candle_list, ignore_conflicts=True, batch_size=100000)
        print("Candles updated successfully!")
