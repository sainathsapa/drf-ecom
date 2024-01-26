# backends.py

from django.contrib.auth.backends import ModelBackend
from customer.models import Customer
from rest_framework.authentication import TokenAuthentication
from .models import UserAuthTokenModel


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            customer = Customer.objects.get(customer_email=username)

            if customer.customer_pwd == password:
                return customer
        except Customer.DoesNotExist:
            return None

    # def get_user(self,user)


class CustomAuthToken(TokenAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        print(token)
        if token:
            try:
                TokenFetch = UserAuthTokenModel.objects.get(key=token)
                print(TokenFetch)

                if TokenFetch.key == token:
                    return TokenFetch.customer, None
            except TokenFetch.DoesNotExist:
                return None
        else:
            return None, None


# class UserAuthTokenBackend(TokenAuthentication):
#     model = UserAuthTokenModel
