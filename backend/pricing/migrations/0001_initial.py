# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-29 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PricingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exp_mult', models.DecimalField(decimal_places=5, max_digits=6)),
                ('exponent', models.DecimalField(decimal_places=5, max_digits=6)),
                ('constMargin', models.DecimalField(decimal_places=5, max_digits=6)),
                ('min_relative_margin_error', models.DecimalField(decimal_places=5, max_digits=6)),
                ('max_relative_margin_error', models.DecimalField(decimal_places=5, max_digits=6)),
                ('custType', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='crm.Customer')),
            ],
        ),
    ]
