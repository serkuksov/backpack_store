from django.db.models import Prefetch, Avg

from products.models import *
from reviews.models import *


def get_top_products():
    top_products = (Product.objects.
                    prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                    annotate(arefmetical_averages_review=Avg('review__rating')).
                    order_by('-arefmetical_averages_review', '-id')[:4])
    return top_products


def get_new_products():
    new_products = (Product.objects.
                    prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                    annotate(arefmetical_averages_review=Avg('review__rating')).
                    order_by('-id')[:8])
    return new_products


def is_review_user(product, user):
    return Review.objects.filter(product=product, user=user).exists()
