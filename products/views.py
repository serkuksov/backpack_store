from django.shortcuts import render
from products.models import Product


def detail(request, pk=None):
    product = Product.objects.filter(id=pk).first()
    context = {
        'product': product,
        'title': product.name,
    }
    return render(request, 'products/detail.html', context)
