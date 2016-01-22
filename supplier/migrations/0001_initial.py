# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 23:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Supplier')),
                ('search_url', models.CharField(blank=True, max_length=255, verbose_name='Search URL')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('is_used', models.BooleanField(default=True, verbose_name='This supplier is used')),
                ('is_backup', models.BooleanField(default=False, verbose_name='This supplier is a backup supplier')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last modified')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='This supplier is soft-deleted')),
            ],
        ),
    ]
