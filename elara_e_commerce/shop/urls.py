from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    #URLS FOR CATEGORY
    path('categories/', views.category_list, name='category_list'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),

    #URLS FOR PRODUCTS
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>', views.product_detail, name='product_detail'),

    #URLS FOR CART
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    #URLS FOR ORDERS
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>', views.order_detail, name='order_detail'),

    #URLS FOR SHIPPING ADDRESS
    path('shipping/', views.shipping_address, name='shipping_address'),
]