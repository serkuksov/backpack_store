from django.contrib import admin

from reviews import models


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'product',
        'rating',
    ]
    list_filter = [
        'user',
        'product',
        'rating',
    ]
    list_editable = [
        'rating',
    ]
