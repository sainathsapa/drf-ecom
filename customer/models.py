from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser

# Create your models here.
# from seller.models import Product


class Customer(models.Model):
    """
    CUSTOMER MODEL

    Customer model for end user to utilize auth services and other operations
    """

    REQUIRED_FIELDS = (
        "customer_name",
        "customer_mobile",
    )
    USERNAME_FIELD = "customer_email"
    PASSWORD_FIELD = "customer_pwd"

    customer_id = models.BigAutoField(primary_key=True)
    customer_name = models.CharField(max_length=50)
    customer_email = models.EmailField(max_length=60, unique=True)
    customer_pwd = models.CharField(max_length=250)

    customer_mobile = models.CharField(max_length=10)
    customer_default_pin_code = models.CharField(max_length=6, default="504103")
    customer_address = models.ManyToManyField("customer.Address", null=True, blank=True)
    customer_orders = models.ManyToManyField("customer.Order", null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    def __str__(self):
        return self.customer_name

    # def check_password(self,pwd):
    #     return True if self.customer_pwd == pwd else False


class Address(models.Model):
    ADDRESS_TYPE_CHOOSE = (
        (
            "HOME",
            "HOME TYPE [ ALL_DAY_DELIVERY ]",
        ),
        (
            "OFFICE",
            "COMMERICAL [ DELIVERY_ON_WORKING_DAYS_9AM_-_10PM ]",
        ),
    )

    customer_address_id = models.BigAutoField(primary_key=True)
    customeraddress_space_name = models.CharField(max_length=50)
    customer_address_hno_street = models.CharField(max_length=150)
    customer_address_city = models.CharField(max_length=30)

    customer_address_type = models.CharField(
        choices=ADDRESS_TYPE_CHOOSE, default="HOME", max_length=150
    )
    customer_address_pin_code = models.CharField(max_length=6)
    customerID = models.ForeignKey(
        "Customer", verbose_name="CustomerID", on_delete=models.CASCADE, null=True
    )

    # def __str__(self):
    #     return self.customerID.customer_name + " ADDRESS " + str(self.customer_address_id)

    def get_address_space_name(self):
        return self.customeraddress_space_name

    def complete_address(self):
        return self.customer_address_hno_street + self.customer_address_city


class Order(models.Model):
    ORDER_STATUS = (
        ("ORDERED", "Order Placed"),
        ("SHIPPED", "Order Shipped"),
        ("RETURN", "Order Returned"),
        ("CANCEL", "Order Cancelled"),
    )

    customer_orderd_id = models.BigAutoField(primary_key=True)
    customer_order_address = models.ForeignKey(
        "Address", on_delete=models.CASCADE, blank=True, null=True
    )
    customer_ordered_products = models.ManyToManyField(
        "seller.Product", verbose_name="listofProductsOrdred", blank=True, null=True
    )
    customer_order_timestamp = models.DateTimeField(auto_now_add=True)
    customerID = models.ForeignKey(
        "Customer", verbose_name="CustomerOrdered", on_delete=models.CASCADE, null=True
    )
    # customer_ordered_sellerID = models.ManyToManyField(
    #     "seller.Seller", verbose_name="OrderedFulFillOrderedID", on_delete=models.CASCADE, null=True)
    customer_order_status = models.CharField(
        max_length=150, choices=ORDER_STATUS, default="ORDERED"
    )
    customer_order_return = models.BooleanField(default=False)
    customer_order_returnID = models.ForeignKey(
        "Return",
        verbose_name="ReturnID",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # def test(self):
    #     return self.customerID.customer_name if self.customerID.customer_name else "" + " ORDER " + str(self.customer_orderd_id)

    def order_total(self):
        return sum([i.product_price for i in self.customer_ordered_products.all()])

    def sellers(self):
        return ", ".join(
            set(i.seller_name() for i in self.customer_ordered_products.all())
        )


class Return(models.Model):
    RETURN_STATUS = (
        ("PENDING", "Return View Pending"),
        ("ACCEPTED", "Return Accepted"),
        ("REJECTED", "Return Rejected"),
    )
    customer_order_return_id = models.BigAutoField(primary_key=True)
    customer_order_return_status = models.CharField(
        choices=RETURN_STATUS, max_length=150, default="PENDING"
    )
    customer_return_order_id = models.ForeignKey(
        "Order", blank=True, null=True, on_delete=models.CASCADE
    )

    # customer_ordered_return_sellerID = models.ForeignKey("seller.SellerUser", verbose_name="OrderedFulFillOrderedID", on_delete=models.CASCADE, null = True)

    def save(self, *args, **kwargs):
        super(Return, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return (
            self.customer_return_order_id.customerID.customer_name
            + " RETURN of ORDER "
            + str(self.customer_return_order_id.customer_orderd_id)
            + " FROM "
            + str(self.customer_return_order_id.sellers)
        )
