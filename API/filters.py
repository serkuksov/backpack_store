from django_filters import rest_framework as filters

from products.models import Product, Category


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    """Фильтр для отображения списка продуктов"""
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = CharInFilter(field_name='category__name', lookup_expr='in')

    class Meta:
        model = Product
        fields = (
            'category',
        )
