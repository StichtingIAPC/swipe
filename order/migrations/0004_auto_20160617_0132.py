# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-16 23:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_auto_20160617_0126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
