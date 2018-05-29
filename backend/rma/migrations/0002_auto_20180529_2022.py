# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-29 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rma', '0001_initial'),
        ('article', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerrmatask',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.Transaction'),
        ),
        migrations.AddField(
            model_name='testrmastate',
            name='test_rma',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rma.TestRMA'),
        ),
        migrations.AddField(
            model_name='testrma',
            name='customer_rma_task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rma.CustomerRMATask'),
        ),
        migrations.AddField(
            model_name='testrma',
            name='transaction_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.TransactionLine'),
        ),
        migrations.AddField(
            model_name='stockrma',
            name='article_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.ArticleType'),
        ),
        migrations.AddField(
            model_name='directrefundrma',
            name='refund_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.RefundTransactionLine'),
        ),
    ]
