# Generated by Django 5.0.1 on 2024-01-24 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0015_alter_customer_options_alter_customer_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='is_authenticated',
            field=models.BooleanField(default=False),
        ),
    ]