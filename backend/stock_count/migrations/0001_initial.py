# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-29 18:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
        ('stock', '0001_initial'),
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscrepancySolution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock_label', models.CharField(max_length=30, null=True)),
                ('stock_key', models.IntegerField(null=True)),
                ('article_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.ArticleType')),
            ],
        ),
        migrations.CreateModel(
            name='StockCountDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('stock_change_set', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='stock.StockChangeSet')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_count_stockcountdocument_created_by', to=settings.AUTH_USER_MODEL)),
                ('user_modified', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stock_count_stockcountdocument_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StockCountLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_count', models.IntegerField()),
                ('in_count', models.IntegerField()),
                ('out_count', models.IntegerField()),
                ('physical_count', models.IntegerField()),
                ('average_value_currency', money.models.CurrencyField(max_length=3)),
                ('average_value', money.models.CostField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('text', models.CharField(max_length=255)),
                ('accounting_group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='money.AccountingGroup')),
                ('article_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.ArticleType')),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='stock_count.StockCountDocument')),
            ],
        ),
        migrations.CreateModel(
            name='TemporaryArticleCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('checked', models.BooleanField(default=False)),
                ('article_type', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='article.ArticleType')),
            ],
        ),
    ]
