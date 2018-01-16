# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-14 21:24
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0002_auto_20160914_2324'),
        ('stock', '0001_squashed_0005_merge'),
        ('article', '0004_wishabletype_labels'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_currency', money.models.CurrencyField(max_length=3)),
                ('amount', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.PaymentType')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('salesperiod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.SalesPeriod')),
                ('stock_change_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.StockChangeSet')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField()),
                ('price_currency', money.models.CurrencyField(max_length=3)),
                ('price_vat', money.models.VATLevelField(decimal_places=6, max_digits=15)),
                ('price', money.models.PriceField(decimal_places=5, max_digits=28, no_currency_field=True, no_vat_field=True)),
                ('count', models.IntegerField()),
                ('isRefunded', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='OtherCostTransactionLine',
            fields=[
                ('transactionline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.TransactionLine')),
            ],
            bases=('sales.transactionline',),
        ),
        migrations.CreateModel(
            name='OtherTransactionLine',
            fields=[
                ('transactionline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.TransactionLine')),
            ],
            bases=('sales.transactionline',),
        ),
        migrations.CreateModel(
            name='SalesTransactionLine',
            fields=[
                ('transactionline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.TransactionLine')),
                ('labeltype', models.CharField(blank=True, max_length=255, null=True, validators=[django.core.validators.RegexValidator(message='Labeltype should be longer than zero characters', regex='^.+$')])),
                ('labelkey', models.IntegerField(blank=True, null=True)),
                ('cost_currency', money.models.CurrencyField(max_length=3)),
                ('cost', money.models.CostField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleType')),
            ],
            options={
                'abstract': False,
            },
            bases=('sales.transactionline', models.Model),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Transaction'),
        ),
        migrations.AddField(
            model_name='payments',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Transaction'),
        ),
    ]
