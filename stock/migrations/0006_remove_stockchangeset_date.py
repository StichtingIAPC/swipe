# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-23 22:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_stockchange_memo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockchangeset',
            name='date',
        ),
    ]
