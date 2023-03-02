from rest_framework import serializers

from carts.models import Cart
from products.models import *
from reviews.models import Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = (
            "user",
            "rating",
            "text_review",
            "created_date",
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('name',)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ('name',)


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    colour = serializers.SlugRelatedField(slug_field='name', read_only=True)
    brand = serializers.SlugRelatedField(slug_field='name', read_only=True)
    arefmetical_averages_review = serializers.IntegerField(read_only=True)
    images = ImageSerializer(many=True)
    review_set = ReviewSerializer(many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = [image['image'] for image in representation['images']]
        return representation

    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = (
            'id',
            'product',
            'quantity',
        )
