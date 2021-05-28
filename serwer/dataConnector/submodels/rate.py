from django.db import models
from .exchangeinfo import ExchangeInfo
from binance.client import Client

BinanceClient = Client("y4IYuRu7rcBuBRxbT57hdrUE12UpvMZdzJOdqPGrdS4jTU2oi9onl4bNxvZ6qMEj",
                       "BZ3y4qZ8019zzU6F2hv4WLbDnpeIQMBIuefMHxb1qPeloUayZUbOv1Che8Fzy34C")


class Rate(models.Model):
    symbol = models.ForeignKey(ExchangeInfo, on_delete=models.CASCADE)
    price_change = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    price_change_percent = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    weighted_avg_price = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    prev_close_price = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    last_price = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    last_qty = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    bid_price = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    ask_price = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    open_price = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    high_price = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    low_price = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    volume = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    quote_volume = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    open_time = models.BigIntegerField(blank=False)
    close_time = models.BigIntegerField(blank=False)
    first_id = models.IntegerField(blank=False)
    last_id = models.IntegerField(blank=False)
    count = models.IntegerField(blank=False)

    def str(self):
        return self.symbol


def update_rates():
    print("Rates update start")
    print("Fetching data from API")
    exchange_rates = BinanceClient.get_ticker()

    rates_list = []

    for x in exchange_rates:
        get_symbol = ExchangeInfo.objects.filter(symbol=x['symbol']).count()

        if get_symbol > 0:
            new_rate = Rate(symbol=ExchangeInfo.objects.get(symbol=x['symbol']), price_change=x['priceChange'],
                            price_change_percent=x['priceChangePercent'], weighted_avg_price=x['weightedAvgPrice'],
                            prev_close_price=x['prevClosePrice'], last_price=x['lastPrice'], last_qty=x['lastQty'],
                            bid_price=x['bidPrice'], ask_price=x['askPrice'], open_price=x['openPrice'],
                            high_price=x['highPrice'], low_price=x['lowPrice'], volume=x['volume'],
                            quote_volume=x['quoteVolume'], open_time=x['openTime'], close_time=x['closeTime'],
                            first_id=x['firstId'], last_id=x['lastId'], count=x['count'])
            rates_list.append(new_rate)

    print("Inserting data to database")

    Rate.objects.bulk_create(rates_list, ignore_conflicts=True)
    print("Exchange rates updated successfully!")
