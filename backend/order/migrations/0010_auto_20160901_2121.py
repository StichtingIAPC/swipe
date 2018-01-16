# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-01 19:21
from __future__ import unicode_literals

from django.db import migrations
import money.models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20160819_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderline',
            name='final_sales_price',
            field=money.models.PriceField(decimal_places=5, default=None, max_digits=28, no_currency_field=True, no_vat_field=True, null=True),
        ),
        migrations.AddField(
            model_name='orderline',
            name='final_sales_price_currency',
            field=money.models.CurrencyField(default='XXX', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderline',
            name='final_sales_price_vat',
            field=money.models.VATLevelField(decimal_places=6, default=100, max_digits=15),
            preserve_default=False,
        ),
    ]