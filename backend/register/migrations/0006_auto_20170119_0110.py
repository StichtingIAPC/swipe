# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-19 00:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_paymenttype_is_invoicing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='denominationcount',
            old_name='amount',
            new_name='number',
        ),
    ]