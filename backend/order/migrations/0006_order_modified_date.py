# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-08-11 20:39
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20160803_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='modified_date',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 11, 20, 39, 6, 232385, tzinfo=utc)),
            preserve_default=False,
        ),
    ]