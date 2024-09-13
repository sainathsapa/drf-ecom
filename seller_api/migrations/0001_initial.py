# Generated by Django 5.0.1 on 2024-01-30 09:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("seller", "0003_product_product_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="SellerAuthTokenModel",
            fields=[
                (
                    "key",
                    models.CharField(
                        max_length=40,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Key",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "seller",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="auth_token",
                        to="seller.seller",
                        verbose_name="Seller",
                    ),
                ),
            ],
        ),
    ]
