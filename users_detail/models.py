from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model


class UserDetail(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    phone = PhoneNumberField(verbose_name='Номер телефона', null=True, unique=True)

    def __str__(self):
        return f'Дополнительные данные для пользователя {self.user}'
