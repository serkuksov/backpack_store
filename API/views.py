from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import pagination
from rest_framework.response import Response

from API.serializers import *
from products.models import *


class ProductResultsSetPagination(pagination.PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductResultsSetPagination
    permission_classes = (permissions.AllowAny,)

    # @action(detail=False, methods=['get'])
    # def category(self, request):
    #     cat = Category.objects.all()
    #     serializer = CategorySerializer(instance=cat, many=True)
    #     return Response({'category': serializer.data})
