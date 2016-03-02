# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-25 18:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('book_value_currency', money.models.CurrencyField(max_length=3)),
                ('book_value', money.models.CostField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleType')),
            ],
        ),
        migrations.CreateModel(
            name='StockChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('book_value_currency', money.models.CurrencyField(max_length=3)),
                ('book_value', money.models.CostField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('is_in', models.BooleanField()),
                ('memo', models.CharField(max_length=255, null=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleType')),
            ],
        ),
        migrations.CreateModel(
            name='StockChangeSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('memo', models.CharField(max_length=255, null=True)),
                ('enum', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='stockchange',
            name='change_set',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stock.StockChangeSet'),
        ),
    ]
