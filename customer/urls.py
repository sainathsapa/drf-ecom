from django.urls import path

# importing views from views..py
from .views import CustomerRegisterView, LogginPageView, LogOutView, IndexPageCustomer, ViewProduct, viewCatList
from .logged_pages import *
urlpatterns = [
    path("", IndexPageCustomer, name="IndexView of Customer"),
    path("view_product/<int:id>", ViewProduct, name="View Product Customer"),
    path("view_cat/<str:catList>", viewCatList,
         name="View Product CatList Customer"),
    path("register", CustomerRegisterView.as_view()),
    path("login", LogginPageView.as_view()),
    path("logout", LogOutView.as_view()),




    # LoggedUserPages
    path("dashboard", customer_dashboard),
    path("orders", customer_orders),
    path("add_to_bag/<int:id>", add_to_bag),
    path("get_bag", get_bag),

    path("remove_bag/<int:id>", remove_bag),
    path("checkout", checkout),

    path("view_order/<int:id>", view_customer_order),
    path("edit_order/<int:id>", edit_customer_order),
    path("return_order/<int:id>", return_order),
    path("cancel_order/<int:id>", cancel_order),




    path("my_address", view_customer_address),
    path("edit_address/<int:id>", edit_address),
    path("delete_address/<int:id>", delete_address),




]



