from django.urls import path
from . import views
from .views import add_to_cart, view_cart
from .views import checkout
from .views import payment, order_success
from .views import generate_invoice
from .views import add_to_cart, update_cart, remove_from_cart

urlpatterns = [
    path('', views.Product_list, name= 'products' ),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/", view_cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("payment/<int:order_id>/", payment, name="payment"),
    path("order-success/<int:order_id>/", order_success, name="order_success"),
    path("invoice/<int:order_id>/", generate_invoice, name="generate_invoice"),
    path("update-cart/<int:cart_id>/", update_cart, name="update_cart"),
     path("remove-from-cart/<int:cart_id>/", remove_from_cart, name="remove_from_cart"),
]
