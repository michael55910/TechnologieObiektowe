from django.db import models
from coinpaprika import client as Coinpaprika

CoinpaprikaClient = Coinpaprika.Client()


class Cryptocurrency(models.Model):
    #     class CoinType(models.TextChoices):
    #         COIN = 1, 'coin'
    #         TOKEN = 2, 'token'

    COIN_TYPE = (
        ('coin', 'coin'),
        ('token', 'token'),
    )

    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    symbol = models.CharField(max_length=10, blank=False)
    rank = models.IntegerField(blank=False)
    is_new = models.BooleanField(blank=False)
    is_active = models.BooleanField(blank=False)
    type = models.CharField(choices=COIN_TYPE, max_length=5, blank=False)

    def str(self):
        return self.name


def update_coins():
    print("Cryptocurrency update start")
    print("Fetching data from API")

    available_coins = CoinpaprikaClient.coins()

    coins_list = []

    for x in available_coins:
        new_coin = Cryptocurrency(id=x['id'], name=x['name'], symbol=x['symbol'], rank=x['rank'],
                                  is_new=x['is_new'], is_active=x['is_active'], type=x['type'])
        coins_list.append(new_coin)

    print("Inserting data to database")

    Cryptocurrency.objects.bulk_create(coins_list, ignore_conflicts=True)

    print("Cryptocurrency updated successfully!")
