from django.db.models import Prefetch, Subquery, OuterRef, Count, Q, Avg
from django.shortcuts import render, HttpResponse
from django.views.generic import View, DetailView, ListView, CreateView

from products.models import *
from products import servises
from reviews.models import *
from reviews.forms import *
from reviews.views import *


class ProductDetailView(DetailView, ReviewCreateView):
    """Карточка продукта"""
    model = Product
    slug_field = 'id'
    template_name = 'products/detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (queryset.select_related('brand', 'category').
                    prefetch_related(
            Prefetch('images', queryset=Image.objects.all()),
            Prefetch('review_set', queryset=Review.objects.all()),
        ).
                    annotate(count_review=Count('review')).
                    annotate(arefmetical_averages_review=Avg('review__rating'))
                    )
        return queryset

    def get_initial(self):
        return {
            'user': self.request.user,
            'product': self.object,
        }

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context = context | {
            'title': context['product'].name,
            'top_products': servises.get_top_products(),
            'is_review_user': servises.is_review_user(product=self.object,
                                                      user=self.request.user) if self.request.user.is_active else 0,
        }
        context = context | super(ReviewCreateView, self).get_context_data(**kwargs)
        return context

    def form_invalid(self, form):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(form=form))


class IndexView(View):
    """Главная страница"""

    def get(self, request):
        context = {
            'title': 'Главная страница',
            'top_products': servises.get_top_products(),
            'new_products': servises.get_new_products(),
        }
        return render(request, 'products/index.html', context)


class ProductsView(ListView):
    """Страница каталога"""
    model = Product
    queryset = (Product.objects.
                prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                order_by('id'))
    template_name = 'products/catalog.html'
    paginate_by = 2

    def get_ordering(self):
        sort = self.request.GET.get('sort')
        if sort:
            if sort == '1':
                return '-id'
            elif sort == '2':
                return 'price'
            elif sort == '3':
                return '-price'
            elif sort == '0':
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
        queryset = queryset.prefetch_related(Prefetch('images', queryset=Image.objects.all()))
        ordering = self.get_ordering()
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    def get_sorts(self):
        sort = self.request.GET.getlist('sort')
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
        brands = Product.objects.values('brand__name', 'brand_id').annotate(total=Count('id'))
        get_params = ''.join(
            [f'{key}={value}&' for key, value in self.request.GET.items() if key != 'page' and key != 'sort'])
        context = context | {
            'title': 'Каталог',
            'brands': brands,
            'get_params': get_params,
            'sorts': self.get_sorts()
        }
        return context
