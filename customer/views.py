from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse
from django.views import View
from .custom_forms import CustomerRegistration, CustomerAddressRegistationForm
from .models import Customer, Address
from django.views.generic.edit import CreateView
from seller.models import *

# Create your views here.


class CustomerRegisterView(CreateView):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "customer/register.html",
            {"navCat": cat_list(), "userForm": CustomerRegistration,
             "userAddressForm": CustomerAddressRegistationForm},
        )

    def post(self, request, *args, **kwargs):

        # PERSONAL DETAILS
        personal_name = request.POST.get("customer_name")
        personal_email = request.POST.get("customer_email")
        personal_pwd = request.POST.get("customer_pwd")
        personal_mobile = request.POST.get("customer_mobile")

        address_space = request.POST.get("customeraddress_space_name")
        address_type = request.POST.get("customer_address_type")
        address_steet = request.POST.get("customer_address_hno_street")
        address_city = request.POST.get("customer_address_city")
        address_pin = request.POST.get("customer_address_pin_code")
        saveUserModel = Customer(customer_name=personal_name, customer_email=personal_email,
                                 customer_pwd=personal_pwd, customer_mobile=personal_mobile, customer_default_pin_code=address_pin)
        saveUserModel.save()
        saveAddressModel = Address(customeraddress_space_name=address_space, customer_address_hno_street=address_steet,
                                   customer_address_city=address_city, customer_address_type=address_type, customer_address_pin_code=address_pin, customerID=saveUserModel)
        saveAddressModel.save()
        # request.session['userlogin'] = saveUserModel
        return render(request, 'customer/reg_sucess.html')


def IndexPageCustomer(request):
    # print([i.category_products.all() for i in product_cat_list.all()])

    return render(
        request, "customer/index.html", {"navCat": cat_list(),
                                         "ProdCat": cat_list()}
    )


def ViewProduct(request, id):
    get_product_info = Product.objects.filter(product_id=id)[0]
    return render(
        request,
        "customer/view_product.html",
        {"navCat": cat_list(), "ProdCat": cat_list(), "Product": get_product_info},
    )


def viewCatList(request, catList):
    product_listof_Cat = [
        Product.objects.all().filter(
            product_category=ProductCategory.objects.get(category_id=i)
        )
        for i in catList.split(",")
    ]
    print(product_listof_Cat)
    # productList = {}
    # for cat in product_listof_Cat:
    #     tempProductFetch = Product.objects.filter(product_category=cat)
    #     print(tempProductFetch)
    # product_listof_Cat = [Product.objects.all().filter()]

    return render(
        request,
        "customer/view_cat.html",
        {"navCat": cat_list(), "ProdCat": product_listof_Cat},
    )


def cat_list():
    return ProductCategory.objects.prefetch_related("category_products")


class LogginPageView(CreateView):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(
            request,
            "customer/login.html",
            {"navCat": cat_list()},
        )

    def post(self, request: HttpRequest, *args: str, **kwargs: Any):

        userEmail = request.POST.get("email")

        userPWD = request.POST.get("password")

        user_model_fetch = Customer.objects.get(
            customer_email=userEmail, customer_pwd=userPWD)
        if (user_model_fetch):
            request.session['useremail'] = user_model_fetch.customer_email
            request.session['user_cart'] = []

            return HttpResponseRedirect("/customer/dashboard")


class LogOutView(CreateView):
    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        del request.session['useremail']
        return render(request, 'customer/error.html', {"ERROR": "User Logged out sucessfully"})
