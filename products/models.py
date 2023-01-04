from django.db import models


class Product(models.Model):
    name = models.CharField()
    price = models.PositiveIntegerField()
    description = models.TextField()
    size = models.CharField()
    colour = models.CharField()
    quantity = models.PositiveSmallIntegerField()
    category = models.ForeignKey('Category', on_delete=models.PROTECT)


class Category(models.Model):
    name = models.CharField()
