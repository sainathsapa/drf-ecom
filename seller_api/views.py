from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from customer.models import Order
from customer_api.serializers import CustomerOrderSerializer
from .serializers import *
from rest_framework.permissions import IsAuthenticated

from seller.models import Seller
from rest_framework.authentication import BasicAuthentication
from .auth import CustomAuthToken, CustomAuthBackend
from .models import SellerAuthTokenModel


class OrderViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, CustomAuthToken, CustomAuthBackend]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = CustomerOrderSerializer

    def list(self, request, *args, **kwargs):
        orders = Order.objects.all()
        serializer = CustomerOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, *args, **kwargs):
        order = self.get_object()
        serializer = CustomerOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        order = self.get_object()
        serializer = CustomerOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        order = self.get_object()
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    authentication_classes = [BasicAuthentication, CustomAuthToken, CustomAuthBackend]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        product = ProductSerializer().create(request.data)
        response = ProductSerializer(product, many=False).data
        return Response(response, status=status.HTTP_201_CREATED)

    def list(self, request):
        product = Product.objects.all()
        product_ser = ProductSerializer(product, many=True)
        return Response(product_ser.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        product = Product.objects.filter(product_id=pk)
        if product.count():
            prod_ser = ProductSerializer(product.first(), many=False)
            return Response(prod_ser.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            {"ERROR": 404, "Message": "NO Prod FOUND"}, status=status.HTTP_404_NOT_FOUND
        )

    def update(self, request, pk=None):
        product = Product.objects.filter(product_id=pk).first()

        product_ser = ProductSerializer(product, data=request.data)
        if product_ser.is_valid():
            product_ser.save()
            return Response("Data Updated")

        return Response("Data Updated Failed")

    def adress(self, request):
        return Response("Address")

    def delete(self, request, pk=None):
        address = Customer.objects.filter(customer_id=pk).delete()
        return Response(
            {"SUCESS": "DELETED", "Message": "Record Deleted"},
            status=status.HTTP_200_OK,
        )


class AuthTokenViewSet(viewsets.ViewSet):
    def create(self, request):
        seller_object = Seller.objects.filter(
            seller_user_id=request.data["seller_user_id"],
            seller_pwd=request.data["seller_pwd"],
        ).first()

        if seller_object:
            token = SellerAuthTokenModel.objects.create(seller=seller_object)
            # print(token.key)
            return Response(
                {"Success": "Login", "Token": token.key}, status=status.HTTP_201_CREATED
            )
        else:
            return Response({"ERROR": "NO USER"}, status=status.HTTP_201_CREATED)
