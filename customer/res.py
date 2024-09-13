from .models import *
from seller.models import Product
from import_export import fields, resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
class CustomerResource(resources.ModelResource):
    # email = fields.Field(attribute='email', column_name='customer_email')
    customer_order_total_price = fields.Field(
        column_name='customer_order_total_price',
        attribute='order_total'
    )
    class Meta:
        model = Customer
        import_id_fields = ('customer_id', )

        exclude = ('is_anonymous','is_anonymous','is_authenticated','is_active','is_staff' )
    
    
    
class AddressResource(resources.ModelResource):
    customer_name = fields.Field(
        column_name='customer_name',
        attribute='customerID',
        widget=ForeignKeyWidget(Address, field='customer_name'))

    class Meta:
        model = Address
        import_id_fields = ('customer_address_id', )

        exclude=('customerID')
        
        
        
class OrderResource(resources.ModelResource):
    customer_order_total_price = fields.Field(
        column_name='customer_order_total_price',
        attribute='order_total'
    )
    
    customer_ordered_products = fields.Field(
        column_name='customer_ordered_products',
        attribute='customer_ordered_products',
        widget=ManyToManyWidget(Product, field='product_name', separator='|')
    )
    
    
    
    customer_ordered_product_avg_price = fields.Field(
        column_name='customer_ordered_product_avg_price',
        attribute='avg_price',
    )

    class Meta:
        model = Order
        import_id_fields = ('customer_orderd_id', )

        fields = (
            'customer_orderd_id',
            'customer_order_address',
            'customer_ordered_products',
            'customer_order_timestamp',
            'customerID',
            'customer_order_status',
            'customer_order_return',
            'customer_order_returnID',
            'customer_order_total_price',  # Include the new field for total price
        )
        export_order = fields

    def dehydrate_customer_order_total_price(self, order):
        return order.order_total()
