# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-09 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestCostType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost_currency', money.models.CurrencyField(max_length=3)),
                ('cost', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestMoneyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_currency', money.models.CurrencyField(max_length=3)),
                ('money', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestOtherMoneyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_currency', money.models.CurrencyField(max_length=3)),
                ('money', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestPriceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_currency', money.models.CurrencyField(max_length=3)),
                ('price_vat', money.models.VATLevelField(decimal_places=6, max_digits=8)),
                ('price', money.models.PriceField(decimal_places=5, max_digits=28, no_currency_field=True, no_vat_field=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestSalesPriceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_currency', money.models.CurrencyField(max_length=3)),
                ('price_vat', money.models.VATLevelField(decimal_places=6, max_digits=8)),
                ('price_cost', models.DecimalField(decimal_places=5, max_digits=28)),
                ('price', money.models.SalesPriceField(decimal_places=5, max_digits=28, no_cost_field=True, no_currency_field=True, no_vat_field=True)),
            ],
        ),
        migrations.CreateModel(
            name='VAT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vatrate', models.DecimalField(decimal_places=6, max_digits=8)),
                ('name', models.CharField(max_length=255)),
                ('active', models.BooleanField()),
            ],
        ),
    ]
