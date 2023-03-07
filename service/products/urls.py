from django.urls import path
from products.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='detail'),
    path('catalog/', ProductsView.as_view(), name='catalog'),
]
