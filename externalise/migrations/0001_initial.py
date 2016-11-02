# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-02 01:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0005_auto_20161019_1900'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExternaliseDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('memo', models.TextField()),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='externalise_externalisedocument_created_by', to=settings.AUTH_USER_MODEL)),
                ('user_modified', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='externalise_externalisedocument_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ExternaliseLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField()),
                ('cost_currency', money.models.CurrencyField(max_length=3)),
                ('cost', money.models.CostField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('article_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleType')),
                ('externalise_document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='externalise.ExternaliseDocument')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='externalise_externaliseline_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
