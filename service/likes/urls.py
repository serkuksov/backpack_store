from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from likes.views import *

urlpatterns = [
    path('', LikeListView.as_view(), name='like_list'),
    path('del_like/<int:pk>/', del_like, name='del_like'),
    path('add_like/<int:pk>', add_like, name='add_like'),
]
