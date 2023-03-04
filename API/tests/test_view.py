import json
import os
from io import BytesIO

from PIL import Image as PILImage
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from products.models import Brand, Category, Color, Product, Image
from API.serializers import BrandSerializer, ProductSerializer, ReviewSerializer
from reviews.models import Review


class ViewTestCase(TestCase):
    """Тесты для View"""

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

    def test_get_brand_list(self):
        """Тест по отображению списка брендов с использованием API"""
        url = reverse('API:brands')
        response = self.client.get(path=url)
        test_data = [
            'brand_1',
            'brand_2',
        ]
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(test_data, response.data)

    def test_get_product_list(self):
        """Тест по отображению списка продуктов с использованием API"""
        url = reverse('API:products')
        response = self.client.get(path=url)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)

        list_url_images = [
            'http://testserver' + self.image_1.image.url,
            'http://testserver' + self.image_2.image.url,
        ]
        list_reviews = ReviewSerializer([self.review_2, self.review_1], many=True).data
        self.assertEqual(response_data[0]['name'], 'product_1')
        self.assertEqual(response_data[0]['price'], 1000)
        self.assertEqual(response_data[0]['category'], 'category_1')
        self.assertEqual(response_data[0]['brand'], 'brand_1')
        self.assertEqual(response_data[0]['colour'], 'colour_1')
        self.assertEqual(response_data[0]['arefmetical_averages_review'], 4)
        self.assertEqual(response_data[0]['images'], list_url_images)
        self.assertEqual(response_data[0]['review_set'], list_reviews)

        self.assertEqual(response_data[1]['price'], 750)
        self.assertEqual(response_data[1]['category'], 'category_2')
        self.assertEqual(response_data[1]['brand'], 'brand_1')
        self.assertEqual(response_data[1]['colour'], 'colour_1')
        self.assertEqual(len(response_data[1]['images']), 1)

    def test_get_product_list_filter_min_price(self):
        """Тест по отображению фильтрованного списка продуктов по
        минимальной цене с использованием API"""
        url = reverse('API:products')

        filter_params = {'min_price': 900}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], 'product_1')
        self.assertEqual(response_data[1]['name'], 'product_3')

    def test_get_product_list_filter_max_price(self):
        """Тест по отображению фильтрованного списка продуктов по
        минимальной цене с использованием API"""
        url = reverse('API:products')

        filter_params = {'max_price': 1200}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], 'product_1')
        self.assertEqual(response_data[1]['name'], 'product_2_test')

    def test_get_product_list_filter_category(self):
        """Тест по отображению фильтрованного списка продуктов по
         части имени категории API"""
        url = reverse('API:products')

        filter_params = {'category': 'category_1'}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['name'], 'product_1')

    def test_get_product_list_pagenation(self):
        """Тест пагинации отображения продуктов API"""
        url = reverse('API:products')

        filter_params = {'page': 2}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['name'], 'product_3')

        filter_params = {'page_size': 3}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 3)

    def test_get_product_list_search(self):
        """Тест поиска для отображения продуктов API"""
        url = reverse('API:products')

        filter_params = {'search': 'tes'}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], 'product_2_test')
        self.assertEqual(response_data[1]['name'], 'product_3')

        filter_params = {'search': 'brand_2'}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]['name'], 'product_3')

    def test_get_product_list_ordering(self):
        """Тест для отображения сортированного списка продуктов API"""
        url = reverse('API:products')

        filter_params = {'ordering': '-id'}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['name'], 'product_3')
        self.assertEqual(response_data[1]['name'], 'product_2_test')

        filter_params = {'ordering': '-price'}
        response = self.client.get(path=url, data=filter_params)
        response_data = response.data.get('results')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['price'], 1500)
        self.assertEqual(response_data[1]['price'], 1000)
