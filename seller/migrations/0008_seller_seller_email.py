# Generated by Django 5.0.1 on 2024-02-01 12:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("seller", "0007_product_product_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="seller",
            name="seller_email",
            field=models.EmailField(blank=True, max_length=150),
        ),
    ]