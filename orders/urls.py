from inspect import getmembers
from tkinter import N
from django.urls import path 
from .views import getMyOrders, getOrders, getOrderById, addOrderItems, updateOrderToDelivered, updateOrderToPaid

app_name = 'orders' 

urlpatterns = [
    path('', getOrders, name='order'),
    path('add/', addOrderItems, name='add-orders'),
    path('my-orders/', getMyOrders, name='my-orders'),
    path('<str:pk>/', updateOrderToDelivered, name='order-delivered'),
    path('<str:pk>/', getOrderById, name='user-order'),
    path('<str:pk>/pay/', updateOrderToPaid, name='pay')
]