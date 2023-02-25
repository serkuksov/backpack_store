from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, PasswordChangeView

from orders.servises import get_orders
from users_detail.forms import *


class MyLoginView(LoginView):
    """Страница входа"""
    template_name = 'users_detail/login.html'
    form_class = LoginUserForm


class AccountView(UpdateView):
    """Информация об аккаунте и возможность редактирования"""
    model = get_user_model()
    template_name = 'users_detail/my-account.html'
    form_class = UpdateUserForm

    def get_success_url(self):
        return reverse('users_detail:account', kwargs={'pk': self.object.id})

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('userdetail')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = context | {
            'orders': get_orders(user=self.request.user)
        }
        return context


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
