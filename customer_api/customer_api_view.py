from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from customer.models import Order, Customer, Address
from .serializers import (
    CustomerOrderSerializer,
    CustomerProfileSerializer,
    CustomerAddressSerilizer,
)


from rest_framework.authentication import BasicAuthentication
from .auth import CustomAuthToken, CustomAuthBackend
from .models import UserAuthTokenModel

# Create your views here.


class CustomerProfile(APIView):
    authentication_classes = [BasicAuthentication, CustomAuthToken, CustomAuthBackend]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customer_profile = Customer.objects.filter(customer_id=pk).first()
        response = CustomerProfileSerializer(customer_profile, many=False).data
        return Response(response, status=status.HTTP_200_OK)


class CustomerOrders(APIView):
    authentication_classes = [BasicAuthentication, CustomAuthToken, CustomAuthBackend]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        customer_order = Order.objects.filter(customer_orderd_id=pk).first()
        customer_order_response = CustomerOrderSerializer(customer_order, many=False)
        return Response(customer_order_response.data, status=status.HTTP_200_OK)

    def get(self, request, pk=None, order=None):
        customer_order = Order.objects.filter(
            customerID=pk, customer_orderd_id=order
        ).first()
        customer_order_response = CustomerOrderSerializer(customer_order, many=False)
        return Response(customer_order_response.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        # customer_order =.objects.filter(customer_orderd_id=pk).first()
        customer = Customer.objects.filter(customer_id=pk).first()
        customer_order_response = CustomerOrderSerializer(many=False).create(
            request.data, customer
        )
        return Response(customer_order_response, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, order=None):
        # customer_order =.objects.filter(customer_orderd_id=pk).first()

        order = Order.objects.filter(customer_orderd_id=order, customerID=pk).delete()
        return Response(
            {"SUCESS": "DELETED", "Message": "Record Deleted"},
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk=None, order=None):
        # customer_order =.objects.filter(customer_orderd_id=pk).first()

        order = Order.objects.filter(customer_orderd_id=order, customerID=pk).first()
        customer_ser = CustomerOrderSerializer(order, data=request.data)
        if customer_ser.is_valid():
            customer_ser.save()
        return Response(customer_ser.data, status=status.HTTP_200_OK)


class CustomerViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    authentication_classes = [BasicAuthentication, CustomAuthToken, CustomAuthBackend]
    permission_classes = [IsAuthenticated]


    def create(self, request):
        customer_create = CustomerProfileSerializer().create(request.data)
        response = CustomerProfileSerializer(customer_create, many=False).data
        return Response(response, status=status.HTTP_201_CREATED)

    def list(self, request):
        customer = Customer.objects.all()
        customer_ser = CustomerProfileSerializer(customer, many=True)
        return Response(customer_ser.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        customer = Customer.objects.filter(customer_id=pk)
        if customer.count():
            customer_ser = CustomerProfileSerializer(customer.first(), many=False)
            return Response(customer_ser.data, status=status.HTTP_202_ACCEPTED)
        return Response(
            {"ERROR": 404, "Message": "NO User FOUND"}, status=status.HTTP_404_NOT_FOUND
        )

    def update(self, request, pk=None):
        customer = Customer.objects.filter(customer_id=pk).first()

        customer_ser = CustomerProfileSerializer(customer, data=request.data)
        if customer_ser.is_valid():
            customer_ser.save()
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
        customer_object = Customer.objects.filter(
            customer_email=request.data["customer_email"],
            customer_pwd=request.data["customer_pwd"],
        ).first()

        if customer_object:
            token = UserAuthTokenModel.objects.create(customer=customer_object)
            # print(token.key)
            return Response(
                {"Success": "Login", "Token": token.key}, status=status.HTTP_201_CREATED
            )
        else:
            return Response({"ERROR": "NO USER"}, status=status.HTTP_201_CREATED)


class AfterAuthView(viewsets.ViewSet):
    def list(self, request):
        return Response({"Auth": "Token"}, status=status.HTTP_200_OK)
