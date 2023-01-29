from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.db import IntegrityError
from phonenumber_field.formfields import PhoneNumberField

from users_detail.models import UserDetail


class RegisterUserForm(UserCreationForm):
    """Форма регистрации"""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form__input'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form__input'}))
    phone = PhoneNumberField(label='Номер телефона', widget=forms.TextInput(attrs={'class': 'form__input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form__input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form__input'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'phone', 'password1', 'password2',)

    def save(self, commit=True):
        user = super().save(commit=True)
        UserDetail.objects.create(user=user, phone=self.cleaned_data['phone'])
        return user

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if UserDetail.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Не уникальный номер телефона")
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с данным email уже зарегистрирован")
        return email


class LoginUserForm(AuthenticationForm):
    """Форма входа"""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form__input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form__input'}))


class UserDetailChangeForm(UserChangeForm):
    """Добавление в форму редактирования пользователей в админке дополнительных полей"""
    phone = PhoneNumberField(label='Номер телефона')

    def __init__(self, *args, **kwargs):
        super(UserDetailChangeForm, self).__init__(*args, **kwargs)
        self.fields['phone'].initial = self.instance.userdetail.phone

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone')
