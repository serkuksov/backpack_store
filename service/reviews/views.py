from django.shortcuts import render
from django.views import generic

from . import models, forms


class ReviewCreateView(generic.CreateView):
    """Класс отображения формы создания отзыва.
    Используется для наследования в при создании отображения карточки продукта"""

    model = models.Review
    form_class = forms.ReviewForm
