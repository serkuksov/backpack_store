from django.db.models import Prefetch, Subquery, OuterRef
from django.shortcuts import render, HttpResponse
from products.models import Product, Image


def detail(request, pk=None):
    product = (Product.objects.filter(id=pk).
               select_related('brand', 'category').
               prefetch_related(Prefetch('images', queryset=Image.objects.all())).
               first())
    additional_products = (Product.objects.
                           prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                           # only('name', 'price').
                           order_by('?')[:4])
    context = {
        'product': product,
        'title': product.name,
        'additional_products': additional_products,
    }
    return render(request, 'products/detail.html', context)
