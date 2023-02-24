from django.db import models
from django.core import validators
from django.contrib.auth import get_user_model
from django.urls import reverse

from products.models import *


class Review(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(verbose_name='Рейтинг',
                                              validators=[
                                                  validators.MaxValueValidator(5),
                                                  validators.MinValueValidator(1)
                                              ],
                                              default=5)
    text_review = models.TextField(max_length=1000,
                                   verbose_name='Текст отзыва')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Отзыв пользователя: {self.user}'

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.product.id})

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created_date',)
        unique_together = ('user', 'product',)
