# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-09 00:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organisationtypefieldvalue',
            old_name='organisation',
            new_name='object',
        ),
        migrations.RenameField(
            model_name='persontypefieldvalue',
            old_name='person',
            new_name='object',
        ),
        migrations.AlterUniqueTogether(
            name='organisationtypefieldvalue',
            unique_together=set([('typefield', 'type', 'object')]),
        ),
        migrations.AlterUniqueTogether(
            name='persontypefieldvalue',
            unique_together=set([('typefield', 'type', 'object')]),
        ),
    ]
