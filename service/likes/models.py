from django.contrib.auth import get_user_model
from django.db import models

from products.models import Product


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
        unique_together = ('user', 'product',)
        ordering = ('-id',)

    def __str__(self):
        return f'{self.user} - {self.product}'
