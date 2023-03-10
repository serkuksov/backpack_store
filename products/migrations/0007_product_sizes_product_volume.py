# Generated by Django 4.1.5 on 2023-01-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0006_brand_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.CharField(max_length=128, null=True, verbose_name='Размер в формате "Д × В × Ш" cm'),
        ),
        migrations.AddField(
            model_name='product',
            name='volume',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='Объем в литрах'),
        ),
    ]
