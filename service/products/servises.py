from django.db.models import Prefetch, Avg, Count

from products.models import *
from reviews.models import *


def get_products():
    """Получить продукты с сортировкой по количеству заказов"""
    products = (Product.objects.
                prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                annotate(arefmetical_averages_review=Avg('review__rating')))
    return products


def get_detail_product():
    """Получить продукт со всеми параметрами и отзывами"""
    product = (get_products().select_related('brand', 'category').
               prefetch_related('review_set').
               annotate(count_review=Count('review'))
               )
    return product


def get_top_products():
    """Получить 4 самых топовых продукта по количеству заказов"""
    top_products = get_products().order_by('-arefmetical_averages_review', '-id')[:4]
    return top_products


def get_new_products():
    """Получить 8 последне добавленных товара"""
    new_products = get_products().order_by('-id')[:8]
    return new_products


def is_review_user(product, user):
    """Проверка наличия отзывов у пользователя для продукта"""
    return Review.objects.filter(product=product, user=user).exists()
