from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, \
    PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path
from users_detail.views import *

# TODO нужно настроить отправку писем
urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/<int:pk>/', AccountView.as_view(), name='account'),
    # path('password_change/',
    #      PasswordChangeView.as_view(template_name='users_detail/change_password.html'),
    #      name='password_change'),
    path('password_reset/',
         PasswordResetView.as_view(
             template_name='users_detail/reset_password.html',
             subject_template_name='users_detail/reset_subject.txt',
             email_template_name='users_detail/reset_email.txt'),
         name='password_reset'),
    path('accounts/password_reset/done/',
         PasswordResetDoneView.as_view(
             template_name='users_detail/email_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='users_detail/confirm_password.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         PasswordResetCompleteView.as_view(
             template_name='users_detail/password_confirmed.html'),
         name='password_reset_complete'),
]
