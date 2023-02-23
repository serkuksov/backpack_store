from rest_framework import serializers

from products.models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('url',)


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    # images = ImageSerializer()

    class Meta:
        model = Product
        fields = '__all__'
