# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-12-12 21:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import money.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assortment', '0001_initial'),
        ('money', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCombination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WishableType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='AndProductType',
            fields=[
                ('wishabletype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.WishableType')),
            ],
            bases=('article.wishabletype',),
        ),
        migrations.CreateModel(
            name='OrProductType',
            fields=[
                ('wishabletype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.WishableType')),
                ('fixed_price_currency', money.models.CurrencyField(max_length=3)),
                ('fixed_price', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True, null=True)),
            ],
            bases=('article.wishabletype',),
        ),
        migrations.CreateModel(
            name='SellableType',
            fields=[
                ('wishabletype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.WishableType')),
            ],
            bases=('article.wishabletype',),
        ),
        migrations.AddField(
            model_name='wishabletype',
            name='labels',
            field=models.ManyToManyField(blank=True, to='assortment.AssortmentLabel'),
        ),
        migrations.CreateModel(
            name='ArticleType',
            fields=[
                ('sellabletype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.SellableType')),
                ('fixed_price_currency', money.models.CurrencyField(max_length=3)),
                ('fixed_price', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True, null=True)),
                ('ean', models.BigIntegerField(null=True)),
                ('serial_number', models.BooleanField(default=True)),
            ],
            bases=('article.sellabletype',),
        ),
        migrations.CreateModel(
            name='OtherCostType',
            fields=[
                ('sellabletype_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='article.SellableType')),
                ('fixed_price_currency', money.models.CurrencyField(max_length=3)),
                ('fixed_price', money.models.MoneyField(decimal_places=5, max_digits=28, no_currency_field=True)),
            ],
            bases=('article.sellabletype',),
        ),
        migrations.AddField(
            model_name='sellabletype',
            name='accounting_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money.AccountingGroup'),
        ),
        migrations.AddField(
            model_name='productcombination',
            name='and_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.AndProductType'),
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
        migrations.AlterUniqueTogether(
            name='productcombination',
            unique_together=set([('article_type', 'and_product')]),
        ),
    ]
