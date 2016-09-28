# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-25 15:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0001_squashed_0006_accountinggroup'),
        ('sales', '0006_remove_transaction_stock_change_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='othertransactionline',
            name='accounting_group',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='money.AccountingGroup'),
            preserve_default=False,
        ),
    ]
