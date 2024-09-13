from django.db import models


# Create your models here.
class Seller(models.Model):
    seller_id = models.BigAutoField(primary_key=True)
    seller_name = models.CharField(max_length=150, blank=True)
    seller_email = models.EmailField(max_length=150, blank=True)
    seller_user_id = models.CharField(max_length=50)
    seller_pwd = models.CharField(max_length=250)

    seller_city = models.CharField(max_length=50)
    seller_mobile = models.CharField(max_length=10)
    seller_products = models.ManyToManyField(
        "seller.Product", verbose_name="listOfSellerProd", null=True, blank=True
    )

    def __str__(self):
        return self.seller_name


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_price = models.IntegerField(max_length=6)
    product_image = models.ImageField(
        upload_to="files/products_images/",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True,
    )
    product_category = models.ManyToManyField(
        "seller.ProductCategory", verbose_name="listOfCat"
    )
    products_sellers = models.ManyToManyField("seller.Seller")
    product_quantity = models.IntegerField(default=1)

    def __str__(self):
        return (
            self.product_name
            + "  -  "
            + "".join(str(i) + ", " for i in self.product_category.all())
        )

    def cat_id(self):
        return ",".join(str(i.category_id) for i in self.product_category.all())

    def cat_name(self):
        return ", ".join(str(i) for i in self.product_category.all())

    def seller_name(self):
        return ", ".join(str(i) for i in self.products_sellers.all())


class ProductCategory(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    category_products = models.ManyToManyField(
        "seller.Product", verbose_name="listOfProd", blank=True, null=True
    )

    def __str__(self):
        return self.category_name
