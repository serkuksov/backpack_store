# Generated by Django 4.1.5 on 2023-01-04 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('size', models.CharField(max_length=8)),
                ('colour', models.CharField(max_length=64)),
                ('quantity', models.PositiveSmallIntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='products.category')),
            ],
        ),
    ]
