from django.shortcuts import render
from .models import Vendor
from .serializers import VendorSerializer

from rest_framework.response import Response 
from rest_framework.decorators import api_view
from rest_framework import status

from django.contrib.auth.hashers import make_password


@api_view(['GET'])
def get_vendors(request):
    vendors = Vendor.objects.all()
    serializer = VendorSerializer(vendors, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register_vendor(request):
    data = request.data
    try:
        vendor = Vendor.objects.create(
            name = data['name'],
            creator = data['creator'],
            password = make_password(data['password'])
        )
    except:
        message = {'detail':'Cannot create vendor'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
