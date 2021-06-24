# Generated by Django 3.2 on 2021-06-01 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataConnector', '0002_auto_20210601_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='candle',
            name='prediction_type',
            field=models.CharField(blank=True, choices=[('MLRW', 'Multiple Linear Regression (with windows)'), ('GP', 'Gaussian Process (without previous values)'), ('MLRP', 'Multiple Linear Regression (with previous values)'), ('ELM', 'Extream Learning Machine (without previous values)')], max_length=4),
        ),
    ]