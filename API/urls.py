from django.urls import path
from rest_framework import routers

from API.views import *

router = routers.SimpleRouter()
router.register(r'carts', CartViewSet, basename='cart')

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='products'),
    path('brands/', BrandListView.as_view(), name='brands'),
]

urlpatterns += router.urls
