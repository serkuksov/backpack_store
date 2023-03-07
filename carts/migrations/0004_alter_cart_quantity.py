# Generated by Django 4.1.5 on 2023-03-07 07:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('carts', '0003_alter_cart_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1,
                                                   validators=[django.core.validators.MinValueValidator(limit_value=1)],
                                                   verbose_name='Количество товаров'),
        ),
    ]
