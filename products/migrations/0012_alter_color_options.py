# Generated by Django 4.1.5 on 2023-01-21 13:20

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0011_alter_product_brand_alter_product_colour'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='color',
            options={'ordering': ['name'], 'verbose_name': 'Цвет', 'verbose_name_plural': 'Цвета'},
        ),
    ]
