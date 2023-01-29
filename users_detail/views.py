from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, FormView
from django import forms
from django.contrib.auth.views import LoginView, LogoutView

from users_detail.forms import *


class MyLoginView(LoginView):
    """Странца входа"""
    # TODO релизовать функционал кнопки Запомни меня
    template_name = 'users_detail/login.html'
    form_class = LoginUserForm


class RegisterUser(CreateView):
    """Страница регистрации"""
    form_class = RegisterUserForm
    template_name = 'users_detail/register.html'
    success_url = reverse_lazy('users_detail:login')

    def form_valid(self, form):
        """Метод переопределен для автоматического входа после регистрации"""
        self.object = form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())
