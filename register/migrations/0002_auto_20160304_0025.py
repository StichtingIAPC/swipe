# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-03 23:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='moneyinout',
            name='amount',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=28),
        ),
        migrations.AddField(
            model_name='register',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='registerperiod',
            name='beginTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='salesperiod',
            name='beginTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
