from django.urls import path 
from .views import get_vendors, register_vendor

app_name = 'vendors'

urlpatterns = [
    path('', get_vendors, name='vendors'),
    path('register/', register_vendor, name='register_vendor')
]