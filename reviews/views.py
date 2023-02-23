from django.shortcuts import render
from django.views import generic

from . import models, forms


class ReviewCreateView(generic.CreateView):
    model = models.Review
    form_class = forms.ReviewForm
