from django.contrib import admin

from likes.models import Like

@admin.register(Like)
class AdminLike(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
    )

