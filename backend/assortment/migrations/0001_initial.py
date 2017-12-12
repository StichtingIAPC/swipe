# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 21:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('description', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(editable=False, max_length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='AssortmentUnitType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_short', models.CharField(blank=True, editable=False, max_length=8)),
                ('type_long', models.CharField(editable=False, max_length=255)),
                ('value_type', models.CharField(choices=[('b', 'boolean'), ('i', 'integer'), ('n', 'decimal'), ('s', 'string')], editable=False, max_length=1)),
                ('incremental_type', models.CharField(blank=True, choices=[('ISQ', 'the ISQ standard is in powers of 1024 (2^10), starting with 1024^0: [], Ki, Mi, ...'), ('MIL', 'millions, billions, etc`'), ('SI', 'the SI standard is in powers of 1000, starting with 1000^-4: f, n, u, m, [], K, ...')], max_length=3, null=True)),
            ],
            options={
                'ordering': ['type_short', 'type_long'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='assortmentunittype',
            unique_together=set([('type_short', 'value_type'), ('type_long', 'value_type')]),
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
        migrations.AlterUniqueTogether(
            name='assortmentlabel',
            unique_together=set([('value', 'label_type')]),
        ),
    ]
