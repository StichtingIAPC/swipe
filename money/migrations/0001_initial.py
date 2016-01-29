# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 16:26
from __future__ import unicode_literals

from django.db import migrations, models
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestMoneyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_currency', money.models.CurrencyField(max_length=3)),
                ('money', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
            ],
        ),
        migrations.CreateModel(
            name='VAT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.DecimalField(decimal_places=6, max_digits=7, verbose_name='VAT Rate')),
                ('name', models.CharField(max_length=255, verbose_name='VAT Name')),
                ('active', models.BooleanField()),
            ],
        ),
    ]
