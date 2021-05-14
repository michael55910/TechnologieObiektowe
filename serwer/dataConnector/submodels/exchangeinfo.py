from django.db import models
from binance.client import Client

BinanceClient = Client("y4IYuRu7rcBuBRxbT57hdrUE12UpvMZdzJOdqPGrdS4jTU2oi9onl4bNxvZ6qMEj",
                       "BZ3y4qZ8019zzU6F2hv4WLbDnpeIQMBIuefMHxb1qPeloUayZUbOv1Che8Fzy34C")


class ExchangeInfo(models.Model):
    symbol = models.CharField(max_length=20, primary_key=True)
    status = models.CharField(max_length=20, blank=False)
    base_asset = models.CharField(max_length=20, blank=False)
    base_asset_precision = models.IntegerField(blank=False, default="0")
    quote_asset = models.CharField(max_length=20, blank=False)
    quote_precision = models.IntegerField(blank=False, default="0")
    quote_asset_precision = models.IntegerField(blank=False, default="0")

    def str(self):
        return self.symbol


def update_exchanges():
    print("ExchangeInfo update start")
    print("Fetching data from API")

    exchange_info = BinanceClient.get_exchange_info()
    symbols = exchange_info['symbols']

    exchange_list = []

    for symbol in symbols:
        new_exchange = ExchangeInfo(symbol=symbol['symbol'], status=symbol['status'], base_asset=symbol['baseAsset'],
                                    base_asset_precision=symbol['baseAssetPrecision'], quote_asset=symbol['quoteAsset'],
                                    quote_precision=symbol['quotePrecision'],
                                    quote_asset_precision=symbol['quoteAssetPrecision'])
        exchange_list.append(new_exchange)

    print("Inserting data to database")

    ExchangeInfo.objects.bulk_create(exchange_list, ignore_conflicts=True)

    print("ExchangeInfo updated successfully!")
