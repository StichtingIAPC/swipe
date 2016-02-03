# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-03 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('money', '0002_auto_20160203_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('vat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.VAT')),
            ],
        ),
    ]
