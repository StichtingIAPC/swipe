# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 21:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
        ('crm', '0001_initial'),
        ('rma', '0001_initial'),
        ('money', '0001_initial'),
        ('register', '0001_initial'),
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
            name='PriceOverride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=255)),
                ('original_price_currency', money.models.CurrencyField(max_length=3)),
                ('original_price_vat', money.models.VATLevelField(decimal_places=6, max_digits=15)),
                ('original_price', money.models.PriceField(decimal_places=5, max_digits=28, no_currency_field=True, no_vat_field=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer')),
                ('salesperiod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.SalesPeriod')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_transaction_created_by', to=settings.AUTH_USER_MODEL)),
                ('user_modified', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_transaction_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TransactionLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('num', models.IntegerField()),
                ('price_currency', money.models.CurrencyField(max_length=3)),
                ('price_vat', money.models.VATLevelField(decimal_places=6, max_digits=15)),
                ('price', money.models.PriceField(decimal_places=5, max_digits=28, no_currency_field=True, no_vat_field=True)),
                ('count', models.IntegerField()),
                ('isRefunded', models.BooleanField(default=False)),
                ('text', models.CharField(max_length=128)),
                ('order', models.IntegerField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherCostTransactionLine',
            fields=[
                ('transactionline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.TransactionLine')),
                ('other_cost_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.OtherCostType')),
            ],
            options={
                'abstract': False,
            },
            bases=('sales.transactionline',),
        ),
        migrations.CreateModel(
            name='OtherTransactionLine',
            fields=[
                ('transactionline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.TransactionLine')),
            ],
            options={
                'abstract': False,
            },
            bases=('sales.transactionline',),
        ),
        migrations.CreateModel(
            name='RefundTransactionLine',
            fields=[
                ('transactionline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.TransactionLine')),
                ('creates_rma', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('sales.transactionline',),
        ),
        migrations.CreateModel(
            name='SalesTransactionLine',
            fields=[
                ('transactionline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.TransactionLine')),
                ('cost_currency', money.models.CurrencyField(max_length=3)),
                ('cost', money.models.CostField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleType')),
            ],
            options={
                'abstract': False,
            },
            bases=('sales.transactionline',),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='accounting_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.AccountingGroup'),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='original_price',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.PriceOverride'),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Transaction'),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_transactionline_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_transactionline_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Transaction'),
        ),
        migrations.AddField(
            model_name='refundtransactionline',
            name='sold_transaction_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sold_line', to='sales.TransactionLine'),
        ),
        migrations.AddField(
            model_name='refundtransactionline',
            name='test_rma',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rma.TestRMA'),
        ),
    ]
