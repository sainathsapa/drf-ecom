# backends.py

from django.contrib.auth.backends import ModelBackend
from seller.models import Seller
from rest_framework.authentication import TokenAuthentication
from .models import SellerAuthTokenModel


class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            seller = Seller.objects.get(seller_user_id=username)

            if seller.seller_pwd == password:
                return seller
        except Seller.DoesNotExist:
            return None

    # def get_user(self,user)


class CustomAuthToken(TokenAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        print(token)
        if token:
            try:
                TokenFetch = SellerAuthTokenModel.objects.get(key=token)
                print(TokenFetch)

                if TokenFetch.key == token:
                    return TokenFetch.seller, None
            except TokenFetch.DoesNotExist:
                return None
        else:
            return None, None


