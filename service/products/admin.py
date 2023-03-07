from django.contrib import admin
from products.models import *


class ImageInline(admin.StackedInline):
    model = Image


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ]
    list_display = ('name', 'category', 'price')
    list_editable = ('price',)

    class Meta:
        model = Product


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Image)
admin.site.register(Brand)
admin.site.register(Color)
