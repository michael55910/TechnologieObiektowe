# Generated by Django 3.0.5 on 2021-04-11 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataConnector', '0002_auto_20210411_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='type',
            field=models.CharField(choices=[('C', 'coin'), ('T', 'token')], max_length=1),
        ),
    ]
