# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-05 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_stocklock_stocklocklog'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockchangeset',
            name='source',
            field=models.CharField(choices=[('cash_register', 'Cash register'), ('supplication', 'Supplication'), ('rma', 'RMA'), ('internalise', 'Internalise'), ('externalise', 'Externalise'), ('revaluation', 'Revaluation'), ('stock_count', 'Stock count')], default='', max_length=50),
            preserve_default=False,
        ),
    ]