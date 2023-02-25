from django.db.models import F, Sum, Prefetch

from orders.models import Order, OrderDetails


def get_orders(user):
    """Получить заказы товаров пользователя"""
    orders = (Order.objects.
              filter(user=user).
              prefetch_related(Prefetch('orderdetails_set', queryset=OrderDetails.objects.select_related('product'))).
              annotate(total_price=Sum(F('orderdetails__quantity') * F('orderdetails__unit_price')))
              )
    return orders
