from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from carts.models import Cart


class CartListView(LoginRequiredMixin, ListView):
    model = Cart
    template_name = 'carts/cart.html'

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


class CartDeleteView(DeleteView):
    model = Cart
    success_url = reverse_lazy('carts:cart_list')
