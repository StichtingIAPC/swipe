# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-27 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pricing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricingmodel',
            name='id',
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='function_identifier',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]