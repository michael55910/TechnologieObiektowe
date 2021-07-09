from django.db import models
from django.utils.translation import gettext_lazy as _


class PredictionType(models.TextChoices):
    MLRW = 'MLRW', _('Multiple Linear Regression (with Windows)')
    GP = 'GP', _('Gaussian Process (without previous values)')
    MLRP = 'MLRP', _('Multiple Linear Regression (with Previous values)')
    ELM = 'ELM', _('Extreme Learning Machine (without previous values)')
