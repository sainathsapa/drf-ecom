from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from customer_api.models import UserAuthTokenModel
from customer.models import Customer


class CustomerAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_customer = Customer.objects.create(
            customer_name="Test Customer",
            customer_email="sainath.sit@gmail.com",
            customer_pwd="testpassword",
        )
        self.test_token = UserAuthTokenModel.objects.create(customer=self.test_customer)

        self.client.credentials(HTTP_AUTHORIZATION=self.test_token.key)
        self.headers = {"Authorization": self.test_token}

    def test_customer_profile(self):
        url = reverse("customer_details", kwargs={"pk": self.test_customer.pk})
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        
    def test_create_order(self):
        url = reverse("order_details", kwargs={"pk": self.test_customer.pk})
        order_data = {
            "customer_order_status": "ORDERED",
            "customer_order_return": False,
            "customer_order_returnID": None,
            "customer_ordered_products": [] 
        }
        response = self.client.post(url, order_data, format="json", headers=self.headers)
        self.assertEqual(response.status_code, 200)  # Assuming you return 200 on success
        # Add additional assertions as needed
    def test_order_details(self):
        url = reverse("order_details", kwargs={"pk": self.test_customer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_order_retrieve(self):
        order_id = "12345"  # Example order ID
        url = reverse(
            "order_retrieve", kwargs={"pk": self.test_customer.pk, "order": order_id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.client.logout()
