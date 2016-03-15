# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-15 19:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssortmentArticleBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('parent_tag', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assortment.AssortmentArticleBranch')),
            ],
        ),
        migrations.CreateModel(
            name='AssortmentLabel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField(editable=False, max_length=64)),
            ],
            options={
                'ordering': ['label_type', 'value'],
            },
        ),
        migrations.CreateModel(
            name='AssortmentLabelType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_long', models.CharField(max_length=64, unique=True)),
                ('name_short', models.CharField(editable=False, max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssortmentUnitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_short', models.CharField(editable=False, max_length=8)),
                ('type_long', models.CharField(editable=False, max_length=255)),
                ('counting_type', models.CharField(choices=[('b', 'boolean'), ('i', 'integer'), ('n', 'decimal'), ('s', 'string')], editable=False, max_length=1)),
                ('incremental_type', models.CharField(blank=True, choices=[('EU', 'the EU thousands, millions and milliards `standard`'), ('ISQ', 'the ISQ standard is in powers of 1024 (2^10), starting with 1024^0: [], Ki, Mi, ...'), ('SI', 'the SI standard is in powers of 1000, starting with 1000^-4: f, n, u, m, [], K, ...'), ('US', 'the US thousands, millions and billions `standard`')], max_length=3, null=True)),
            ],
            options={
                'ordering': ['type_short', 'type_long'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='assortmentunittype',
            unique_together=set([('type_long', 'counting_type'), ('type_short', 'counting_type')]),
        ),
        migrations.AddField(
            model_name='assortmentlabeltype',
            name='unit_type',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='assortment.AssortmentUnitType'),
        ),
        migrations.AddField(
            model_name='assortmentlabel',
            name='label_type',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='assortment.AssortmentLabelType'),
        ),
        migrations.AddField(
            model_name='assortmentarticlebranch',
            name='presumed_labels',
            field=models.ManyToManyField(to='assortment.AssortmentLabelType'),
        ),
        migrations.AlterUniqueTogether(
            name='assortmentlabel',
            unique_together=set([('value', 'label_type')]),
        ),
    ]
