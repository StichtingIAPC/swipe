# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-03 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocklog',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
