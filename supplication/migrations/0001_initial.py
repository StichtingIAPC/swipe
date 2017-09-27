# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-07 17:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('logistics', '0005_auto_20160901_2024'),
        ('article', '0003_auto_20160810_2229'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('supplier', '0002_auto_20160813_0229'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('supplier_identifier', models.CharField(max_length=30)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='supplier.Supplier')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplication_invoice_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackingDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('supplier_identifier', models.CharField(max_length=30)),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='supplier.Supplier')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplication_packingdocument_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackingDocumentLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('line_cost_currency', money.models.CurrencyField(max_length=3)),
                ('line_cost', money.models.CostField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('line_cost_after_invoice_currency', money.models.CurrencyField(max_length=3)),
                ('line_cost_after_invoice', money.models.CostField(decimal_places=5, default=None, max_digits=28, no_currency_field=True, null=True)),
                ('article_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleType')),
                ('invoice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='supplication.Invoice')),
                ('packing_document', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='supplication.PackingDocument')),
                ('supplier_order_line', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logistics.SupplierOrderLine')),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplication_packingdocumentline_created_by', to=settings.AUTH_USER_MODEL)),
                ('user_modified', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supplication_packingdocumentline_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]