# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-26 12:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_auto_20170119_0110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registerperiod',
            name='register',
        ),
        migrations.RemoveField(
            model_name='registerperiod',
            name='sales_period',
        ),
        migrations.RemoveField(
            model_name='moneyinout',
            name='register_period',
        ),
        migrations.RemoveField(
            model_name='registercount',
            name='register_period',
        ),
        migrations.AddField(
            model_name='moneyinout',
            name='register',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='register.Register'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='moneyinout',
            name='sales_period',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='register.SalesPeriod'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registercount',
            name='register',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='register.Register'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='registercount',
            name='sales_period',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='register.SalesPeriod'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RegisterPeriod',
        ),
    ]
