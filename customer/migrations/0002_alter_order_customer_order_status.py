# Generated by Django 5.0.1 on 2024-01-13 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='customer_order_status',
            field=models.CharField(choices=[('ORDERED', 'Order Placed'), ('SHIPPED', 'Order Shipped'), ('RETURN', 'Order Returned')], default='ORDERED', max_length=150),
        ),
    ]
