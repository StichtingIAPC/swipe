# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-02 21:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('money', '0002_currencydata_denomination'),
    ]

    operations = [
        migrations.CreateModel(
            name='DenominationCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('denomination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.Denomination')),
            ],
        ),
        migrations.CreateModel(
            name='MoneyInOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Register',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_cash_register', models.BooleanField()),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.CurrencyData')),
            ],
        ),
        migrations.CreateModel(
            name='RegisterCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_opening_count', models.BooleanField()),
                ('amount', models.DecimalField(decimal_places=5, max_digits=28)),
            ],
        ),
        migrations.CreateModel(
            name='RegisterPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginTime', models.DateTimeField()),
                ('endTime', models.DateField(null=True)),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Register')),
            ],
        ),
        migrations.CreateModel(
            name='SalesPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beginTime', models.DateTimeField()),
                ('endTime', models.DateTimeField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='registerperiod',
            name='sales_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.SalesPeriod'),
        ),
        migrations.AddField(
            model_name='registercount',
            name='register_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.RegisterPeriod'),
        ),
        migrations.AddField(
            model_name='moneyinout',
            name='register_period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.RegisterPeriod'),
        ),
        migrations.AddField(
            model_name='denominationcount',
            name='register_count',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.RegisterCount'),
        ),
    ]
