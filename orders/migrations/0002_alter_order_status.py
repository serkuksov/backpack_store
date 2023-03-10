# Generated by Django 4.1.5 on 2023-02-23 15:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[('Новый заказ', 'New Order'), ('В работе', 'In Work'), ('В доставке', 'In Delivery'),
                         ('Выполнен', 'Completed')], default='Новый заказ', max_length=25,
                verbose_name='Статус заказа'),
        ),
    ]
