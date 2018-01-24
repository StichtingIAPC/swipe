# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-23 20:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0005_auto_20160901_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockwish',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics_stockwish_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stockwishtableline',
            name='article_type',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='article.ArticleType'),
        ),
        migrations.AlterField(
            model_name='stockwishtableline',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics_stockwishtableline_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stockwishtableline',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics_stockwishtableline_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='stockwishtablelog',
            name='article_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.ArticleType'),
        ),
        migrations.AlterField(
            model_name='stockwishtablelog',
            name='stock_wish',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='logistics.StockWish'),
        ),
        migrations.AlterField(
            model_name='stockwishtablelog',
            name='supplier_order',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='logistics.SupplierOrder'),
        ),
        migrations.AlterField(
            model_name='stockwishtablelog',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics_stockwishtablelog_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supplierorder',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='supplier.Supplier'),
        ),
        migrations.AlterField(
            model_name='supplierorder',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics_supplierorder_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supplierorderline',
            name='article_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.ArticleType'),
        ),
        migrations.AlterField(
            model_name='supplierorderline',
            name='order_line',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='order.OrderLine'),
        ),
        migrations.AlterField(
            model_name='supplierorderline',
            name='supplier_article_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='supplier.ArticleTypeSupplier'),
        ),
        migrations.AlterField(
            model_name='supplierorderline',
            name='supplier_order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logistics.SupplierOrder'),
        ),
        migrations.AlterField(
            model_name='supplierorderline',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics_supplierorderline_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supplierorderline',
            name='user_modified',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics_supplierorderline_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='supplierorderstate',
            name='supplier_order_line',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='logistics.SupplierOrderLine'),
        ),
        migrations.AlterField(
            model_name='supplierorderstate',
            name='user_created',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='logistics_supplierorderstate_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
