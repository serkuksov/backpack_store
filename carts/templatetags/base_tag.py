from django.template import Library

register = Library()


@register.filter
def multiply(value, multiplier):
    return value * multiplier
