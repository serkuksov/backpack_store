from django.contrib import admin

from carts.models import Cart


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'quantity',
    )
