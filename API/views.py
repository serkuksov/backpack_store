from django.shortcuts import render
from rest_framework import generics

from API.serializers import ProductSerializer
from products.models import Product


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
