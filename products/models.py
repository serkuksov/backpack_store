from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    sizes = models.CharField(max_length=128, verbose_name='Размер в формате "Д × В × Ш" cm', null=True)
    volume = models.PositiveSmallIntegerField(verbose_name='Объем в литрах', null=True)
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    colour = models.ForeignKey('Color', on_delete=models.PROTECT, verbose_name='Цвет')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    brand = models.ForeignKey('Brand', on_delete=models.PROTECT, verbose_name='Бренд', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['id']

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


class Color(models.Model):
    name = models.CharField('Цвет', max_length=32)
    hex_color = models.CharField('Цвет в виде HEX', max_length=7, default="#ffffff", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'
        ordering = ['name']


class Brand(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название бренда')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
        ordering = ['name']


def get_image_filename(instance: Product(), filename) -> str:
    slug = slugify(instance.product.name)
    return f'products_images/{slug}-{filename}'


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Изображение')

    def __str__(self):
        return f'Изображение {self.id} для {self.product.name}'

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['product']
