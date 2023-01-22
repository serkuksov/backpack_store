from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users_detail.forms import RegisterUserForm


def login(request):
    pass


class DataMixin:
    pass


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'users_detail/login-register.html'
    success_url = reverse_lazy('products:index')
