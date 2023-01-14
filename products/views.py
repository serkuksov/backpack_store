from django.db.models import Prefetch, Subquery, OuterRef, Count
from django.shortcuts import render, HttpResponse
from django.views.generic import View, DetailView, ListView

from products.models import *


class ProductDetailView(DetailView):
    """Карточка продукта"""
    model = Product
    slug_field = 'id'
    template_name = 'products/detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (queryset.select_related('brand', 'category').
                    prefetch_related(Prefetch('images', queryset=Image.objects.all())))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_products = (Product.objects.
                        prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                        order_by('?')[:4])
        context = context | {
            'title': context['product'].name,
            'top_products': top_products,
        }
        return context


class IndexView(View):
    """Главная страница"""

    def get(self, request):
        top_products = (Product.objects.
                        prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                        order_by('?')[:4])
        new_products = (Product.objects.
                        prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                        order_by('-id')[:8])
        context = {
            'title': 'Главная страница',
            'top_products': top_products,
            'new_products': new_products,
        }
        return render(request, 'products/index.html', context)


class ProductsView(ListView):
    model = Product
    queryset = (Product.objects.
                prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                order_by('id'))
    template_name = 'products/catalog.html'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        categories = Category.objects.all()
        brands = Product.objects.values('brand__name').annotate(total=Count('id'))
        context = context | {
            'title': 'Каталог',
            'categories': categories,
            'brands': brands,
        }
        return context
