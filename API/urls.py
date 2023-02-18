from django.urls import path

from API.views import ProductAPIView

urlpatterns = [
    path('product_list/', ProductAPIView.as_view(), name='product_list'),
]
