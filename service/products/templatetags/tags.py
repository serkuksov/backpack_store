from django.template import Library
from ..models import *

register = Library()


@register.filter(name='range_templates')
def range_templates(number):
    if number:
        number = round(number)
        return range(number)
    else:
        return []
