# Generated by Django 4.1.5 on 2023-01-14 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0010_alter_color_hex_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='products.brand',
                                    verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='product',
            name='colour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.color',
                                    verbose_name='Цвет'),
        ),
    ]
