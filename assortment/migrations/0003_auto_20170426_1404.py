# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-04-26 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assortment', '0002_auto_20170119_2241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assortmentunittype',
            name='type_short',
            field=models.CharField(blank=True, editable=False, max_length=8),
        ),
    ]
