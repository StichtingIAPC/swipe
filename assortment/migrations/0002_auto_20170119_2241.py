# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-19 21:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_remove_wishabletype_branch'),
        ('assortment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assortmentarticlebranch',
            name='parent_tag',
        ),
        migrations.RemoveField(
            model_name='assortmentarticlebranch',
            name='presumed_labels',
        ),
        migrations.DeleteModel(
            name='AssortmentArticleBranch',
        ),
    ]
