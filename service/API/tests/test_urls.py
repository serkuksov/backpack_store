from django.test import TestCase
from django.urls import reverse, resolve

from API import views


class UrlsTestCase(TestCase):
    """Тесты для urls"""

    def test_products_url_resolves(self):
        url = reverse('API:products')
        self.assertEquals(resolve(url).func.cls, views.ProductListAPIView)

    def test_brands_url_resolves(self):
        url = reverse('API:brands')
        self.assertEquals(resolve(url).func.cls, views.BrandListView)

    def test_carts_url_resolves(self):
        url = reverse('API:cart-list')
        self.assertEqual(resolve(url).func.cls, views.CartViewSet)
        url = reverse('API:cart-detail', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.cls, views.CartViewSet)
