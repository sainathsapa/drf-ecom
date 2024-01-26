# Generated by Django 5.0.1 on 2024-01-23 06:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0008_customer_customer_address'),
        ('seller', '0003_product_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_email',
            field=models.EmailField(db_column='username', max_length=60),
        ),
        migrations.AlterField(
            model_name='customer',
            name='customer_pwd',
            field=models.CharField(db_column='password', max_length=250),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_order_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.address'),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_ordered_products',
            field=models.ManyToManyField(blank=True, null=True, to='seller.product', verbose_name='listofProductsOrdred'),
        ),
    ]
