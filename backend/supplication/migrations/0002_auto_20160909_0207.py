# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-09 00:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='packingdocument',
            name='timestamp',
        ),
    ]