# Generated by Django 4.1.5 on 2023-01-14 11:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0009_color_alter_product_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='hex_color',
            field=models.CharField(default='#ffffff', max_length=7, verbose_name='Цвет в виде HEX'),
        ),
    ]