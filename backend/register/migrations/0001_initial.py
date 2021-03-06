# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-29 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosingCountDifference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difference_currency', money.models.CurrencyField(max_length=3)),
                ('difference', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
            ],
        ),
        migrations.CreateModel(
            name='DenominationCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('denomination', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.Denomination')),
            ],
        ),
        migrations.CreateModel(
            name='MoneyInOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=28)),
            ],
        ),
        migrations.CreateModel(
            name='OpeningCountDifference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('difference_currency', money.models.CurrencyField(max_length=3)),
                ('difference', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_invoicing', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('is_cash_register', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.CurrencyData')),
                ('payment_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.PaymentType')),
            ],
            options={
                'permissions': (('open_register', 'Can open a register'), ('close_register', 'Can close a register')),
            },
        ),
        migrations.CreateModel(
            name='RegisterCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_opening_count', models.BooleanField()),
                ('amount', models.DecimalField(decimal_places=5, default=-1.0, max_digits=28)),
                ('time_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.Register')),
            ],
        ),
        migrations.CreateModel(
            name='SalesPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginTime', models.DateTimeField(auto_now_add=True)),
                ('endTime', models.DateTimeField(null=True)),
                ('closing_memo', models.CharField(default=None, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SalesPeriodDifference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=5, default=0.0, max_digits=28)),
                ('currency_data', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.CurrencyData')),
                ('sales_period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.SalesPeriod')),
            ],
        ),
        migrations.AddField(
            model_name='registercount',
            name='sales_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.SalesPeriod'),
        ),
        migrations.AddField(
            model_name='openingcountdifference',
            name='register_count',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='register.RegisterCount'),
        ),
        migrations.AddField(
            model_name='moneyinout',
            name='register',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.Register'),
        ),
        migrations.AddField(
            model_name='moneyinout',
            name='sales_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.SalesPeriod'),
        ),
        migrations.AddField(
            model_name='denominationcount',
            name='register_count',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.RegisterCount'),
        ),
        migrations.AddField(
            model_name='closingcountdifference',
            name='sales_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='register.SalesPeriod'),
        ),
    ]
