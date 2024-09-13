from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from .res import *
# Register your models here.

class SellerAdmin(ImportExportModelAdmin):
    resource_class = SellerResource
    
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
# add models to ADMIN_SITE
admin.site.register(Seller, SellerAdmin)
admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)

