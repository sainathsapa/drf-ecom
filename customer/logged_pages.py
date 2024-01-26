from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.forms.models import model_to_dict

from .models import Customer, Address, Order, Return
from seller.models import *
from .custom_forms import DisplayListOfProduct, CustomerAddressRegistationForm

# Create your views here.


def cat_list():
    return ProductCategory.objects.prefetch_related("category_products")


def check_login(func):
    def decorated(request, *args, **kwargs):
        if 'useremail' not in request.session:
            # return render(request, 'customer/error.html', {"ERROR": "Your Not Logged In"})
            return HttpResponseRedirect('/customer/login')
        return func(request, *args, **kwargs)
    return decorated


# class DashboardView(CreateView):
@check_login
def customer_dashboard(request):

    order_list = Order.objects.filter(customerID=get_user(request))[:5:-1]
    dash_dict = {}
    dash_dict['orders'] = Order.objects.filter(
        customerID=get_user(request)).count()

    dash_dict['returns'] = Order.objects.filter(
        customerID=get_user(request), customer_order_return=True).count()
    dash_dict['address'] = Address.objects.filter(
        customerID=get_user(request)).count()

    return render(
        request,
        "customer/logged_pages/dash.html",
        {"navCat": cat_list(),
         'customer_orders': order_list,
         'dash_dict': dash_dict
         },
    )


@check_login
def add_to_bag(request, id):
    if id not in request.session['user_cart']:
        request.session['user_cart'] += [id]
    return HttpResponseRedirect("/customer")


@check_login
def get_bag(request):

    # return HttpResponse(request.session['user_cart'])
    list_of_prod = [Product.objects.get(product_id=i)
                    for i in request.session['user_cart']]
    tot = sum([i.product_price for i in list_of_prod])
    user_address = Address.objects.all().filter(
        customerID=get_user(request))

    if (len(list_of_prod) == 0):
        return HttpResponseRedirect("/customer")

    return render(request, 'customer/logged_pages/view_cart.html', {
        "products": list_of_prod,
        'navCat': cat_list(),
        'product_value': tot,
        'user_address': user_address
    })


@check_login
def remove_bag(request, id):

    if id in request.session['user_cart']:
        request.session['user_cart'].remove(id)
        request.session.modified = True
    return HttpResponseRedirect('/customer/get_bag')


@check_login
def checkout(request):
    if request.method == "POST":
        # PROCESS ORDER
        list_of_prod = [Product.objects.get(product_id=i)
                        for i in request.session['user_cart']]
        list_of_seller = [i.seller_name for i in list_of_prod]

        address_id = request.POST.get('customer_address')
        create_order = Order.objects.create(customer_order_address=Address.objects.get(customer_address_id=address_id),
                                            customerID=get_user(request))
        create_order.customer_ordered_products.add(*list_of_prod)

        request.session['user_cart'] = []
        request.session.modified = True
        # PASS TO
        return HttpResponseRedirect('/customer/checkout')
    else:
        return render(
            request,
            "customer/logged_pages/thanks.html",
            {"navCat": cat_list(),
             }
        )


@check_login
def customer_orders(request):

    order_list = Order.objects.filter(customerID=get_user(request))[::-1]

    return render(
        request,
        "customer/logged_pages/orders.html",
        {"navCat": cat_list(),
         'customer_orders': order_list,
         },
    )


@check_login
def view_customer_order(request, id):

    order_list = Order.objects.get(customer_orderd_id=id)
    print(order_list)
    return render(
        request,
        "customer/logged_pages/view_order.html",
        {"navCat": cat_list(), 'customer_order': order_list},
    )


@check_login
def edit_customer_order(request, id):
    if request.method == "POST":
        new_address_for_order = request.POST.get(
            "customer_order_address_updated")
        update_order = Order.objects.filter(customer_orderd_id=id).update(
            customer_order_address=new_address_for_order)

        return HttpResponse(update_order)
    order_list = Order.objects.get(customer_orderd_id=id)
    dict_to_pass = {}
    dict_to_pass['user_address'] = Address.objects.all().filter(
        customerID=get_user(request))

    return render(request, 'customer/logged_pages/edit_order.html',
                  {
                      "navCat": cat_list(),
                      'user_det': dict_to_pass,
                      'customer_order': order_list
                  })


