# Generated by Django 5.0.1 on 2024-01-30 09:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("seller", "0004_product_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="product_image",
            field=models.ImageField(blank=True, null=True, upload_to=None),
        ),
    ]
