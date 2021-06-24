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

    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    symbol = models.CharField(max_length=10, blank=False, unique=True)
    rank = models.IntegerField(blank=False)
    is_new = models.BooleanField(blank=False)
    is_active = models.BooleanField(blank=False)
    type = models.CharField(choices=COIN_TYPE, max_length=5, blank=False)

    def str(self):
        return self.name

    def __str__(self):
        return '%s' % self.symbol
        # return '%s (%s)' % (self.name, self.symbol)


def update_coins():
    print("Cryptocurrency update start")
    print("Fetching data from API")

    available_coins = CoinpaprikaClient.coins()

    coins_list = []

    for x in available_coins:
        if x['is_active'] and x['type'] == 'coin':
            new_coin = Cryptocurrency(id=x['id'], name=x['name'], symbol=x['symbol'], rank=x['rank'],
                                      is_new=x['is_new'], is_active=x['is_active'], type=x['type'])
            coins_list.append(new_coin)

    print("Inserting data to database")

    Cryptocurrency.objects.bulk_create(coins_list, ignore_conflicts=True)

    print("Cryptocurrency updated successfully!")
