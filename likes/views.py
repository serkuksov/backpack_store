from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, CreateView, FormView, UpdateView
from django import forms

from likes.models import Like


class LikeListView(LoginRequiredMixin, ListView):
    model = Like

    # template_name = 'likes/likes.html'

    def get_context_data(self):
        context = super().get_context_data()
        print(context)
        return context


@login_required
def del_like(request, pk):
    like = Like.objects.filter(user=request.user, product=pk)
    like.delete()
    return redirect('likes:like_list')


@login_required
def add_like(request, pk):
    like = Like.objects.filter(user=request.user, product=pk)
    if not like.exists():
        like = Like.objects.create(user=request.user, product_id=pk)
    return redirect(request.META['HTTP_REFERER'])
