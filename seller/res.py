from customer.models import *
from .models import *
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget


class SellerResource(resources.ModelResource):
    class Meta:
        model = Seller
        import_id_fields = ('seller_id', )

        exclude = ('is_anonymous','is_anonymous','is_authenticated','is_active','is_staff' )      
        
    
    
# class OrderResource(resources.ModelResource):
#     customer_name = fields.Field(
#         column_name='customer_name',
#         attribute='customerID',
#         widget=ForeignKeyWidget(Customer, field='customer_name'))
    
#     customer_order_address = fields.Field(
#         column_name='customer_address',
#         attribute='customer_order_address',
#         widget=ForeignKeyWidget(Address, field='customeraddress_space_name'))
    
#     customer_ordered_products = fields.Field(
#         column_name='customer_ordered_products',
#         attribute='customer_ordered_products',
#         widget=ManyToManyWidget(Product, field='product_name', separator='|')
#     )
#     class Meta:
#         model = Order
#         import_id_fields = ('customer_orderd_id', )

        
        
        
        
class ProductResource(resources.ModelResource):
    product_category = fields.Field(
        column_name='product_category',
        attribute='product_category',
        widget=ManyToManyWidget(ProductCategory, field='category_name', separator='|')
    )
    
    products_sellers = fields.Field(
        column_name='products_sellers',
        attribute='products_sellers',
        widget=ManyToManyWidget(Seller, field='seller_name', separator='|')
    )
    
    
    # product_image = fields.Field(
    #             column_name='product_image',
    #             attribute='product_image',

    # )
    class Meta:
        model = Product
        import_id_fields = ('product_id', )

        