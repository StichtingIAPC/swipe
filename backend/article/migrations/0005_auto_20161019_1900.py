# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-19 17:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_wishabletype_labels'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wishabletype',
            options={'ordering': ['name']},
        ),
    ]