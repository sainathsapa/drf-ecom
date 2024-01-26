from django.contrib import admin
from .models import *
# Register your models here.

# add models to ADMIN_SITE
admin.site.register(Seller)
admin.site.register(ProductCategory)
admin.site.register(Product)

