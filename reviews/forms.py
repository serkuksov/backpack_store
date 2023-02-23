from django import forms
from django.core import validators

from . import models


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, min_value=1, widget=forms.NumberInput(attrs={'class': "quantity-input"}),
                                initial=5)

    class Meta:
        model = models.Review
        fields = [
            'user',
            'product',
            'rating',
            'text_review',
        ]
        widgets = {
            'user': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'text_review': forms.Textarea(attrs={'class': "form__input form__input--textarea"}),
        }
