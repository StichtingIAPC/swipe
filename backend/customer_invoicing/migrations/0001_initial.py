# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-27 21:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sales', '0003_auto_20161026_0124'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('invoice_name', models.CharField(max_length=255)),
                ('invoice_address', models.CharField(max_length=255)),
                ('invoice_zip_code', models.CharField(max_length=255)),
                ('invoice_city', models.CharField(max_length=255)),
                ('invoice_country', models.CharField(max_length=255)),
                ('invoice_email_address', models.CharField(max_length=255)),
                ('to_be_paid_currency', money.models.CurrencyField(max_length=3)),
                ('to_be_paid', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('paid_currency', money.models.CurrencyField(max_length=3)),
                ('paid', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
                ('handled', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomInvoiceLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=255)),
                ('price_currency', money.models.CurrencyField(max_length=3)),
                ('price_vat', money.models.VATLevelField(decimal_places=6, max_digits=15)),
                ('price', money.models.PriceField(decimal_places=5, max_digits=28, no_currency_field=True, no_vat_field=True)),
                ('user_created', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_invoicing_custominvoiceline_created_by', to=settings.AUTH_USER_MODEL)),
                ('user_modified', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_invoicing_custominvoiceline_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('date_modified', models.DateTimeField(auto_now_add=True)),
                ('payment_currency', money.models.CurrencyField(max_length=3)),
                ('payment', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomCustInvoice',
            fields=[
                ('custinvoice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='customer_invoicing.CustInvoice')),
            ],
            options={
                'abstract': False,
            },
            bases=('customer_invoicing.custinvoice',),
        ),
        migrations.CreateModel(
            name='ReceiptCustInvoice',
            fields=[
                ('custinvoice_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='customer_invoicing.CustInvoice')),
                ('receipt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.Transaction')),
            ],
            options={
                'abstract': False,
            },
            bases=('customer_invoicing.custinvoice',),
        ),
        migrations.AddField(
            model_name='custpayment',
            name='cust_invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_invoicing.CustInvoice'),
        ),
        migrations.AddField(
            model_name='custpayment',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_invoicing_custpayment_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='custpayment',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_invoicing_custpayment_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='custinvoice',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_invoicing_custinvoice_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='custinvoice',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_invoicing_custinvoice_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='custominvoiceline',
            name='custom_invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_invoicing.CustomCustInvoice'),
        ),
    ]