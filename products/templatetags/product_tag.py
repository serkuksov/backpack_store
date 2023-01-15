from django.template import Library
from ..models import *

register = Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_brands():
    return Brand.objects.all()


@register.simple_tag()
def get_colors():
    return Color.objects.all()
