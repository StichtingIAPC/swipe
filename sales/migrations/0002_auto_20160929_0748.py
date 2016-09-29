# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-29 05:48
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0001_squashed_0007_othertransactionline_accounting_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othercosttransactionline',
            name='other_cost_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.OtherCostType'),
        ),
        migrations.AlterField(
            model_name='othertransactionline',
            name='accounting_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.AccountingGroup'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date_modified',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_transaction_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_transaction_modified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
