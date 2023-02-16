from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView, FormView, UpdateView
from django import forms

from carts.forms import SetCartForms
from carts.models import Cart


class CartListView(LoginRequiredMixin, FormView):
    model = Cart
    form_class = SetCartForms
    template_name = 'carts/cart.html'
    success_url = reverse_lazy('carts:cart_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['queryset'] = (Cart.objects.
                              filter(user=self.request.user).
                              select_related('product').
                              prefetch_related('product__images').
                              annotate(total_price=(F('quantity') * F('product__price'))))
        return kwargs

    def form_valid(self, form):
        for sub_form in form:
            if sub_form.cleaned_data.get('DELETE'):
                sub_form.instance.delete()
            else:
                sub_form.instance.quantity = sub_form.cleaned_data.get('quantity')
                sub_form.instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = Cart.objects.filter(user=self.request.user)
        total_price = cart_items.aggregate(total_price=Sum(F('quantity') * F('product__price')))
        context = context | total_price
        return context


@login_required
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user)
    cart.delete()
    # if elm in cart:
    #     elm.delete()
    return redirect('carts:cart_list')
