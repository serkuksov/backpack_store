from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from users_detail.forms import UserDetailChangeForm
from users_detail.models import UserDetail

admin.site.unregister(get_user_model())


@admin.register(get_user_model())
class UserDetailAdmin(UserAdmin):
    """Дополнение админки Пользователя дополнительными параметрами"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'phone')
    form = UserDetailChangeForm
    fieldsets = UserAdmin.fieldsets + ((("Дополнительные данные о пользователе"), {"fields": ("phone",)}),)

    def phone(self, obj):
        return obj.userdetail.phone

    phone.short_description = 'Номер телефона'

    def save_model(self, request, obj, form, change):
        try:
            obj.userdetail.phone = form.cleaned_data.get('phone')
            obj.userdetail.save()
        except UserDetail.DoesNotExist:
            UserDetail.objects.create(user=obj, phone=form.cleaned_data.get('phone'))
        super().save_model(request, obj, form, change)
