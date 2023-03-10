from django.db.models import F, Sum

from carts.models import Cart


def get_carts(user):
    """Получить корзину товаров пользователя"""
    carts = (Cart.objects.
             filter(user=user).
             select_related('product').
             annotate(total_price=(F('quantity') * F('product__price')))
             )
    return carts


def get_carts_and_images(user):
    """Получить корзину товаров пользователя c картинками товаров"""
    carts = get_carts(user).prefetch_related('product__images')
    return carts


def get_total_price_carts(user):
    """Получить стоимость корзины пользователя"""
    total_price_carts = (Cart.objects.
                         filter(user=user).
                         aggregate(total_price_carts=Sum(F('quantity') * F('product__price')))
                         )
    return total_price_carts
