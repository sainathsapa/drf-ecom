# Generated by Django 5.0.1 on 2024-01-10 10:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seller', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('customer_address_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customeraddress_space_name', models.CharField(max_length=50)),
                ('customer_address_hno_street', models.CharField(max_length=150)),
                ('customer_address_city', models.CharField(max_length=30)),
                ('customer_address_type', models.CharField(choices=[('HOME', 'HOME TYPE [ ALL_DAY_DELIVERY ]'), ('OFFICE', 'COMMERICAL [ DELIVERY_ON_WORKING_DAYS_9AM_-_10PM ]')], default='HOME', max_length=150)),
                ('customer_address_pin_code', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('customer_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_email', models.EmailField(max_length=60)),
                ('customer_pwd', models.CharField(max_length=250)),
                ('customer_mobile', models.CharField(max_length=10)),
                ('customer_default_pin_code', models.CharField(default='504103', max_length=6)),
                ('customer_address', models.ManyToManyField(blank=True, null=True, to='customer.address')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='customerID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer', verbose_name='CustomerID'),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('customer_orderd_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customer_order_timestamp', models.DateTimeField(auto_now_add=True)),
                ('customer_order_status', models.CharField(choices=[('ORDERED', 'Order Placed'), ('SHIPPED', 'Order Shipped'), ('REJECTED', 'Order Shipped'), ('RETURN', 'Order Returned')], default='ORDERED', max_length=150)),
                ('customer_order_return', models.BooleanField(default=False)),
                ('customerID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer', verbose_name='CustomerOrdered')),
                ('customer_order_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.address')),
                ('customer_ordered_products', models.ManyToManyField(to='seller.product', verbose_name='listofProductsOrdred')),
                ('customer_ordered_sellerID', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.seller', verbose_name='OrderedFulFillOrderedID')),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='customer_orders',
            field=models.ManyToManyField(blank=True, null=True, to='customer.order'),
        ),
        migrations.CreateModel(
            name='Return',
            fields=[
                ('customer_order_return_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('customer_order_return_status', models.CharField(choices=[('PENDING', 'Return View Pending'), ('ACCEPTED', 'Return Accepted'), ('REJECTED', 'Return Rejected')], default='PENDING', max_length=150)),
                ('customer_return_order_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='customer_order_returnID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.return', verbose_name='ReturnID'),
        ),
    ]
