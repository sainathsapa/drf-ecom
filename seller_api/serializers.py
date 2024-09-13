from rest_framework import serializers
from customer.models import Order, Customer, Address
from seller.models import ProductCategory, Product


class ProductTypeSerializer(serializers.ModelSerializer):
    # from .serializers import CustomerProfileSerializer
    # customer = CustomerProfileSerializer(many=False)
    # customer = Customer.objects.filter(customer_id=).first()

    class Meta:
        model = ProductCategory
        fields = "__all__"

    def create(self, validated_data):
        create_address = ProductCategory.objects.create(**validated_data)

        return create_address

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        # If 'id' is present in the input data, include it in the internal value
        if "category_products" in data:
            ret["category_products"] = data["category_products"]

        return ret

    def update(self, instance, validated_data):
        category_products = validated_data.pop(
            "category_products", instance.category_products
        )

        instance.category_name = validated_data.get(
            "category_name", instance.category_name
        )
        print(category_products)
        for product in category_products:
            product_id = Product.objects.filter(product_id=product)
            if product_id.exists():
                instance.category_products.add(product_id)

            else:
                return "Return Create Product First"

        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    # customer_address = serializers.SerializerMethodField('return_address')
    product_category = ProductTypeSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"

    # def return_address(self, obj):

    #     customer_address_list=Address.objects.all().filter(customerID=obj.customer_id)
    #     return  CustomerAddressSerilizer(customer_address_list, many=True).data

    def create(self, validated_data):
        category = validated_data.pop("category_products")

        product = Product.objects.create(**validated_data)
        for cat in category:
            temp_cat_id = ProductCategory.objects.create(**cat)
            product.category_products.add(temp_cat_id)
        return product

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        if "category_products" or "products_sellers" in data:
            ret["product_category"] = data["product_category"]

        return ret

    def update(self, instance, validated_data):
        instance.product_name = validated_data.get(
            "product_name", instance.product_name
        )
        instance.product_price = validated_data.get(
            "product_price", instance.product_price
        )
        cat_lsit = validated_data.pop("product_category")
        instance.product_category.set(None)
        instance.save()

        for cat in cat_lsit:
            cat_id = ProductCategory.objects.filter(category_id=cat.get("category_id"))
            if cat_id.exists():
                instance.product_category.add(
                    cat_id.first().category_id
                )  # i['customerID']=instance

            else:
                self.create_prod(instance, cat)
                print("ADD Create")

        instance.save()
        return instance

    def create_prod(self, instance, data):
        temp_type_id = ProductCategory.objects.create(**data)
        instance.product_category.add(temp_type_id)
        return True


class CustomerOrderSerializer(serializers.ModelSerializer):
    # customerID = CustomerProfileSerializer(many=False)
    # customer_address = CustomerAddressSerilizer(many=False)
    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data, pk):
        order_products = validated_data.pop("customer_ordered_products")
        # print(order_products)
        validated_data["customerID"] = pk
        order = Order.objects.create(**validated_data)
        for prod in order_products:
            order.customer_ordered_products.add(prod)
        return {"Order": "Created", "Sucess": "OK"}

    def update(self, instance, validated_data):
        instance.customer_order_status = validated_data.get(
            "customer_order_status", instance.customer_order_status
        )

        return instance
