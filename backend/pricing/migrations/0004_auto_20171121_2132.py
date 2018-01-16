# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-21 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_squashed_0005_person_user'),
        ('pricing', '0003_pricingmodel_margin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pricingmodel',
            name='function_identifier',
        ),
        migrations.RemoveField(
            model_name='pricingmodel',
            name='margin',
        ),
        migrations.RemoveField(
            model_name='pricingmodel',
            name='name',
        ),
        migrations.RemoveField(
            model_name='pricingmodel',
            name='position',
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='constMargin',
            field=models.DecimalField(decimal_places=5, default=1.21, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='custType',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer'),
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='exp_mult',
            field=models.DecimalField(decimal_places=5, default=1.21, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='exponent',
            field=models.DecimalField(decimal_places=5, default=1, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='max_relative_margin_error',
            field=models.DecimalField(decimal_places=5, default=1, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='min_relative_margin_error',
            field=models.DecimalField(decimal_places=5, default=1, max_digits=6),
            preserve_default=False,
        ),
    ]