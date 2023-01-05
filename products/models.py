from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    # size = models.CharField(max_length=8, verbose_name='Размер')
    colour = models.CharField(max_length=64, verbose_name='Цвет')
    # quantity = models.PositiveSmallIntegerField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'pk': self.pk})


class Category(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


def get_image_filename(instance: Product(), filename) -> str:
    slug = slugify(instance.product.name)
    return f'products_images/{slug}-{filename}'


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    images = models.ImageField(upload_to=get_image_filename, verbose_name='Изображение')

    def __str__(self):
        return f'Изображение {self.id} для {self.product.name}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['product']
