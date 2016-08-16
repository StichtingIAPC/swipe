# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 19:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('supplier', '0001_initial'),
        ('money', '0001_squashed_0006_accountinggroup')
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='AndProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('has_fixed_price', models.BooleanField(default=False)),
                ('fixed_price_currency', money.models.CurrencyField(max_length=3)),
                ('fixed_price_vat', money.models.VATLevelField(decimal_places=6, max_digits=15)),
                ('fixed_price_cost', models.DecimalField(decimal_places=5, max_digits=28)),
                ('fixed_price', money.models.SalesPriceField(decimal_places=5, max_digits=28, no_cost_field=True, no_currency_field=True, no_vat_field=True)),
                ('book_keeping_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.AccountingGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrProductType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherCostType',
            fields=[
                ('name', models.CharField(max_length=255)),
                ('price', money.models.MoneyField(decimal_places=5, default=0, max_digits=28, no_currency_field=True)),
                ('price_currency', money.models.CurrencyField(default=0, max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCombination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('and_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.AndProductType')),
            ],
        ),
        migrations.AddField(
            model_name='articletype',
            name='accounting_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.AccountingGroup'),
        ),
        migrations.RemoveField(
            model_name='articletype',
            name='name',
        ),
        migrations.AddField(
            model_name='productcombination',
            name='article_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.ArticleType'),
        ),
        migrations.AddField(
            model_name='orproducttype',
            name='article_types',
            field=models.ManyToManyField(to='article.ArticleType'),
        ),
        migrations.RemoveField(
            model_name='andproducttype',
            name='fixed_price',
        ),
        migrations.RemoveField(
            model_name='andproducttype',
            name='fixed_price_cost',
        ),
        migrations.RemoveField(
            model_name='andproducttype',
            name='fixed_price_currency',
        ),
        migrations.RemoveField(
            model_name='andproducttype',
            name='fixed_price_vat',
        ),
        migrations.CreateModel(
            name='WishableType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='andproducttype',
            name='book_keeping_group',
        ),
        migrations.RemoveField(
            model_name='andproducttype',
            name='has_fixed_price',
        ),
        migrations.RemoveField(
            model_name='andproducttype',
            name='id',
        ),
        migrations.RemoveField(
            model_name='andproducttype',
            name='name',
        ),
        migrations.RemoveField(
            model_name='articletype',
            name='id',
        ),
        migrations.RemoveField(
            model_name='orproducttype',
            name='id',
        ),
        migrations.RemoveField(
            model_name='orproducttype',
            name='name',
        ),
        migrations.AddField(
            model_name='articletype',
            name='fixed_price',
            field=money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True, null=True),
        ),
        migrations.AddField(
            model_name='articletype',
            name='fixed_price_currency',
            field=money.models.CurrencyField(default=0, max_length=3),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='SellableType',
            fields=[
                ('wishabletype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.WishableType')),
            ],
            bases=('article.wishabletype',),
        ),
        migrations.AddField(
            model_name='orproducttype',
            name='wishabletype_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.WishableType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='andproducttype',
            name='sellabletype_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.SellableType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='articletype',
            name='sellabletype_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.SellableType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='othercosttype',
            name='sellabletype_ptr',
            field=models.OneToOneField(auto_created=True, default=0, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.SellableType'),
            preserve_default=False,
        ),
        migrations.RenameField(
            model_name='othercosttype',
            old_name='price',
            new_name='fixed_price',
        ),
        migrations.RenameField(
            model_name='othercosttype',
            old_name='price_currency',
            new_name='fixed_price_currency',
        ),
        migrations.RemoveField(
            model_name='othercosttype',
            name='name',
        ),
        migrations.AddField(
            model_name='orproducttype',
            name='fixed_price',
            field=money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True, null=True),
        ),
        migrations.AddField(
            model_name='orproducttype',
            name='fixed_price_currency',
            field=money.models.CurrencyField(default='EUR', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='wishabletype',
            name='name',
            field=models.CharField(default='Blank', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='othercosttype',
            name='fixed_price',
            field=money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True),
        ),
        migrations.AlterField(
            model_name='othercosttype',
            name='fixed_price_currency',
            field=money.models.CurrencyField(max_length=3),
        ),
        migrations.AlterUniqueTogether(
            name='productcombination',
            unique_together=set([('article_type', 'and_product')]),
        ),
    ]