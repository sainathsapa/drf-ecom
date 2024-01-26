from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

urlpatterns = [
    # path('', HomeView.as_view() ,name="API Home"),
]
router = DefaultRouter()
router.register(r"order", OrderViewSet, basename="orders")
router.register(r"product", ProductViewSet, basename="orders")
router.register(r"auth_token", AuthTokenViewSet, basename="AuthToken")


urlpatterns += router.urls
