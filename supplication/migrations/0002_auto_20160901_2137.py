# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-09-01 19:37
from __future__ import unicode_literals

from django.db import migrations
import money.models


class Migration(migrations.Migration):

    dependencies = [
        ('supplication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='packingdocumentline',
            name='line_cost_after_invoice',
            field=money.models.CostField(decimal_places=5, default=None, max_digits=28, no_currency_field=True, null=True),
        ),
        migrations.AddField(
            model_name='packingdocumentline',
            name='line_cost_after_invoice_currency',
            field=money.models.CurrencyField(default='XXX', max_length=3),
            preserve_default=False,
        ),
    ]
