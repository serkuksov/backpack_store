from django.db.models import Prefetch, Subquery, OuterRef, Count, Q
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
    """Страница каталога"""
    model = Product
    queryset = (Product.objects.
                prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                order_by('id'))
    template_name = 'products/catalog.html'
    paginate_by = 9

    def get_ordering(self):
        sort = self.request.GET.getlist('sort')
        print(sort)
        if sort:
            sort = sort[-1]
            if sort == '1':
                return '-id'
            elif sort == '2':
                return 'price'
            elif sort == '3':
                return '-price'
        else:
            return 'id'

    def get_queryset(self):
        queryset = Product.objects
        category_id = self.request.GET.getlist('category')
        if category_id:
            queryset = queryset.filter(category__in=category_id)
        color_id = self.request.GET.getlist('color')
        if color_id:
            queryset = queryset.filter(colour__in=color_id)
        price = self.request.GET.getlist('price')
        if price:
            if price[0] == '1':
                queryset = queryset.filter(price__lt=1000)
            elif price[0] == '2':
                queryset = queryset.filter(price__lte=3000, price__gte=1000)
            else:
                queryset = queryset.filter(price__gt=3000)
        brand_id = self.request.GET.getlist('brand')
        if brand_id:
            queryset = queryset.filter(brand__in=brand_id)
        ordering = self.get_ordering()
        print(ordering)
        queryset = (queryset.
                    prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                    order_by(ordering))
        return queryset

    def get_sorts(self):
        sort = self.request.GET.getlist('sort')
        print(sort)
        if sort:
            sort = sort[-1]
            if sort == '1':
                return [
                    ['По новизне', 1],
                    ['По популярности', 0],
                    ['По возрастанию цены', 2],
                    ['По убыванию цены', 3],
                ]
            elif sort == '2':
                return [
                    ['По возрастанию цены', 2],
                    ['По популярности', 0],
                    ['По новизне', 1],
                    ['По убыванию цены', 3],
                ]
            elif sort == '3':
                return [
                    ['По убыванию цены', 3],
                    ['По популярности', 0],
                    ['По новизне', 1],
                    ['По возрастанию цены', 2],
                ]
        else:
            return [
                ['По популярности', 0],
                ['По новизне', 1],
                ['По возрастанию цены', 2],
                ['По убыванию цены', 3],
            ]

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, object_list=None, **kwargs)
        # categories = Category.objects.all()
        brands = Product.objects.values('brand__name', 'brand_id').annotate(total=Count('id'))
        get_params = ''.join(
            [f'{key}={value}&' for key, value in self.request.GET.items() if key != 'page' and key != 'sort'])
        context = context | {
            'title': 'Каталог',
            # 'categories': categories,
            'brands': brands,
            'get_params': get_params,
            'sorts': self.get_sorts()
        }
        return context
