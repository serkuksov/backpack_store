from django.shortcuts import render
from django.views.generic import ListView

from carts.models import Cart


class CartListView(ListView):
    model = Cart
    template_name = 'carts/cart.html'
