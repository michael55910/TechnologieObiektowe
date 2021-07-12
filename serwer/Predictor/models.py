import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from dataConnector.submodels import ExchangeInfo
from dataConnector.submodels import Candle


class PredictionType(models.TextChoices):
    MLRW = 'MLRW', _('Multiple Linear Regression (with Windows)')
    GP = 'GP', _('Gaussian Process (without previous values)')
    MLRP = 'MLRP', _('Multiple Linear Regression (with Previous values)')
    ELM = 'ELM', _('Extreme Learning Machine (without previous values)')


prediction_models_directory = 'prediction_models/'


def get_available_prediction_models():
    return os.listdir(prediction_models_directory)


class Prediction(models.Model):
    id = models.BigAutoField(primary_key=True)
    symbol = models.ForeignKey(ExchangeInfo, on_delete=models.CASCADE)
    interval = models.CharField(choices=Candle.KLINE_INTERVAL, max_length=3, blank=False)
    prediction_model = models.CharField(blank=False, max_length=200)
    prediction_time = models.DateTimeField(blank=False)

    class Meta:
        unique_together = ('symbol', 'interval', 'prediction_model', 'prediction_time')
        get_latest_by = 'open_time'


class PredictedData(models.Model):
    close_time = models.BigIntegerField(blank=False)
    predicted_y = models.DecimalField(blank=False, decimal_places=8, max_digits=14)
    prediction = models.ForeignKey(Prediction, on_delete=models.CASCADE)
