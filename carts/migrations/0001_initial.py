# Generated by Django 4.1.5 on 2023-01-29 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('products', '0012_alter_color_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='Количество товаров')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product',
                                              verbose_name='Товар')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL,
                                           verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Корзина товаров',
                'verbose_name_plural': 'Корзины товаров',
            },
        ),
    ]
