# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-15 23:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.RenameField('VAT', 'rate', 'vatrate')
    ]