from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from orders.views import *

urlpatterns = [
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
]
