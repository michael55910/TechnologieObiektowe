# Generated by Django 3.2 on 2021-04-22 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_time', models.BigIntegerField(default='0')),
                ('open', models.FloatField(default='0')),
                ('high', models.FloatField(default='0')),
                ('low', models.FloatField(default='0')),
                ('close', models.FloatField(default='0')),
                ('volume', models.FloatField(default='0')),
                ('close_time', models.BigIntegerField(default='0')),
                ('quote_asset_volume', models.FloatField(default='0')),
                ('number_of_trades', models.IntegerField(default='0')),
                ('taker_buy_base_asset_volume', models.FloatField(default='0')),
                ('taker_buy_quote_asset_volume', models.FloatField(default='0')),
                ('ignore', models.FloatField(default='0')),
            ],
        ),
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('symbol', models.CharField(max_length=10)),
                ('rank', models.IntegerField()),
                ('is_new', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('type', models.CharField(choices=[('coin', 'coin'), ('token', 'token')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=8)),
                ('price_change', models.FloatField()),
                ('price_change_percent', models.FloatField()),
                ('weighted_avg_price', models.FloatField()),
                ('prev_close_price', models.FloatField()),
                ('last_price', models.FloatField()),
                ('last_qty', models.FloatField()),
                ('bid_price', models.FloatField()),
                ('ask_price', models.FloatField()),
                ('open_price', models.FloatField()),
                ('high_price', models.FloatField()),
                ('low_price', models.FloatField()),
                ('volume', models.FloatField()),
                ('quote_volume', models.FloatField()),
                ('open_time', models.IntegerField()),
                ('close_time', models.IntegerField()),
                ('first_id', models.IntegerField()),
                ('last_id', models.IntegerField()),
                ('count', models.IntegerField()),
            ],
        ),
    ]
