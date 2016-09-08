# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-02 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assortment', '0001_initial'),
        ('article', '0003_auto_20160810_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishabletype',
            name='labels',
            field=models.ManyToManyField(to='assortment.AssortmentLabel'),
        ),
        migrations.AddField(
            model_name='wishabletype',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='assortment.AssortmentArticleBranch'),
            preserve_default=False,
        ),
    ]
