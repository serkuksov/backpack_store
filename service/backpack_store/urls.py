from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from . import yasg

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include(('products.urls', 'products'))),
    path('user/', include(('users_detail.urls', 'users_detail'))),
    path('cart/', include(('carts.urls', 'carts'))),
    path('order/', include(('orders.urls', 'orders'))),
    path('likes/', include(('likes.urls', 'likes'))),
    path('API/v1/', include(('API.urls', 'API'))),
    path('auto_drf/', include('rest_framework.urls', namespace='rest_framework')),
    # path('API/v1/auto/', include('djoser.urls')),
    path('API/v1/auto/', include('djoser.urls.authtoken')),

    # path('silk/', include('silk.urls', namespace='silk')),
]

urlpatterns += yasg.urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
