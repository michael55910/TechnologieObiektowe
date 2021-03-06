# Generated by Django 3.2.4 on 2021-06-25 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataConnector', '0005_auto_20210625_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candle',
            name='quote_asset_volume',
            field=models.DecimalField(decimal_places=8, max_digits=18),
        ),
        migrations.AlterField(
            model_name='candle',
            name='taker_buy_base_asset_volume',
            field=models.DecimalField(decimal_places=8, max_digits=18),
        ),
        migrations.AlterField(
            model_name='candle',
            name='taker_buy_quote_asset_volume',
            field=models.DecimalField(decimal_places=8, max_digits=18),
        ),
        migrations.AlterField(
            model_name='candle',
            name='volume',
            field=models.DecimalField(decimal_places=8, max_digits=18),
        ),
    ]
