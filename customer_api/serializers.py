from rest_framework import serializers
from customer.models import Order, Customer, Address


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "customer_name",
            "customer_email",
            "customer_pwd",
            "customer_mobile",
            "customer_default_pin_code",
            "customer_address",
            "customer_orders",
            'customer_name'
        ]


class CustomerAddressSerilizer(serializers.ModelSerializer):
    # from .serializers import CustomerProfileSerializer
    # customer = CustomerProfileSerializer(many=False)
    # customer = Customer.objects.filter(customer_id=).first()

    class Meta:
        model = Address
        fields = "__all__"

    def create(self, validated_data):
        # validated_data['customerID']=Customer.objects.filter(customer_id=validated_data['customerID'].customer_id).first()

        create_address = Address.objects.create(**validated_data)
        # customer = Customer.objects.filter(customer_id=c_id).first()
        # temp_address_id = Customer.objects.cre
        # create_address.customerID.set(customer)

        return create_address

    def update(self, instance, validated_data):
        # address_list = validated_data.get('customer_address', instance.customer_address)

        instance.customeraddress_space_name = validated_data.get(
            "customeraddress_space_name", instance.customeraddress_space_name
        )
        instance.customer_address_hno_street = validated_data.get(
            "customer_address_hno_street", instance.customer_address_hno_street
        )
        instance.customer_address_city = validated_data.get(
            "customer_address_city", instance.customer_address_city
        )
        instance.customer_address_type = validated_data.get(
            "customer_address_type", instance.customer_address_type
        )
        instance.customer_address_pin_code = validated_data.get(
            "customer_address_pin_code", instance.customer_address_pin_code
        )
        instance.save()

        return instance


class CustomerProfileSerializer(serializers.ModelSerializer):
    # customer_address = serializers.SerializerMethodField('return_address')
    customer_address = CustomerAddressSerilizer(many=True)

    class Meta:
        model = Customer
        fields = [
            "customer_name",
            "customer_email",
            "customer_mobile",
            "customer_default_pin_code",
            "customer_address",
        ]

    # def return_address(self, obj):

    #     customer_address_list=Address.objects.all().filter(customerID=obj.customer_id)
    #     return  CustomerAddressSerilizer(customer_address_list, many=True).data

    def create(self, validated_data):
        address = validated_data.pop("customer_address")

        customer = Customer.objects.create(**validated_data)
        for ad in address:
            ad["customerID"] = customer
            temp_address_id = Address.objects.create(**ad)
            customer.customer_address.add(temp_address_id)
        return customer

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        # If 'id' is present in the input data, include it in the internal value
        if "customer_address" in data:
            ret["customer_address"] = data["customer_address"]

        return ret

    def update(self, instance, validated_data):
        instance.customer_name = validated_data.get(
            "customer_name", instance.customer_name
        )
        instance.customer_email = validated_data.get(
            "customer_email", instance.customer_email
        )
        instance.customer_mobile = validated_data.get(
            "customer_mobile", instance.customer_mobile
        )
        instance.customer_default_pin_code = validated_data.get(
            "customer_default_pin_code", instance.customer_default_pin_code
        )
        address_list = validated_data.pop("customer_address")
        print(address_list)
        for address_data in address_list:
            address_id = address_data.get("customer_address_id")
            if address_id:
                ad_instance = Address.objects.filter(
                    customer_address_id=address_id
                ).first()  # i['customerID']=instance
                ser = CustomerAddressSerilizer(ad_instance, data=address_data)
                if ser.is_valid():
                    ser.save()

            else:
                self.create_address(instance, address_data)
                print("ADD Create")

        instance.save()
        return instance

    def create_address(self, instance, data):
        data["customerID"] = instance
        temp_address_id = Address.objects.create(**data)
        instance.customer_address.add(temp_address_id)
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
        return {"Order": "Created", "Success": "OK"}

    def update(self, instance, validated_data):
        instance.customer_order_status = validated_data.get(
            "customer_order_status", instance.customer_order_status
        )

        instance.save()
        return instance
