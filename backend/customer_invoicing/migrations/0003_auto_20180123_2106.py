# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-23 20:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_invoicing', '0002_invoicefieldorganisation_invoicefieldperson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custinvoice',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_invoicing_custinvoice_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='custinvoice',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_invoicing_custinvoice_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='custominvoiceline',
            name='custom_invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer_invoicing.CustomCustInvoice'),
        ),
        migrations.AlterField(
            model_name='custominvoiceline',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_invoicing_custominvoiceline_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='custominvoiceline',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_invoicing_custominvoiceline_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='custpayment',
            name='cust_invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='customer_invoicing.CustInvoice'),
        ),
        migrations.AlterField(
            model_name='custpayment',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_invoicing_custpayment_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='custpayment',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='customer_invoicing_custpayment_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invoicefieldorganisation',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='address', to='crm.OrganisationTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldorganisation',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='city', to='crm.OrganisationTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldorganisation',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='country', to='crm.OrganisationTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldorganisation',
            name='email_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='email', to='crm.OrganisationTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldorganisation',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='org_name', to='crm.OrganisationTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldorganisation',
            name='zip_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='zip', to='crm.OrganisationTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldperson',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='address', to='crm.PersonTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldperson',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='city', to='crm.PersonTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldperson',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='country', to='crm.PersonTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldperson',
            name='email_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='email', to='crm.PersonTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldperson',
            name='name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='pers_name', to='crm.PersonTypeField'),
        ),
        migrations.AlterField(
            model_name='invoicefieldperson',
            name='zip_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='zip', to='crm.PersonTypeField'),
        ),
        migrations.AlterField(
            model_name='receiptcustinvoice',
            name='receipt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sales.Transaction'),
        ),
    ]