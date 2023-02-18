from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from carts.views import *

urlpatterns = [
    path('', CartListView.as_view(), name='cart_list'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('add_cart/<int:pk>', add_cart, name='add_cart'),
]
