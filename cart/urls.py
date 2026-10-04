from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:dish_id>/', views.cart_add, name='cart_add'),
    path('increase/<int:dish_id>/', views.cart_increase, name='cart_increase'),
    path('decrease/<int:dish_id>/', views.cart_decrease, name='cart_decrease'),
    path('remove/<int:dish_id>/', views.cart_remove, name='cart_remove'),
]