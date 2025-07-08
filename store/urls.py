from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('producto/<int:pk>/', views.product_detail, name='product_detail'),  
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.order_create, name='order_create'),
    path('register/', views.register, name='register'),
    path('mis-pedidos/', views.order_history, name='order_history'),
]

