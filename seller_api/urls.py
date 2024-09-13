from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('', HomeView.as_view() ,name="API Home"),
]
router = DefaultRouter()
router.register(r"order", OrderViewSet, basename="orders_seller")
router.register(r"product", ProductViewSet, basename="prod_seller")
router.register(r"auth_token_seller", AuthTokenViewSet, basename="AuthToken_seller")


urlpatterns += router.urls
