from django.db.models import Sum

from carts.models import Cart


def count_cart_user_context_processor(request):
    """Добавление на все страницы сайта информации о количестве товаров в
    корзине пользователя"""
    context = {}
    if request.user.is_authenticated:
        count_cart_user = (Cart.objects.
                           filter(user=request.user).
                           annotate(count=Sum('quantity')).
                           all())
        context['count_cart_user'] = count_cart_user
    return context
