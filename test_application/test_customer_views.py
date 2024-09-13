from django.test import TestCase
from django.urls import reverse, resolve
from customer.views import (
    IndexPageCustomer,
    ViewProduct,
    viewCatList,
    CustomerRegisterView,
    LogginPageView,
    LogOutView,
)

from customer.logged_pages import (
    customer_dashboard,
    customer_orders,
    add_to_bag,
    get_bag,
    remove_bag,
    checkout,
    view_customer_order,
    edit_customer_order,
    return_order,
    cancel_order,
    view_customer_address,
    edit_address,
    delete_address,
)


class CustomerURLsTestCase(TestCase):
    def test_index_page_customer_url(self):
        url = reverse('index')
        self.assertEqual(url, '/customer/')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, IndexPageCustomer)

    def test_view_product_url(self):
        url = reverse('customer_product_view', kwargs={'id': 1})
        self.assertEqual(url, '/customer/view_product/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, ViewProduct)

    def test_view_cat_list_url(self):
        url = reverse('customer_view_list', kwargs={'catList': '1,2,3'})
        self.assertEqual(url, '/customer/view_cat/1,2,3')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, viewCatList)

    def test_customer_register_url(self):
        url = reverse('customer_register')
        self.assertEqual(url, '/customer/register')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, 'view')

    def test_loggin_page_url(self):
        url = reverse('customer_login')
        self.assertEqual(url, '/customer/login')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, 'view')

    def test_log_out_url(self):
        url = reverse('customer_logout')
        self.assertEqual(url, '/customer/logout')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func.__name__, 'view')

    def test_customer_dashboard_url(self):
        url = reverse('customer_dashboard')
        self.assertEqual(url, '/customer/dashboard')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, customer_dashboard)

    def test_customer_orders_url(self):
        url = reverse('customer_orders')
        self.assertEqual(url, '/customer/orders')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, customer_orders)

    def test_customer_add_to_bag_url(self):
        url = reverse('customer_add_to_bag', kwargs={'id': 1})
        self.assertEqual(url, '/customer/add_to_bag/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, add_to_bag)

    def test_customer_get_bag_url(self):
        url = reverse('customer_get_bag')
        self.assertEqual(url, '/customer/get_bag')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, get_bag)

    def test_customer_remove_bag_item_url(self):
        url = reverse('customer_remove_bag_item', kwargs={'id': 1})
        self.assertEqual(url, '/customer/remove_bag/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, remove_bag)

    def test_customer_checkout_cart_url(self):
        url = reverse('customer_checkout_cart')
        self.assertEqual(url, '/customer/checkout')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, checkout)

    def test_customer_view_order_url(self):
        url = reverse('customer_view_order', kwargs={'id': 1})
        self.assertEqual(url, '/customer/view_order/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, view_customer_order)

    def test_customer_edit_order_url(self):
        url = reverse('customer_edit_order', kwargs={'id': 1})
        self.assertEqual(url, '/customer/edit_order/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, edit_customer_order)

    def test_customer_return_order_url(self):
        url = reverse('customer_return_order', kwargs={'id': 1})
        self.assertEqual(url, '/customer/return_order/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, return_order)

    def test_customer_cancel_order_url(self):
        url = reverse('customer_cancel_order', kwargs={'id': 1})
        self.assertEqual(url, '/customer/cancel_order/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, cancel_order)

    def test_customer_list_address_url(self):
        url = reverse('customer_list_address')
        self.assertEqual(url, '/customer/my_address')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, view_customer_address)

    def test_customer_edit_address_url(self):
        url = reverse('customer_edit_address', kwargs={'id': 1})
        self.assertEqual(url, '/customer/edit_address/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, edit_address)

    def test_customer_delete_address_url(self):
        url = reverse('customer_delete_address', kwargs={'id': 1})
        self.assertEqual(url, '/customer/delete_address/1')
        resolver_match = resolve(url)
        self.assertEqual(resolver_match.func, delete_address)