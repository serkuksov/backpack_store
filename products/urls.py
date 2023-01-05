from django.urls import path
from products.views import detail

urlpatterns = [
    # path('', home, name='home'),
    path('product/<int:pk>/', detail, name='detail'),
]
