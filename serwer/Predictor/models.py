import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from dataConnector.submodels import ExchangeInfo


class PredictionType(models.TextChoices):
    MLRW = 'MLRW', _('Multiple Linear Regression (with Windows)')
    GP = 'GP', _('Gaussian Process (without previous values)')
    MLRP = 'MLRP', _('Multiple Linear Regression (with Previous values)')
    ELM = 'ELM', _('Extreme Learning Machine (without previous values)')


def get_available_prediction_models():
    return os.listdir('prediction_models/')


class PredictedData(models.Model):
    from dataConnector.submodels import Candle
    symbol = models.ForeignKey(ExchangeInfo, on_delete=models.CASCADE)
    interval = models.CharField(choices=Candle.KLINE_INTERVAL, max_length=3, blank=False)
    prediction_model = models.CharField(blank=False, max_length=200)
    prediction_time = models.DateTimeField(blank=False)
    close_time = models.BigIntegerField(blank=False)
    predicted_y = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
