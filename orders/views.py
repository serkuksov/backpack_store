from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from carts.models import Cart
from carts.servises import get_carts, get_total_price_carts
from .models import *
from .forms import *


class AddressCreateView(LoginRequiredMixin, generic.CreateView):
    """Добавление адреса доставки заказа"""
    model = Address
    form_class = AddressForm


class OrderCreateView(AddressCreateView):
    """Оформление заказа и отображение продуктов в заказе"""
    template_name = 'orders/order_create.html'

    def get_success_url(self):
        return reverse('users_detail:account', kwargs={'pk': self.request.user.pk})

    @transaction.atomic
    def form_valid(self, form):
        self.object = form.save()
        order = Order.objects.create(user=self.request.user,
                                     address=self.object)
        carts = Cart.objects.filter(user=self.request.user).all()
        for cart in carts:
            OrderDetails.objects.create(order=order,
                                        product=cart.product,
                                        quantity=cart.quantity,
                                        unit_price=cart.product.price)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context | {
            'carts': get_carts(self.request.user),
        } | get_total_price_carts(self.request.user)
        return context
