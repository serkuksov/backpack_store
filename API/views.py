from rest_framework import viewsets
from rest_framework import generics
from rest_framework import permissions
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from API.serializers import *
from carts.models import Cart
from products.models import *
from products.servises import get_products
from .filters import *


class ProductListPagination(pagination.PageNumberPagination):
    """Пагинатор для списка товаров"""
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10


class ProductListAPIView(generics.ListAPIView):
    """Отображение списка товаров, картинок и отзывов к ним"""
    queryset = get_products().select_related('brand', 'category', 'colour').prefetch_related('review_set').all()
    serializer_class = ProductSerializer
    pagination_class = ProductListPagination
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    filterset_class = ProductFilter
    search_fields = (
        'name',
        'brand__name',
        'description',
    )
    ordering_fields = (
        'id',
        'price',
        'arefmetical_averages_review',
    )


class BrandListView(APIView):
    """Отображение списка брендов"""
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        brand = Brand.objects.all()
        serializer = BrandSerializer(brand, many=True)
        brand_names = [brand['name'] for brand in serializer.data]
        return Response(brand_names)


class CartViewSet(viewsets.ModelViewSet):
    """CRUD корзины пользователя"""
    serializer_class = CartSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user).select_related('product').all()
        return queryset

    def perform_create(self, serializer):
        """Создание объекта корзины с привязкой к пользователю из запроса"""
        serializer.save(user=self.request.user)