@check_login
def return_order(request, id):

    get_order = Order.objects.filter(customer_orderd_id=id)
    create_return = Return(
        customer_return_order_id=get_order.first()).save()
    get_order.update(customer_order_returnID=create_return.customer_order_return_id,
                     customer_order_return=True,
                     customer_order_status="RETURN")
    order_list = Order.objects.filter(customerID=get_user(request))[::-1]

    return render(
        request,
        "customer/logged_pages/orders.html",
        {"navCat": cat_list(),
         'customer_orders': order_list,
         "msg": {"status": "RETURN",
                 "message": "Orderd {order} has been requested for return by {user}".format(order=id, user=get_user(request))
                 }
         },
    )


@check_login
def cancel_order(request, id):

    get_order = Order.objects.filter(customer_orderd_id=id)
    get_order.update(
        customer_order_status="CANCEL")
    order_list = Order.objects.filter(customerID=get_user(request))[::-1]

    return render(
        request,
        "customer/logged_pages/orders.html",
        {"navCat": cat_list(),
         'customer_orders': order_list,
         "msg": {"status": "RETURN",
                 "message": "Order {order} has been cancelled by {user}".format(order=id, user=get_user(request))
                 }
         },
    )


@check_login
def view_customer_address(request):
    address_list = Address.objects.filter(customerID=get_user(request))

    if request.method == "POST":
        user_address_form = CustomerAddressRegistationForm(request.POST)
        if user_address_form.is_valid():
            un_commited_form = user_address_form.save(commit=False)
            un_commited_form.customerID = get_user(request)
            un_commited_form.save()

            return render(
                request,
                "customer/logged_pages/my_address.html",
                {"navCat": cat_list(), 'customer_address': address_list,
                  'form': CustomerAddressRegistationForm,
                 "msg": {"status": "UPDATE",
                         "message": "Address Added Successfully for {user}".format(user=get_user(request))
                         }
                 },

            )

    return render(
        request,
        "customer/logged_pages/my_address.html",
        {"navCat": cat_list(), 'customer_address': address_list,
         'form': CustomerAddressRegistationForm},
    )


@check_login
def edit_address(request, id):

    get_address = Address.objects.filter(
        customerID=get_user(request), customer_address_id=id)
    if request.method == "POST":
        address_list = Address.objects.filter(customerID=get_user(request))
        form_values = request.POST
        space_name = form_values['get_address_space_name']
        add_type = form_values['customer_address_type']
        street = form_values['customer_address_hno_street']
        add_city = form_values['customer_address_city']
        pin_code = form_values['customer_address_pin_code']

        get_address.update(
            customeraddress_space_name=space_name,

            customer_address_hno_street=street,

            customer_address_city=add_city,
            customer_address_type=add_type,

            customer_address_pin_code=pin_code

        )
        return render(
            request,
            "customer/logged_pages/my_address.html",
            {"navCat": cat_list(), 'customer_address': address_list,
                'form': CustomerAddressRegistationForm,
                "msg": {"status": "UPDATE",
                        "message": "Address Edited Successfully for {user}".format(user=get_user(request))
                        }
             },

        )

        return HttpResponse(request.POST)

    return render(
        request,
        "customer/logged_pages/edit_address.html",
        {"navCat": cat_list(), 'customer_address': get_address.first()}

    )


@check_login
def delete_address(request, id):

    get_address = Address.objects.filter(
        customerID=get_user(request), customer_address_id=id)
    address_list = Address.objects.filter(customerID=get_user(request))

    if request.method == "GET":
        get_address.delete()
        return render(
            request,
            "customer/logged_pages/my_address.html",
            {"navCat": cat_list(), 'customer_address': address_list,
                'form': CustomerAddressRegistationForm,
                "msg": {"status": "DELETE",
                        "message": "Address Deleted Successfully by {user}".format(user=get_user(request))
                        }
             },

        )


def get_user(request):
    return Customer.objects.get(customer_email=request.session['useremail'])
