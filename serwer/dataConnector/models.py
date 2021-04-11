from django.db import models


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
    symbol = models.CharField(max_length=4, blank=False)
    rank = models.IntegerField(blank=False)
    is_new = models.BooleanField(blank=False)
    is_active = models.BooleanField(blank=False)
    type = models.CharField(choices=COIN_TYPE, max_length=5, blank=False)

    def str(self):
        return self.name


class Rates(models.Model):

    def str(self):
        return self.name
