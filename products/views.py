from django.db.models import Prefetch, Subquery, OuterRef
from django.shortcuts import render, HttpResponse
from products.models import Product, Image


def detail(request, pk=None):
    product = (Product.objects.filter(id=pk).
               select_related('brand', 'category').
               prefetch_related(Prefetch('images', queryset=Image.objects.all())).
               first())
    qs = (Product.objects.
          prefetch_related(Prefetch('images', queryset=Image.objects.all())).
          order_by('?')[:4])
    products = []
    for elm in qs:
        products.append({
            'id': elm.id,
            'name': elm.name,
            'price': elm.price,
            'url_img': elm.images.all()[0].image.url,
        })
    context = {
        'product': product,
        'title': product.name,
        'images': product.images.all(),
        'products': products,
    }
    return render(request, 'products/detail.html', context)
