import os
from collections import OrderedDict
from io import BytesIO

from PIL import Image as PILImage
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Prefetch, Avg
from django.test import TestCase

from carts.models import Cart
from products.models import Brand, Category, Color, Product, Image
from API.serializers import ReviewSerializer, CartSerializer, CartListSerializer, ProductSerializer
from reviews.models import Review


class SerializerTestCase(TestCase):
    """Тесты для всех сериализоторов"""

    def setUp(self) -> None:
        self.brand_1 = Brand.objects.create(name='brand_1')
        self.brand_2 = Brand.objects.create(name='brand_2')

        self.category_1 = Category.objects.create(name='category_1')
        self.category_2 = Category.objects.create(name='category_2')

        self.colour_1 = Color.objects.create(name='colour_1')

        self.product_1 = Product.objects.create(
            name='product_1',
            sizes='10 × 10 × 10',
            volume=10,
            price=1000,
            description='description_1',
            colour=self.colour_1,
            category=self.category_1,
            brand=self.brand_1,
        )
        self.product_2 = Product.objects.create(
            name='product_2_test',
            sizes='10 × 10 × 10',
            volume=10,
            price=750,
            description='description_2',
            colour=self.colour_1,
            category=self.category_2,
            brand=self.brand_1,
        )
        self.product_3 = Product.objects.create(
            name='product_3',
            sizes='10 × 10 × 10',
            volume=10,
            price=1500,
            description='description_test',
            colour=self.colour_1,
            category=self.category_2,
            brand=self.brand_2,
        )

        self.image_1 = Image.objects.create(product=self.product_1,
                                            image=self.create_test_image())
        self.image_2 = Image.objects.create(product=self.product_1,
                                            image=self.create_test_image())
        self.image_3 = Image.objects.create(product=self.product_2,
                                            image=self.create_test_image())
        self.image_4 = Image.objects.create(product=self.product_3,
                                            image=self.create_test_image())

        self.user_1 = get_user_model().objects.create(username='user_1')
        self.review_1 = Review.objects.create(
            user=self.user_1,
            product=self.product_1,
            text_review='text_1',
            rating=3
        )
        self.user_2 = get_user_model().objects.create(username='user_2')
        self.review_2 = Review.objects.create(
            user=self.user_2,
            product=self.product_1,
            text_review='text_2',
            rating=5
        )

        self.cart_1 = Cart.objects.create(
            user=self.user_1,
            product=self.product_1,
        )
        self.cart_2 = Cart.objects.create(
            user=self.user_1,
            product=self.product_2,
        )
        self.cart_3 = Cart.objects.create(
            user=self.user_2,
            product=self.product_1,
        )

    def tearDown(self):
        images = Image.objects.all()
        for image in images:
            os.remove(image.image.path)

    def create_test_image(self):
        """Создание тестового изображения"""
        # Генерируем изображение и сохраняем его во временном файле
        image = PILImage.new('RGB', (100, 100), (255, 0, 0))
        # Создаем временный файл в памяти
        buffer = BytesIO()
        image.save(buffer, 'jpeg')
        image_data = buffer.getvalue()
        image_file = InMemoryUploadedFile(buffer, None, 'test.jpg', 'image/jpeg', len(image_data), None)
        return image_file

    def test_product_serializer(self):
        """Тест по отображению списка продуктов с использованием API"""
        queryset = (Product.objects.
                    annotate(arefmetical_averages_review=Avg('review__rating')).
                    prefetch_related(Prefetch('images', queryset=Image.objects.all())).
                    prefetch_related(Prefetch('review_set', queryset=Review.objects.select_related('user').all())).
                    all())
        serialized_data = ProductSerializer(queryset, many=True).data
        list_url_images = [
            self.image_1.image.url,
            self.image_2.image.url,
        ]
        list_reviews = ReviewSerializer([self.review_2, self.review_1], many=True).data
        self.assertEqual(serialized_data[0]['name'], 'product_1')
        self.assertEqual(serialized_data[0]['price'], 1000)
        self.assertEqual(serialized_data[0]['category'], 'category_1')
        self.assertEqual(serialized_data[0]['brand'], 'brand_1')
        self.assertEqual(serialized_data[0]['colour'], 'colour_1')
        self.assertEqual(serialized_data[0]['arefmetical_averages_review'], 4)
        self.assertEqual(serialized_data[0]['images'], list_url_images)
        self.assertEqual(serialized_data[0]['review_set'], list_reviews)

        self.assertEqual(serialized_data[1]['price'], 750)
        self.assertEqual(serialized_data[1]['category'], 'category_2')
        self.assertEqual(serialized_data[1]['brand'], 'brand_1')
        self.assertEqual(serialized_data[1]['colour'], 'colour_1')
        self.assertEqual(len(serialized_data[1]['images']), 1)

    def test_cart_list_serializer(self):
        """Тест для отображения списка корзины продуктов"""
        queryset = Cart.objects.filter(user=self.user_1).all()
        serializer_data = CartListSerializer(queryset, many=True).data
        test_data = [
            {
                'id': 2,
                'product': 'product_2_test',
                'quantity': 1
            },
            {
                'id': 1,
                'product': 'product_1',
                'quantity': 1
            }
        ]
        self.assertEqual(serializer_data, test_data)
