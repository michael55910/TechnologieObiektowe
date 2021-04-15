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
        return self.name
