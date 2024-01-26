from django.contrib import admin
from .models import *
# Register your models here.

# add models to ADMIN_SITE
admin.site.register(Customer)
admin.site.register(Address)
admin.site.register(Order)
admin.site.register(Return)

