from django.urls import path
from users_detail.views import *

urlpatterns = [
    path('login-register/', RegisterUser.as_view(), name='login-register'),
]
