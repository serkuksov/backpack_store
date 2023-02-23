from django.urls import path, include
from rest_framework import routers

from API.views import ProductListAPIView

# router = routers.SimpleRouter()
# router.register(r'', ProductListAPIView)

urlpatterns = [
    path('products/', ProductListAPIView.as_view()),
    # path('product/', ProductAPIViewSet.as_view({'get': 'list', 'post': 'create'}), name='product'),
    # path('product/<int:pk>/', ProductAPIViewSet.as_view({'get': 'retrieve'}), name='product'),
]
