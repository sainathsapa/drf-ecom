from django.test import TestCase
from faker import Faker
from customer.models import Customer, Address, Order, Return

class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.customer = Customer.objects.create(
            customer_name=self.fake.name(),
            customer_email="sainath.sit@gmail.com",
            customer_pwd=self.fake.password(),
            customer_mobile=self.fake.phone_number()
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.customer_name, self.customer.customer_name)
        self.assertEqual(self.customer.customer_email, self.customer.customer_email)
        self.assertEqual(self.customer.customer_pwd, self.customer.customer_pwd)
        self.assertEqual(self.customer.customer_mobile, self.customer.customer_mobile)

class AddressModelTestCase(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.customer = Customer.objects.create(
            customer_name=self.fake.name(),
            customer_email="sainath.sit@gmail.com",
            customer_pwd=self.fake.password(),
            customer_mobile=self.fake.phone_number()
        )
        self.address = Address.objects.create(
            customeraddress_space_name=self.fake.word(),
            customer_address_hno_street=self.fake.street_address(),
            customer_address_city=self.fake.city(),
            customer_address_type=self.fake.random_element(elements=('HOME', 'OFFICE')),
            customer_address_pin_code=self.fake.zipcode(),
            customerID=self.customer
        )

    def test_address_creation(self):
        self.assertEqual(self.address.customeraddress_space_name, self.address.customeraddress_space_name)
        self.assertEqual(self.address.customer_address_hno_street, self.address.customer_address_hno_street)
        self.assertEqual(self.address.customer_address_city, self.address.customer_address_city)
        self.assertEqual(self.address.customer_address_type, self.address.customer_address_type)
        self.assertEqual(self.address.customer_address_pin_code, self.address.customer_address_pin_code)

class OrderModelTestCase(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.customer = Customer.objects.create(
            customer_name=self.fake.name(),
            customer_email="sainath.sit@gmail.com",
            customer_pwd=self.fake.password(),
            customer_mobile=self.fake.phone_number()
        )
        self.address = Address.objects.create(
            customeraddress_space_name=self.fake.word(),
            customer_address_hno_street=self.fake.street_address(),
            customer_address_city=self.fake.city(),
            customer_address_type=self.fake.random_element(elements=('HOME', 'OFFICE')),
            customer_address_pin_code=self.fake.zipcode(),
            customerID=self.customer
        )
        self.order = Order.objects.create(
            customer_order_address=self.address,
            customer_order_status=self.fake.random_element(elements=('ORDERED', 'SHIPPED', 'RETURN', 'CANCEL')),
            customerID=self.customer
        )

    def test_order_creation(self):
        self.assertEqual(self.order.customer_order_address, self.order.customer_order_address)
        self.assertEqual(self.order.customer_order_status, self.order.customer_order_status)

class ReturnModelTestCase(TestCase):
    def setUp(self):
        self.fake = Faker()
        self.customer = Customer.objects.create(
            customer_name=self.fake.name(),
            customer_email="sainath.sit@gmail.com",
            customer_pwd=self.fake.password(),
            customer_mobile=self.fake.phone_number()
        )
        self.address = Address.objects.create(
            customeraddress_space_name=self.fake.word(),
            customer_address_hno_street=self.fake.street_address(),
            customer_address_city=self.fake.city(),
            customer_address_type=self.fake.random_element(elements=('HOME', 'OFFICE')),
            customer_address_pin_code=self.fake.zipcode(),
            customerID=self.customer
        )
        self.order = Order.objects.create(
            customer_order_address=self.address,
            customer_order_status=self.fake.random_element(elements=('ORDERED', 'SHIPPED', 'RETURN', 'CANCEL')),
            customerID=self.customer
        )
        self.return_order = Return.objects.create(
            customer_order_return_status=self.fake.random_element(elements=('PENDING', 'ACCEPTED', 'REJECTED')),
            customer_return_order_id=self.order
        )

    def test_return_creation(self):
        self.assertEqual(self.return_order.customer_order_return_status, self.return_order.customer_order_return_status)
