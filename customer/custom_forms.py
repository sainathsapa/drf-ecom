from django import forms
from .models import Customer, Order, Address
from seller.models import Product
from django.forms.widgets import CheckboxSelectMultiple
from django.forms.models import ModelMultipleChoiceField


class CustomerRegistration(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["customer_name", "customer_email",
                  "customer_pwd", "customer_mobile"]
        widgets = {i: forms.TextInput(
            attrs={"class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}) for i in fields}

    # date = forms.DateInput()
    # orders = forms.ModelMultipleChoiceField(
    #     queryset=Order.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )

    # Address = forms.ModelMultipleChoiceField(
    #     queryset=Address.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )


class CustomerAddressRegistationForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["customeraddress_space_name", "customer_address_type",
                  "customer_address_hno_street", "customer_address_city", "customer_address_pin_code"]
        widgets = {i: forms.TextInput(
            attrs={"class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"}) for i in fields}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer_address_type'] = forms.ChoiceField(
            choices=self._meta.model.ADDRESS_TYPE_CHOOSE)


class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "%s: %s Rs. %s" % (obj.product_name, obj.cat_name(), obj.product_price)


class DisplayListOfProduct(forms.ModelForm):

    Add_NewP_Products = CustomSelectMultiple(queryset=Product.objects.all())

    class Meta:
        model = Order
        exclude = ('customer_order_address', 'customer_ordered_products', 'customerID', 'customer_ordered_sellerID',
                   'customer_order_status', 'customer_order_return', 'customer_order_returnID')
