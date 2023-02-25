from django.db.models import F, Sum

from orders.models import Order


def get_orders(user):
    """Получить заказы товаров пользователя"""
    orders = (Order.objects.
              filter(user=user).
              prefetch_related('orderdetails_set').
              annotate(total_price=Sum(F('orderdetails__quantity') * F('orderdetails__unit_price')))
              )
    return orders
