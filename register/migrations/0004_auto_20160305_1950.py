# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-05 18:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20160304_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registercount',
            name='amount',
            field=models.DecimalField(decimal_places=5, default=-1.0, max_digits=28),
        ),
    ]
