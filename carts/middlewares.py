from django.db.models import Sum

from carts.models import Cart


def count_cart_user_context_processor(request):
    context = {}
    if request.user.is_authenticated:
        if Cart.objects.filter(user=request.user).exists():
            context['count_cart_user'] = Cart.objects.filter(user=request.user).aggregate(Sum('quantity'))[
                'quantity__sum']
    return context
