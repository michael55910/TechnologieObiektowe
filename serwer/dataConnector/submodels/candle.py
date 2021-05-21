from django.db import models
from binance.client import Client

BinanceClient = Client("y4IYuRu7rcBuBRxbT57hdrUE12UpvMZdzJOdqPGrdS4jTU2oi9onl4bNxvZ6qMEj",
                       "BZ3y4qZ8019zzU6F2hv4WLbDnpeIQMBIuefMHxb1qPeloUayZUbOv1Che8Fzy34C")


class Candle(models.Model):
    id = models.CharField(max_length=80, primary_key=True)
    symbol = models.CharField(max_length=20, blank=False)
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


def update_candles():
    print("Candle update start")

    candle_pairs = ["BNBBTC"]

    current_symbol = "BNBBTC"
    interval = "1 day ago UTC"

    print("Fetching data from API")

    # candles = BinanceClient.get_historical_klines(current_symbol, Client.KLINE_INTERVAL_1MINUTE, interval)
    candles = BinanceClient.get_historical_klines(current_symbol, Client.KLINE_INTERVAL_1MINUTE, "1 Dec, 2007",
                                                  "12 May, 2021")

    candle_list = []

    for x in candles:
        id = str(x[0]) + current_symbol + interval + str(x[6])

        new_candle = Candle(id=id, symbol=current_symbol, open_time=x[0], open=x[1], high=x[2], low=x[3],
                            close=x[4], volume=x[5], close_time=x[6],
                            quote_asset_volume=x[7], number_of_trades=x[8],
                            taker_buy_base_asset_volume=x[9], taker_buy_quote_asset_volume=x[10],
                            ignore=x[11])
        candle_list.append(new_candle)

    print("Inserting data to database")

    Candle.objects.bulk_create(candle_list, ignore_conflicts=True, batch_size=1000)
    print("Candles updated successfully!")