from django.contrib import admin

from . import models


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'user',
        'status',
    )
    list_filter = (
        'user',
        'status',
    )
    list_editable = (
        'status',
    )
    readonly_fields = (
        'user',
    )


@admin.register(models.OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'unit_price',
    )
