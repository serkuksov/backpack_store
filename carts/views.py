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
from carts.servises import get_carts, get_total_price_carts


class CartListView(LoginRequiredMixin, FormView):
    model = Cart
    form_class = SetCartForms
    template_name = 'carts/cart.html'
    success_url = reverse_lazy('carts:cart_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['queryset'] = get_carts(user=self.request.user)
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
        context = context | get_total_price_carts(user=self.request.user)
        return context


@login_required
def clear_cart(request):
    cart = Cart.objects.filter(user=request.user)
    cart.delete()
    return redirect('carts:cart_list')


@login_required
def add_cart(request, pk):
    cart = Cart.objects.filter(user=request.user, product=pk)
    if cart.exists():
        cart = cart.first()
        cart.quantity += 1
        cart.save()
    else:
        cart = Cart.objects.create(user=request.user, product_id=pk)
    return redirect(request.META['HTTP_REFERER'])
