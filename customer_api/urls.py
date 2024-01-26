"""
URL configuration for eCommerce_Django_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from .views import HomeView
from .customer_api_view import *
from rest_framework.routers import DefaultRouter

# from .auth_view import CustomerAuthenticationView

urlpatterns = [
    path("home", HomeView.as_view(), name="API Home"),
    path("home_profile/<str:pk>", CustomerProfile.as_view(), name="Customer Details"),
    path("order/<str:pk>/", CustomerOrders.as_view(), name="Order Details"),
    path("order/<str:pk>/<str:order>/", CustomerOrders.as_view(), name="Order Retrive"),
    path("auth/", AfterAuthView.as_view({"get": "list"}), name="Auth Login"),
    # path("auth/", CustomerAuthenticationView.as_view(), name="customer-authentication"),
]
router = DefaultRouter()
router.register(r"customer", CustomerViewSet, basename="customer")
router.register(r"auth_token", AuthTokenViewSet, basename="auth_token")


# router.register(r'address', AddressViewSet, basename="address")
# router.register(r'orders', OrderViewSet, basename="orders")


# router.register(r'orders', AddressViewSet, basename="address")


urlpatterns += router.urls
