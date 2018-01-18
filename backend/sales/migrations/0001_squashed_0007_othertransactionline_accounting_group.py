# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 18:33
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc
import money.models


class Migration(migrations.Migration):

    replaces = [('sales', '0001_initial'), ('sales', '0002_auto_20160918_2054'), ('sales', '0003_remove_transaction_time'), ('sales', '0004_auto_20160918_2058'), ('sales', '0005_auto_20160920_1711'), ('sales', '0006_remove_transaction_stock_change_set'), ('sales', '0007_othertransactionline_accounting_group')]

    initial = True

    dependencies = [
        ('article', '0004_wishabletype_labels'),
        ('crm', '0001_squashed_0005_person_user'),
        ('money', '0001_squashed_0006_accountinggroup'),
        ('register', '0002_auto_20160914_2324'),
        ('stock', '0001_squashed_0005_merge'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('salesperiod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.SalesPeriod')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 9, 18, 18, 54, 17, 136328, tzinfo=utc))),
                ('user_created', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sales_transaction_created_by', to=settings.AUTH_USER_MODEL)),
                ('user_modified', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sales_transaction_modified_by', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer')),
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
                ('other_cost_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='article.OtherCostType')),
            ],
            bases=('sales.transactionline',),
        ),
        migrations.CreateModel(
            name='OtherTransactionLine',
            fields=[
                ('transactionline_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sales.TransactionLine')),
                ('accounting_group', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='money.AccountingGroup')),
            ],
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
            bases=('sales.transactionline', models.Model),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Transaction'),
        ),
        migrations.AddField(
            model_name='payment',
            name='transaction',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Transaction'),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='date_created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='transactionline',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionline',
            name='user_created',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sales_transactionline_created_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionline',
            name='user_modified',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sales_transactionline_modified_by', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionline',
            name='order',
            field=models.IntegerField(null=True),
        ),
    ]
