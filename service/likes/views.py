from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView

from likes.models import Like


class LikeListView(LoginRequiredMixin, ListView):
    """Отображение списка избранного текущего пользователя"""
    model = Like

    def get_queryset(self):
        queryset = (Like.objects.
                    filter(user=self.request.user).
                    select_related('product').
                    prefetch_related('product__images'))
        return queryset


@login_required
def del_like(request, pk):
    """Удаляет товар из избранного пользователя"""
    like = Like.objects.filter(user=request.user, product=pk)
    like.delete()
    return redirect('likes:like_list')


@login_required
def add_like(request, pk):
    """Добавляет товар в избранное пользователя"""
    like = Like.objects.filter(user=request.user, product=pk)
    if not like.exists():
        Like.objects.create(user=request.user, product_id=pk)
    return redirect(request.META['HTTP_REFERER'])
