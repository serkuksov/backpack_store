from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product


class Address(models.Model):
    country = models.CharField(max_length=25, verbose_name='Страна')
    region = models.CharField(max_length=25, verbose_name='Регион')
    city = models.CharField(max_length=25, verbose_name='Город')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    postal_code = models.PositiveSmallIntegerField(verbose_name='Индекс')

    def __str__(self):
        return f'{self.country}/{self.region}/{self.city}/{self.address}'

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'


class Order(models.Model):
    class StatusOrder(models.TextChoices):
        NEW_ORDER = 'Новый заказ', 'Новый заказ'
        IN_WORK = 'В работе', 'В работе'
        IN_DELIVERY = 'В доставке', 'В доставке'
        COMPLETED = 'Выполнен', 'Выполнен'

    user = models.ForeignKey(get_user_model(),
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата заказа')
    update = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    address = models.ForeignKey(Address,
                                on_delete=models.PROTECT,
                                verbose_name='Адрес доставки')
    status = models.CharField(max_length=25,
                              verbose_name='Статус заказа',
                              choices=StatusOrder.choices,
                              default=StatusOrder.NEW_ORDER)

    def __str__(self):
        return f'Заказ № {self.id}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderDetails(models.Model):
    order = models.ForeignKey(Order,
                              on_delete=models.CASCADE,
                              verbose_name='Заказ')
    product = models.ForeignKey(Product,
                                on_delete=models.PROTECT,
                                verbose_name='Продукт')
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество продуктов')
    unit_price = models.PositiveSmallIntegerField(verbose_name='Цена одного продукта')

    def __str__(self):
        return f'{self.order} - {self.product}: {self.quantity} шт.'

    class Meta:
        verbose_name = 'Позиция в заказе'
        verbose_name_plural = 'Позиции в заказе'
        unique_together = ('order', 'product',)
