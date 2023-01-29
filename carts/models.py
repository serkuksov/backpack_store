from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество товаров', default=1)

    class Meta:
        verbose_name = 'Корзина товаров'
        verbose_name_plural = 'Корзины товаров'
        unique_together = ('user', 'product',)

    def __str__(self):
        return f'{self.user} - {self.product}'
