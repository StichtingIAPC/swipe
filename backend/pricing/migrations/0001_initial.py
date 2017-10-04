# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-26 19:22
from __future__ import unicode_literals

from django.db import migrations, models
import pricing.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PricingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('position', models.IntegerField(unique=True, validators=[pricing.models.validate_bigger_than_0])),
            ],
        ),
    ]